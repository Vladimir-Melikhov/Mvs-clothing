<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <AppHeader variant="dark" />

    <!-- Profile Content -->
    <div class="max-w-7xl mx-auto px-6 py-12 mt-20">
      <div class="mb-8">
        <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900" style="font-family: Georgia, serif;">My Profile</h1>
        <p class="mt-2 text-sm text-gray-600 tracking-wide">Manage your account information</p>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <!-- Sidebar -->
        <div class="md:col-span-1">
          <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div class="p-6 border-b border-gray-200">
              <div class="text-center">
                <div class="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span class="text-2xl font-light text-gray-600">
                    {{ userInitials }}
                  </span>
                </div>
                <h2 class="text-lg font-medium text-gray-900">{{ fullName }}</h2>
                <p class="text-sm text-gray-600">{{ user?.email }}</p>
              </div>
            </div>

            <nav class="p-4">
              <ul class="space-y-2">
                <li>
                  <router-link
                    to="/profile"
                    class="block px-4 py-2 text-sm font-medium text-gray-900 bg-gray-100 rounded"
                  >
                    Profile Information
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/profile/edit"
                    class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded transition-colors"
                  >
                    Edit Profile
                  </router-link>
                </li>
                <li>
                  <router-link
                    to="/profile/change-password"
                    class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded transition-colors"
                  >
                    Change Password
                  </router-link>
                </li>
                <li>
                  <button
                    @click="handleLogout"
                    class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded transition-colors"
                  >
                    Logout
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>

        <!-- Main Content -->
        <div class="md:col-span-2">
          <div class="bg-white border border-gray-200 rounded-lg p-8">
            <h3 class="text-xl font-light tracking-wide mb-6 text-gray-900">Profile Information</h3>

            <!-- Email Verification Alert -->
            <div v-if="!user?.is_email_verified" class="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div class="flex items-start">
                <div class="flex-1">
                  <p class="text-sm font-medium text-yellow-800">Email Not Verified</p>
                  <p class="mt-1 text-sm text-yellow-700">
                    Please verify your email address to access all features.
                  </p>
                </div>
                <button
                  @click="handleResendVerification"
                  :disabled="resendLoading"
                  class="ml-4 px-4 py-2 text-xs font-medium text-yellow-800 hover:bg-yellow-100 border border-yellow-300 rounded transition-colors"
                  :class="{ 'opacity-50 cursor-not-allowed': resendLoading }"
                >
                  {{ resendLoading ? 'Sending...' : 'Resend Email' }}
                </button>
              </div>
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
              <p class="text-sm text-green-800">{{ successMessage }}</p>
            </div>

            <!-- Profile Details -->
            <div class="space-y-6">
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <p class="text-base text-gray-900">{{ user?.first_name || 'Not provided' }}</p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <p class="text-base text-gray-900">{{ user?.last_name || 'Not provided' }}</p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                <div class="flex items-center">
                  <p class="text-base text-gray-900">{{ user?.email }}</p>
                  <span
                    v-if="user?.is_email_verified"
                    class="ml-2 inline-flex items-center px-2 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded"
                  >
                    Verified
                  </span>
                  <span
                    v-else
                    class="ml-2 inline-flex items-center px-2 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-800 rounded"
                  >
                    Not Verified
                  </span>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                <p class="text-base text-gray-900">{{ user?.phone_number || 'Not provided' }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                <p class="text-base text-gray-900">{{ formattedDateOfBirth }}</p>
              </div>

              <div class="pt-6 border-t border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">Member Since</label>
                <p class="text-base text-gray-900">{{ formattedCreatedAt }}</p>
              </div>

              <div class="pt-6 border-t border-gray-200">
                <router-link
                  to="/profile/edit"
                  class="inline-flex justify-center px-6 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
                >
                  EDIT PROFILE
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/layout/AppHeader.vue'

const router = useRouter()
const authStore = useAuthStore()

const successMessage = ref('')
const resendLoading = ref(false)

const user = computed(() => authStore.user)
const fullName = computed(() => authStore.fullName)

const userInitials = computed(() => {
  if (user.value?.first_name && user.value?.last_name) {
    return `${user.value.first_name[0]}${user.value.last_name[0]}`.toUpperCase()
  }
  return user.value?.email?.[0]?.toUpperCase() || '?'
})

const formattedDateOfBirth = computed(() => {
  if (!user.value?.date_of_birth) return 'Not provided'
  return new Date(user.value.date_of_birth).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

const formattedCreatedAt = computed(() => {
  if (!user.value?.created_at) return 'Unknown'
  return new Date(user.value.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const handleResendVerification = async () => {
  successMessage.value = ''
  resendLoading.value = true

  try {
    const result = await authStore.resendVerificationEmail()
    if (result.success) {
      successMessage.value = result.message
    }
  } finally {
    resendLoading.value = false
  }
}

onMounted(async () => {
  if (!user.value) {
    await authStore.fetchProfile()
  }
})
</script>