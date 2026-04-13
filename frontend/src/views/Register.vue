<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-white rounded-2xl shadow-sm p-8 w-full max-w-sm border border-orange-100">
      <h2 class="text-2xl font-semibold text-gray-700 mb-1">Create account an Account</h2>
      <p class="text-gray-400 text-sm mb-6">Join BrightUp today</p>

      <input v-model="form.username" placeholder="Username" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-pink-300 mb-3" />
      <input v-model="form.email" type="email" placeholder="Email" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-pink-300 mb-3" />
      <input v-model="form.password" type="password" placeholder="Password" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-pink-300 mb-4" />

      <button @click="handleRegister" class="w-full bg-pink-100 text-black py-3 rounded-full text-sm hover:bg-pink-200 transition cursor-pointer">
        Register
      </button>

      <p v-if="error" class="text-red-400 text-xs text-center mt-3">{{ error }}</p>
      <div v-if="success" class="text-center mt-3 flex flex-col items-center gap-2">
        <p class="text-black text-sm inline-block rounded-lg bg-green-200">Account created!</p>
        <router-link to="/login" class="text-pink-400 text-sm">Login here</router-link>
      </div>
      <p class="text-center text-sm text-gray-400 mt-4">
        Already have an account? <router-link to="/login" class="text-pink-400">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const form = ref({ username: '', email: '', password: '' })
const error = ref('')
const success = ref(false)

async function handleRegister() {
  try {
    await auth.registerUser(form.value)
    success.value = true
    error.value = ''
  } catch (e) {
    error.value = 'Registration failed. Username or email may already exist.'
  }
}
</script>