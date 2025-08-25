<template>
<div class="card bg-base-100 shadow peer" :id="medication.id">
    <div class="text-red-400 hidden peer-target:block">text</div>
    <div class="card-body p-3">
        <div  class="absolute -top-1 -left-1 text-gray-300 text-md">
        </div>
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-1 md:gap-0">
            <div>
                <p class="font-semibold">
                    <span v-if="medication.schedules?.length > 0" class="text-gray-300 tooltip" :data-tip="$t('medication_item.planned')">
                        <font-awesome :icon="faStopwatch" />
                    </span>
                    {{ medication.name}}</p>
                <p class="text-sm text-gray-500">{{ medication.default_dose_amount }} {{ medication.default_dose_unit }}</p>
            </div>
            <div class="flex gap-2">
                <button 
                v-if="medication.schedules?.length === 0" 
                @click="$emit('do_plan_exist_medication', medication.id)"
                class="btn btn-primary btn-sm"
                >{{ $t('medication_item.plan') }}</button>
                <button class="btn btn-secondary btn-sm" @click="take_mdicine">
                    <span v-if="!on_take">{{ $t('medication_item.take') }}</span>
                    <span v-else class="loading loading-spinner loading-sm"></span>

                </button>
                <button class="btn btn-success btn-sm" @click="$emit('update_exist_medication', medication.id)">{{ $t('medication_item.edit') }}</button>
                <button class="btn btn-outline btn-sm" @click="delete_mdicine(medication.id)">{{ $t('medication_item.del') }}</button>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { faStopwatch, faTimeline, faTimes } from '@fortawesome/free-solid-svg-icons'
import dayjs from 'dayjs'

const props = defineProps(['medication'])
const { $api } = useNuxtApp()
const emit = defineEmits(['load_medication_list'])
const on_progress = ref(false)

const on_take = ref(false)

const trigger = async () => {
    try{
        const result = await emit('load_medication_list'); 
        if (result.length > 0) {
            await result[0];
            await nextTick()
        }
    } catch {} finally {
        on_progress.value = false
    }
};

const take_mdicine = async () => {
    try {
        on_take.value = true
        await $api('/medication/medication-logs/create/', {
            method: 'POST',
            body: {
                "medication": props.medication.id,
                "dose": props.medication.default_dose_amount,
                "taken_status": 'taken',
            }
        })
    } catch {} finally {
        await trigger()
        on_take.value = false
        on_progress.value = false
    }
}



const delete_mdicine = async (medication_id) => {
    try {
        await $api(`medication/medications/${medication_id}/`, {
            method: 'DELETE'
        })
    } catch {} finally {
        await trigger()
        on_progress.value = false
    }
}

</script>
<style>
@keyframes ping-once {
  75%, 100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.ping-once {
  animation: ping-once 0.6s cubic-bezier(0, 0, 0.2, 1) 1;
}
</style>
