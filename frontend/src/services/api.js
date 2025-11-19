import axios from 'axios'
import router from '@/router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const setAccessToken = (token) => {
  if (token) {
    sessionStorage.setItem('access_token', token)
  } else {
    sessionStorage.removeItem('access_token')
  }
}

export const setRefreshToken = (token) => {
  if (token) {
    sessionStorage.setItem('refresh_token', token)
  } else {
    sessionStorage.removeItem('refresh_token')
  }
}

export const setCurrentUser = (user) => {
  if (user) {
    sessionStorage.setItem('current_user', JSON.stringify(user))
  } else {
    sessionStorage.removeItem('current_user')
  }
}

export const getAccessToken = () => {
  return sessionStorage.getItem('access_token')
}

export const getRefreshToken = () => {
  return sessionStorage.getItem('refresh_token')
}

export const getCurrentUser = () => {
  const user = sessionStorage.getItem('current_user')
  return user ? JSON.parse(user) : null
}

export const clearTokens = () => {
  sessionStorage.removeItem('access_token')
  sessionStorage.removeItem('refresh_token')
  sessionStorage.removeItem('current_user')
}

apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = getRefreshToken()
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })

          if (response.data.access) {
            setAccessToken(response.data.access)
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`
            return apiClient(originalRequest)
          }
        }
      } catch (refreshError) {
        clearTokens()
        router.push({ name: 'login' })
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (userData) => apiClient.post('/auth/register/', userData),
  login: (credentials) => apiClient.post('/auth/login/', credentials),
  logout: () => {
    clearTokens()
    return Promise.resolve()
  },
  getProfile: () => apiClient.get('/auth/profile/'),
  updateProfile: (userData) => apiClient.put('/auth/profile/update/', userData),
  changePassword: (passwordData) => apiClient.post('/auth/password/change/', passwordData),
  requestPasswordReset: (email) =>
    apiClient.post('/auth/password/reset/request/', { email }),
  confirmPasswordReset: (data) => apiClient.post('/auth/password/reset/confirm/', data),
  verifyEmail: (token) => apiClient.post('/auth/email/verify/', { token }),
  resendVerificationEmail: () => apiClient.post('/auth/email/resend/'),
}

export default apiClient
