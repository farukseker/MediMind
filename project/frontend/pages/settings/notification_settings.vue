<template>
  <section class="px-4 space-y-6 max-w-md mx-auto">
    <!-- Header -->
    <header class="flex items-center gap-4 py-2">
      <button class="btn btn-ghost p-0 text-xl" @click="go(-1)">
        <font-awesome :icon="faArrowLeft" />
      </button>
      <h1 class="text-xl font-bold">Bildirim Ayarları</h1>
    </header>

    <div 
      class="btn btn-ghost shadow text-warning font-semibold p-2"
      v-if="settings.notifications_enabled && !isUserAllowNotfication"
      @click="handleSubscribe"
    >
      <font-awesome :icon="faWarning" />  
      Bİldirim alabilmek için, <span class="font-bold underline">izin vermelisiniz</span>
    </div>

    <!-- General toggle -->
    <div class="form-control">
      <label class="label cursor-pointer">
        <span class="label-text font-semibold">Tüm bildirimler aktif</span>
        <input type="checkbox" class="toggle toggle-primary" v-model="settings.notifications_enabled" />
      </label>
    </div>
    <span class="label text-error text-sm" v-if="settings.notifications_enabled && !isUserAllowNotfication">
      Lütfen bildirimlere <span class="underline font-bold cursor-pointer" @click="handleSubscribe">izin veriniz </span>
    </span>
    <!-- Time Range Setting -->
    <fieldset class="fieldset shadow rounded-box p-4 space-y-2">
      <legend class="font-bold text-lg">Saat Aralığı</legend>
      <label class="label cursor-pointer">
        <span class="label-text">Sadece belirli saatlerde bildirim al</span>
        <input type="checkbox" class="toggle toggle-secondary" v-model="settings.use_time_range" :disabled="!settings.notifications_enabled || onSettingsLoad" />
      </label>
      <div class="flex gap-4 items-center">
        <label class="form-control w-full">
          <span class="label-text">Başlangıç</span>
          <input type="time" class="input input-bordered" v-model="settings.start_time" :disabled="!settings.notifications_enabled || !settings.use_time_range" />
        </label>
        <label class="form-control w-full">
          <span class="label-text">Bitiş</span>
          <input type="time" class="input input-bordered" v-model="settings.end_time" :disabled="!settings.notifications_enabled || !settings.use_time_range" />
        </label>
      </div>
    </fieldset>

    <!-- Notification types -->
    <fieldset class="fieldset shadow rounded-box p-4 space-y-4">
      <legend class="font-bold text-lg">Bildirim Türleri</legend>

      <label class="label cursor-pointer justify-between">
        <span class="label-text">İlaç hatırlatıcısı</span>
        <input type="checkbox" class="toggle toggle-success" v-model="settings.medication_enabled" :disabled="!settings.notifications_enabled || onSettingsLoad" />
      </label>

      <label class="label cursor-pointer justify-between">
        <span class="label-text">Su hatırlatıcısı</span>
        <input type="checkbox" class="toggle toggle-info" v-model="settings.water_enabled" :disabled="!settings.notifications_enabled || onSettingsLoad" />
      </label>

      <label class="label cursor-pointer justify-between">
        <span class="label-text">Kilo takibi hatırlatıcısı</span>
        <input type="checkbox" class="toggle toggle-warning" v-model="settings.weight_enabled" :disabled="!settings.notifications_enabled || onSettingsLoad" />
      </label>
    </fieldset>

    <!-- Save Button -->
    <div class="text-end">
      <button
        class="btn btn-primary"
        @click="updateUserNotificationSettings"
        :disabled="onUpdate"
      >
      <span v-if="!onUpdate">Kaydet</span>
      <span v-else class="loading loading-spinner loading-xs"></span>
    </button>
    </div>
  </section>
</template>

<script setup>
import { 
    faArrowLeft,
    faWarning
 } from '@fortawesome/free-solid-svg-icons'
import { onMounted } from 'vue';
import { useLocaleRouter } from '~/composables/useLocaleRouter'
import { usePushNotification } from '~/composables/usePushNotification';

const { subscribe } = usePushNotification();
const { go } = useLocaleRouter()
const { $api } = useNuxtApp()

const onUpdate = ref(false)
const onSettingsLoad = ref(false)
const isUserAllowNotfication = ref(false)

onMounted(async () => {
  try {
    onSettingsLoad.value = true
    isUserAllowNotfication.value = Notification.permission === 'granted'
    await getUserNotificationSettings()
  } finally {
    onSettingsLoad.value = false
  }
})

const settings = ref({
    notifications_enabled: true,
    medication_enabled: true,
    water_enabled: true,
    weight_enabled: true,
    use_time_range: true,
    start_time: '08:00',
    end_time: '22:00'
})

const getUserNotificationSettings = async () => {
  const response = await $api('notification/settings/')
  Object.assign(settings.value, response)
}

const updateUserNotificationSettings = async () => {
  try {
      onUpdate.value = true
      const response = await $api('notification/settings/', {
        method: 'PUT',
        body: settings.value
      })
      Object.assign(settings.value, response)
  } finally {
      onUpdate.value = false
  }
}

watch(
    () => settings.value.notifications_enabled,
    async (enabled) => {
    if (enabled){
      await handleSubscribe()
    }
})

const handleSubscribe = async () => {
  try {
    await subscribe()
    isUserAllowNotfication.value = Notification.permission === 'granted'
  } finally {
    if (Notification.permission === 'granted'){
        await updateUserNotificationSettings()
    }
  }
}

</script>