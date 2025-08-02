<template>
   <div class="p-4 space-y-4 max-w-md mx-auto">
  <headersMainHeader :title="$t('counter.title')">
      <div 
          @click="go('/new_counter')"
          class="rounded shadow bg-base-200 border-2 border-dashed border-gray-400 text-gray-600 px-2 py-0 flex cursor-pointer min-w-fit text-sm">
          <span class="my-auto">{{ $t('counter.add_counter') }}</span>
      </div>
  </headersMainHeader>
  <NavTabsNav />

  <article>
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
