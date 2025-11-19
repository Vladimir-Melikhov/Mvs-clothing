<template>
    <div class="min-h-screen bg-gray-50">
      <AppHeader variant="dark" />
  
      <div class="max-w-7xl mx-auto px-6 py-12 mt-20">
        <div class="mb-8">
          <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900" style="font-family: Georgia, serif;">
            My Orders
          </h1>
          <p class="mt-2 text-sm text-gray-600 tracking-wide">
            View and manage your orders
          </p>
        </div>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          <p class="mt-4 text-sm text-gray-600">Loading orders...</p>
        </div>

        <div v-else-if="!ordersStore.hasOrders" class="text-center py-16">
          <div class="w-24 h-24 mx-auto mb-6 text-gray-300">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <h2 class="text-xl font-light text-gray-900 mb-4">No orders yet</h2>
          <p class="text-sm text-gray-600 mb-8">Start shopping to create your first order</p>
          <router-link
            to="/products"
            class="inline-block px-8 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
          >
            SHOP NOW
          </router-link>
        </div>
  
        <!-- Orders List -->
        <div v-else class="space-y-4">
          <div
            v-for="order in ordersStore.orders"
            :key="order.id"
            class="bg-white border border-gray-200 p-6"
          >
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-lg font-medium text-gray-900">
                  Order #{{ order.order_number }}
                </h3>
                <p class="text-sm text-gray-600 mt-1">
                  {{ formatDate(order.created_at) }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-lg font-medium text-gray-900">${{ order.total }}</p>
                <span
                  class="inline-block mt-1 px-3 py-1 text-xs font-medium tracking-wider"
                  :class="getStatusClass(order.status)"
                >
                  {{ order.status_display }}
                </span>
              </div>
            </div>
  
            <!-- Order Items Preview -->
            <div class="border-t border-gray-200 pt-4 mb-4">
              <div class="flex gap-4 overflow-x-auto">
                <div
                  v-for="item in order.items.slice(0, 3)"
                  :key="item.id"
                  class="flex-shrink-0 w-16 h-20 bg-gray-100"
                >
                  <img
                    v-if="item.product.primary_image"
                    :src="getImageUrl(item.product.primary_image)"
                    :alt="item.product.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div v-if="order.items.length > 3" class="flex items-center">
                  <span class="text-sm text-gray-600">+{{ order.items.length - 3 }} more</span>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between pt-4 border-t border-gray-200">
              <router-link
                :to="`/orders/${order.id}`"
                class="text-sm text-gray-900 hover:text-gray-600 tracking-wide transition-colors"
              >
                VIEW DETAILS →
              </router-link>
              <button
                v-if="order.status === 'pending' || order.status === 'processing'"
                @click="handleCancelOrder(order.id)"
                class="text-sm text-red-600 hover:text-red-800 tracking-wide transition-colors"
              >
                CANCEL ORDER
              </button>
            </div>
          </div>

          <div
            v-if="ordersStore.pagination.total_pages > 1"
            class="mt-8 flex justify-center"
          >
            <nav class="flex items-center space-x-2">
              <button
                @click="goToPage(ordersStore.pagination.current_page - 1)"
                :disabled="!ordersStore.pagination.previous"
                class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
  
              <span class="px-4 py-2 text-sm text-gray-700">
                Page {{ ordersStore.pagination.current_page }} of {{ ordersStore.pagination.total_pages }}
              </span>
  
              <button
                @click="goToPage(ordersStore.pagination.current_page + 1)"
                :disabled="!ordersStore.pagination.next"
                class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useOrdersStore } from '@/stores/orders'
  import AppHeader from '@/components/layout/AppHeader.vue'
  
  const ordersStore = useOrdersStore()
  const loading = ref(true)
  const currentPage = ref(1)
  
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
  
  const handleCancelOrder = async (orderId) => {
    if (!confirm('Are you sure you want to cancel this order?')) {
      return
    }
  
    const result = await ordersStore.cancelOrder(orderId)
  
    if (result.success) {
      alert(result.message)
    } else {
      alert(result.message)
    }
  }
  
  const goToPage = async (page) => {
    if (page > 0 && page <= ordersStore.pagination.total_pages) {
      currentPage.value = page
      loading.value = true
      await ordersStore.fetchOrders({ page })
      loading.value = false
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
  
  onMounted(async () => {
    await ordersStore.fetchOrders()
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