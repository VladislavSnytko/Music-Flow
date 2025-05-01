<template>
  <div class="music-player">

    <div class="frame">
      <img id="cover" src="" alt="Обложка трека" class="image_track">
    </div>
    <div class="player-content">
      <div class="song-info">
        <audio id="audio" preload="auto"></audio>
        <h2 id="title" class="song-title">Название трека</h2>
        <p id="artist" class="song-artist">Исполнитель</p>
      </div>

      <!-- <div class="progress-container">
        <div class="progress-line" :style="gradientStyle"></div> -->
      <!-- <div class="progress-dot" :style="{ left: `${(currentTime / duration) * 100}%` }" @mousedown="startDrag"></div> -->
      <!-- <input class="progress-dot" :style="{ left: `${(currentTime / duration) * 100}%` }" @mousedown="startDrag" id="progress" value="0" min="0" step="10"> -->
      <!-- <span id="current-time" class="time current-time">0:00</span>
        <span id="duration" class="time duration">0:00</span>
      </div> -->


      <TimeBar :currentTime="currentTime" :duration="duration" @seek="onSeek">
      </TimeBar>

        <div class="time-display">
          <span id="current-time" class="time current-time">{{ formatTime(currentTime) }}</span>
          <span id="duration" class="time duration">{{ formatTime(duration) }}</span>
        </div>


      <!-- <div class="controls">
        <button class="play-btn-past" @click="prevTrack">
          <play_past_button />
        </button>

        <button id="pause-btn" class="play-btn" @click="sendPlayCommand">
          <play_button_pause />
          
        </button>
        <button id="play-btn" class="play-btn" @click="sendPauseCommand">
          <play_button_active />
        </button>

        <button class="play-btn-next" @click="nextTrack">
          <play_next_button />
        </button>
      </div>
    </div> -->

      <div class="controls">
        <!-- <div class="volume-control">
          <input type="range" min="0" max="1" step="0.01" v-model="volume" @input="updateVolume" />
        </div> -->
        <play-control-block :is-playing="isPlaying" @play="sendPlayCommand" @pause="sendPauseCommand" @prev="prevTrack"
          @next="nextTrack" />
      </div>
    </div>

    <button class="heart-btn">

    </button>

    <!-- <audio id="audio" preload="auto"></audio> -->

    <!-- <audio 
        ref="audioPlayer"
        :src="src"
        @timeupdate="updateProgress"
        @loadedmetadata="updateDuration"
      ></audio> -->

  </div>
</template>

<script>
import play_button_pause from '@/assets/play_button_pause.vue';
import play_button_active from '@/assets/play_button_active.vue';
import play_past_button from '@/assets/play_past_button.vue';
import play_next_button from '@/assets/play_next_button.vue';
import playControlBlock from '@/components/play-control-block.vue';
import TimeBar from '../components/time-bar.vue';

// function initWebSocket() {
//   // userId = getCookie('user_id');
//   // console.log(userId['user_id']);
//   let userId = "9d9f17c3-ad1e-441f-9955-0590286bc61c";
//   console.log(1);
//   if (!userId) {
//     alert('Требуется авторизация');
//     // window.location.href = '/login';
//     return;
//   }
//   console.log(window.location.host);
//   const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
//   console.log(228)
//   let socket = new WebSocket(`wss://abs-negative-relate-adverse.trycloudflare.com/room/faf1c5d6-da2f-4fb5-88a6-7023d40d62ff/ws`);


//   socket.onopen = () => {
//     console.log('Connected to room', roomId);
//     socket.send(JSON.stringify({
//       type: "get_participants"
//     }));
//   };

//   // socket.onmessage = (event) => {
//   //   const data = JSON.parse(event.data);
//   //   console.log(data)
//   //   handleSocketMessage(data);
//   // };

//   socket.onclose = () => {
//     console.log('Disconnected from room');
//   };
// }

