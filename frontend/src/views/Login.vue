<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-white rounded-2xl shadow-sm p-8 w-full max-w-sm border border-pink-100">
      <h2 class="text-2xl font-semibold text-gray-700 mb-1">Welcome back!</h2>
      <p class="text-gray-400 text-sm mb-6">Login to your BrightUp account</p>

      <input v-model="form.username" placeholder="Username" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-pink-300 mb-3" />
      <input v-model="form.password" type="password" placeholder="Password" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-pink-300 mb-4" />

      <button @click="handleLogin" class="w-full text-black py-3 rounded-full text-sm transition bg-pink-50 cursor-pointer hover:bg-pink-100">
        Login
      </button>

      <p v-if="error" class="text-red-400 text-xs text-center mt-3">{{ error }}</p>
      <p class="text-center text-sm text-gray-400 mt-4">
        No account? <router-link to="/register" class="text-pink-400 hover:text-pink-500">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ username: '', password: '' })
const error = ref('')

async function handleLogin() {
  try {
    await auth.loginUser(form.value)
    if (auth.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/dashboard')
    }
  } catch (e) {
    error.value = 'Invalid username or password'
  }
}
</script>