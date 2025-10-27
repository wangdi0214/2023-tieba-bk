import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token'))
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  // Actions
  const login = async (credentials) => {
    try {
      const response = await api.post('/auth/login/', credentials)
      const { access, refresh, user: userData } = response.data
      
      token.value = access
      user.value = userData
      
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  const register = async (userData) => {
    try {
      const response = await api.post('/auth/register/', userData)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const checkLoginStatus = async () => {
    if (token.value) {
      try {
        const response = await api.get('/auth/user/')
        user.value = response.data
      } catch (error) {
        logout()
      }
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await api.put('/auth/user/', profileData)
      user.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  return {
    // 状态
    user,
    token,
    isLoggedIn,
    
    // Actions
    login,
    register,
    logout,
    checkLoginStatus,
    updateProfile
  }
})