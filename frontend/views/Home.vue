<template>
  <div>
    <h1>Welcome to BrightUp 🌟</h1>
    <p>Your daily card</p>

    <div v-if="card">
      <h3>{{ card.title }}</h3>
      <p>{{ card.message }}</p>
      <span v-if="card.category">Category: {{ card.category }}</span>
    </div>

    <div v-else-if="loading">Loading your card...</div>
    <div v-else>No cards available today.</div>

    <div v-if="!auth.isLoggedIn">
      <p>Login to save your card and track your mood!</p>
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">Register</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTodayCard } from '../services/api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const card = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getTodayCard()
    card.value = res.data.card
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>