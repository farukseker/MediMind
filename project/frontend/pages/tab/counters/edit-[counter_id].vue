<template>
<section class="max-w-md mx-auto">
    <header class="flex bg-base-100 border-b border-primary p-4 sticky top-0 z-10 rounded-b-md shdow max-w-md mx-auto">
        <div 
        @click="go('/tab/counters/view_all_counters')"
        class="w-[36px] my-auto z-10">
            <font-awesome :icon="faArrowLeft" />
        </div>
        <div class="w-full my-auto">Plan adı ve sırası </div>
        <div class="w-fit">
            <button class="btn btn-sm btn-primary text-white" @click="saveCounter" :disabled="on_counter_save">
                <span v-if="!on_counter_save">Kaydet</span>
                <span v-else class="w-full text-center">
                    <span class="loading loading-infinity loading-md"></span>
                </span>
            </button>
        </div>
    </header>

    <fieldset class="w-full fieldset border-b-2 shadow-md border-base-300 rounded-box p-4 flex flex-col gap-2">
        <legend class="fieldset-legend font-bold">Sayaç bilgileri</legend>
        <article v-if="!on_load_counter_data && counter_data">
            <div class="flex flex-col">
                <label class="label w-full text-md font-semibold">
                    Sayaç adı *
                </label>
                <input class="input w-full" type="text" placeholder="Sayaç adı" v-model="counter_data.name"/>
                <p class="label w-full text-xs">Sayaç isimi boş bırakılamaz</p>
            </div>
            <div class="flex flex-col">
                <label class="label w-full text-md font-semibold">
                    Sayma şekili (opsyonel)
                </label>
                <input class="input w-full" type="text" placeholder="Sayıma şekli" v-model="counter_data.unit"/>
            </div>
            <div class="flex flex-col">
                <label class="label w-full text-md font-semibold">
                    Bölüm aralık tipi
                </label>
                <select class="select select-bordered w-full" name="split_type" v-model="counter_data.split_type">
                    <option disabled selected>Bölüm aralık tipi, günlük, haftalık, aylık</option>
                    <option value="daily">Günlük</option>
                    <option value="weekly">Haftalık</option>
                    <option value="monthly">Aylık</option>
                    <option value="nosplit">Bölme yok</option>
                </select>
                <!-- <p class="label w-full text-xs">Bölüm aralık tipi varsayılan günlük olarak seçilmiştir </p> -->
            </div>
            <hr class="my-2 p-0">
            <label class="label">
                Diğer bilgiler
            </label>
            <div class="grid grid-cols-3">
                <div>Oluşturulma tarihi :</div>
                <div class="col-span-2">{{ counterCreatedDate() }}</div>
                <div>Son sayım :</div>
                <div class="col-span-2">{{ counter_data.interval_count }}</div>
            </div>
        </article>
        <article v-else class="w-full text-center">
            <span class="loading loading-infinity loading-md"></span>
        </article>
    </fieldset>
    
    <fieldset class="w-full fieldset border-b-2 shadow-md border-base-300 rounded-box p-3 flex flex-row justify-around gap-2">
        <legend class="fieldset-legend font-bold">Kısayollar</legend>
            <button :disabled="on_load_counter_data" @click="counter_tick(1)" class="btn btn-primary"><font-awesome :icon="faPlus"/></button>
            <button :disabled="on_load_counter_data" @click="counter_tick(-1)" class="btn btn-secondary"><font-awesome :icon="faMinus"/></button>
            <!-- class="w-full"></div> -->
            <button :disabled="on_load_counter_data" class="btn btn-error">full reset</button>
            <button :disabled="on_load_counter_data" class="btn btn-error">delete</button>
    </fieldset>

    <fieldset v-if="counter_entries" class="w-full fieldset border-b-2 shadow-md border-base-300 rounded-box flex flex-col gap-2">
        <legend class="fieldset-legend font-bold">Sayaç grafiği</legend>
            <ApexChart 
                v-show="!on_load_counter_entries"
                class="pe-4 pt-1"
                type="line" 
                height="350" 
                :options="chartOptions" 
                :series="series" 
            />
        <article v-show="on_load_counter_entries" class="w-full text-center">
            <span class="loading loading-infinity loading-md"></span>
        </article>
    </fieldset>

    <fieldset v-if="counter_entries" class="w-full fieldset border-b-2 shadow-md border-base-300 rounded-box p-2 flex flex-col gap-2">
        <legend class="fieldset-legend font-bold">Sayaç geçmişi</legend>
        <article v-if="!on_load_counter_entries" class="grid grid-cols-6 text-center gap-3">
            <template v-for="entry, index in counter_entries" v-bind:key="index">
                <div class="col-span-4 my-auto">{{ toDate(entry.date) }}</div>
                <div class="col-span-1 my-auto">{{ entry.count }}</div>
                <div class="col-span-1 my-auto">
                    <button class="btn btn-sm btn-error" @click="deleteEntriesRange(index)">delete</button>
                </div>
            </template>
        </article>
        <article v-else class="w-full text-center">
            <span class="loading loading-infinity loading-md"></span>
        </article>
    </fieldset>

