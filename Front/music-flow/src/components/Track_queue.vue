<template>
  <div class="queue-container">
    <h3 class="queue-title">Очередь треков ({{ tracks.length }})</h3>

    <!-- Прокручиваемый блок -->
    <div class="queue-scroll-wrapper">
      <ul class="queue-list">
        <li 
          v-for="(track, index) in tracks" 
          :key="index"
          :class="['queue-item', { 'current': index === currentTrackIndex }]"
        >
          <img 
            :src="track.cover" 
            :alt="track.title" 
            class="track-cover"
            v-if="track.cover"
          >
          <div class="avatar-placeholder" v-else>
            {{ track.title.charAt(0).toUpperCase() }}
          </div>
          <div class="track-info">
            <span class="track-name">{{ track.title }}</span>
            <span class="track-artist">{{ track.artist }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tracks: {
      type: Array,
      required: true,
      default: () => []
    },
    currentTrackIndex: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style scoped>
.queue-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 16px;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 2rem 0 0 2rem;
  box-sizing: border-box;
  height: 100%;
}

/* Заголовок — не прокручивается */
.queue-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-align: center;
  text-shadow: 0 0 10px rgba(0, 217, 231, 0.5);
  margin-bottom: 10px;
  flex-shrink: 0;
}

/* Область прокрутки */
.queue-scroll-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 8px; /* чтобы скролл не наезжал на контент */
  border-radius: 20px;
}

/* Стилизуем скроллбар */
.queue-scroll-wrapper::-webkit-scrollbar {
  width: 8px;
}

.queue-scroll-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.queue-scroll-wrapper::-webkit-scrollbar-thumb {
  background-color: rgba(208, 188, 255, 0.3);
  border-radius: 4px;
  transition: background-color 0.3s;
}

.queue-scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background-color: rgba(208, 188, 255, 0.5);
}

/* Список треков */
.queue-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Элементы */
.queue-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: rgba(208, 188, 255, 0.08);
  border: 1px solid rgba(208, 188, 255, 0.2);
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.queue-item.current {
  background: rgba(208, 188, 255, 0.2);
  border-color: rgba(208, 188, 255, 0.4);
  box-shadow: 0 0 15px rgba(208, 188, 255, 0.2);
}

/* Обложка и информация */
.track-cover {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  margin-right: 15px;
  object-fit: cover;
  background: linear-gradient(135deg, #D0BCFF 0%, #2EA48C 100%);
}

.avatar-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin-right: 15px;
  color: #1F1431;
  background: linear-gradient(135deg, #D0BCFF 0%, #2EA48C 100%);
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.3);
}

.track-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.track-name {
  font-weight: 500;
  color: white;
  font-size: 1.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  font-size: 0.9rem;
  color: #ccc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>