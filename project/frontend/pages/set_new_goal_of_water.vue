<template>
  <section class="px-4 space-y-4 max-w-md mx-auto">
    <header class="flex">
      <button class="btn btn-ghost ps-0 text-xl" @click="go('/tab/water_tracking')">
        <font-awesome :icon="faArrowLeft" />
      </button>
      <h1 class="text-xl font-bold w-full text-center my-auto -ms-4">Yeni hedef belirle</h1>
    </header>

    <article class="space-y-4">
      <!-- Kilo Girişi -->
       <div>
        <label class="block mb-1 font-semibold">Mevsim seçin</label>
        <select v-model="selectedSeason" class="select select-bordered w-full">
          <option value="summer">Yaz</option>
          <option value="autumn">Sonbahar</option>
          <option value="winter">Kış</option>
          <option value="spring">İlkbahar</option>
        </select>
        <p class="label text-xs">
          Yaz ve Kış aylarında tüketmeniz gereken sıvı miktarı farklıdır.
        </p>
      </div>
      <div>
        <label class="block mb-1 font-semibold">Kilonuz (kg)</label>
        <input type="number" v-model.number="weight" class="input input-bordered w-full" />
      </div>

      <!-- Hesapla Butonu -->
      <button class="btn btn-primary w-full" @click="handleCalculate">Günlük ihtiyacı hesapla</button>

      <hr class="bg-base">

      <form @submit.prevent="saveTarget" class="mt-2 flex flex-col gap-4">
        <!-- Hedef Girişi -->
        <div>
          <label class="block mb-1 font-semibold">Günlük hedefiniz (mililitre)</label>
          <input ref="targetInput" type="number" v-model.number="target" class="input input-bordered w-full" />
        </div>

        <!-- Kaydet Butonu -->
        <button class="btn btn-success w-full" type="submit">Kaydet</button>
      </form>
    </article>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import { useLocaleRouter } from '~/composables/useLocaleRouter'

const { go } = useLocaleRouter()
const { $api } = useNuxtApp()

const weight = ref(null)
const target = ref(null)
const targetInput = ref(null)

const selectedSeason = ref('')

const getSeason = (date = new Date()) => {
  const month = date.getMonth() + 1
  if ([12, 1, 2].includes(month)) return 'winter'
  if ([3, 4, 5].includes(month)) return 'spring'
  if ([6, 7, 8].includes(month)) return 'summer'
  return 'autumn'
}

const calculateWaterIntake = (weight) => {
  const season = selectedSeason.value || getSeason()
  let base = weight * 33
  if (season === 'summer') base += 500
  if (season === 'winter') base -= 200
  return Math.round(base)
}

const handleCalculate = () => {
  if (!weight.value) return alert('Lütfen kilonuzu girin')
  target.value = calculateWaterIntake(weight.value)
  targetInput.value?.focus()
}

const saveTarget = async () => {
  if (!target.value) {
    alert('Lütfen bir hedef belirleyin')
    return
  }

  try {
    const res = await $api('/health/water/goal/', {
      method: 'PUT',
      body: JSON.stringify({
        daily_goal: target.value
      })
    })

    if (!res.daily_goal) throw new Error('API isteği başarısız')
    go('/tab/water_tracking')
  } catch (e) {
    console.error(e)
  }
}
onMounted(() => {
  selectedSeason.value = getSeason()
})
</script>
