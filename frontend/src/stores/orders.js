import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ordersAPI } from '@/services/orders'

export const useOrdersStore = defineStore('orders', () => {
  // State
  const orders = ref([])
  const currentOrder = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    page_size: 20,
    total_pages: 0,
    current_page: 1,
  })

  // Getters
  const hasOrders = computed(() => orders.value.length > 0)

  // Actions
  const fetchOrders = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await ordersAPI.getOrders(params)

      if (response.data.success) {
        orders.value = response.data.data.results
        pagination.value = {
          count: response.data.data.count,
          next: response.data.data.next,
          previous: response.data.data.previous,
          page_size: response.data.data.page_size,
          total_pages: response.data.data.total_pages,
          current_page: response.data.data.current_page,
        }
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch orders'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchOrderById = async (orderId) => {
    loading.value = true
    error.value = null

    try {
      const response = await ordersAPI.getOrderById(orderId)

      if (response.data.success) {
        currentOrder.value = response.data.data
        return { success: true, order: response.data.data }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch order'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const createOrder = async (orderData) => {
    loading.value = true
    error.value = null

    try {
      const response = await ordersAPI.createOrder(orderData)

      if (response.data.success) {
        currentOrder.value = response.data.data
        return { success: true, order: response.data.data, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to create order'
      const errors = err.response?.data?.errors || {}
      error.value = errorMessage

      return { success: false, message: errorMessage, errors }
    } finally {
      loading.value = false
    }
  }

  const cancelOrder = async (orderId) => {
    loading.value = true
    error.value = null

    try {
      const response = await ordersAPI.cancelOrder(orderId)

      if (response.data.success) {
        // Update order in list if it exists
        const orderIndex = orders.value.findIndex((o) => o.id === orderId)
        if (orderIndex !== -1) {
          orders.value[orderIndex] = response.data.data
        }

        // Update current order if it matches
        if (currentOrder.value?.id === orderId) {
          currentOrder.value = response.data.data
        }

        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to cancel order'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const clearCurrentOrder = () => {
    currentOrder.value = null
  }

  return {
    // State
    orders,
    currentOrder,
    loading,
    error,
    pagination,
    // Getters
    hasOrders,
    // Actions
    fetchOrders,
    fetchOrderById,
    createOrder,
    cancelOrder,
    clearCurrentOrder,
  }
})
