import { defineStore } from 'pinia'
import { login, register } from '../services/api'

function parseToken(token) {
  try {
    const base64 = token.split('.')[1]
    return JSON.parse(atob(base64))
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
  },

  actions: {
    async loginUser(credentials) {
      const res = await login(credentials)
      this.token = res.data.access_token
      localStorage.setItem('token', this.token)

      // Decode token to get role
      const payload = parseToken(this.token)
      this.user = { id: payload.sub, username: payload.username, role: payload.role }
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    async registerUser(data) {
      const res = await register(data)
      this.user = res.data
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})