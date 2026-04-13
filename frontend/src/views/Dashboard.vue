<template>
  <div class="max-w-2xl mx-auto px-4 py-10">
    <div class="bg-blue-100 rounded-2xl px-4 py-4">
      <h2 class="text-3xl font-semibold text-amber-900 mb-1">Hi, {{ auth.user?.username || 'there' }}!</h2>
      <p class="text-gray-400 text-sm mb-8">Let's track your daily mood </p>
    </div>
    

    <!-- Rate Mood -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 mb-6">
      <div v-if="!ratedToday">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">How are you feeling today?</h3>
        <div class="flex gap-2 justify-center mb-4">
          <button
            v-for="star in 5"
            :key="star"
            @click="selectedRating = star"
            class="text-4xl transition-transform hover:scale-110"
            :class="selectedRating >= star ? 'text-yellow-400' : 'text-gray-200'"
            style="background:none; padding:0; border:none; box-shadow:none"
          >★</button>
        </div>
        <textarea
          v-model="note"
          placeholder="Add a note (optional)"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm outline-none focus:border-orange-300 mb-4 resize-none"
          rows="3"
        ></textarea>
        <button
          @click="submitRating"
          :disabled="!selectedRating"
          class="w-full bg-orange-400 text-white py-3 rounded-full text-sm hover:bg-orange-500 transition disabled:opacity-40"
        >
          Submit Rating
        </button>
        <p v-if="ratingError" class="text-red-400 text-xs text-center mt-2">{{ ratingError }}</p>
      </div>
      <div v-else class="text-center py-4 ">
        <CalendarCheck class="mx-auto block w-20 h-20" />
        <p class="text-gray-500">You've already rated today!</p>
        <p class="text-gray-300 text-xs mt-1">See you tomorrow!</p>
      </div>
    </div>

    <!-- Mood Chart -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 mb-6" v-if="history.length > 0">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-700">Mood Over Time </h3>
        <!-- Filter buttons -->
        <div class="flex gap-2">
          <button
            v-for="f in filters"
            :key="f.value"
            @click="changeChartFilter(f.value)"
            class="text-xs px-3 py-1 rounded-full border transition"
            :class="activeChartFilter === f.value
              ? 'bg-orange-400 text-white border-orange-400'
              : 'bg-white text-gray-400 border-gray-200 hover:border-orange-300'"
            style="box-shadow:none"
          >{{ f.label }}</button>
        </div>
      </div>

      <!-- Average -->
      <div class="flex items-center gap-3 mb-4 px-4 py-3 bg-orange-50 rounded-xl">
        <div>
          <p class="text-xs text-gray-400">Average mood ({{ filters.find(f => f.value === activeChartFilter)?.label }})</p>
          <p class="text-xl font-semibold text-orange-400">
            {{ average }} <span class="text-yellow-400 text-base">{{ '★'.repeat(Math.round(average)) }}</span>
          </p>
        </div>
      </div>

      <Line :data="chartData" :options="chartOptions" />
    </div>

    <!-- Mood History -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-orange-100">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-700">Mood History</h3>
        <!-- Filter buttons -->
        <div class="flex gap-2">
          <button
            v-for="f in filters"
            :key="f.value"
            @click="changeFilter(f.value)"
            class="text-xs px-3 py-1 rounded-full border transition"
            :class="activeFilter === f.value
              ? 'bg-orange-400 text-white border-orange-400'
              : 'bg-white text-gray-400 border-gray-200 hover:border-orange-300'"
            style="box-shadow:none"
          >{{ f.label }}</button>
        </div>
      </div>
      <div v-if="filteredHistory.length === 0" class="text-center text-gray-300 py-4">No mood ratings for this period.</div>
      <div v-else class="flex flex-col gap-3">
        <div
          v-for="mood in paginatedHistory"
          :key="mood.id"
          class="flex items-center justify-between px-4 py-3 bg-orange-50 rounded-xl"
        >
          <div>
            <p class="text-sm text-gray-500">{{ mood.rated_at }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ mood.note || '—' }}</p>
          </div>
          <p class="text-yellow-400 text-lg">{{ '★'.repeat(mood.rating) }}<span class="text-gray-200">{{ '★'.repeat(5 - mood.rating) }}</span></p>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6">
        <button
          @click="currentPage = Math.max(1, currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-full border border-gray-200 text-sm transition disabled:opacity-40"
          :class="currentPage === 1 ? 'cursor-not-allowed' : 'hover:border-orange-400'"
        >
          ← Prev
        </button>
        <div class="flex items-center gap-2">
          <span v-for="page in totalPages" :key="page"
            @click="currentPage = page"
            :class="currentPage === page ? 'bg-orange-400 text-white' : 'bg-white text-gray-600 border border-gray-200'"
            class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer text-sm transition hover:border-orange-400"
          >{{ page }}</span>
        </div>
        <button
          @click="currentPage = Math.min(totalPages, currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-full border border-gray-200 text-sm transition disabled:opacity-40"
          :class="currentPage === totalPages ? 'cursor-not-allowed' : 'hover:border-orange-400'"
        >
          Next →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { rateMood, getMoodHistory } from '../services/api'
