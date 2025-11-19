import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  authAPI,
  setAccessToken,
  setRefreshToken,
  setCurrentUser,
  getCurrentUser,
  clearTokens,
} from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(getCurrentUser())
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const isEmailVerified = computed(() => user.value?.is_email_verified || false)
  const fullName = computed(() => user.value?.full_name || user.value?.email || '')

  // Actions
  const register = async (userData) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.register(userData)

      if (response.data.success) {
        const { user: userData, tokens } = response.data.data

        // Store tokens in memory
        setAccessToken(tokens.access)
        setRefreshToken(tokens.refresh)
        setCurrentUser(userData)

        user.value = userData

        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Registration failed'
      const errors = err.response?.data?.errors || {}
      error.value = errorMessage

      return { success: false, message: errorMessage, errors }
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.login(credentials)

      if (response.data.success) {
        const { user: userData, tokens } = response.data.data

        // Store tokens in memory
        setAccessToken(tokens.access)
        setRefreshToken(tokens.refresh)
        setCurrentUser(userData)

        user.value = userData

        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Login failed'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    await authAPI.logout()
    user.value = null
    error.value = null
  }

  const fetchProfile = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.getProfile()

      if (response.data.success) {
        user.value = response.data.data
        setCurrentUser(response.data.data)
        return { success: true }
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch profile'
      return { success: false }
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (userData) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.updateProfile(userData)

      if (response.data.success) {
        user.value = response.data.data
        setCurrentUser(response.data.data)
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Update failed'
      const errors = err.response?.data?.errors || {}
      error.value = errorMessage

      return { success: false, message: errorMessage, errors }
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.changePassword(passwordData)

      if (response.data.success) {
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Password change failed'
      const errors = err.response?.data?.errors || {}
      error.value = errorMessage

      return { success: false, message: errorMessage, errors }
    } finally {
      loading.value = false
    }
  }

  const requestPasswordReset = async (email) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.requestPasswordReset(email)

      if (response.data.success) {
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Request failed'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const confirmPasswordReset = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.confirmPasswordReset(data)

      if (response.data.success) {
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Password reset failed'
      const errors = err.response?.data?.errors || {}
      error.value = errorMessage

      return { success: false, message: errorMessage, errors }
    } finally {
      loading.value = false
    }
  }

  const verifyEmail = async (token) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.verifyEmail(token)

      if (response.data.success) {
        if (user.value) {
          user.value.is_email_verified = true
          setCurrentUser(user.value)
        }
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Verification failed'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const resendVerificationEmail = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.resendVerificationEmail()

      if (response.data.success) {
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to resend email'
      error.value = errorMessage

      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    user,
    loading,
    error,
    // Getters
    isAuthenticated,
    isEmailVerified,
    fullName,
    // Actions
    register,
    login,
    logout,
    fetchProfile,
    updateProfile,
    changePassword,
    requestPasswordReset,
    confirmPasswordReset,
    verifyEmail,
    resendVerificationEmail,
  }
})
