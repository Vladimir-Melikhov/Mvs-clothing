<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 elegant-gradient">
    <div class="max-w-md w-full">
      <div class="text-center mb-10">
        <h1 class="text-5xl font-light tracking-wider mb-4" style="font-family: 'Times New Roman', Georgia, serif;">
          <router-link to="/" class="hover:text-gray-600 transition-colors">Mvs-Clothing</router-link>
        </h1>
        <div class="divider-line w-16 mx-auto mb-6"></div>
        <h2 class="text-2xl font-light tracking-wide text-gray-900">Create Account</h2>
        <p class="mt-2 text-sm text-gray-600">Join Mvs-Clothing</p>
      </div>

      <div class="bg-white py-8 px-8 shadow-sm border border-gray-200">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">FIRST NAME</label>
            <input
              id="first_name"
              v-model="formData.first_name"
              type="text"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="John"
            />
          </div>

          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">LAST NAME</label>
            <input
              id="last_name"
              v-model="formData.last_name"
              type="text"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="Doe"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">EMAIL ADDRESS</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">PASSWORD</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="Minimum 8 characters"
            />
          </div>

          <div>
            <label for="password_confirm" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">CONFIRM PASSWORD</label>
            <input
              id="password_confirm"
              v-model="formData.password_confirm"
              type="password"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm"
              placeholder="Confirm your password"
            />
          </div>

          <div v-if="generalError" class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 text-sm">
            <p>{{ generalError }}</p>
          </div>

          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="submit-btn w-full flex justify-center py-3 px-4 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white focus:outline-none transition-all"
            >
              <span v-if="!isLoading">CREATE ACCOUNT</span>
              <span v-else>CREATING ACCOUNT...</span>
            </button>
          </div>
        </form>

        <div class="mt-6">
          <div class="divider-line mb-6"></div>
          <p class="text-center text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="font-medium text-black hover:text-gray-600 transition-colors tracking-wide">
              SIGN IN
            </router-link>
          </p>
        </div>
      </div>

      <div class="mt-6 text-center">
        <router-link to="/" class="text-sm text-gray-600 hover:text-black transition-colors tracking-wide">
          ← BACK TO HOME
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: '',
})

const generalError = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  generalError.value = ''
  isLoading.value = true

  try {
    const result = await authStore.register(formData)
    if (result.success) {
      router.push('/')
    } else {
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
