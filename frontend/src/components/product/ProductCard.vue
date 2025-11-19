<!--
File: frontend/src/components/product/ProductCard.vue
Purpose: Reusable product card component for displaying product in lists
-->

<template>
    <router-link
      :to="`/products/${product.slug}`"
      class="group block bg-white border border-gray-200 overflow-hidden transition-all duration-300 hover:shadow-lg"
    >
      <!-- Product Image -->
      <div class="relative aspect-[3/4] overflow-hidden bg-gray-100">
        <img
          v-if="imageUrl"
          :src="imageUrl"
          :alt="product.name"
          class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          @error="handleImageError"
        />
        <div
          v-else
          class="w-full h-full flex items-center justify-center text-gray-400"
        >
          <span class="text-sm">No Image</span>
        </div>
  
        <!-- Sale Badge -->
        <div
          v-if="product.is_on_sale"
          class="absolute top-4 left-4 bg-black text-white px-3 py-1 text-xs tracking-wider"
        >
          -{{ product.discount_percentage }}%
        </div>
  
        <!-- Out of Stock Badge -->
        <div
          v-if="!product.is_in_stock"
          class="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 text-xs tracking-wider"
        >
          OUT OF STOCK
        </div>
      </div>
  
      <!-- Product Info -->
      <div class="p-4">
        <!-- Category & Brand -->
        <div class="flex items-center justify-between mb-2">
          <p class="text-xs text-gray-500 tracking-wider uppercase">
            {{ product.category_name }}
          </p>
          <p v-if="product.brand" class="text-xs text-gray-400 tracking-wider">
            {{ product.brand }}
          </p>
        </div>
  
        <!-- Product Name -->
        <h3
          class="text-sm font-medium text-gray-900 mb-3 line-clamp-2 group-hover:text-gray-600 transition-colors"
        >
          {{ product.name }}
        </h3>
  
        <!-- Price -->
        <div class="flex items-center space-x-2">
          <span class="text-base font-medium text-gray-900">
            ${{ product.price }}
          </span>
          <span
            v-if="product.is_on_sale"
            class="text-sm text-gray-400 line-through"
          >
            ${{ product.compare_at_price }}
          </span>
        </div>
  
        <!-- Gender Tag -->
        <div class="mt-3">
          <span
            class="inline-block px-2 py-1 text-xs text-gray-600 border border-gray-300 tracking-wider uppercase"
          >
            {{ product.gender }}
          </span>
        </div>
      </div>
    </router-link>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  /**
   * Props definition for product card
   */
  const props = defineProps({
    product: {
      type: Object,
      required: true,
    },
  })
  
  /**
   * Get image URL - handles both absolute and relative URLs
   */
  const imageUrl = computed(() => {
    const img = props.product.primary_image
    
    if (!img) return null
    
    // If already absolute URL, return as is
    if (img.startsWith('http://') || img.startsWith('https://')) {
      return img
    }
    
    // If relative URL, prepend backend URL
    return `http://localhost:8002${img}`
  })
  
  /**
   * Handle image load error
   */
  const handleImageError = (e) => {
    console.error('Failed to load image for product:', props.product.name)
    console.error('Image URL:', imageUrl.value)
    console.error('Original primary_image:', props.product.primary_image)
  }
  </script>
  
  <style scoped>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  </style>
  