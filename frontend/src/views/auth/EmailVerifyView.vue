<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 elegant-gradient">
    <div class="max-w-md w-full">
      <!-- Logo and Header -->
      <div class="text-center mb-10">
        <h1 class="text-5xl font-light tracking-wider mb-4" style="font-family: 'Times New Roman', Georgia, serif;">
          <router-link to="/" class="hover:text-gray-600 transition-colors">Mvs-Clothing</router-link>
        </h1>
        <div class="divider-line w-16 mx-auto mb-6"></div>
        <h2 class="text-2xl font-light tracking-wide text-gray-900">Email Verification</h2>
      </div>

      <!-- Verification Content -->
      <div class="bg-white py-8 px-8 shadow-sm border border-gray-200">
        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
          <p class="mt-4 text-sm text-gray-600">Verifying your email...</p>
        </div>

        <!-- Success State -->
        <div v-else-if="verified" class="text-center space-y-4">
          <div class="w-16 h-16 bg-green-100 rounded-full mx-auto flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Email Verified Successfully!</h3>
          <p class="text-sm text-gray-600">
            Your email has been verified. You can now access all features of your account.
          </p>
          <div class="pt-4">
            <router-link
              to="/profile"
              class="inline-block px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
            >
              GO TO PROFILE
            </router-link>
          </div>
        </div>

        <!-- Error State -->
        <div v-else class="text-center space-y-4">
          <div class="w-16 h-16 bg-red-100 rounded-full mx-auto flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Verification Failed</h3>
          <p class="text-sm text-gray-600">
            {{ errorMessage || 'The verification link is invalid or has expired.' }}
          </p>
          <div class="pt-4 space-x-4">
            <router-link
              to="/"
              class="inline-block px-6 py-3 border border-gray-300 text-sm font-medium tracking-widest text-gray-700 bg-white hover:bg-gray-50 transition-all"
            >
              GO HOME
            </router-link>
            <router-link
              to="/login"
              class="inline-block px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
            >
              SIGN IN
            </router-link>
          </div>
        </div>
      </div>

      <!-- Back to Home -->
      <div class="mt-6 text-center">
        <router-link to="/" class="text-sm text-gray-600 hover:text-black transition-colors tracking-wide">
          ← BACK TO HOME
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const isLoading = ref(true)
const verified = ref(false)
const errorMessage = ref('')

const verifyEmail = async () => {
  const token = route.query.token

  if (!token) {
    errorMessage.value = 'Verification token is missing'
    isLoading.value = false
    return
  }

  try {
    const result = await authStore.verifyEmail(token)

    if (result.success) {
      verified.value = true
    } else {
      errorMessage.value = result.message
    }
  } catch (error) {
    errorMessage.value = 'An unexpected error occurred during verification'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  verifyEmail()
})
</script>

<style scoped>
.elegant-gradient {
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 50%, #f8f8f8 100%);
}

.divider-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
