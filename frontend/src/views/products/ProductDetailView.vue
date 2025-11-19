<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <AppHeader variant="dark" />

    <div v-if="loading" class="min-h-screen flex items-center justify-center mt-20">
      <p class="text-gray-600">Loading...</p>
    </div>
    <div v-else-if="error" class="min-h-screen flex items-center justify-center mt-20">
      <p class="text-red-600">{{ error }}</p>
    </div>
    <div v-else-if="currentProduct" class="bg-white">
      <div class="max-w-7xl mx-auto px-6 py-12 mt-20">
        <div class="grid md:grid-cols-2 gap-12">
          <!-- Product Images -->
          <div>
            <!-- Main Image -->
            <div class="aspect-[3/4] bg-gray-100 mb-4 overflow-hidden">
              <img
                v-if="selectedImage"
                :src="selectedImage"
                :alt="currentProduct.name"
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
            <div v-if="currentProduct.images && currentProduct.images.length > 1" class="grid grid-cols-4 gap-4">
              <div
                v-for="(image, index) in currentProduct.images"
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
                  :alt="image.alt_text || currentProduct.name"
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
              <span class="text-black uppercase">{{ currentProduct.category.name }}</span>
            </div>

            <!-- Product Name -->
            <h1 class="text-3xl font-light text-gray-900 mb-2 tracking-wide">
              {{ currentProduct.name }}
            </h1>

            <!-- Brand -->
            <p v-if="currentProduct.brand" class="text-sm text-gray-600 mb-4 tracking-wider">
              {{ currentProduct.brand }}
            </p>

            <!-- Price -->
            <div class="flex items-center space-x-3 mb-6">
              <span class="text-2xl font-medium text-gray-900">${{ currentProduct.price }}</span>
              <span
                v-if="currentProduct.is_on_sale"
                class="text-lg text-gray-400 line-through"
              >
                ${{ currentProduct.compare_at_price }}
              </span>
              <span
                v-if="currentProduct.is_on_sale"
                class="px-3 py-1 bg-black text-white text-xs tracking-wider"
              >
                -{{ currentProduct.discount_percentage }}% OFF
              </span>
            </div>

            <!-- Stock Status -->
            <div class="mb-6">
              <span
                v-if="currentProduct.is_in_stock"
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
            <div v-if="currentProduct.available_sizes && currentProduct.available_sizes.length > 0" class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <label class="block text-sm font-medium text-gray-900 tracking-wider">
                  SIZE
                </label>
              </div>
              <div class="grid grid-cols-5 gap-2">
                <button
                  v-for="size in currentProduct.available_sizes"
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
            <div v-if="currentProduct.available_colors && currentProduct.available_colors.length > 0" class="mb-6">
              <label class="block text-sm font-medium text-gray-900 mb-3 tracking-wider">
                COLOR: {{ selectedColorName }}
              </label>
              <div class="flex space-x-3">
                <button
                  v-for="color in currentProduct.available_colors"
                  :key="color.color"
                  @click="handleColorSelect(color)"
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

            <!-- Add to Cart Button -->
            <div class="mb-6">
              <button
                v-if="isAuthenticated"
                @click="handleAddToCart"
                :disabled="!currentProduct.is_in_stock || addingToCart"
                class="w-full px-6 py-4 border border-black text-sm font-medium tracking-widest transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                :class="
                  currentProduct.is_in_stock && !addingToCart
                    ? 'text-white bg-black hover:bg-gray-900'
                    : 'text-gray-400 bg-gray-100 border-gray-300'
                "
              >
                <span v-if="addingToCart">ADDING TO CART...</span>
                <span v-else-if="!currentProduct.is_in_stock">OUT OF STOCK</span>
                <span v-else>ADD TO CART</span>
              </button>
              <router-link
                v-else
                to="/login"
                class="block w-full px-6 py-4 border border-black text-sm font-medium tracking-widest text-center text-black bg-white hover:bg-black hover:text-white transition-all"
              >
                LOG IN TO PURCHASE
              </router-link>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="addToCartMessage" class="mb-6">
              <div
                class="px-4 py-3 text-sm transition-all"
                :class="
                  addToCartSuccess
                    ? 'bg-green-50 border border-green-200 text-green-800'
                    : 'bg-red-50 border border-red-200 text-red-800'
                "
              >
                <p>{{ addToCartMessage }}</p>
                <router-link
                  v-if="addToCartSuccess"
                  to="/cart"
                  class="text-green-900 underline font-medium mt-1 inline-block"
                >
                  View Cart
                </router-link>
              </div>
            </div>

            <!-- Product Description -->
            <div class="border-t border-gray-200 pt-6 mt-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                DESCRIPTION
              </h3>
              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {{ currentProduct.description }}
              </p>
            </div>

            <!-- Product Details -->
            <div class="border-t border-gray-200 pt-6 mt-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                PRODUCT DETAILS
              </h3>
              <dl class="space-y-2">
                <div v-if="currentProduct.sku" class="flex">
                  <dt class="text-sm text-gray-600 w-32">SKU:</dt>
                  <dd class="text-sm text-gray-900">{{ currentProduct.sku }}</dd>
                </div>
                <div class="flex">
                  <dt class="text-sm text-gray-600 w-32">Gender:</dt>
                  <dd class="text-sm text-gray-900 uppercase">{{ currentProduct.gender }}</dd>
                </div>
              </dl>
            </div>

            <!-- Care Instructions -->
            <div
              v-if="currentProduct.care_instructions"
              class="border-t border-gray-200 pt-6 mt-6"
            >
              <h3 class="text-sm font-medium text-gray-900 mb-3 tracking-wider">
                CARE INSTRUCTIONS
              </h3>
              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {{ currentProduct.care_instructions }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()
const productsStore = useProductsStore()
const cartStore = useCartStore()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)
const addingToCart = ref(false)
const addToCartMessage = ref('')
const addToCartSuccess = ref(false)

