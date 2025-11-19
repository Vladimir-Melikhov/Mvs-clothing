import apiClient from './api'

export const paymentAPI = {
  // Create Stripe checkout session
  createCheckoutSession: (orderId) => 
    apiClient.post('/payment/create-checkout-session/', { order_id: orderId }),

  // Get payment details for an order
  getPaymentByOrder: (orderId) => 
    apiClient.get(`/payment/order/${orderId}/`),
}

export default paymentAPI