import { useAuthStore } from '../stores/auth'
import { Line } from 'vue-chartjs'
import { CalendarCheck, ChartLine } from '@lucide/vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler)

const auth = useAuthStore()
const selectedRating = ref(0)
const note = ref('')
const ratedToday = ref(false)
const ratingError = ref('')
const history = ref([])
const activeFilter = ref('all')
const activeChartFilter = ref('all')
const currentPage = ref(1)
const itemsPerPage = 5

const filters = [
  { label: 'Day', value: 'day' },
  { label: 'Week', value: 'week' },
  { label: 'Month', value: 'month' },
  { label: 'All', value: 'all' },
]

const filteredHistory = computed(() => {
  const now = new Date()
  return history.value.filter(m => {
    const date = new Date(m.rated_at)
    if (activeFilter.value === 'day') {
      return date.toDateString() === now.toDateString()
    } else if (activeFilter.value === 'week') {
      const weekAgo = new Date(now)
      weekAgo.setDate(now.getDate() - 7)
      return date >= weekAgo
    } else if (activeFilter.value === 'month') {
      const monthAgo = new Date(now)
      monthAgo.setMonth(now.getMonth() - 1)
      return date >= monthAgo
    }
    return true
  })
})

const paginatedHistory = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredHistory.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredHistory.value.length / itemsPerPage)
})

const filteredChartHistory = computed(() => {
  const now = new Date()
  return history.value.filter(m => {
    const date = new Date(m.rated_at)
    if (activeChartFilter.value === 'day') {
      return date.toDateString() === now.toDateString()
    } else if (activeChartFilter.value === 'week') {
      const weekAgo = new Date(now)
      weekAgo.setDate(now.getDate() - 7)
      return date >= weekAgo
    } else if (activeChartFilter.value === 'month') {
      const monthAgo = new Date(now)
      monthAgo.setMonth(now.getMonth() - 1)
      return date >= monthAgo
    }
    return true
  })
})

const average = computed(() => {
  if (filteredChartHistory.value.length === 0) return 0
  const sum = filteredChartHistory.value.reduce((acc, m) => acc + m.rating, 0)
  return (sum / filteredChartHistory.value.length).toFixed(1)
})

const chartData = computed(() => {
  const sorted = [...filteredChartHistory.value].reverse()
  return {
    labels: sorted.map(m => m.rated_at),
    datasets: [{
      label: 'Mood Rating',
      data: sorted.map(m => m.rating),
      borderColor: '#fb923c',
      backgroundColor: 'rgba(251, 146, 60, 0.1)',
      borderWidth: 2,
      pointBackgroundColor: '#fb923c',
      pointRadius: 5,
      tension: 0.4,
      fill: true,
    }]
  }
})

const chartOptions = {
  responsive: true,
  scales: {
    y: {
      min: 1,
      max: 5,
      ticks: {
        stepSize: 1,
        callback: (val) => '★'.repeat(val)
      },
      grid: { color: '#fef3ec' }
    },
    x: { grid: { display: false } }
  },
  plugins: {
    legend: { display: false }
  }
}

onMounted(async () => {
  await loadHistory()
})

async function loadHistory() {
  try {
    const res = await getMoodHistory()
    history.value = res.data
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
    ratingError.value = 'Failed to submit. Try again.'
  }
}

function changeFilter(filterValue) {
  activeFilter.value = filterValue
  currentPage.value = 1
}

function changeChartFilter(filterValue) {
  activeChartFilter.value = filterValue
}
</script>