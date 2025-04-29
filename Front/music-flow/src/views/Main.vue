<template>
    <MusicPlayer
  title="Название трека"
  artist="Исполнитель"
  src="/path/to/audio.mp3"
  @prev="handlePrev"
  @next="handleNext"
/>
</template>


<script setup>
import MusicPlayer from "@/components/player.vue"


</script>
