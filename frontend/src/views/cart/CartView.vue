<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <AppHeader variant="dark" />

    <!-- Cart Content -->
    <div class="max-w-7xl mx-auto px-6 py-12 mt-20">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900" style="font-family: Georgia, serif;">
          Shopping Cart
        </h1>
        <p class="mt-2 text-sm text-gray-600 tracking-wide">
          {{ cartStore.totalItems }} {{ cartStore.totalItems === 1 ? 'item' : 'items' }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
        <p class="mt-4 text-sm text-gray-600">Loading cart...</p>
      </div>

      <!-- Empty Cart -->
      <div v-else-if="cartStore.isEmpty" class="text-center py-16">
        <div class="w-24 h-24 mx-auto mb-6 text-gray-300">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1"
              d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
            />
          </svg>
        </div>
        <h2 class="text-xl font-light text-gray-900 mb-4">Your cart is empty</h2>
        <p class="text-sm text-gray-600 mb-8">Add items to get started</p>
        <router-link
          to="/products"
          class="inline-block px-8 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
        >
          CONTINUE SHOPPING
        </router-link>
      </div>

      <!-- Cart Items -->
      <div v-else class="grid lg:grid-cols-3 gap-8">
        <!-- Items List -->
        <div class="lg:col-span-2 space-y-4">
          <div
            v-for="item in cartStore.items"
            :key="item.id"
            class="bg-white border border-gray-200 p-6 flex gap-6"
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
              <router-link
                :to="`/products/${item.product.slug}`"
                class="text-base font-medium text-gray-900 hover:text-gray-600 transition-colors"
              >
                {{ item.product.name }}
              </router-link>

              <p v-if="item.product.brand" class="text-sm text-gray-600 mt-1">
                {{ item.product.brand }}
              </p>

              <!-- Variant Details -->
              <div v-if="item.variant_details" class="mt-2 text-sm text-gray-600">
                <span>Size: {{ item.variant_details.size }}</span>
                <span class="mx-2">|</span>
                <span>Color: {{ item.variant_details.color }}</span>
              </div>

              <!-- Price -->
              <p class="mt-3 text-base font-medium text-gray-900">
                ${{ item.price }}
              </p>

              <!-- Quantity Controls -->
              <div class="mt-4 flex items-center gap-4">
                <div class="flex items-center border border-gray-300">
                  <button
                    @click="decreaseQuantity(item)"
                    :disabled="updatingItem === item.id"
                    class="px-3 py-2 hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                    </svg>
                  </button>
                  <span class="px-4 text-sm font-medium">{{ item.quantity }}</span>
                  <button
                    @click="increaseQuantity(item)"
                    :disabled="updatingItem === item.id"
                    class="px-3 py-2 hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                  </button>
                </div>

                <button
                  @click="removeItem(item.id)"
                  :disabled="updatingItem === item.id"
                  class="text-sm text-red-600 hover:text-red-800 transition-colors disabled:opacity-50"
                >
                  Remove
                </button>
              </div>
            </div>

            <!-- Total Price -->
            <div class="text-right">
              <p class="text-base font-medium text-gray-900">
                ${{ item.total_price }}
              </p>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white border border-gray-200 p-6 sticky top-24">
            <h2 class="text-lg font-medium text-gray-900 mb-4 tracking-wide">
              ORDER SUMMARY
            </h2>

            <div class="space-y-3 mb-6">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-gray-900 font-medium">${{ cartStore.subtotal }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Shipping</span>
                <span class="text-gray-900">Calculated at checkout</span>
              </div>
            </div>

            <div class="border-t border-gray-200 pt-4 mb-6">
              <div class="flex justify-between">
                <span class="text-base font-medium text-gray-900">Total</span>
                <span class="text-lg font-medium text-gray-900">${{ cartStore.subtotal }}</span>
              </div>
            </div>

            <router-link
              to="/checkout"
              class="block w-full px-6 py-3 border border-black text-sm font-medium tracking-widest text-center text-white bg-black hover:bg-gray-900 transition-all mb-3"
            >
              CHECKOUT
            </router-link>

            <router-link
              to="/products"
              class="block w-full px-6 py-3 border border-gray-300 text-sm font-medium tracking-widest text-gray-700 bg-white hover:bg-gray-50 transition-all text-center"
            >
              CONTINUE SHOPPING
            </router-link>

            <button
              v-if="!cartStore.isEmpty"
              @click="handleClearCart"
              class="w-full mt-3 text-sm text-red-600 hover:text-red-800 transition-colors"
            >
              Clear Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import AppHeader from '@/components/layout/AppHeader.vue'

const cartStore = useCartStore()
const loading = ref(true)
const updatingItem = ref(null)

const getImageUrl = (url) => {
  if (url && url.startsWith('http')) {
    return url
  }
  return `http://localhost:8002${url || ''}`
}

const increaseQuantity = async (item) => {
  updatingItem.value = item.id
  await cartStore.updateCartItem(item.id, item.quantity + 1)
  updatingItem.value = null
}

const decreaseQuantity = async (item) => {
  if (item.quantity === 1) {
    if (confirm('Remove this item from cart?')) {
      await removeItem(item.id)
    }
    return
  }

  updatingItem.value = item.id
  await cartStore.updateCartItem(item.id, item.quantity - 1)
  updatingItem.value = null
}

const removeItem = async (itemId) => {
  updatingItem.value = itemId
  await cartStore.removeCartItem(itemId)
  updatingItem.value = null
}

const handleClearCart = async () => {
  if (confirm('Are you sure you want to clear your cart?')) {
    await cartStore.clearCart()
  }
}

onMounted(async () => {
  await cartStore.fetchCart()
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