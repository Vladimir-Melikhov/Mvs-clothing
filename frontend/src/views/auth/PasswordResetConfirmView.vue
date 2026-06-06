<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 elegant-gradient">
    <div class="max-w-md w-full">
      <!-- Logo and Header -->
      <div class="text-center mb-10">
        <h1 class="text-5xl font-light tracking-wider mb-4" style="font-family: 'Times New Roman', Georgia, serif;">
          <router-link to="/" class="hover:text-gray-600 transition-colors">Mvs-Clothing</router-link>
        </h1>
        <div class="divider-line w-16 mx-auto mb-6"></div>
        <h2 class="text-2xl font-light tracking-wide text-gray-900">Set New Password</h2>
        <p class="mt-2 text-sm text-gray-600">Enter your new password below</p>
      </div>

      <!-- Reset Confirm Form -->
      <div class="bg-white py-8 px-8 shadow-sm border border-gray-200">
        <form v-if="!submitted" @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Token (hidden or from URL) -->
          <input type="hidden" v-model="formData.token" />

          <!-- New Password -->
          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              NEW PASSWORD
            </label>
            <input
              id="new_password"
              v-model="formData.new_password"
              type="password"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              :class="{ 'border-red-500': errors.new_password }"
              placeholder="Minimum 8 characters"
            />
            <p v-if="errors.new_password" class="mt-1 text-sm text-red-600">{{ errors.new_password[0] }}</p>
          </div>

          <!-- Confirm New Password -->
          <div>
            <label for="new_password_confirm" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              CONFIRM NEW PASSWORD
            </label>
            <input
              id="new_password_confirm"
              v-model="formData.new_password_confirm"
              type="password"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              :class="{ 'border-red-500': errors.new_password_confirm }"
              placeholder="Confirm your new password"
            />
            <p v-if="errors.new_password_confirm" class="mt-1 text-sm text-red-600">{{ errors.new_password_confirm[0] }}</p>
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
              <span v-if="!isLoading">RESET PASSWORD</span>
              <span v-else>RESETTING...</span>
            </button>
          </div>
        </form>

        <!-- Success Message -->
        <div v-else class="text-center space-y-4">
          <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 text-sm">
            <p>{{ successMessage }}</p>
          </div>
          <p class="text-sm text-gray-600">
            Your password has been successfully reset. You can now sign in with your new password.
          </p>
          <router-link
            to="/login"
            class="inline-block px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
          >
            SIGN IN
          </router-link>
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
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const formData = reactive({
  token: '',
  new_password: '',
  new_password_confirm: '',
})

const errors = ref({})
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const submitted = ref(false)

const handleSubmit = async () => {
  errors.value = {}
  errorMessage.value = ''
  isLoading.value = true

  try {
    const result = await authStore.confirmPasswordReset(formData)

    if (result.success) {
      successMessage.value = result.message
      submitted.value = true
    } else {
      if (result.errors) {
        errors.value = result.errors
      }
      errorMessage.value = result.message
    }
  } catch (error) {
    errorMessage.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Get token from URL query parameter
  formData.token = route.query.token || ''

  if (!formData.token) {
    errorMessage.value = 'Invalid or missing reset token'
  }
})
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
