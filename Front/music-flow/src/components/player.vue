<template>
  <div ref="playerElement">  <!-- Добавлено -->
    <div class="send-container">
      <input type="text" id="track-url" placeholder="Вставьте ссылку на трек из Яндекс.Музыки" class="Send_link">
        <send id="load-btn" class="Send" @click="playTrack"></send>
    </div>
  </div>
  <div class="music-player">
    <!-- Прелоадер с анимацией -->
    <div class="preloader" v-if="isLoading">
      <div class="preloader-content">
        <div class="wave-container">
          <Logo class="Logo-player"></Logo>
          
          <!-- <div class="wave" v-for="i in 5" :key="i" :style="`--index:${i}`"></div> -->
        </div>
        <div class="loading-text">Загрузка плеера...</div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="player-container" v-show="!isLoading">
      <div class="frame" ref="frame">
        <img id="cover" src="" alt="Обложка трека" class="image_track" ref="coverImage">
      </div>

      <div class="player-content">
        <div class="song-info" ref="songInfo">
          <audio id="audio" preload="auto" ref="audioElement"></audio>
          <h2 id="title" class="song-title">{{ currentTrackTitle }}</h2>
          <p id="artist" class="song-artist">{{ currentArtist }}</p>
        </div>

        <div class="progress-container">
          <TimeBar :currentTime="currentTime" :duration="duration" @seek="onSeek" ref="timeBar" />
        </div>

        <div class="controls" ref="controls">
          <play-control-block :is-playing="isPlaying" @play="sendPlayCommand" @pause="sendPauseCommand"
            @prev="prevTrack" @next="nextTrack" ref="playControl" />
        </div>
      </div>
      <volume 
            v-if="!isLoading"
            :volume="currentVolume"
            @update:volume="handleVolumeUpdate"
            ref="volumeControl"
      ></volume>
    </div>
  </div>
</template>

<script>
import play_button_pause from '@/assets/play_button_pause.vue';
import play_button_active from '@/assets/play_button_active.vue';
import play_past_button from '@/assets/play_past_button.vue';
import play_next_button from '@/assets/play_next_button.vue';
import playControlBlock from '@/components/play-control-block.vue';
import volume from '@/components/volume.vue';
import Send from '@/assets/Send.vue';
import Logo from '@/assets/Logo-for-player.vue';
import TimeBar from '../components/time-bar.vue';
import { gsap } from 'gsap';
import { CustomEase } from 'gsap/CustomEase';
gsap.registerPlugin(CustomEase);
const DOMAIN = import.meta.env.VITE_DOMAIN;




