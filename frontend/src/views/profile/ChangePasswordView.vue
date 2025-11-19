<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <AppHeader variant="dark" />

    <!-- Change Password Form -->
    <div class="max-w-2xl mx-auto px-6 py-12 mt-20">
      <div class="mb-8">
        <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900" style="font-family: Georgia, serif;">Change Password</h1>
        <p class="mt-2 text-sm text-gray-600 tracking-wide">Update your account password</p>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg p-8">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Current Password -->
          <div>
            <label for="old_password" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              CURRENT PASSWORD
            </label>
            <input
              id="old_password"
              v-model="formData.old_password"
              type="password"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.old_password }"
              placeholder="Enter your current password"
            />
            <p v-if="errors.old_password" class="mt-1 text-sm text-red-600">{{ errors.old_password[0] }}</p>
          </div>

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
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.new_password }"
              placeholder="Minimum 8 characters"
            />
            <p v-if="errors.new_password" class="mt-1 text-sm text-red-600">{{ errors.new_password[0] }}</p>
            <p class="mt-2 text-xs text-gray-500">
              Password must be at least 8 characters long and contain a mix of letters, numbers, and symbols.
            </p>
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
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.new_password_confirm }"
              placeholder="Confirm your new password"
            />
            <p v-if="errors.new_password_confirm" class="mt-1 text-sm text-red-600">{{ errors.new_password_confirm[0] }}</p>
          </div>

          <!-- Error Message -->
          <div
            v-if="generalError"
            class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 text-sm rounded transition-all"
          >
            <p>{{ generalError }}</p>
          </div>

          <!-- Success Message -->
          <div
            v-if="successMessage"
            class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 text-sm rounded transition-all"
          >
            <p>{{ successMessage }}</p>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between pt-6 border-t border-gray-200">
            <router-link
              to="/profile"
              class="px-6 py-3 text-sm font-medium tracking-widest text-gray-600 hover:text-black transition-colors"
            >
              CANCEL
            </router-link>
            <button
              type="submit"
              :disabled="isLoading"
              class="submit-btn px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
              :class="{ 'opacity-60 cursor-not-allowed': isLoading }"
            >
              <span v-if="!isLoading">CHANGE PASSWORD</span>
              <span v-else>CHANGING...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})

const errors = ref({})
const generalError = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  errors.value = {}
  generalError.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    const result = await authStore.changePassword(formData)

    if (result.success) {
      successMessage.value = result.message
      formData.old_password = ''
      formData.new_password = ''
      formData.new_password_confirm = ''

      setTimeout(() => {
        router.push('/profile')
      }, 2000)
    } else {
      if (result.errors) {
        errors.value = result.errors
      }
      generalError.value = result.message
    }
  } catch (error) {
    generalError.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
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
</style>