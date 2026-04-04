<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="form.username" placeholder="Username" required />
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
    <p v-if="success" style="color:green">Account created! <router-link to="/login">Login here</router-link></p>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
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