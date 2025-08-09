<script setup>
import { ref, watch } from 'vue'
import { onClickOutside } from '@vueuse/core'

const { modelValue } = defineProps({
  modelValue: { type: Boolean, default: false }, 
})

const emit = defineEmits(['update:modelValue'])

const modalRef = ref(null)

onClickOutside(modalRef, () => {
  emit('update:modelValue', false)
})

const isVisible = ref(modelValue)
watch(() => modelValue, val => isVisible.value = val)
</script>

<template>
  <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
    <div ref="modalRef" class="bg-base-100 p-4 rounded shadow shadow-primary w-96 relative">
      <button 
        @click="emit('update:modelValue', false)" 
        class="absolute top-2 right-2 px-2 py-1 btn btn-circle btn-ghost"
      >
        ✕
      </button>
      <slot />
    </div>
  </div>
</template>