</section>
</template>

<script setup>
import { useLocaleRouter } from '~/composables/useLocaleRouter'
import { faMinus, faArrowLeft, faPlus } from '@fortawesome/free-solid-svg-icons'
import dayjs from 'dayjs'
import { computed, onMounted } from 'vue'


const { go } = useLocaleRouter()
const { $api } = useNuxtApp()

const route = useRoute()

let initialSplitType = null


const counter_data = ref(null)
const counter_entries = ref([])

const toDate = (date) => dayjs(date).toDate()
const counterCreatedDate = () => toDate(counter_data.created_at)

const on_load_counter_data = ref(true)
const on_load_counter_entries = ref(true)
const on_count_tick = ref(false)
const on_counter_save = ref(false)

const loadCounterData = async () => {
    let counter_id = route.params.counter_id
    let response;

    response = await $api(
        `/counter/${counter_id}/`
    )
    counter_data.value = response
    initialSplitType = counter_data.value.split_type
    on_load_counter_data.value = false
}

const loadCounterEntries = async () => {
    let counter_id = route.params.counter_id
    let response;

    response = await $api(
        `/counter/${counter_id}/entry/`
    )
    counter_entries.value = response
    on_load_counter_entries.value = false
}

const loadWraper = async () => {
    await loadCounterData()
    await loadCounterEntries()
}

onMounted(loadWraper)

const primaryColor = ref('#00E396')

onMounted(() => {
  const rootStyles = getComputedStyle(document.documentElement)
  const value = rootStyles.getPropertyValue('--color-primary').trim()
  primaryColor.value = value
})

const series = computed(() => (
    [{
        name: "Count",
        data: counter_entries.value.map(item => [new Date(item.date).getTime(), item.count])
    }]
))

const chartOptions = computed(() => ({
    chart: {
        type: 'line',
        toolbar: { show: false },
        zoom: { enabled: false }
    },
    xaxis: {
        type: 'datetime'
    },
    stroke: {
        curve: 'smooth'
    },
    markers: {
        size: 4
    },
    colors: [primaryColor.value],
    dataLabels: {
        enabled: true
    }
}))


const saveCounter = async () => {
    let counter_id = route.params.counter_id
    let response;
    
    try{
        on_counter_save.value = true
        
        response = await $api(
            `/counter/${counter_id}/`,
            {
                method: "PUT",
                body: counter_data.value
            }
        )
        counter_data.value = response
        if (counter_data.value.split_type !== initialSplitType) {
            initialSplitType = counter_data.value.split_type
            await loadCounterEntries()
        }
    } finally {
        on_counter_save.value = false
    }
}

const counter_tick = async (value) => {
  try {
    let counter_id = route.params.counter_id

    await $api('/counter/tick/', {
      method: 'POST',
      body: {
        counter: counter_id,
        value: value
      }     
    })

    if (value > 0) {
        ++counter_data.value.interval_count
    } else if ( value < 0){
        --counter_data.value.interval_count
    }
    
  } catch (e) {
    console.error(e)
  } finally {
    await loadCounterEntries()
  }
}

const deleteEntriesRange = async (delete_index) => {
    let counter_id = route.params.counter_id
    await $api(`/counter/${counter_id}/entry/${delete_index}/`, {method:"DELETE"}) 
    await loadCounterEntries()
}
</script>