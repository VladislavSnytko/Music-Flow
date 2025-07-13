<template>
  <div class="player">
    <!-- Аудио элемент (скрытый) -->
    <audio ref="audioElement" preload="auto"></audio>
    
    <!-- Обложка и информация о треке -->
    <div class="cover-container">
      <img :src="currentTrack.cover" alt="Обложка" class="cover-image">
    </div>
    
    <!-- Информация о треке -->
    <div class="track-info">
      <h2 class="track-title">{{ currentTrack.title }}</h2>
      <p class="track-artist">{{ currentTrack.artist }}</p>
    </div>
    
    <!-- Элементы управления -->
    <div class="controls">
      <button @click="prevTrack">Previous</button>
      <button @click="togglePlay">{{ isPlaying ? 'Pause' : 'Play' }}</button>
      <button @click="nextTrack">Next</button>
    </div>
    
    <!-- Прогресс бар -->
    <input 
      type="range" 
      v-model="progress" 
      min="0" 
      :max="duration"
      @input="seek"
      class="progress-bar"
    >
  </div>
</template>

<script>
// Импортируем логику из отдельного файла
import usePlayer from './player.js'

export default {
  props: {
    initialTrack: Object
  },
  
  setup(props) {
    // Используем композицию для выноса логики
    const {
      audioElement,
      currentTrack,
      isPlaying,
      progress,
      duration,
      togglePlay,
      prevTrack,
      nextTrack,
      seek
    } = usePlayer(props.initialTrack)

    return {
      audioElement,
      currentTrack,
      isPlaying,
      progress,
      duration,
      togglePlay,
      prevTrack,
      nextTrack,
      seek
    }
  }
}
</script>

<style scoped src="./player.css"></style>