export default {
  components: { play_button_pause,
    volume,
    Send,
    Logo, 
    play_button_active, 
    play_past_button, 
    play_next_button, 
    playControlBlock, 
    TimeBar},
    props: {
    song: {
        type: Object,
        default: () => ({ name: '', artist: '', src: '' })
      }
    },
    
    audioRef: {
      type: Object,
      required: true
    },

    data() {
    return {
      isLoading: true,
      currentTrackTitle: 'Название трека',
      currentArtist: 'Исполнитель',
      isPlaying: false,
      currentTime: 0,
      currentVolume: 1,
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
      audioElement() {
        return this.$refs.audioElement;
    }
  },

  playEntranceAnimation() {
  try {
    const playerElement = this.$refs.playerElement || this.$el; // fallback на корневой элемент
    if (!playerElement?.children) {
      console.error("Элемент или его children не найдены");
      return;
    }
    gsap.from(playerElement.children, { opacity: 0, duration: 1 });
  } catch (error) {
    console.error("Ошибка анимации:", error);
  }
  try {
    // Проверка наличия ссылки на элемент и его детей
    const playerElement = this.$refs.playerElement;
    
    if (!playerElement) {
      console.error('Player element not found');
      return; // Если элемент не найден, не продолжаем анимацию
    }

    if (!playerElement.children) {
      console.error('Player element does not have children');
      return; // Если у элемента нет детей, не продолжаем анимацию
    }

    // Убедимся, что все элементы загружены перед анимацией
    this.$nextTick(() => {
      // Проверяем, что DOM обновился, и только тогда запускаем анимацию
      gsap.from(playerElement.children, { opacity: 0, duration: 1 });
    });
  } catch (error) {
    // Ловим и выводим ошибку, если что-то пошло не так
    console.error('Error during entrance animation', error);
  }
},

// Допустим, твоя асинхронная загрузка контента выглядит так:
loadContent() {
  this.loadImage().then(() => {
    // Когда загрузка завершена, запускаем анимацию
    this.$nextTick(() => {
      this.playEntranceAnimation();
    });
  }).catch((error) => {
    // Если произошла ошибка при загрузке
    console.error('Error loading content', error);
  });
},

  async mounted() {
    // await this.hideLoader();
    
    
    
    this.currentAudio = this.$refs.audioElement; // Инициализируем currentAudio из ref
    await this.initWebSocket();
    
    // Проверяем, что все refs существуют
    if (!this.$refs.frame || !this.$refs.coverImage || !this.$refs.songInfo || 
        !this.$refs.timeBar || !this.$refs.controls || !this.$refs.playControl) {
      console.error('Не все refs инициализированы');
      return;
    }
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
  this.interval = setInterval(async () => {
    if (this.currentAudio && !isNaN(this.currentAudio.duration)) {
      await this.updateTimeDisplay();
    }
  }, 1000);

  // Обработчик для ползунка
  this.progress = document.getElementById('progress');
  if (this.progress) {
    this.progress.addEventListener('input', async (e) => {
      if (!this.isSyncing && this.currentAudio) {
        const newPosition = parseFloat(e.target.value);
        this.currentAudio.currentTime = newPosition;
        await this.sendSeekCommand(newPosition);
      }
    });
  }

  // Обработчики для аудио элемента
  this.currentAudio.addEventListener('timeupdate', async () => {
    if (!this.isSyncing && this.currentAudio) {
      if (this.progress) this.progress.value = this.currentAudio.currentTime;
      this.currentTime = this.currentAudio.currentTime;
      await this.updateTimeDisplay();
    }
  });

  this.currentAudio.addEventListener('loadedmetadata', async () => {
    if (this.currentAudio && this.progress) {
      this.progress.max = this.currentAudio.duration;
      this.duration = this.currentAudio.duration;
      await this.updateTimeDisplay();
    }
  });
  this.handleVolumeUpdate(0);
},
beforeUnmount() {
    if (this.socket) {
      this.socket.close(1000, "Page closed");  // 1000 = нормальное закрытие
      this.socket = null;
    }
    clearInterval(this.interval);
  },
methods: {


  async getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
  },



  handleVolumeUpdate(volume) {
    this.currentVolume = volume;
    if (this.currentAudio) {
      this.currentAudio.volume = volume;
    }
  },


  async initWebSocket() {
  // Получаем user_id из куки
  const userIdFromCookie = await this.getCookie('user_id');
  console.log(this.userIdFromCookie);
  
  // Проверяем, есть ли user_id в куках
  if (!userIdFromCookie) {
    alert('Требуется авторизация');
    return;
  }

  this.userId = userIdFromCookie;
  this.currentAudio = document.getElementById('audio');
  console.log(this.currentAudio);

      // const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
      this.socket = new WebSocket(
        `wss://${DOMAIN}/room/faf1c5d6-da2f-4fb5-88a6-7023d40d62ff/ws?user_id=${this.userId}`
      );

      this.socket.onopen = () => {
        console.log('Connected to room');
        this.socket.send(JSON.stringify({ type: "get_participants" }));
      };

      this.socket.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
        await this.handleSocketMessage(data);
      };

      this.socket.onclose = () => {
        console.log('Disconnected from room');
      };
    },
    async sendPlayCommand() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        await this.socket.send(JSON.stringify({
          type: 'play',
          position: this.currentAudio.currentTime
        }));
        console.log('this.currentAudio.src:', this.currentAudio.src);
        this.currentAudio.play();
        await this.updatePlayerUI(true);
        this.isPlaying = true;
      }
    },
    async sendPauseCommand() {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        await this.socket.send(JSON.stringify({
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
    async syncPlayback(playing, position) {
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
    async sendSeekCommand(position) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        await this.socket.send(JSON.stringify({
          type: 'seek',
          position: position
        }));
      }
    },

    async onSeek(currentTime) {
    if (!this.isSyncing && this.currentAudio) {
      this.currentAudio.currentTime = currentTime;
      this.sendSeekCommand(currentTime);
  }
},
    async handleSocketMessage(data) {
      switch (data.type) {
        case 'request_current_time':
          // Отправляем текущее время с идентификатором запроса
          console.log(9, this.currentAudio.currentTime);
          await this.socket.send(JSON.stringify({
            type: "current_time",
            position: this.currentAudio.currentTime,
            request_id: data.request_id  // Добавляем ID запроса
          }));
          break;
        case 'init':
          // Обрабатываем все данные сразу
          if (data.track_url) {
            await this.loadTrack(data.track_url, async () => {
              console.log('time from bd:', data.current_time);
              this.currentAudio.currentTime = data.current_time;
              if (data.is_playing) {
                this.currentAudio.play().catch(e => console.log('Play error:', e));
                await this.updatePlayerUI(true);
                this.isPlaying = true;
              } else {
                this.currentAudio.pause();
                await this.updatePlayerUI(false);
                this.isPlaying = false;
              }
            });
          }
          // updateParticipantsList(data.room.list_of_participants);
          break;
        case 'track_state':  // Новый тип сообщения
          await this.loadTrack(data.url, async () => {
            this.currentAudio.currentTime = data.position;
            if (data.is_playing) {
              this.currentAudio.play().catch(e => console.log('Play error:', e));
              await this.updatePlayerUI(true);
              this.isPlaying = true;
            } else {
              this.currentAudio.pause();
              await this.updatePlayerUI(false);
              this.isPlaying = false;
            }
          });
          break;
        case 'play':
          console.log('from socket play:', data);
          await this.handlePlayMessage(data);
          break;
        case 'pause':
          await this.handlePauseMessage(data);
          break;
        // case 'change_track':
        //   await this.handleChangeTrackMessage(data);
        //   break;
        case 'change_track':
        if (data.tracks && data.tracks.length > 0 && !this.isSyncing) {
          await this.loadTrack(data.tracks[data.index]);
        }
        break;
        case 'seek':
          console.log(data)
          await this.handleSeekMessage(data);
          break;
        case 'participants_update':
          console.log(`participants:`, data.participants);
          // updateParticipantsList(data.participants);
          break;
        case 'load_track':
          await this.loadTrack(data.url);
          break
        // ... другие типы сообщений
      }
    },
    async handlePlayMessage(data) {
      await this.syncPlayback(true, data.position);
      await this.updatePlayerUI(true);
      this.isPlaying = true;
      console.log('this.currentAudio.duration', this.currentAudio.duration);
      this.currentAudio.play();
    },
    async handlePauseMessage(data) {
      await this.syncPlayback(false, data.position);
      await this.updatePlayerUI(false);
      this.isPlaying = false;
      this.currentAudio.pause();
    },
    async handleChangeTrackMessage(data) {
      if (data.tracks && data.tracks.length > 0) {
        await this.loadTrack(data.tracks[data.index]);
      }
    },
    async handleSeekMessage(data) {
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
    // async loadTrack(trackUrl, callback) {
    //   console.log(`in load`, trackUrl);
    //   if (!trackUrl) return;

    //   this.currentTrack = trackUrl;
    //   const data = {
    //     user_id: "9d9f17c3-ad1e-441f-9955-0590286bc61c",
    //     password: 'secret'
    //   };
    //   this.currentAudio.src = `https://${DOMAIN}/stream?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`;

    //   const trackInfo = await fetch(`https://${DOMAIN}/track_info?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`);
    //   console.log(`trackInfo: `, trackInfo);
      
    //   await fetch(`https://${DOMAIN}/stream?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`)
    //     .then(response => {
    //       const trackInfo = JSON.parse(response.headers.get('Track-Info'));
    //       console.log('response:', response.headers);
          
    //       document.getElementById('title').textContent = trackInfo.title;
    //       document.getElementById('artist').textContent = trackInfo.artist;
    //       document.getElementById('cover').src = trackInfo.cover;

    //       // Добавляем обработчик для определения когда трек готов к воспроизведению
    //       this.currentAudio.oncanplay = async () => {
    //         await callback();
    //         this.currentAudio.oncanplay = null;
    //       };
    //       this.currentAudio.load();
    //     })
    //     // .catch(error => {
    //     //   console.error('Ошибка:', error);
    //     //   alert('Не удалось загрузить трек');
    //     // });
    // },
  async playTrack() {

    const url = document.getElementById('track-url').value.trim();
    console.log(url);
    if (!url.includes('music.yandex.')) {
      alert('Пожалуйста, введите ссылку Яндекс.Музыки');
      return;
    }

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log(`socket open`);
      this.sendAddTrack(url);
    } 
    // else {
    //   await this.loadTrack(url);
    // }
  },
  async sendTrackChange(trackUrl) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log(3);
      await this.socket.send(JSON.stringify({
        type: 'previous_track',
        tracks: [trackUrl],
        index: 0
      }));
    }
  },
  async sendAddTrack(trackUrl) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {

      await this.socket.send(JSON.stringify({
        type: 'add_track',
        tracks: [trackUrl]
      }));
    }
  },
  async sendNextTrack() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {

      this.sendPauseCommand();
      await this.socket.send(JSON.stringify({
        type: 'next_track'
      }));
    }
  },
  async sendPrevTrack() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      if (this.currentAudio.currentTime > 5){
        this.onSeek(0);
      }
      else {
        this.sendPauseCommand();
        await this.socket.send(JSON.stringify({
          type: 'previous_track'
        }));
      }}
  },
    async hideLoader() {
      // Анимация исчезновения прелоадера
      await gsap.to(".preloader", {
        opacity: 0,
        duration: 0.8,
        ease: "power2.out",
        onComplete: () => {
          this.isLoading = false;
          this.$nextTick(() => this.playEntranceAnimation());
        }
      });
    },
    
    async playEntranceAnimation() {
      // Последовательная анимация появления элементов
      const tl = gsap.timeline();
      
      tl.from(this.$refs.frame, {
        scale: 0.9,
        y: 30,
        opacity: 0,
        duration: 1,
        ease: "back.out(1.7)"
      })
      .from(this.$refs.coverImage, {
        scale: 1.1,
        opacity: 0,
        duration: 1.2,
        ease: "power2.out"
      }, "-=0.5")
      .from(this.$refs.songInfo.children, {
        y: 20,
        opacity: 0,
        duration: 0.7,
        stagger: 0.1,
        ease: "power2.out"
      })
      tl.from(this.$refs.timeBar.$el, {
        scaleX: 0,
        duration: 1,
        transformOrigin: "left center",
        ease: "power3.out"
      }, "<+0.5") // Начинается через 0.3 сек после начала предыдущей анимации
      .from(this.$refs.playControl.$el, {
        y: 20,
        opacity: 0,
        duration: 0.8,
        ease: "elastic.out(1, 0.5)"
      }, "<+0.5") // "<" означает "запустить в тот же момент времени, что и предыдущая анимация"

      if (this.$refs.volumeControl?.$el) {
        tl.from(this.$refs.volumeControl.$el, {
          y: 30,
          opacity: 0,
          duration: 0.8,
          ease: "elastic.out(1, 0.5)"
        }, "-=0.3");
      }

      return tl;
    },
    
    async loadTrack(trackUrl) {
      try {
        this.isLoading = true;
        await this.showLoadingState();
        
        const response = await fetch(`https://${DOMAIN}/track_and_stream?url=${encodeURIComponent(trackUrl)}&user_id=${this.userId}`);
        const data = await response.json();
        
        // Обновляем данные
        this.currentTrackTitle = data.title;
        this.currentArtist = data.artist;
        this.$refs.coverImage.src = data.cover;
        
        // Устанавливаем источник аудио
        this.currentAudio.src = `https://${DOMAIN}${data.stream_url}`;
        
        // Ждем загрузки аудио
        await new Promise((resolve) => {
          this.currentAudio.oncanplay = () => {
            this.hideLoader();
            this.currentAudio.oncanplay = null;
            resolve();
          };
          this.currentAudio.load();
          
        });
        
        // Запускаем анимацию завершения загрузки
        
        
      } catch (error) {
        console.error('Ошибка загрузки трека:', error);
        await this.showErrorState();
        throw error;
      }
    },
    
    async showLoadingState() {
      // Можно добавить специальную анимацию для состояния загрузки
      await gsap.to([this.$refs.coverImage, this.$refs.songInfo], {
        opacity: 0.8,
        duration: 0.3,
        ease: "power1.out"
      });
    },
    
    async showErrorState() {
      // Анимация для состояния ошибки
      const tl = gsap.timeline();
      
      tl.to(".preloader", {
        backgroundColor: "rgba(80, 18, 34, 0.8)",
        duration: 0.5
      })
      .to(".loading-text", {
        text: "Ошибка загрузки",
        duration: 0.3
      })
      .to(".wave", {
        backgroundColor: "#ff4d4d",
        duration: 0.3
      });
      
      return tl;
    },
    async updatePlayerUI(isPlaying) {
      // document.getElementById('play-btn').hidden = !isPlaying;
      // document.getElementById('pause-btn').hidden = isPlaying;
      console.log();
    },
    async updateTimeDisplay() {
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
    async formatTime(seconds) {
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
      // this.$emit('prev');
      this.sendPrevTrack();
    },
    nextTrack() {
      // this.$emit('next');
      this.sendNextTrack();
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


/* Временный стиль для Sand Track */
.send-container {
  @apply absolute left-10 bottom-10;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  max-width: 500px;
}

.Send{
  cursor: pointer;
}

.Send_link {
  background-color: rgba(160, 85, 245, 0.068); /* #171222 с 25% opacity */
  min-width: 80px;
  min-height: 10px;
  backdrop-filter: blur(10px);

  width: 100%;
  border: none;
  border-radius: 30px;
  padding: 10px 12px;
  color: white;
  outline: none;
}

.Send_link::placeholder {
  color: rgba(255, 255, 255, 0.7);
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

/* Общие стили плеера */
.music-player {
  position: absolute;
  right: 5px;
  top: 80px;
  width: 450px;
  height: 90%;
  min-height: 700px;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 60px;
  backdrop-filter: blur(10px);
  padding: 30px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* .music-player {
  position: absolute;
  width: 500px;
  height: 970px;
  right: 5px;
  top: 80px;
  height: 90%;
  width: auto;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 60px;
  backdrop-filter: blur(10px);
  padding: 20px;
  box-sizing: border-box;
} */

.player-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Стили для фрейма с обложкой */
.frame {
  position: relative;
  width: 100%;
  height: 400px;
  min-height: 400px;
  margin: 0 auto 30px;
  background: rgba(18, 11, 33, 0.75);
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.212);
  border-radius: 30px;
  overflow: hidden;
  flex-shrink: 0;
}

.frame {
  position: relative;
  width: 400px;
  height: 400px;
  margin: 0 auto;
  background: rgba(18, 11, 33, 0.75);
  border-radius: 30px;
}

.image_track {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 30px;
  user-select: none;
  pointer-events: none;
}

/* Стили для контента плеера */
.player-content {
  width: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 0 15px;
  user-select: none;
}

.player-content { 
  width: 100%;
  height: 40%;
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Выравнивание контента по левому краю */
  position: relative; /* Для правильного позиционирования дочерних элементов */
  padding: 0 10px; /* Для создания отступов внутри контейнера */
}


.song-info {
  text-align: left;
  margin-bottom: 20px;
}

.song-info {
  position: relative;
  top: 10px;
  text-align: left;
  margin-top: 10px;    /* Отступ сверху */
  margin-bottom: 45px; /* Отступ снизу */
  margin-left: 0;      /* Небольшой отступ слева, если нужно */
  width: 100%;         /* Чтобы занимал всю доступную ширину */
}

.song-title {
  font-size: 30px;
  font-weight: bold;
  color: #9925BA;
  /* opacity: 0.75; */
  /* margin-bottom: 5px; */
}

.song-artist {
  font-size: 20px;
  font-weight: bold;
  color: #935DA2;
  margin-top: 5px;
  margin-bottom: 5px;
}

/* Стили для прогресс-бара */
.progress-container {
  width: 100%;
  margin: 15px 0;
}

/* Стили для элементов управления */
.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
}

/* Стили для прелоадера */
.preloader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background: linear-gradient(135deg, #0d6e863d 0%, #30047583 100%); */
  background: rgba(18, 11, 33, 0.75);
  border: 2px solid #10adb87e;
  border-radius: 1rem;
  border-radius: 60px;
  backdrop-filter: blur(50px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.preloader-content {
  /* opacity: 0.5; */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.wave-container {
  display: flex;
  align-items: flex-end;
  height: 60px;
  gap: 8px;
}

.Logo-player{
  z-index: 5;
  size: 500px;
}

.wave {
  width: 10px;
  height: 40px;
  backdrop-filter: blur(10px);
  background: linear-gradient(to top, #ff00dd, #ff0077a8);
  border-radius: 10px;
  transform-origin: bottom center;
  opacity: calc(0.6 + var(--index) * 0.1);
}

.wave:nth-child(odd) {
  height: 60px;
}

.loading-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
  text-transform: uppercase;
  font-weight: 300;
}
</style>