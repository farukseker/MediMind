<template>
  <div class="flex flex-col items-center gap-4">

    <div class="w-full max-w-xl bg-white dark:bg-gray-900 rounded-xl shadow p-2">
      <h2 class="text-lg font-semibold text-center mb-2">Kilo Değişimi Grafiği</h2>
      <ApexChart
        type="line"
        height="300"
        :options="chartOptions"
        :series="chartSeries"
      />
    </div>

    <ul class="w-full space-y-2 mb-6">
      <li
        v-for="(entry, index) in weightHistory"
        :key="index"
        class="bg-white rounded-lg shadow p-3 text-sm flex justify-between"
      >
        <span>{{ entry.weight }} kg</span>
        <span class="text-gray-500">{{ entry.date }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
const newWeight = ref(null)
const weightHistory = ref([])

const addWeight = () => {
  if (!newWeight.value || newWeight.value <= 0) return

  const now = new Date()
  weightHistory.value.unshift({
    weight: newWeight.value,
    date: now.toLocaleDateString('tr-TR'),
  })

  newWeight.value = null
}

const latestWeight = computed(() => {
  return weightHistory.value[0]?.weight || '-'
})

const weightChange = computed(() => {
  if (weightHistory.value.length < 2) return 0
  return (weightHistory.value[0].weight - weightHistory.value[1].weight).toFixed(1)
})

// ApexCharts için verileri formatla
const chartSeries = computed(() => [
  {
    name: 'Kilo',
    data: weightHistory.value.map(entry => entry.weight).reverse(),
  },
])

const chartOptions = computed(() => ({
  chart: {
    id: 'weight-chart',
    toolbar: { show: false },
  },
  xaxis: {
    categories: weightHistory.value.map(entry => entry.date).reverse(),
  },
  stroke: {
    curve: 'smooth',
  },
  markers: {
    size: 4,
  },
  colors: ['#3b82f6'], // Tailwind primary-500
  yaxis: {
    title: {
      text: 'Kilo (kg)',
    },
  },
}))
</script>
