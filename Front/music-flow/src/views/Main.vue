<template>
  <div>
    <AudioPlayer :song="currentSong" />
    
    <!-- <div class="parent">
    <timeBar class="temp" :currentTime="10" :duration="25"></timeBar> </div> -->
  </div>
</template>

<script>
import AudioPlayer from '@/components/player.vue';
// import timeBar from '@/components/time-bar.vue';


export default {
  components: {
    AudioPlayer,
    // timeBar
  },
  data() {
    return {
      currentSong: {
        name: 'Name of song',
        artist: 'Songer',
        src: 'path/to/your/audio/file.mp3'
      }
    }
  }
}
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

</style>