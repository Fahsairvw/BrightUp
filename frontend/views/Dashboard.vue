<template>
  <div>
    <h2>My Dashboard</h2>

    <!-- Rate Mood -->
    <div v-if="!ratedToday">
      <h3>How are you feeling today?</h3>
      <div>
        <button 
          v-for="star in 5" 
          :key="star" 
          @click="selectedRating = star"
          :style="{ color: selectedRating >= star ? 'gold' : 'gray', fontSize: '2rem' }"
        >★</button>
      </div>
      <textarea v-model="note" placeholder="Add a note (optional)"></textarea>
      <button @click="submitRating" :disabled="!selectedRating">Submit</button>
      <p v-if="ratingError" style="color:red">{{ ratingError }}</p>
    </div>
    <div v-else>
      <p>✅ You have already rated today!</p>
    </div>

    <!-- Mood History -->
    <div>
      <h3>My Mood History</h3>
      <div v-if="history.length === 0">No mood ratings yet.</div>
      <table v-else>
        <thead>
          <tr>
            <th>Date</th>
            <th>Rating</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mood in history" :key="mood.id">
            <td>{{ mood.rated_at }}</td>
            <td>{{ '★'.repeat(mood.rating) }}</td>
            <td>{{ mood.note || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { rateMood, getMoodHistory } from '../services/api'

const selectedRating = ref(0)
const note = ref('')
const ratedToday = ref(false)
const ratingError = ref('')
const history = ref([])

onMounted(async () => {
  await loadHistory()
})

async function loadHistory() {
  try {
    const res = await getMoodHistory()
    history.value = res.data

    // Check if already rated today
    const today = new Date().toISOString().split('T')[0]
    ratedToday.value = history.value.some(m => m.rated_at === today)
  } catch (e) {
    console.error(e)
  }
}

async function submitRating() {
  try {
    await rateMood({ rating: selectedRating.value, note: note.value })
    ratedToday.value = true
    await loadHistory()
  } catch (e) {
    ratingError.value = 'Failed to submit rating. Try again.'
  }
}
</script>