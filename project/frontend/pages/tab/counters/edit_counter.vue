<template>
<div class="p-4 space-y-4 max-w-md mx-auto">
    <h2 class="text-secondary">Sayaçlar</h2>
  <article>
    <ul class="flex flex-col gap-2">
        <li v-for="(counter, index) in counters_list">
            <div class="card border border-primary-content flex flex-row justify-between p-2 gap-2">
                <div>
                    <strong>{{ counter.name }}</strong>
                    <p>
                        <span class="text-secondary-content text-sm">Sayım:</span><span class="text-secondary text-sm">{{ counter.count }}</span>
                    </p>
                </div>
                <div class="my-auto text-xl font-mono border-b border-secondary-content">
                    {{ counter.count }}
                </div>
                <div class="flex gap-2 my-auto">
                    <button :disabled="counter.is_progress" class="btn btn-sm btn-primary" @click="counter_tick(index, 1)"><font-awesome :icon="faPlus" /></button>
                    <button :disabled="counter.is_progress" class="btn btn-sm btn-error text-white" @click="counter_tick(index, -1)"><font-awesome :icon="faMinus" /></button>
                        <div class="w-full"></div>
                    <button :disabled="counter.is_progress" class="btn btn-sm btn-secondary text-white">Edit</button>
                </div>
            </div>
        </li>
    </ul>
  </article>
</div>
</template>

<script setup>
import { useLocaleRouter } from '~/composables/useLocaleRouter'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'

const { $api } = useNuxtApp()
const { go } = useLocaleRouter()

const counters_list = ref([])
const on_loading = ref(false)

const loadCounters = async () => {
    const data = await $api('/counter/')
    counters_list.value = data.map(counter => ({
      ...counter,
      is_progress: false
    }))
}

onMounted(async () => {
  try {
    on_loading.value = true
    await loadCounters()
  } catch {} finally {
    on_loading.value = false
  }
})

const counter_tick = async (counter_index, value) => {
  try {
    console.log(value)

    let counter_id = counters_list.value[counter_index].id
    counters_list.value[counter_index].is_progress = true
    await $api('/counter/tick/', {
      method: 'POST',
      body: {
        counter: counter_id,
        value: value
      }
    })
    if (value > 0) {
        ++counters_list.value[counter_index].count
    } else if ( value < 0){
        --counters_list.value[counter_index].count
    }
  } catch (e) {
    console.error(e)
  } finally {
    counters_list.value[counter_index].is_progress = false
  }
}

</script>