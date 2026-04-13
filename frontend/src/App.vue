<template>
  <div class="min-h-screen" style="background-color: var(--color-sunshine);">
    <nav class="shadow-sm px-6 py-4 flex items-center justify-between" style="background-color: var(--color-bg);">
      <router-link to="/" class="flex items-center gap-2 text-xl font-semibold" style="color: white;">
        BrightUp 
      </router-link>
      <div class="flex items-center gap-6">
        <!-- Admin tab -->
        <template v-if="auth.isAdmin">
          <router-link to="/admin" class="text-sm text-white hover:text-yellow-100 transition" :class="{ 'border-b-2 border-yellow-300': isActive('/admin') }">Admin</router-link>
          <button @click="logout" class="text-white px-4 py-2 rounded-full text-sm hover:opacity-80 transition" style="background-color: var(--color-blush);">Logout</button>
        </template>
        <!-- Regular users-->
        <template v-else-if="auth.isLoggedIn">
          <router-link to="/" class="text-sm text-white hover:text-yellow-100 transition" :class="{ 'border-b-2 border-yellow-300': isActive('/') }">Home</router-link>
          <router-link to="/dashboard" class="text-sm text-white hover:text-yellow-100 transition" :class="{ 'border-b-2 border-yellow-300': isActive('/dashboard') }">Dashboard</router-link>
          <button @click="logout" class="text-white px-4 py-2 rounded-full text-sm hover:opacity-80 transition" style="background-color: var(--color-blush);">Logout</button>
        </template>
        <!-- Not logged in -->
        <template v-else>
          <router-link to="/" class="text-sm text-white hover:text-yellow-100 transition" :class="{ 'border-b-2 border-yellow-300': isActive('/') }">Home</router-link>
          <router-link to="/login" class="text-sm text-white hover:text-yellow-100 transition" :class="{ 'border-b-2 border-yellow-300': isActive('/login') }">Login</router-link>
          <router-link to="/register" class="text-white px-4 py-2 rounded-full text-sm hover:opacity-80 transition" style="background-color: var(--color-blush);">Register</router-link>
        </template>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter, useRoute } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

function logout() {
  auth.logout()
  router.push('/login')
}

function isActive(path) {
  return route.path === path
}
</script>