export default {
  components: { play_button_pause, 
    play_button_active, 
    play_past_button, 
    play_next_button, 
    playControlBlock, 
    TimeBar},
  
  data() {
    return {
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      // volume: 1,
      interval: null,
      isDragging: false,
      socket: null,  // Добавляем socket в data
      userId: null,
      currentAudio: null,
      isSyncing: false,
      currentTrack: null,
      isPlaying: false,
      progress: null
    }
  },
  computed: {
    // formattedCurrentTime() {
    //   return this.formatTime(this.currentTime);
    // },
    // formattedDuration() {
    //   return this.formatTime(this.duration);
    // },
    gradientStyle() {
      const position = (this.currentTime / this.duration) * 100
      const transitionWidth = 50 // Увеличил ширину перехода
      return {
        background: `linear-gradient(to right,
          #00CED1 0%,
          #00CED1 calc(${position}% - ${transitionWidth}px),
          color-mix(in   srgb, #00CED1 75%, #8A2BE2 25%) calc(${position}% - ${transitionWidth*0.66}px),
          color-mix(in srgb, #00CED1 50%, #8A2BE2 50%) calc(${position}% - ${transitionWidth*0.33}px),
          color-mix(in srgb, #00CED1 25%, #8A2BE2 75%) ${position}%,
          #8A2BE2 calc(${position}% + 5px),
          #8A2BE2 100%)`,
          // background: `linear-gradient(to right,
          // #00CED1 0%,
          // #00CED1 ${this.progressPercentage - 20}%,
          // #8A2BE2 ${this.progressPercentage}%,
          // #8A2BE2 100%)`,
          width: '100%',
          height: '5px',
          borderRadius: '5px',
          position: 'absolute'
            }
    },
  },
  mounted() {
  this.initWebSocket();
  // this.currentAudio = document.getElementById('audio');
  this.handleDrag = this.handleDrag.bind(this);
  this.stopDrag = this.stopDrag.bind(this);
  
  // Добавляем проверку существования элемента
  if (!this.currentAudio) {
    console.error('Audio element not found');
    return;
  }

  // if (this.currentAudio) {
  //   this.currentAudio.volume = this.volume;
  // }

  // Обновляем интервал времени
  this.interval = setInterval(() => {
    if (this.currentAudio && !isNaN(this.currentAudio.duration)) {
      this.updateTimeDisplay();
    }
  }, 1000);

  // Обработчик для ползунка
  this.progress = document.getElementById('progress');
  if (this.progress) {
    this.progress.addEventListener('input', (e) => {
      if (!this.isSyncing && this.currentAudio) {
        const newPosition = parseFloat(e.target.value);
        this.currentAudio.currentTime = newPosition;
        this.sendSeekCommand(newPosition);
      }
    });
  }

  // Обработчики для аудио элемента
  this.currentAudio.addEventListener('timeupdate', () => {
    if (!this.isSyncing && this.currentAudio) {
      if (this.progress) this.progress.value = this.currentAudio.currentTime;
      this.currentTime = this.currentAudio.currentTime;
      this.updateTimeDisplay();
    }
  });

  this.currentAudio.addEventListener('loadedmetadata', () => {
    if (this.currentAudio && this.progress) {
      this.progress.max = this.currentAudio.duration;
      this.duration = this.currentAudio.duration;
      this.updateTimeDisplay();
    }
  });
},
  methods: {
    initWebSocket() {
      this.userId = "9d9f17c3-ad1e-441f-9955-0590286bc61c"; // Замените на реальный ID
      this.currentAudio = document.getElementById('audio');
      console.log(this.currentAudio)
      if (!this.userId) {
        alert('Требуется авторизация');
        return;
      }

      const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
      this.socket = new WebSocket(
        `wss://hardly-jane-time-functions.trycloudflare.com/room/faf1c5d6-da2f-4fb5-88a6-7023d40d62ff/ws?user_id=9d9f17c3-ad1e-441f-9955-0590286bc61c`
      );

      this.socket.onopen = () => {
        console.log('Connected to room');
        this.socket.send(JSON.stringify({ type: "get_participants" }));
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
        this.handleSocketMessage(data);
      };

      this.socket.onclose = () => {
        console.log('Disconnected from room');
      };
    },
    sendPlayCommand() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({
          type: 'play',
          position: this.currentAudio.currentTime
        }));
        this.currentAudio.play();
        this.updatePlayerUI(true);
        this.isPlaying = true;
      }
    },
    sendPauseCommand() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({
          type: 'pause',
          position: this.currentAudio.currentTime
        }));
        this.currentAudio.pause();
        this.updatePlayerUI(false);
        this.isPlaying = false;
      }
    },
    // updateVolume() {
    //   if (this.currentAudio) {
    //     this.currentAudio.volume = this.volume;
    //   }
    // },
    syncPlayback(playing, position) {
      this.isSyncing = true;

      if (Math.abs(this.currentAudio.currentTime - position) > 0.5) {
        this.currentAudio.currentTime = position;
      }

      if (playing && this.currentAudio.paused) {
        this.currentAudio.play().catch(e => console.log('Play error:', e));
        this.updatePlayerUI(true);
        this.isPlaying = true;
      } else if (!playing && !this.currentAudio.paused) {
        this.currentAudio.pause();
        this.updatePlayerUI(false);
        this.isPlaying = false;
      }

      setTimeout(() => { this.isSyncing = false; }, 100);
    },
    sendSeekCommand(position) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({
          type: 'seek',
          position: position
        }));
      }
    },

    onSeek(currentTime) {
    if (!this.isSyncing && this.currentAudio) {
      this.currentAudio.currentTime = currentTime;
      this.sendSeekCommand(currentTime);
  }
},
    handleSocketMessage(data) {
      switch (data.type) {
        case 'request_current_time':
          // Отправляем текущее время с идентификатором запроса
          console.log(9, this.currentAudio.currentTime);
          this.socket.send(JSON.stringify({
            type: "current_time",
            position: this.currentAudio.currentTime,
            request_id: data.request_id  // Добавляем ID запроса
          }));
          break;
        case 'init':
          // Обрабатываем все данные сразу
          if (data.track_url) {
            this.loadTrack(data.track_url, () => {
              console.log('time from bd:', data.current_time);
              this.currentAudio.currentTime = data.current_time;
              if (data.is_playing) {
                this.currentAudio.play().catch(e => console.log('Play error:', e));
                this.updatePlayerUI(true);
                this.isPlaying = true;
              } else {
                this.currentAudio.pause();
                this.updatePlayerUI(false);
                this.isPlaying = false;
              }
            });
          }
          // updateParticipantsList(data.room.list_of_participants);
          break;
        case 'track_state':  // Новый тип сообщения
          this.loadTrack(data.url, () => {
            this.currentAudio.currentTime = data.position;
            if (data.is_playing) {
              this.currentAudio.play().catch(e => console.log('Play error:', e));
              this.updatePlayerUI(true);
              this.isPlaying = true;
            } else {
              this.currentAudio.pause();
              this.updatePlayerUI(false);
              this.isPlaying = false;
            }
          });
          break;
        case 'play':
          console.log('from socket play:', data);
          this.handlePlayMessage(data);
          break;
        case 'pause':
          this.handlePauseMessage(data);
          break;
        case 'change_track':
          this.handleChangeTrackMessage(data);
          break;
        case 'seek':
          console.log(data)
          this.handleSeekMessage(data);
          break;
        case 'participants_update':
          // updateParticipantsList(data.participants);
          break;
        case 'load_track':
          this.loadTrack(data.url);
          break
        // ... другие типы сообщений
      }
    },
    handlePlayMessage(data) {
      this.syncPlayback(true, data.position);
      this.updatePlayerUI(true);
      this.isPlaying = true;
      console.log('this.currentAudio.duration', this.currentAudio.duration);
      this.currentAudio.play();
    },
    handlePauseMessage(data) {
      this.syncPlayback(false, data.position);
      this.updatePlayerUI(false);
      this.isPlaying = false;
      this.currentAudio.pause();
    },
    handleChangeTrackMessage(data) {
      if (data.tracks && data.tracks.length > 0) {
        this.loadTrack(data.tracks[data.index]);
      }
    },
    handleSeekMessage(data) {
      if (!this.isSyncing) {
        this.isSyncing = true;
        console.log('pos:', data.position);
        this.currentAudio.currentTime = data.position;
        console.log('this.currentAudio.currentTime', this.currentAudio.currentTime);
        if (this.progress){
          this.progress.value = data.position;
        }
        setTimeout(() => { this.isSyncing = false; }, 100);
      }
    },
    loadTrack(trackUrl, callback) {
      console.log(`in load`, trackUrl);
      if (!trackUrl) return;

      this.currentTrack = trackUrl;
      const data = {
        user_id: "9d9f17c3-ad1e-441f-9955-0590286bc61c",
        password: 'secret'
      };
      this.currentAudio.src = `https://hardly-jane-time-functions.trycloudflare.com/stream?url=${encodeURIComponent(trackUrl)}`;

      const trackInfo = fetch(`https://hardly-jane-time-functions.trycloudflare.com/track_info?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`);
      console.log(`trackInfo: `, trackInfo);
      
      fetch(`https://hardly-jane-time-functions.trycloudflare.com/stream?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`)
        .then(response => {
          const trackInfo = JSON.parse(response.headers.get('Track-Info'));
          console.log('response:', response.headers);
          
          document.getElementById('title').textContent = trackInfo.title;
          document.getElementById('artist').textContent = trackInfo.artist;
          document.getElementById('cover').src = trackInfo.cover;

          // Добавляем обработчик для определения когда трек готов к воспроизведению
          this.currentAudio.oncanplay = () => {
            callback();
            this.currentAudio.oncanplay = null;
          };
        })
        // .catch(error => {
        //   console.error('Ошибка:', error);
        //   alert('Не удалось загрузить трек');
        // });
    },
    updatePlayerUI(isPlaying) {
      // document.getElementById('play-btn').hidden = !isPlaying;
      // document.getElementById('pause-btn').hidden = isPlaying;
      console.log();
    },
    updateTimeDisplay() {
  // if (!this.currentAudio || isNaN(this.currentAudio.duration)) return;
  
  this.$nextTick(() => {
    const currentTimeEl = document.getElementById('current-time');
    const durationEl = document.getElementById('duration');
    
    if (currentTimeEl) {
      currentTimeEl.textContent = this.formatTime(this.currentAudio.currentTime || 0);
    }
    if (durationEl) {
      durationEl.textContent = this.formatTime(this.currentAudio.duration || 0);
    }
  });
},
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    },
    togglePlay() {
      const audio = this.$refs.audioPlayer; // ссылка на аудио элемент через this.$refs.audioPlayer
      if (this.isPlaying){
        audio.pause();
      }
      else{
        audio.play();
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
      if (!this.isDragging){
      this.currentTime = e.target.currentTime;
    }
    },
    updateDuration() {
      this.duration = this.$refs.audioPlayer.duration;
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },

    handleSeek(e) {
    if (this.isDragging || !this.duration) return;
  
  const progressBar = e.currentTarget;
  const rect = progressBar.getBoundingClientRect();
  const clickPosition = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
  this.currentTime = (clickPosition / rect.width) * this.duration;
  this.currentAudio.currentTime = this.currentTime;
  this.sendSeekCommand(this.currentTime);
  },

  startDrag(e) {
  console.log('Start drag'); // убедитесь, что это выводится
  this.isDragging = true;
  document.addEventListener('mousemove', this.handleDrag);
  document.addEventListener('mouseup', this.stopDrag);
  e.preventDefault();
},

handleDrag(e) {
  if (!this.isDragging) return;

  const progressBar = document.querySelector('.progress-container');
  if (!progressBar) return;

  const rect = progressBar.getBoundingClientRect();
  const dragPosition = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
  const newTime = (dragPosition / rect.width) * this.duration;

  this.currentTime = newTime;
  this.currentAudio.currentTime = newTime;

  this.$forceUpdate(); // заставить Vue перерисовать
},

  stopDrag() {
    if (!this.isDragging) return;
    
    this.isDragging = false;
    document.removeEventListener('mousemove', this.handleDrag);
    document.removeEventListener('mouseup', this.stopDrag);
    
    this.sendSeekCommand(this.currentAudio.currentTime);
  }
}
}
// document.addEventListener('DOMContentLoaded', initWebSocket);
</script>


