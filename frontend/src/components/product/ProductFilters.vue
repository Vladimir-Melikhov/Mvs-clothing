<!--
File: frontend/src/components/product/ProductFilters.vue
Purpose: Filters component for product catalog
-->

<template>
    <div class="bg-white border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-6 tracking-wide">FILTERS</h3>
  
      <!-- Category Filter -->
      <div class="mb-8">
        <h4 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">CATEGORY</h4>
        <div class="space-y-2">
          <label class="flex items-center cursor-pointer group">
            <input
              type="radio"
              value=""
              v-model="localFilters.category"
              @change="emitFilters"
              class="w-4 h-4 text-black border-gray-300 focus:ring-black"
            />
            <span class="ml-3 text-sm text-gray-700 group-hover:text-black transition-colors">
              All Categories
            </span>
          </label>
          <label
            v-for="category in categories"
            :key="category.id"
            class="flex items-center cursor-pointer group"
          >
            <input
              type="radio"
              :value="category.slug"
              v-model="localFilters.category"
              @change="emitFilters"
              class="w-4 h-4 text-black border-gray-300 focus:ring-black"
            />
            <span class="ml-3 text-sm text-gray-700 group-hover:text-black transition-colors">
              {{ category.name }}
            </span>
          </label>
        </div>
      </div>
  
      <!-- Gender Filter -->
      <div class="mb-8">
        <h4 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">GENDER</h4>
        <div class="space-y-2">
          <label
            v-for="gender in genderOptions"
            :key="gender.value"
            class="flex items-center cursor-pointer group"
          >
            <input
              type="radio"
              :value="gender.value"
              v-model="localFilters.gender"
              @change="emitFilters"
              class="w-4 h-4 text-black border-gray-300 focus:ring-black"
            />
            <span class="ml-3 text-sm text-gray-700 group-hover:text-black transition-colors">
              {{ gender.label }}
            </span>
          </label>
        </div>
      </div>
  
      <!-- Price Range Filter -->
      <div class="mb-8">
        <h4 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">PRICE RANGE</h4>
        <div class="space-y-3">
          <div>
            <label class="block text-xs text-gray-600 mb-1">Min Price</label>
            <input
              type="number"
              v-model.number="localFilters.min_price"
              @change="emitFilters"
              placeholder="0"
              class="w-full px-3 py-2 border border-gray-300 text-sm focus:outline-none focus:border-black"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-600 mb-1">Max Price</label>
            <input
              type="number"
              v-model.number="localFilters.max_price"
              @change="emitFilters"
              placeholder="1000"
              class="w-full px-3 py-2 border border-gray-300 text-sm focus:outline-none focus:border-black"
            />
          </div>
        </div>
      </div>
  
      <!-- Stock Filter -->
      <div class="mb-8">
        <label class="flex items-center cursor-pointer group">
          <input
            type="checkbox"
            v-model="localFilters.in_stock"
            @change="emitFilters"
            class="w-4 h-4 text-black border-gray-300 focus:ring-black"
          />
          <span class="ml-3 text-sm text-gray-700 group-hover:text-black transition-colors">
            In Stock Only
          </span>
        </label>
      </div>
  
      <!-- Clear Filters Button -->
      <button
        @click="clearFilters"
        class="w-full px-4 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
      >
        CLEAR FILTERS
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps({
    categories: {
      type: Array,
      default: () => [],
    },
    filters: {
      type: Object,
      default: () => ({}),
    },
  })
  
  const emit = defineEmits(['update:filters'])
  
  const genderOptions = [
    { value: '', label: 'All' },
    { value: 'men', label: 'Men' },
    { value: 'women', label: 'Women' },
    { value: 'unisex', label: 'Unisex' },
  ]
  
  const localFilters = ref({
    category: props.filters.category || '',
    gender: props.filters.gender || '',
    min_price: props.filters.min_price || null,
    max_price: props.filters.max_price || null,
    in_stock: props.filters.in_stock || false,
  })
  
  watch(
    () => props.filters,
    (newFilters) => {
      localFilters.value = {
        category: newFilters.category || '',
        gender: newFilters.gender || '',
        min_price: newFilters.min_price || null,
        max_price: newFilters.max_price || null,
        in_stock: newFilters.in_stock || false,
      }
    },
    { deep: true }
  )
  
  const emitFilters = () => {
    const filters = { ...localFilters.value }
    
    // Remove empty values
    Object.keys(filters).forEach((key) => {
      if (filters[key] === '' || filters[key] === null || filters[key] === false) {
        delete filters[key]
      }
    })
  
    emit('update:filters', filters)
  }
  
  const clearFilters = () => {
    localFilters.value = {
      category: '',
      gender: '',
      min_price: null,
      max_price: null,
      in_stock: false,
    }
    emitFilters()
  }
  </script>
