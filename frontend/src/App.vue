<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/dashboard" v-if="auth.isLoggedIn">Dashboard</router-link>
      <router-link to="/admin" v-if="auth.isAdmin">Admin</router-link>
      <router-link to="/login" v-if="!auth.isLoggedIn">Login</router-link>
      <router-link to="/register" v-if="!auth.isLoggedIn">Register</router-link>
      <button v-if="auth.isLoggedIn" @click="logout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>