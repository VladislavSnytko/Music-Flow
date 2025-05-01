<template>
  <div>
    <AudioPlayer :song="currentSong" />
  </div>
</template>

<script>
import AudioPlayer from '@/components/player.vue';


export default {
  components: {
    AudioPlayer,
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
.temp{
  @apply absolute left-10 bottom-10;
}
</style>