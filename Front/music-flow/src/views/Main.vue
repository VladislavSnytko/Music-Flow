<template>
  <div :class="['player-wrapper', { visible: isPlayerVisible }]">
    <AudioPlayer :song="currentSong" />
  </div>
</template>








<script>
import AudioPlayer from '@/components/player.vue';

export default {
  components: {AudioPlayer},
  data() {
    return {
      currentSong: {
        name: 'Name of song',
        artist: 'Songer',
        src: 'path/to/your/audio/file.mp3'
      },
      isPlayerVisible: false
    };
  },
  mounted() {
    setTimeout(() => {
      this.isPlayerVisible = true;
    }, 100); // Небольшая задержка для срабатывания анимации
  }
};
</script>


<style>
.parent {
  display: flex;
  justify-content: center; /* Горизонтальное центрирование */
  align-items: center;     /* Вертикальное центрирование */
  height: 100vh;           /* Высота родительского контейнера (100% высоты экрана) */
}

.temp {
  max-height: 700px;
  max-width: 700px;
}

.player-wrapper {
  opacity: 0;
  transition: opacity 1s ease;
}

.player-wrapper.visible {
  opacity: 1;
}
</style>