<template>
<UNotifications />
<!-- <div class="font-[Roboto] flex flex-1 flex-col w-full"> -->
<div class="font-rosemary flex flex-1 flex-col w-full"> 
  <div class="pb-20">
    <slot />
  </div>
  <NavBottomNav />
</div>
</template>

<script setup>
definePageMeta({
  pageTransition: {
    name: 'rotate'
  }
})

const themeStore = useThemeStore()

onMounted(() => {
  themeStore.setTheme(themeStore.theme)
})

// onMounted(() => {
//     const theme = localStorage.getItem('theme') || 'light'
//     document.documentElement.setAttribute('data-theme', theme)
// })

// useHead({
//   script: [
//     {
//       src: "https://analytics.farukseker.com.tr/script.js",
//       defer: true,
//       "data-website-id": "67e2e352-b6a5-448c-ba35-ddc4be704189"
//     }
//   ]
// })
</script>
<style>
.rotate-enter-active,
.rotate-leave-active {
  transition: all 0.4s;
}
.rotate-enter-from,
.rotate-leave-to {
  opacity: 0;
  transform: rotate3d(1, 1, 1, 15deg);
}
</style>

