import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartAPI } from '@/services/cart'

export const useCartStore = defineStore('cart', () => {
  // State
  const cart = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const items = computed(() => cart.value?.items || [])
  const totalItems = computed(() => cart.value?.total_items || 0)
  const subtotal = computed(() => cart.value?.subtotal || 0)
  const isEmpty = computed(() => totalItems.value === 0)

  // Actions
  const fetchCart = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.getCart()
      
      if (response.data.success) {
        cart.value = response.data.data
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch cart'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const addToCart = async (productId, variantId = null, quantity = 1) => {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.addToCart({
        product_id: productId,
        variant_id: variantId,
        quantity: quantity,
      })

      if (response.data.success) {
        cart.value = response.data.data
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to add to cart'
      error.value = errorMessage
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const updateCartItem = async (itemId, quantity) => {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.updateCartItem(itemId, quantity)

      if (response.data.success) {
        cart.value = response.data.data
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to update cart item'
      error.value = errorMessage
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const removeCartItem = async (itemId) => {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.removeCartItem(itemId)

      if (response.data.success) {
        cart.value = response.data.data
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to remove cart item'
      error.value = errorMessage
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const clearCart = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.clearCart()

      if (response.data.success) {
        cart.value = response.data.data
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to clear cart'
      error.value = errorMessage
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    cart,
    loading,
    error,
    // Getters
    items,
    totalItems,
    subtotal,
    isEmpty,
    // Actions
    fetchCart,
    addToCart,
    updateCartItem,
    removeCartItem,
    clearCart,
  }
})
