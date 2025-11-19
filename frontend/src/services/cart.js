import apiClient from './api'

export const cartAPI = {
  getCart: () => apiClient.get('/cart/'),

  addToCart: (data) => apiClient.post('/cart/add/', data),

  updateCartItem: (itemId, quantity) => 
    apiClient.patch(`/cart/items/${itemId}/`, { quantity }),

  removeCartItem: (itemId) => apiClient.delete(`/cart/items/${itemId}/`),

  clearCart: () => apiClient.delete('/cart/'),
}

export default cartAPI
