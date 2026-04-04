<template>
  <div>
    <h2>Admin Dashboard</h2>

    <!-- Stats -->
    <div v-if="stats">
      <h3>System Stats</h3>
      <p>👥 Total Users: {{ stats.total_users }}</p>
      <p>😊 Total Ratings: {{ stats.total_ratings }}</p>
      <p>🃏 Total Active Cards: {{ stats.total_active_cards }}</p>
      <p>⭐ Average Mood Rating: {{ stats.average_mood_rating }}</p>
    </div>

    <!-- Add Card -->
    <div>
      <h3>Add New Card</h3>
      <input v-model="newCard.title" placeholder="Title" />
      <input v-model="newCard.message" placeholder="Message" />
      <input v-model="newCard.category" placeholder="Category (optional)" />
      <button @click="submitCard">Add Card</button>
      <p v-if="cardSuccess" style="color:green">Card added! ✅</p>
    </div>

    <!-- Cards List -->
    <div>
      <h3>Manage Cards</h3>
      <div v-for="card in cards" :key="card.id">
        <div v-if="editingId !== card.id">
          <strong>{{ card.title }}</strong> — {{ card.message }}
          <button @click="startEdit(card)">Edit</button>
          <button @click="removeCard(card.id)" style="color:red">Delete</button>
        </div>
        <div v-else>
          <input v-model="editCard.title" />
          <input v-model="editCard.message" />
          <input v-model="editCard.category" />
          <button @click="saveEdit(card.id)">Save</button>
          <button @click="editingId = null">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  getAdminStats, 
  createCard, 
  editCard as updateCard, 
  deleteCard,
  getTodayCard
} from '../services/api'
import axios from 'axios'

const stats = ref(null)
const cards = ref([])
const newCard = ref({ title: '', message: '', category: '' })
const cardSuccess = ref(false)
const editingId = ref(null)
const editCard = ref({ title: '', message: '', category: '' })

onMounted(async () => {
  await loadStats()
  await loadCards()
})

async function loadStats() {
  try {
    const res = await getAdminStats()
    stats.value = res.data
  } catch (e) {
    console.error(e)
  }
}

async function loadCards() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/cards/all')
    cards.value = res.data
  } catch (e) {
    console.error(e)
  }
}

async function submitCard() {
  try {
    await createCard(newCard.value)
    cardSuccess.value = true
    newCard.value = { title: '', message: '', category: '' }
    await loadCards()
  } catch (e) {
    console.error(e)
  }
}

function startEdit(card) {
  editingId.value = card.id
  editCard.value = { title: card.title, message: card.message, category: card.category }
}

async function saveEdit(id) {
  try {
    await updateCard(id, editCard.value)
    editingId.value = null
    await loadCards()
  } catch (e) {
    console.error(e)
  }
}

async function removeCard(id) {
  try {
    await deleteCard(id)
    await loadCards()
  } catch (e) {
    console.error(e)
  }
}
</script>