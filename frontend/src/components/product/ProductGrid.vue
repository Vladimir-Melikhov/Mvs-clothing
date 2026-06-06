<!--
File: frontend/src/components/product/ProductGrid.vue
Purpose: Grid layout component for displaying multiple products
-->

<template>
    <div>
      <!-- Products Grid -->
      <div
        v-if="products.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
  
      <!-- Empty State -->
      <div
        v-else-if="!loading"
        class="text-center py-16"
      >
        <div class="inline-block w-16 h-16 mb-4 text-gray-300">
          <svg
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1"
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
        </div>
        <h3 class="text-xl font-light text-gray-900 mb-2">No Products Found</h3>
        <p class="text-sm text-gray-600">Try adjusting your filters or search criteria</p>
      </div>
  
      <!-- Loading State -->
      <div
        v-if="loading"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <div
          v-for="i in 8"
          :key="i"
          class="animate-pulse"
        >
          <div class="aspect-[3/4] bg-gray-200 mb-4"></div>
          <div class="h-4 bg-gray-200 mb-2"></div>
          <div class="h-4 bg-gray-200 w-2/3"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import ProductCard from './ProductCard.vue'
  
  defineProps({
    products: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
  })
  </script>