const currentProduct = computed(() => productsStore.currentProduct)
const isAuthenticated = computed(() => authStore.isAuthenticated)

// Image handling
const selectedImageIndex = ref(0)

const getImageUrl = (url) => {
  if (url && url.startsWith('http')) {
    return url
  }
  return `http://localhost:8002${url || ''}`
}

const selectedImage = computed(() => {
  if (currentProduct.value?.images && currentProduct.value.images.length > 0) {
    return getImageUrl(currentProduct.value.images[selectedImageIndex.value].image)
  }
  return null
})

const selectImage = (index) => {
  selectedImageIndex.value = index
}

// Variant selection
const selectedSize = ref('')
const selectedColor = ref('')
const selectedColorName = ref('')
const selectedVariantId = ref(null)
const quantity = ref(1)

const handleColorSelect = (color) => {
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
  console.log('Open image modal')
}

// Add to Cart functionality
const handleAddToCart = async () => {
  addingToCart.value = true
  addToCartMessage.value = ''
  addToCartSuccess.value = false

  // Find variant ID if size and color are selected
  let variantId = null
  if (selectedSize.value && selectedColor.value && currentProduct.value.variants) {
    const variant = currentProduct.value.variants.find(
      v => v.size === selectedSize.value && v.color === selectedColor.value
    )
    variantId = variant?.id || null
  }

  try {
    const result = await cartStore.addToCart(
      currentProduct.value.id,
      variantId,
      quantity.value
    )

    if (result.success) {
      addToCartSuccess.value = true
      addToCartMessage.value = result.message
      quantity.value = 1
      
      // Clear message after 5 seconds
      setTimeout(() => {
        addToCartMessage.value = ''
      }, 5000)
    } else {
      addToCartSuccess.value = false
      addToCartMessage.value = result.message
    }
  } catch (err) {
    addToCartSuccess.value = false
    addToCartMessage.value = 'Failed to add to cart'
  } finally {
    addingToCart.value = false
  }
}

// Fetch product data
const fetchProduct = async () => {
  const slug = route.params.slug
  loading.value = true
  error.value = null
  try {
    const result = await productsStore.fetchProductBySlug(slug)
    if (result.success) {
      // Initialize selections
      if (currentProduct.value?.available_sizes?.length > 0) {
        selectedSize.value = currentProduct.value.available_sizes[0]
      }
      if (currentProduct.value?.available_colors?.length > 0) {
        handleColorSelect(currentProduct.value.available_colors[0])
      }
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = err.message || 'Failed to fetch product'
  } finally {
    loading.value = false
  }
}

onMounted(fetchProduct)
</script>