<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 elegant-gradient">
    <div class="max-w-md w-full">
      <!-- Logo and Header -->
      <div class="text-center mb-10">
        <h1 class="text-5xl font-light tracking-wider mb-4" style="font-family: 'Times New Roman', Georgia, serif;">
          <router-link to="/" class="hover:text-gray-600 transition-colors">Mvs-Clothing</router-link>
        </h1>
        <div class="divider-line w-16 mx-auto mb-6"></div>
        <h2 class="text-2xl font-light tracking-wide text-gray-900">Reset Password</h2>
        <p class="mt-2 text-sm text-gray-600">Enter your email to receive reset instructions</p>
      </div>

      <!-- Reset Form -->
      <div class="bg-white py-8 px-8 shadow-sm border border-gray-200">
        <form v-if="!submitted" @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              EMAIL ADDRESS
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="your@email.com"
            />
          </div>

          <!-- Error Message -->
          <div
            v-if="errorMessage"
            class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 text-sm transition-all"
          >
            <p>{{ errorMessage }}</p>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="submit-btn w-full flex justify-center py-3 px-4 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white focus:outline-none transition-all"
              :class="{ 'opacity-60 cursor-not-allowed': isLoading }"
            >
              <span v-if="!isLoading">SEND RESET LINK</span>
              <span v-else>SENDING...</span>
            </button>
          </div>
        </form>

        <!-- Success Message -->
        <div v-else class="text-center space-y-4">
          <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 text-sm">
            <p>{{ successMessage }}</p>
          </div>
          <p class="text-sm text-gray-600">
            If an account exists with this email, you will receive password reset instructions shortly.
          </p>
        </div>

        <!-- Back to Login Link -->
        <div class="mt-6">
          <div class="divider-line mb-6"></div>
          <p class="text-center text-sm text-gray-600">
            Remember your password?
            <router-link
              to="/login"
              class="font-medium text-black hover:text-gray-600 transition-colors tracking-wide"
            >
              SIGN IN
            </router-link>
          </p>
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
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const email = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const submitted = ref(false)

const handleSubmit = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const result = await authStore.requestPasswordReset(email.value)

    if (result.success) {
      successMessage.value = result.message
      submitted.value = true
    } else {
      errorMessage.value = result.message
    }
  } catch (error) {
    errorMessage.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.elegant-gradient {
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 50%, #f8f8f8 100%);
}

.input-field {
  transition: all 0.3s ease;
}

.input-field:focus {
  border-color: #000;
  box-shadow: 0 0 0 1px #000;
}

.submit-btn {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.divider-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
}
</style>
