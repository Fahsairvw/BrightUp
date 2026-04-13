<template>
  <div class="max-w-2xl mx-auto px-4 py-10 text-center">
    <div class="mb-10 bg-amber-100 rounded-2xl p-8 shadow-sm border border-amber-100">
      <h1 class="text-3xl font-semibold text-amber-900 mb-2">Welcome to BrightUp!</h1>
      <p class="text-gray-400 mb-10">Pick a card before you start a messy day!</p>
    </div>
   
    <!-- Already picked today -->
    <div v-if="pickedCard" class="rounded-2xl p-8 shadow-sm border bg-pink-50 border-pink-100">
      <p class="text-xs text-pink-400 font-medium uppercase tracking-wide mb-3">Your card today</p>
      <h2 class="text-2xl font-semibold text-gray-700 mb-3">{{ pickedCard.title }}</h2>
      <p class="text-gray-500 leading-relaxed">{{ pickedCard.message }}</p>
      <span v-if="pickedCard.category" class="inline-block mt-4 px-3 py-1 text-pink-500 text-xs rounded-full">{{ pickedCard.category }}</span>
      <p class="mt-6 text-xs text-gray-400">Come back tomorrow for a new card</p>
    </div>

    <!-- Card picking -->
    <div v-else>
    <p class="text-lg text-gray-700 text-left rounded-2xl px-4 py-2 shadow-sm border border-pink-100 bg-pink-50 font-bold">
      {{ revealed ? 'Your card has been revealed!' : 'Pick a card' }}</p>      
      <div class="flex justify-center gap-4 flex-wrap rounded-2xl p-8 shadow-sm border border-pink-100 bg-pink-50">
        <div
          v-for="(card, index) in displayCards"
          :key="index"
          @click="!revealed && pickThisCard(card)"
          class="cursor-pointer hover:scale-105 transition-transform"
          style="perspective: 1000px"
        >
          <!-- Card flip container -->
          <div
            class="relative w-32 h-48 transition-all duration-700"
            :style="{ transformStyle: 'preserve-3d', transform: selectedIndex === index ? 'rotateY(180deg)' : 'rotateY(0deg)' }"
          >
            <!-- Card Back (face down) -->
            <div
              class="absolute inset-0 rounded-2xl flex items-center justify-center shadow-md bg-red-500"
              style="backface-visibility: hidden"
            >
              <img :src="cardIcon" alt="card icon" class="w-12 h-12" />
            </div>

            <!-- Card Front (revealed) -->
            <div
              class="absolute inset-0 bg-white rounded-2xl shadow-md p-3 flex flex-col items-center justify-center"
              style="backface-visibility: hidden; transform: rotateY(180deg)"
            >
              <p class="text-xs font-semibold mb-1">{{ card.title }}</p>
              <p class="text-xs text-gray-500 leading-tight">{{ card.message }}</p>
            </div>
          </div>
        </div>
    </div>

      <div v-if="!auth.isLoggedIn" class="rounded-2xl px-4 py-2 shadow-sm border border-pink-100 bg-pink-50 font-bold text-sm text-gray-400">
        <router-link to="/login" class="text-orange-400 text-left">Login</router-link> to save your card daily!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllCards, getTodayCard, pickCard } from '../services/api'
import { useAuthStore } from '../stores/auth'
import cardIcon from '../assets/images/icon.png'

const auth = useAuthStore()
const displayCards = ref([])
const pickedCard = ref(null)
const selectedIndex = ref(null)
const revealed = ref(false)

onMounted(async () => {
  try {
    // Check if already picked today
    const todayRes = await getTodayCard()
    if (todayRes.data.card) {
      pickedCard.value = todayRes.data.card
      return
    }

    // Get all cards and shuffle
    const allRes = await getAllCards()
    const shuffled = allRes.data.sort(() => Math.random() - 0.5)
    const cardsToShow = allRes.data.length > 8 ? 8 : allRes.data.length
    displayCards.value = shuffled.slice(0, cardsToShow)
  } catch (e) {
    console.error(e)
  }
})

async function pickThisCard(card) {
  const index = displayCards.value.indexOf(card)
  selectedIndex.value = index
  revealed.value = true

  try {
    await pickCard(card.id)
  } catch (e) {
    // unauth user, just show the card anyway
    console.log('Not saved (not logged in)')
  }

  // After 1.5s show the full card
  setTimeout(() => {
    pickedCard.value = card
  }, 1500)
}
</script>