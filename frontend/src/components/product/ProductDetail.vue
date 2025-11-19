<template>
    <div v-if="product" class="bg-white">
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div class="grid md:grid-cols-2 gap-12">
          <!-- Product Images -->
          <div>
            <!-- Main Image -->
            <div class="aspect-[3/4] bg-gray-100 mb-4 overflow-hidden">
              <img
                v-if="selectedImage"
                :src="selectedImage"
                :alt="product.name"
                class="w-full h-full object-cover cursor-zoom-in"
                @click="openImageModal"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center text-gray-400"
              >
                <span>No Image Available</span>
              </div>
            </div>
  
            <!-- Image Thumbnails -->
            <div v-if="product.images && product.images.length > 1" class="grid grid-cols-4 gap-4">
              <div
                v-for="(image, index) in product.images"
                :key="image.id"
                @click="selectImage(index)"
                class="aspect-square bg-gray-100 cursor-pointer border-2 transition-all"
                :class="
                  selectedImageIndex === index
                    ? 'border-black'
                    : 'border-transparent hover:border-gray-300'
                "
              >
                <img
                  :src="getImageUrl(image.image)"
                  :alt="image.alt_text || product.name"
                  class="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
  
          <!-- Product Info -->
          <div>
            <!-- Breadcrumb -->
            <div class="text-xs text-gray-500 mb-4 tracking-wider">
              <router-link to="/products" class="hover:text-black">PRODUCTS</router-link>
              <span class="mx-2">/</span>
              <span class="text-black uppercase">{{ product.category.name }}</span>
            </div>
  
            <!-- Product Name -->
            <h1 class="text-3xl font-light text-gray-900 mb-2 tracking-wide">
              {{ product.name }}
            </h1>
  
            <!-- Brand -->
            <p v-if="product.brand" class="text-sm text-gray-600 mb-4 tracking-wider">
              {{ product.brand }}
            </p>
  
            <!-- Price -->
            <div class="flex items-center space-x-3 mb-6">
              <span class="text-2xl font-medium text-gray-900">${{ product.price }}</span>
              <span
                v-if="product.is_on_sale"
                class="text-lg text-gray-400 line-through"
              >
                ${{ product.compare_at_price }}
              </span>
              <span
                v-if="product.is_on_sale"
                class="px-3 py-1 bg-black text-white text-xs tracking-wider"
              >
                -{{ product.discount_percentage }}% OFF
              </span>
            </div>
  
            <!-- Stock Status -->
            <div class="mb-6">
              <span
                v-if="product.is_in_stock"
                class="inline-flex items-center text-sm text-green-600"
              >
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                In Stock
              </span>
              <span v-else class="inline-flex items-center text-sm text-red-600">
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"
                  />
                </svg>
                Out of Stock
              </span>
            </div>
  
            <!-- Size Selection -->
            <div v-if="product.available_sizes && product.available_sizes.length > 0" class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <label class="block text-sm font-medium text-gray-900 tracking-wider">
                  SIZE
                </label>
                <button class="text-xs text-gray-600 hover:text-black underline">
                  Size Guide
                </button>
              </div>
              <div class="grid grid-cols-5 gap-2">
                <button
                  v-for="size in product.available_sizes"
                  :key="size"
                  @click="selectedSize = size"
                  class="py-3 border text-sm font-medium transition-all"
                  :class="
                    selectedSize === size
                      ? 'border-black bg-black text-white'
                      : 'border-gray-300 text-gray-900 hover:border-black'
                  "
                >
                  {{ size }}
                </button>
              </div>
            </div>
  
            <!-- Color Selection -->
            <div v-if="product.available_colors && product.available_colors.length > 0" class="mb-6">
              <label class="block text-sm font-medium text-gray-900 mb-3 tracking-wider">
                COLOR: {{ selectedColorName }}
              </label>
              <div class="flex space-x-3">
                <button
                  v-for="color in product.available_colors"
                  :key="color.color"
                  @click="selectColor(color)"
                  class="w-10 h-10 rounded-full border-2 transition-all"
                  :class="
                    selectedColor === color.color
                      ? 'border-black scale-110'
                      : 'border-gray-300 hover:border-gray-400'
                  "
                  :style="{ backgroundColor: color.color_hex || '#cccccc' }"
                  :title="color.color"
                ></button>
              </div>
            </div>
  
            <!-- Quantity -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-900 mb-3 tracking-wider">
                QUANTITY
              </label>
              <div class="flex items-center space-x-4">
                <button
                  @click="decreaseQuantity"
                  :disabled="quantity <= 1"
                  class="w-10 h-10 border border-gray-300 flex items-center justify-center hover:border-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M20 12H4"
                    />
                  </svg>
                </button>
                <span class="text-lg font-medium w-12 text-center">{{ quantity }}</span>
                <button
                  @click="increaseQuantity"
                  class="w-10 h-10 border border-gray-300 flex items-center justify-center hover:border-black transition-all"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </button>
              </div>
            </div>
  
            <!-- Product Description -->
            <div class="border-t border-gray-200 pt-6 mt-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                DESCRIPTION
              </h3>
              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {{ product.description }}
              </p>
            </div>
  
            <!-- Product Details -->
            <div class="border-t border-gray-200 pt-6 mt-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                PRODUCT DETAILS
              </h3>
              <dl class="space-y-2">
                <div v-if="product.sku" class="flex">
                  <dt class="text-sm text-gray-600 w-32">SKU:</dt>
                  <dd class="text-sm text-gray-900">{{ product.sku }}</dd>
                </div>
                <div v-if="product.material" class="flex">
                  <dt class="text-sm text-gray-600 w-32">Material:</dt>
                  <dd class="text-sm text-gray-900">{{ product.material }}</dd>
                </div>
                <div class="flex">
                  <dt class="text-sm text-gray-600 w-32">Gender:</dt>
                  <dd class="text-sm text-gray-900 uppercase">{{ product.gender }}</dd>
                </div>
              </dl>
            </div>
  
            <!-- Care Instructions -->
            <div
              v-if="product.care_instructions"
              class="border-t border-gray-200 pt-6 mt-6"
            >
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                CARE INSTRUCTIONS
              </h3>
              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {{ product.care_instructions }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  
  const props = defineProps({
    product: {
      type: Object,
      required: true,
    },
  })
  
  // Image handling
  const selectedImageIndex = ref(0)
  const selectedImage = computed(() => {
    if (props.product.images && props.product.images.length > 0) {
      return getImageUrl(props.product.images[selectedImageIndex.value].image)
    }
    return null
  })
  
  const selectImage = (index) => {
    selectedImageIndex.value = index
  }
  
  const getImageUrl = (url) => {
    if (url.startsWith('http')) {
      return url
    }
    return `http://localhost:8002${url}`
  }
  
  // Variant selection
  const selectedSize = ref('')
  const selectedColor = ref('')
  const selectedColorName = ref('')
  const quantity = ref(1)
  
  // Initialize with first available options
  watch(
    () => props.product,
    (newProduct) => {
      if (newProduct) {
        if (newProduct.available_sizes && newProduct.available_sizes.length > 0) {
          selectedSize.value = newProduct.available_sizes[0]
        }
        if (newProduct.available_colors && newProduct.available_colors.length > 0) {
          selectColor(newProduct.available_colors[0])
        }
      }
    },
    { immediate: true }
  )
  
  const selectColor = (color) => {
    selectedColor.value = color.color
    selectedColorName.value = color.color
  }
  
  const increaseQuantity = () => {
    quantity.value++
  }
  
  const decreaseQuantity = () => {
    if (quantity.value > 1) {
      quantity.value--
    }
  }
  
  const openImageModal = () => {
    // TODO: Implement image modal/lightbox
    console.log('Open image modal')
  }
  </script>