import apiClient from './api'

export const productsAPI = {
  // Categories
  getCategories: () => apiClient.get('/products/categories/'),
  getCategoryBySlug: (slug) => apiClient.get(`/products/categories/${slug}/`),

  // Products
  getProducts: (params) => apiClient.get('/products/', { params }),
  getProductBySlug: (slug) => apiClient.get(`/products/${slug}/`),
  getFeaturedProducts: (limit = 8) => apiClient.get('/products/featured/', { params: { limit } }),
  getRelatedProducts: (slug, limit = 4) => apiClient.get(`/products/${slug}/related/`, { params: { limit } }),
  searchProducts: (query) => apiClient.get('/products/search/', { params: { q: query } }),
}

export default productsAPI
