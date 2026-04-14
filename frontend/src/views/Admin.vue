<template>
  <div class="max-w-3xl mx-auto px-4 py-10">
    <h2 class="text-3xl font-semibold text-amber-900 mb-1">Admin Dashboard</h2>
    <p class="text-gray-400 text-sm mb-8">Manage BrightUp</p>

    <!-- Stats -->
    <div class="grid grid-cols-2 gap-4 mb-8" v-if="stats">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 text-center">
        <p class="text-3xl font-semibold text-amber-900 mb-4">{{ stats.total_users }}</p>
        <p class="text-gray-400 text-sm mt-1">Total Users</p>
      </div>
       <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 text-center">
        <p class="text-3xl font-semibold text-amber-900 mt-1">{{ stats.total_ratings }}</p>
        <p class="text-gray-400 text-sm mt-1">Total Ratings</p>
      </div>
       <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 text-center">
       <p class="text-3xl font-semibold text-amber-900 mb-4">{{ stats.total_active_cards }}</p>
       <p class="text-gray-400 text-sm mt-1">Active Cards</p>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 text-center">
        <p class="text-3xl font-semibold text-amber-900 mt-1">{{ stats.average_mood_rating }}</p>
        <p class="text-gray-400 text-sm mt-1">Average Ratings</p>
      </div>
    </div>

    <!-- Add Card -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-blue-100 mb-6">
      <h3 class="text-lg font-semibold text-gray-700 mb-4">Add New Card</h3>
      <input v-model="newCard.title" placeholder="Title" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-blue-300 mb-3" />
      <input v-model="newCard.message" placeholder="Message" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-blue-300 mb-3" />
      <input v-model="newCard.category" placeholder="Category (optional)" class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-blue-300 mb-4" />
      <button @click="submitCard" :disabled="!newCard.title || !newCard.message" class="w-full py-3 rounded-full text-sm transition" :class="!newCard.title || !newCard.message ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-blue-100 hover:bg-blue-500'">
        Add Card
      </button>
      <p v-if="cardError" class="text-red-400 text-sm text-center mt-2">{{ cardError }}</p>
      <p v-if="cardSuccess" class="text-green-400 text-sm text-center mt-2">Card added!</p>
    </div>

    <!-- Cards List -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100">
      <h3 class="text-lg font-semibold text-gray-700 mb-4">Manage Cards</h3>
      <div class="flex flex-col gap-3">
        <div v-for="card in cards" :key="card.id" class="bg-orange-50 rounded-xl p-4">
          <div v-if="editingId !== card.id">
            <div class="flex items-start justify-between">
              <div>
                <p class="font-semibold text-gray-700 text-sm">{{ card.title }}</p>
                <p class="text-gray-400 text-xs mt-0.5">{{ card.message }}</p>
                <span v-if="card.category" class="inline-block mt-2 px-2 py-0.5 bg-orange-100 text-orange-400 text-xs rounded-full">{{ card.category }}</span>
              </div>
              <div class="flex gap-2 ml-4">
                <button @click="startEdit(card)" class="text-xs bg-white text-gray-500 px-3 py-1 rounded-full border border-gray-200 hover:border-orange-300">Edit</button>
                <button @click="removeCard(card.id)" class="text-xs bg-white text-red-400 px-3 py-1 rounded-full border border-red-100 hover:border-red-300">Delete</button>
              </div>
            </div>
          </div>
          <div v-else>
            <input v-model="editCardData.title" class="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm outline-none focus:border-orange-300 mb-2" />
            <input v-model="editCardData.message" class="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm outline-none focus:border-orange-300 mb-2" />
            <input v-model="editCardData.category" class="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm outline-none focus:border-orange-300 mb-3" />
            <div class="flex gap-2">
              <button @click="saveEdit(card.id)" class="bg-orange-400 text-white text-xs px-4 py-2 rounded-full hover:bg-orange-500">Save</button>
              <button @click="editingId = null" class="bg-white text-gray-400 text-xs px-4 py-2 rounded-full border border-gray-200">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminStats, createCard, editCard as updateCard, deleteCard, getAllCards } from '../services/api'

const stats = ref(null)
const cards = ref([])
const newCard = ref({ title: '', message: '', category: '' })
const cardSuccess = ref(false)
const cardError = ref('')
const editingId = ref(null)
const editCardData = ref({ title: '', message: '', category: '' })

onMounted(async () => {
  await loadStats()
  await loadCards()
})

async function loadStats() {
  try {
    const res = await getAdminStats()
    stats.value = res.data
  } catch (e) { console.error(e) }
}

async function loadCards() {
  try {
    const res = await getAllCards()
    cards.value = res.data
  } catch (e) { console.error(e) }
}

async function submitCard() {
  cardError.value = ''
  if (!newCard.value.title || !newCard.value.title.trim()) {
    cardError.value = 'Please fill in the title'
    return
  }
  if (!newCard.value.message || !newCard.value.message.trim()) {
    cardError.value = 'Please fill in the message'
    return
  }
  try {
    await createCard(newCard.value)
    cardSuccess.value = true
    newCard.value = { title: '', message: '', category: '' }
    await loadCards()
    setTimeout(() => cardSuccess.value = false, 3000)
  } catch (e) {
    cardError.value = 'Failed to add card'
    console.error(e)
  }
}

function startEdit(card) {
  editingId.value = card.id
  editCardData.value = { title: card.title, message: card.message, category: card.category }
}

async function saveEdit(id) {
  try {
    await updateCard(id, editCardData.value)
    editingId.value = null
    await loadCards()
  } catch (e) { console.error(e) }
}

async function removeCard(id) {
  try {
    await deleteCard(id)
    await loadCards()
  } catch (e) { console.error(e) }
}
</script>