<style scoped>
.music-player {
  position: absolute;
  /* width: 500px;
  height: 970px; */
  right: 5px;
  top: 80px;
  height: 90%;
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

.image_track{
  border-radius: 30px;
}

.player-content {
  width: 100%;
  height: 40%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.song-info {
  position: relative;
  top: 10px;
  transform: translateX(-50%);
  text-align: left;
  margin: 5px;
}

.song-title {
  font-size: 25px;
  color: #9925BA;
  opacity: 0.75;
}

.song-artist {
  font-size: 20px;
  color: rgba(147, 93, 162, 0.6);
  margin: 5px;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  position: absolute;
  bottom: 15%;
  left: 50%;
  transform: translateX(-50%);
}
/*
.play-btn {
  width: 80px;
  height: 80px;
  border: none;
  background: transparent;
  position: relative;
  cursor: pointer;
}

.play-btn:active{
  transform: scale(1.1);
}

.play-btn-past{
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  position: relative;
  cursor: pointer;
}

.play-btn-next{
  width: 40px;
  height: 40px;
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
} */

.progress-container {
  width: 100%;
  height: 5px;
  background: rgba(217, 217, 217, 0.3);
  border-radius: 5px;
  cursor: pointer;
  position: relative;
  margin: 15px 0;
}

.progress-line {
  position: absolute;
  height: 100%;
  border-radius: 5px;
  /* gradientStyle будет управляться через computed свойство */
}

.progress-dot {
  position: absolute;
  width: 100px;
  height: 5px;
  background: #DEB8FF;
  border-radius: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  cursor: grab;
}

.progress-dot:active {
  cursor: grabbing;
  transform: translate(-50%, -50%) scale(1.25);}

.time {
  position: absolute;
  font-family: sans-serif;
  font-size: 15px;
}

.current-time {
  left: 5px;
  top: 10px;
  color: #94F6F6;
  text-shadow: 0px 0px 7.5px #00FFD4;
}

.duration {
  right: 5px;
  top: 10px;
  color: #D794F3;
  text-shadow: 0px 0px 7.5px #EF149F;
}

/* .heart-btn {
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
} */
</style>