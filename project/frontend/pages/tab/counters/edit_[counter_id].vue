<template>
id : {{  $route.params.counter_id }}
</template>

<script setup>
const route = useRoute()

// geçici olarak api call ile counter bilgisi çekilecek sotre restoredan sonra 
// sotre ile id: ile veriler çekilecek aynı anda api ile günceleme yapılabilir olacak
// id: için api'nin tekrardan işlenmesi gerekebilir

const getCounterDetail = async () => {
    await $api()

}
</script>