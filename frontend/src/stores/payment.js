import { defineStore } from 'pinia'
import { ref } from 'vue'
import { paymentAPI } from '@/services/payment'

export const usePaymentStore = defineStore('payment', () => {
  // State
  const currentPayment = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Actions
  const createCheckoutSession = async (orderId) => {
    loading.value = true
    error.value = null

    try {
      const response = await paymentAPI.createCheckoutSession(orderId)

      if (response.data.success) {
        currentPayment.value = response.data.data.payment
        const checkoutUrl = response.data.data.checkout_url
        
        return { 
          success: true, 
          payment: response.data.data.payment,
          checkoutUrl: checkoutUrl
        }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to create checkout session'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const getPaymentByOrder = async (orderId) => {
    loading.value = true
    error.value = null

    try {
      const response = await paymentAPI.getPaymentByOrder(orderId)

      if (response.data.success) {
        currentPayment.value = response.data.data
        return { success: true, payment: response.data.data }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to fetch payment'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const clearCurrentPayment = () => {
    currentPayment.value = null
  }

  return {
    // State
    currentPayment,
    loading,
    error,
    // Actions
    createCheckoutSession,
    getPaymentByOrder,
    clearCurrentPayment,
  }
})