<template>
  <div class="music-player">
    <div class="frame">
      <div class="song-info">
        <h2 class="song-title">{{ title }}</h2>
        <p class="song-artist">{{ artist }}</p>
      </div>

      <div class="progress-container">
        <div class="progress-line"></div>
        <div class="progress-dot"></div>
        <span class="time current-time">{{ formattedCurrentTime }}</span>
        <span class="time duration">{{ formattedDuration }}</span>
      </div>

      <div class="controls">
        <button class="control-btn past" @click="prevTrack">
          <!-- SVG или символ для предыдущего трека -->
        </button>
        <button class="play-btn" @click="togglePlay">
          <play_button/>
        </button>

        

        <button class="control-btn next" @click="nextTrack">
          <!-- SVG или символ для следующего трека -->
        </button>
      </div>

      <button class="heart-btn">

      </button>

      <audio 
        ref="audioPlayer"
        :src="src"
        @timeupdate="updateProgress"
        @loadedmetadata="updateDuration"
      ></audio>
    </div>
  </div>
</template>

<script>
import play_button from '@/assets/play_button.vue';
export default {
  components: { play_button },
  props: {
    title: {
      type: String,
      default: 'Название трека'
    },
    artist: {
      type: String,
      default: 'Исполнитель'
    },
    src: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isPlaying: false,
      currentTime: 0,
      duration: 0
    }
  },
  computed: {
    formattedCurrentTime() {
      return this.formatTime(this.currentTime);
    },
    formattedDuration() {
      return this.formatTime(this.duration);
    }
  },
  methods: {
    togglePlay() {
      if (this.isPlaying) {
        this.$refs.audioPlayer.pause();
      } else {
        this.$refs.audioPlayer.play();
      }
      this.isPlaying = !this.isPlaying;
    },
    prevTrack() {
      this.$emit('prev');
    },
    nextTrack() {
      this.$emit('next');
    },
    updateProgress(e) {
      this.currentTime = e.target.currentTime;
    },
    updateDuration() {
      this.duration = this.$refs.audioPlayer.duration;
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
  }
}
</script>

<style scoped>
.music-player {
  position: absolute;
  /* width: 500px;
  height: 970px; */
  height: 100%;
  width: auto;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 60px;
  backdrop-filter: blur(10px);
  padding: 20px;
  box-sizing: border-box;
}

.frame {
  position: relative;
  width: 400px;
  height: 400px;
  margin: 0 auto;
  background: rgba(18, 11, 33, 0.75);
  border-radius: 30px;
}

.song-info {
  position: absolute;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.song-title {
  font-size: 30px;
  color: #9925BA;
  opacity: 0.8;
  margin: 0;
}

.song-artist {
  font-size: 25px;
  color: rgba(147, 93, 162, 0.6);
  margin: 10px 0 0 0;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
}

.play-btn {
  width: 80px;
  height: 80px;
  border: none;
  background: transparent;
  position: relative;
  cursor: pointer;
}

.play-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(102, 46, 134, 0.67);
  border-radius: 50%;
}

.play-triangle {
  position: absolute;
  width: 0;
  height: 0;
  border-left: 25px solid #B88CD9;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
  left: 55%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.progress-container {
  position: absolute;
  width: 100%;
  bottom: 30%;
}

.progress-line {
  width: 100%;
  height: 2px;
  background: #D9D9D9;
}

.progress-dot {
  position: absolute;
  width: 15px;
  height: 15px;
  background: #DEB8FF;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
}

.time {
  position: absolute;
  font-family: 'Wingdings', sans-serif;
  font-size: 15px;
}

.current-time {
  left: -40px;
  color: #94F6F6;
  text-shadow: 0px 0px 7.5px #00FFD4;
}

.duration {
  right: -40px;
  color: #D794F3;
  text-shadow: 0px 0px 7.5px #EF149F;
}

.heart-btn {
  position: absolute;
  right: 20px;
  top: 20px;
  background: transparent;
  border: none;
  cursor: pointer;
}

.heart-icon {
  width: 24px;
  height: 24px;
  border: 2px solid white;
  transform: rotate(45deg);
  position: relative;
}

.heart-icon::before,
.heart-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
}

.heart-icon::before {
  top: -12px;
  left: 0;
}

.heart-icon::after {
  left: -12px;
  top: 0;
}
</style>