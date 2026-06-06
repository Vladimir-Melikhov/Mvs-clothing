<template>
    <div class="min-h-screen bg-gray-50">
      <!-- Navigation -->
      <AppHeader variant="dark" />
  
      <!-- Page Header -->
      <div class="bg-white border-b border-gray-200 py-12 mt-20">
        <div class="max-w-7xl mx-auto px-6">
          <h1 class="text-4xl font-light tracking-[0.3em] text-gray-900 mb-2" style="font-family: Georgia, serif;">
            Products
          </h1>
          <p class="text-sm text-gray-600 tracking-wide">
            Showing {{ productsStore.pagination.count }} products
          </p>
        </div>
      </div>
  
      <!-- Main Content -->
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div class="grid lg:grid-cols-4 gap-8">
          <!-- Filters Sidebar -->
          <aside class="lg:col-span-1">
            <ProductFilters
              :categories="productsStore.categories"
              :filters="filters"
              @update:filters="updateFilters"
            />
          </aside>
  
          <!-- Products Grid -->
          <main class="lg:col-span-3">
            <!-- Sorting -->
            <div class="flex items-center justify-between mb-6">
              <p class="text-sm text-gray-600">
                {{ productsStore.products.length }} products
              </p>
              <select
                v-model="sortBy"
                @change="handleSortChange"
                class="px-4 py-2 border border-gray-300 text-sm focus:outline-none focus:border-black"
              >
                <option value="-created_at">Newest First</option>
                <option value="created_at">Oldest First</option>
                <option value="price">Price: Low to High</option>
                <option value="-price">Price: High to Low</option>
                <option value="name">Name: A to Z</option>
                <option value="-name">Name: Z to A</option>
              </select>
            </div>
  
            <!-- Products Grid -->
            <ProductGrid
              :products="productsStore.products"
              :loading="productsStore.loading"
            />
  
            <!-- Pagination -->
            <div
              v-if="productsStore.pagination.total_pages > 1"
              class="mt-12 flex justify-center"
            >
              <nav class="flex items-center space-x-2">
                <button
                  @click="goToPage(productsStore.pagination.current_page - 1)"
                  :disabled="!productsStore.pagination.previous"
                  class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
  
                <button
                  v-for="page in displayedPages"
                  :key="page"
                  @click="goToPage(page)"
                  class="px-4 py-2 border text-sm transition-colors"
                  :class="
                    page === productsStore.pagination.current_page
                      ? 'border-black bg-black text-white'
                      : 'border-gray-300 hover:border-black'
                  "
                >
                  {{ page }}
                </button>
  
                <button
                  @click="goToPage(productsStore.pagination.current_page + 1)"
                  :disabled="!productsStore.pagination.next"
                  class="px-4 py-2 border border-gray-300 text-sm hover:border-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </nav>
            </div>
          </main>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useProductsStore } from '@/stores/products'
  import ProductGrid from '@/components/product/ProductGrid.vue'
  import ProductFilters from '@/components/product/ProductFilters.vue'
  import AppHeader from '@/components/layout/AppHeader.vue'
  
  const route = useRoute()
  const router = useRouter()
  const productsStore = useProductsStore()
  
  const filters = ref({})
  const sortBy = ref('-created_at')
  const currentPage = ref(1)
  
  const displayedPages = computed(() => {
    const total = productsStore.pagination.total_pages
    const current = productsStore.pagination.current_page
    const pages = []
  
    if (total <= 7) {
      for (let i = 1; i <= total; i++) {
        pages.push(i)
      }
    } else {
      if (current <= 4) {
        for (let i = 1; i <= 5; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(total)
      } else if (current >= total - 3) {
        pages.push(1)
        pages.push('...')
        for (let i = total - 4; i <= total; i++) {
          pages.push(i)
        }
      } else {
        pages.push(1)
        pages.push('...')
        for (let i = current - 1; i <= current + 1; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(total)
      }
    }
  
    return pages
  })
  
  const updateFilters = (newFilters) => {
    filters.value = newFilters
    currentPage.value = 1
    fetchProducts()
  }
  
  const handleSortChange = () => {
    fetchProducts()
  }
  
  const goToPage = (page) => {
    if (page !== '...' && page > 0 && page <= productsStore.pagination.total_pages) {
      currentPage.value = page
      fetchProducts()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
  
  const fetchProducts = async () => {
    const params = {
      ...filters.value,
      ordering: sortBy.value,
      page: currentPage.value,
    }
  
    await productsStore.fetchProducts(params)
  }
  
  onMounted(async () => {
    await productsStore.fetchCategories()
  
    if (route.query.category) {
      filters.value.category = route.query.category
    }
    if (route.query.gender) {
      filters.value.gender = route.query.gender
    }
  
    await fetchProducts()
  })
  
  watch(
    () => route.query,
    (newQuery) => {
      if (newQuery.category) {
        filters.value.category = newQuery.category
      }
      if (newQuery.gender) {
        filters.value.gender = newQuery.gender
      }
      fetchProducts()
    }
  )
  </script>