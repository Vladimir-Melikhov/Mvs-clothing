import apiClient from './api'

export const ordersAPI = {
  getOrders: (params) => apiClient.get('/orders/', { params }),

  getOrderById: (orderId) => apiClient.get(`/orders/${orderId}/`),

  createOrder: (data) => apiClient.post('/orders/create/', data),

  cancelOrder: (orderId) => apiClient.post(`/orders/${orderId}/cancel/`),
}

export default ordersAPI
