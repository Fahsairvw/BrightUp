<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.username" placeholder="Username" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
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