import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const register = (data) => api.post('/auth/register', data)
export const login = (data) => {
  const form = new URLSearchParams()
  form.append('username', data.username)
  form.append('password', data.password)
  return api.post('/auth/login', form)
}

// Mood
export const rateMood = (data) => api.post('/mood/rate', data)
export const getMoodHistory = () => api.get('/mood/history')

// Cards
export const getTodayCard = () => api.get('/cards/today')
export const pickCard = (cardId) => api.post(`/cards/pick/${cardId}`)
export const getAllCards = () => api.get('/cards/all')

// Admin
export const getAdminStats = () => api.get('/admin/stats')
export const createCard = (data) => api.post('/admin/cards', data)
export const editCard = (id, data) => api.put(`/admin/cards/${id}`, data)
export const deleteCard = (id) => api.delete(`/admin/cards/${id}`)