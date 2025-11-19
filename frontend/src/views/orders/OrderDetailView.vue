<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader variant="dark" />

    <div class="max-w-5xl mx-auto px-6 py-12 mt-20">
      <!-- Payment Status Messages -->
      <div v-if="route.query.payment === 'success'" class="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="flex items-center">
          <svg class="w-6 h-6 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <div>
            <p class="text-sm font-medium text-green-800">Payment Successful!</p>
            <p class="text-sm text-green-700 mt-1">Your order has been confirmed and is being processed.</p>
          </div>
        </div>
      </div>

      <div v-if="route.query.payment === 'cancelled'" class="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div class="flex items-center">
          <svg class="w-6 h-6 text-yellow-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          <div>
            <p class="text-sm font-medium text-yellow-800">Payment Cancelled</p>
            <p class="text-sm text-yellow-700 mt-1">You can retry payment at any time.</p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
        <p class="mt-4 text-sm text-gray-600">Loading order details...</p>
      </div>

      <!-- Order Details -->
      <div v-else-if="order" class="space-y-6">
        <!-- Header -->
        <div class="bg-white border border-gray-200 p-6">
          <div class="flex items-center justify-between mb-4">
            <h1 class="text-2xl font-light tracking-wide text-gray-900">
              Order #{{ order.order_number }}
            </h1>
            <span
              class="px-4 py-2 text-sm font-medium tracking-wider"
              :class="getStatusClass(order.status)"
            >
              {{ order.status_display }}
            </span>
          </div>

          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-2">Order Date</h3>
              <p class="text-sm text-gray-600">{{ formatDate(order.created_at) }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-2">Payment Status</h3>
              <span
                class="inline-block px-3 py-1 text-xs font-medium tracking-wider"
                :class="getPaymentStatusClass(order.payment_status)"
              >
                {{ order.payment_status_display }}
              </span>
            </div>
          </div>

          <!-- Payment Button -->
          <div v-if="order.payment_status === 'pending'" class="mt-6 pt-6 border-t border-gray-200">
            <button
              @click="handlePayment"
              :disabled="processingPayment"
              class="px-6 py-3 border border-black text-sm font-medium tracking-widest transition-all"
              :class="
                processingPayment
                  ? 'text-gray-400 bg-gray-100 border-gray-300 cursor-not-allowed'
                  : 'text-white bg-black hover:bg-gray-900'
              "
            >
              <span v-if="processingPayment">PROCESSING...</span>
              <span v-else>PAY NOW</span>
            </button>
          </div>

          <div v-if="order.tracking_number" class="mt-6 pt-6 border-t border-gray-200">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Tracking Number</h3>
            <p class="text-sm text-gray-600">{{ order.tracking_number }}</p>
          </div>
        </div>

        <!-- Order Items -->
        <div class="bg-white border border-gray-200 p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6 tracking-wide">ORDER ITEMS</h2>

          <div class="space-y-4">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="flex gap-6 pb-4 border-b border-gray-200 last:border-0"
            >
              <!-- Product Image -->
              <div class="w-24 h-32 bg-gray-100 flex-shrink-0">
                <img
                  v-if="item.product.primary_image"
                  :src="getImageUrl(item.product.primary_image)"
                  :alt="item.product.name"
                  class="w-full h-full object-cover"
                />
              </div>

              <!-- Product Details -->
              <div class="flex-1">
                <h3 class="text-base font-medium text-gray-900">{{ item.product.name }}</h3>

                <p v-if="item.product.brand" class="text-sm text-gray-600 mt-1">
                  {{ item.product.brand }}
                </p>

                <!-- Variant Details -->
                <div v-if="item.variant_details" class="mt-2 text-sm text-gray-600">
                  <span>Size: {{ item.variant_details.size }}</span>
                  <span class="mx-2">|</span>
                  <span>Color: {{ item.variant_details.color }}</span>
                </div>

                <div class="mt-3 flex items-center justify-between">
                  <p class="text-sm text-gray-600">Quantity: {{ item.quantity }}</p>
                  <p class="text-base font-medium text-gray-900">${{ item.total_price }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Shipping Information -->
        <div class="bg-white border border-gray-200 p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6 tracking-wide">SHIPPING INFORMATION</h2>

          <div class="space-y-3">
            <div>
              <p class="text-sm font-medium text-gray-900">
                {{ order.shipping_first_name }} {{ order.shipping_last_name }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600">{{ order.shipping_address }}</p>
              <p class="text-sm text-gray-600">
                {{ order.shipping_city }}, {{ order.shipping_state }} {{ order.shipping_postal_code }}
              </p>
              <p class="text-sm text-gray-600">{{ order.shipping_country }}</p>
            </div>
            <div class="pt-3 border-t border-gray-200">
              <p class="text-sm text-gray-600">Email: {{ order.shipping_email }}</p>
              <p class="text-sm text-gray-600">Phone: {{ order.shipping_phone }}</p>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="bg-white border border-gray-200 p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6 tracking-wide">ORDER SUMMARY</h2>

          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Subtotal</span>
              <span class="text-gray-900">${{ order.subtotal }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Shipping</span>
              <span class="text-gray-900">${{ order.shipping_cost }}</span>
            </div>
            <div class="border-t border-gray-200 pt-3 flex justify-between">
              <span class="text-base font-medium text-gray-900">Total</span>
              <span class="text-lg font-medium text-gray-900">${{ order.total }}</span>
            </div>
          </div>

          <div v-if="order.notes" class="mt-6 pt-6 border-t border-gray-200">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Order Notes</h3>
            <p class="text-sm text-gray-600">{{ order.notes }}</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between">
          <router-link
            to="/orders"
            class="text-sm text-gray-600 hover:text-black tracking-wide transition-colors"
          >
            ← BACK TO ORDERS
          </router-link>

          <button
            v-if="order.status === 'pending' || order.status === 'processing'"
            @click="handleCancelOrder"
            :disabled="cancelling"
            class="px-6 py-3 border border-red-600 text-sm font-medium tracking-widest text-red-600 bg-white hover:bg-red-50 transition-all disabled:opacity-50"
          >
            <span v-if="cancelling">CANCELLING...</span>
            <span v-else>CANCEL ORDER</span>
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-16">
        <p class="text-red-600">{{ error || 'Order not found' }}</p>
        <router-link
          to="/orders"
          class="inline-block mt-6 px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
        >
          BACK TO ORDERS
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOrdersStore } from '@/stores/orders'
import { usePaymentStore } from '@/stores/payment'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()
const router = useRouter()
const ordersStore = useOrdersStore()
const paymentStore = usePaymentStore()

const loading = ref(true)
const cancelling = ref(false)
const processingPayment = ref(false)

const order = computed(() => ordersStore.currentOrder)
const error = computed(() => ordersStore.error)

const getImageUrl = (url) => {
  if (url && url.startsWith('http')) {
    return url
  }
  return `http://localhost:8002${url || ''}`
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-orange-100 text-orange-800',
    processing: 'bg-blue-100 text-blue-800',
    shipped: 'bg-purple-100 text-purple-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPaymentStatusClass = (status) => {
  const classes = {
    pending: 'bg-orange-100 text-orange-800',
    paid: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    refunded: 'bg-gray-100 text-gray-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const handlePayment = async () => {
  processingPayment.value = true

  try {
    const result = await paymentStore.createCheckoutSession(order.value.id)

    if (result.success && result.checkoutUrl) {
      // Redirect to Stripe checkout
      window.location.href = result.checkoutUrl
    } else {
      alert(result.message || 'Failed to initiate payment')
      processingPayment.value = false
    }
  } catch (error) {
    alert('An error occurred. Please try again.')
    processingPayment.value = false
  }
}

const handleCancelOrder = async () => {
  if (!confirm('Are you sure you want to cancel this order? This action cannot be undone.')) {
    return
  }

  cancelling.value = true

  const result = await ordersStore.cancelOrder(order.value.id)

  if (result.success) {
    alert(result.message)
  } else {
    alert(result.message)
  }

  cancelling.value = false
}

onMounted(async () => {
  const orderId = parseInt(route.params.id)
  await ordersStore.fetchOrderById(orderId)
  loading.value = false
})
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>