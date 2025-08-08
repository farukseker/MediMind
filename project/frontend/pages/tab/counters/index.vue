<template>
   <div class="p-4 space-y-4 max-w-md mx-auto">
  <headersMainHeader :title="$t('counter.title')">
      <div 
          @click="go('/new_counter')"
          class="rounded shadow btn btn-primary btn-sm btn-dash border-dashed flex cursor-pointer min-w-fit text-sm">
          <span class="my-auto">{{ $t('counter.add_counter') }}</span>
      </div>
  </headersMainHeader>
  <NavTabsNav />

  <article class="flex flex-col gap-2">
    <div class="flex w-full m-auto">
        <button 
            class="btn btn-ghost underline ms-auto"
            @click="go('/tab/counters/view_all_counters')"
            >
            Tüm Sayaçlar
        </button>
    </div>
    <fieldset class="w-full fieldset card rounded-box">
      <div v-if="on_loading" class="w-full text-center">
        <span class="loading loading-infinity loading-md"></span>
      </div>
      <div v-else class="grid grid-cols-3 gap-4">
        <CountersCounterList :counters_list="counters_list" />
        <CountersAddCounterLink />
      </div>
    </fieldset>
  </article>
</div>

</template>

<script setup>
import { useLocaleRouter } from '~/composables/useLocaleRouter'

const { $api } = useNuxtApp()
const { go } = useLocaleRouter()

const counters_list = ref([])
const on_loading = ref(false)

const route = useRoute()
const localePath = useLocalePath()
const isPathEqual = (path) => route.path === localePath(path) 


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
</script> 
