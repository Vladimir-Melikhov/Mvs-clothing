<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <AppHeader variant="dark" />

    <!-- Edit Form Content -->
    <div class="max-w-3xl mx-auto px-6 py-12 mt-20">
      <div class="mb-8">
        <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900" style="font-family: Georgia, serif;">Edit Profile</h1>
        <p class="mt-2 text-sm text-gray-600 tracking-wide">Update your profile information</p>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg p-8">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- First Name -->
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              FIRST NAME
            </label>
            <input
              id="first_name"
              v-model="formData.first_name"
              type="text"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.first_name }"
            />
            <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name[0] }}</p>
          </div>

          <!-- Last Name -->
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              LAST NAME
            </label>
            <input
              id="last_name"
              v-model="formData.last_name"
              type="text"
              required
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.last_name }"
            />
            <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name[0] }}</p>
          </div>

          <!-- Phone Number -->
          <div>
            <label for="phone_number" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              PHONE NUMBER <span class="text-gray-500 font-normal">(Optional)</span>
            </label>
            <input
              id="phone_number"
              v-model="formData.phone_number"
              type="tel"
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.phone_number }"
              placeholder="+1234567890"
            />
            <p v-if="errors.phone_number" class="mt-1 text-sm text-red-600">{{ errors.phone_number[0] }}</p>
          </div>

          <!-- Date of Birth -->
          <div>
            <label for="date_of_birth" class="block text-sm font-medium text-gray-700 mb-2 tracking-wide">
              DATE OF BIRTH <span class="text-gray-500 font-normal">(Optional)</span>
            </label>
            <input
              id="date_of_birth"
              v-model="formData.date_of_birth"
              type="date"
              class="input-field appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none text-sm rounded"
              :class="{ 'border-red-500': errors.date_of_birth }"
            />
            <p v-if="errors.date_of_birth" class="mt-1 text-sm text-red-600">{{ errors.date_of_birth[0] }}</p>
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
              <span v-if="!isLoading">SAVE CHANGES</span>
              <span v-else>SAVING...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const formData = reactive({
  first_name: '',
  last_name: '',
  phone_number: '',
  date_of_birth: '',
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
    const updateData = { ...formData }
    if (!updateData.phone_number) delete updateData.phone_number
    if (!updateData.date_of_birth) delete updateData.date_of_birth

    const result = await authStore.updateProfile(updateData)

    if (result.success) {
      successMessage.value = result.message
      setTimeout(() => {
        router.push('/profile')
      }, 1500)
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

onMounted(async () => {
  if (!user.value) {
    await authStore.fetchProfile()
  }

  if (user.value) {
    formData.first_name = user.value.first_name || ''
    formData.last_name = user.value.last_name || ''
    formData.phone_number = user.value.phone_number || ''
    formData.date_of_birth = user.value.date_of_birth || ''
  }
})
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