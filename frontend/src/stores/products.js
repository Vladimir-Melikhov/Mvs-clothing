import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI } from '@/services/products'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref([])
  const currentProduct = ref(null)
  const categories = ref([])
  const featuredProducts = ref([])
  const relatedProducts = ref([])
  const searchResults = ref([])
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
  const hasProducts = computed(() => products.value.length > 0)
  const hasFeaturedProducts = computed(() => featuredProducts.value.length > 0)
  const hasCategories = computed(() => categories.value.length > 0)

  // Actions
  const fetchCategories = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.getCategories()
      
      if (response.data.success) {
        categories.value = response.data.data
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch categories'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchProducts = async (filters = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.getProducts(filters)
      
      if (response.data.success) {
        products.value = response.data.data.results
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
      error.value = err.response?.data?.message || 'Failed to fetch products'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchProductBySlug = async (slug) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.getProductBySlug(slug)
      
      if (response.data.success) {
        currentProduct.value = response.data.data
        return { success: true, product: response.data.data }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch product'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchFeaturedProducts = async (limit = 8) => {
    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.getFeaturedProducts(limit)
      
      if (response.data.success) {
        featuredProducts.value = response.data.data
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch featured products'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchRelatedProducts = async (slug, limit = 4) => {
    try {
      const response = await productsAPI.getRelatedProducts(slug, limit)
      
      if (response.data.success) {
        relatedProducts.value = response.data.data
        return { success: true }
      }
    } catch (err) {
      console.error('Failed to fetch related products:', err)
      return { success: false }
    }
  }

  const searchProducts = async (query) => {
    if (!query || query.trim().length === 0) {
      searchResults.value = []
      return { success: true }
    }

    loading.value = true
    error.value = null

    try {
      const response = await productsAPI.searchProducts(query)
      
      if (response.data.success) {
        searchResults.value = response.data.data
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Search failed'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const clearSearchResults = () => {
    searchResults.value = []
  }

  const clearCurrentProduct = () => {
    currentProduct.value = null
  }

  return {
    // State
    products,
    currentProduct,
    categories,
    featuredProducts,
    relatedProducts,
    searchResults,
    loading,
    error,
    pagination,
    // Getters
    hasProducts,
    hasFeaturedProducts,
    hasCategories,
    // Actions
    fetchCategories,
    fetchProducts,
    fetchProductBySlug,
    fetchFeaturedProducts,
    fetchRelatedProducts,
    searchProducts,
    clearSearchResults,
    clearCurrentProduct,
  }
})
