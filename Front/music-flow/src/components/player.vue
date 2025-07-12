<template>
  <div ref="playerElement"> 
  </div>
  <div class="music-player">
    <!-- Прелоадер с анимацией -->
    <div class="preloader" v-if="isLoading">
      <div class="preloader-content">
        <div class="wave-container">
          <Logo class="Logo-player"></Logo>
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

        <div class="player-controls">
          <div class="progress-container">
            <TimeBar :currentTime="currentTime" :duration="duration" @seek="onSeek" ref="timeBar" />
          </div>

        <div class="controls" ref="controls">
          <play-control-block :is-playing="isPlaying" @play="sendPlayCommand" @pause="sendPauseCommand"
            @prev="prevTrack" @next="nextTrack" ref="playControl" />
        </div>
        <div class="volume-container">
          <volume 
            v-if="!isLoading"
            :volume="currentVolume"
            @update:volume="handleVolumeUpdate"
            ref="volumeControl"
          />
        </div>
        </div>


      </div>

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
// import Send from '@/assets/Send.vue';
import Logo from '@/assets/Logo-for-player.vue';
import TimeBar from '../components/time-bar.vue';
import { initSocket, sendSocketMessage } from '../utils/playerSocket.js';
import { loadWithMediaSource } from '../utils/mediaSourcePlayer.js';
import { fetchQueue, formatParticipants } from '../utils/roomData.js';
import { gsap } from 'gsap';
import { CustomEase } from 'gsap/CustomEase';
gsap.registerPlugin(CustomEase);
const DOMAIN = import.meta.env.VITE_DOMAIN;




export default {
  emits: ['participants-update', 'update-tracks'], // ✅ Должно быть на верхнем уровне объекта
  components: {
    play_button_pause,
    volume,
    Logo,
    play_button_active,
    play_past_button,
    play_next_button,
    playControlBlock,
    TimeBar
  },
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
        isInitialLoad: true, // <--- добавлено
        currentTrackTitle: 'Название трека',
        currentArtist: 'Исполнитель',
        isPlaying: false,
        currentTime: 0,
        currentVolume: 1,
        duration: 0,
        currentTrackIndex: 0,
        interval: null,
        isDragging: false,
        socket: null,
        userId: null,
        currentAudio: null,
        isSyncing: false,
        currentTrack: null,
        progress: null,
        list_tracks: [],
        room_id: 'faf1c5d6-da2f-4fb5-88a6-7023d40d62ff',
        response: null,
        json_with_list: null,
        nextTrackTimeout: null
      };
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


  async mounted() {
    // await this.hideLoader();
    
    
    
    this.currentAudio = this.$refs.audioElement; // Инициализируем currentAudio из ref

    //     this.currentAudio.addEventListener('ended', () => {
    //   console.log('Трек завершился, плавно переключаем на следующий');
    //   this.sendNextTrack();
    // });
    let isTrackEnding = false;

    this.currentAudio.addEventListener('ended', async () => {
      if (isTrackEnding) return;
      isTrackEnding = true;

      // Ждём 500мс, чтобы "поймать" другие срабатывания
      await new Promise(resolve => setTimeout(resolve, 500));

      // Проверяем, что трек действительно закончился
      if (Math.abs(this.currentAudio.currentTime - this.currentAudio.duration) < 1) {
        await this.sendNextTrack();
      }

      isTrackEnding = false;
    });



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

  updateTracksList(tracksArray, currentIndex) {
    this.list_tracks = tracksArray;
    this.currentTrackIndex = currentIndex;
    this.$emit('update-tracks', tracksArray, currentIndex);
  },


  async initWebSocket() {
    const userIdFromCookie = await this.getCookie('user_id');
    if (!userIdFromCookie) {
      alert('Требуется авторизация');
      return;
    }

    this.userId = userIdFromCookie;
    this.currentAudio = document.getElementById('audio');

    this.socket = initSocket(this.room_id, this.userId, {
      '*': (data) => this.handleSocketMessage(data)
    });
  },
    async sendPlayCommand() {
      sendSocketMessage(this.socket, {
        type: 'play',
        position: this.currentAudio.currentTime
      });
      this.currentAudio.play();
      await this.updatePlayerUI(true);
      this.isPlaying = true;
    },
    async sendPauseCommand() {
      sendSocketMessage(this.socket, {
        type: 'pause',
        position: this.currentAudio.currentTime
      });
      this.currentAudio.pause();
      this.updatePlayerUI(false);
      this.isPlaying = false;
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
      sendSocketMessage(this.socket, {
        type: 'seek',
        position
      });
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
            this.json_with_list = await fetchQueue(this.room_id);
            this.updateTracksList(this.json_with_list.list_track, this.json_with_list.index);
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
        if (data.tracks) {
          this.updateTracksList(data.tracks, data.index);
        }
        break;
        case 'seek':
          console.log(data)
          await this.handleSeekMessage(data);
          break;
        // case 'participants_update':
        //   // Сюда приходят ники участников
        //   console.log(`participants:`, data.participants);
        //   // updateParticipantsList(data.participants);
        //   break;
        case 'participants_update':
          console.log('participants:', data.participants);
          const formattedParticipants = formatParticipants(data.participants);
          this.$emit('participants-update', formattedParticipants);
        break;
        case 'load_track':
          // var response = await fetch(`https://${DOMAIN}/get_queue_tracks?room_id=${this.room_id}`);
          // var json_with_list = await response.json();
          this.updateTracksList(this.json_with_list.list_track, data.index);
          await this.loadTrack(data.url);
          break
        // ... другие типы сообщений
        case 'add_track':
        // if (data.tracks) {
          // const updatedTracks = [...this.list_tracks, ...data.tracks];
          const json_with_list2 = await fetchQueue(this.room_id, data.track_id);
          this.json_with_list.list_track.push(json_with_list2.new_track);
          this.updateTracksList(this.json_with_list.list_track, this.index);
          // this.updateTracksList(updatedTracks, this.currentTrackIndex);
        // }
        break;
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
    //   this.currentAudio.src = `/api/stream?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`;

    //   const trackInfo = await fetch(`/api/track_info?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`);
    //   console.log(`trackInfo: `, trackInfo);
      
    //   await fetch(`/api/stream?url=${encodeURIComponent(trackUrl)}&user_id=${data.user_id}`)
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
  async playTrack(url) {

    // const url = document.getElementById('track-url').value.trim();
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
    sendSocketMessage(this.socket, {
      type: 'previous_track',
      tracks: [trackUrl],
      index: 0
    });
  },
  async sendAddTrack(trackUrl) {
    sendSocketMessage(this.socket, {
      type: 'add_track',
      tracks: [trackUrl]
    });
  },
  // async sendNextTrack() {
  //   if (this.socket && this.socket.readyState === WebSocket.OPEN) {

  //     this.sendPauseCommand();
  //     await this.socket.send(JSON.stringify({
  //       type: 'next_track'
  //     }));
      
  //   }
  // },
  async sendNextTrack() {
    if (this.nextTrackTimeout) clearTimeout(this.nextTrackTimeout);

    this.nextTrackTimeout = setTimeout(async () => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.sendPauseCommand();
        sendSocketMessage(this.socket, { type: 'next_track' });
      }
      this.nextTrackTimeout = null;
    }, 300); // Задержка 300мс
  },
  async sendPrevTrack() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      if (this.currentAudio.currentTime > 5){
        this.onSeek(0);
      }
      else {
        this.sendPauseCommand();
        sendSocketMessage(this.socket, { type: 'previous_track' });
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
          if (this.isInitialLoad) {
            this.isLoading = true;
            this.isInitialLoad = false;
          } else {
            await gsap.to([this.$refs.coverImage, this.$refs.songInfo], {
              opacity: 0,
              y: 20,
              duration: 0.4,
              ease: "power2.in"
            });
          }

          // Reset previous source
          this.currentAudio.src = '';
          await new Promise(r => setTimeout(r, 50));

          const response = await fetch(`/api/tracks/track_and_stream?url=${encodeURIComponent(trackUrl)}&user_id=${this.userId}`);
          const data = await response.json();

          this.currentTrackTitle = data.title;
          this.currentArtist = data.artist;
          this.$refs.coverImage.src = data.cover;

          try {
            await loadWithMediaSource(this.currentAudio, `/api/tracks${data.stream_url}`);
          } catch (e) {
            console.error('MediaSource error, falling back to standard:', e);
            this.currentAudio.src = `/api/tracks${data.stream_url}`;
            await this.currentAudio.load();
          }

          if ('mediaSession' in navigator) {
            navigator.mediaSession.metadata = new MediaMetadata({
              title: data.title,
              artist: data.artist,
              artwork: [{ src: data.cover, sizes: '400x400', type: 'image/jpeg' }]
            });

            navigator.mediaSession.setActionHandler('play', () => this.sendPlayCommand());
            navigator.mediaSession.setActionHandler('pause', () => this.sendPauseCommand());
            navigator.mediaSession.setActionHandler('previoustrack', () => this.prevTrack());
            navigator.mediaSession.setActionHandler('nexttrack', () => this.nextTrack());
          }

          await new Promise((resolve) => {
            const onCanPlay = () => {
              this.currentAudio.removeEventListener('canplay', onCanPlay);
              if (this.isLoading) this.hideLoader();
              resolve();
            };
            this.currentAudio.addEventListener('canplay', onCanPlay);
            this.currentAudio.load();
          });

          await gsap.fromTo(
            [this.$refs.coverImage, this.$refs.songInfo],
            { opacity: 0, y: -20 },
            {
              opacity: 0.8,
              y: 0,
              duration: 0.6,
              ease: "power2.out",
              stagger: 0.1
            }
          );
        } catch (error) {
          console.error('Track loading error:', error);
          this.currentAudio.src = '';
          throw error;
        }
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
.music-player {
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 60px;
  backdrop-filter: blur(10px);
  padding: 40px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.player-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.player-grid {
  display: grid;
  grid-template-areas: 
    "cover content"
    "cover content";
  grid-template-columns: minmax(200px, 1fr) 2fr;
  grid-template-rows: 1fr;
  gap: 20px;
  height: 100%;
}

.player-controls {
  display: flex;
  flex-direction: column;
  gap: min(1.5vh, 15px);
  margin-top: auto;
  width: 100%;
}

.preloader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid #10adb87e;
  border-radius: 60px;
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center; /* Центрирование по горизонтали */
  align-items: center; /* Центрирование по вертикали */
  z-index: 100;
  box-sizing: border-box;
  padding: 0;
}

.preloader-content {
  display: flex;
  flex-direction: column;
  align-items: center; /* Центрирование содержимого по горизонтали */
  justify-content: center; /* Центрирование содержимого по вертикали */
  gap: 30px;
  width: 100%; /* Занимает всю доступную ширину */
  height: 100%; /* Занимает всю доступную высоту */
}

.wave-container {
  display: flex;
  align-items: center; /* Центрирование волн по вертикали */
  justify-content: center; /* Центрирование волн по горизонтали */
  height: 60px;
  gap: 8px;
  width: 100%; /* Занимает всю доступную ширину */
}

.Logo-player {
  width: 120px;
  height: 120px;
  object-fit: contain;
  margin: 0 auto; /* Центрирование логотипа */
}

.loading-text {
  color: rgba(255, 255, 255, 0.85);
  font-size: 18px;
  font-weight: 300;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-align: center;
  padding: 10px 20px;
}



.cover-container {
  grid-area: cover;
  display: flex;
  align-items: center;
  justify-content: center;
}

.frame {
  position: relative;
  width: 100%;
  aspect-ratio: 1/1;
  max-height: 40vh;
  max-width: 40vh;
  margin: 0 auto;
  background: rgba(18, 11, 33, 0.75);
  border-radius: 20px;
  overflow: hidden;
}



.image_track {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
  pointer-events: none;
}

.content-container {
  grid-area: content;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.song-info {
  padding: 20px;
  text-align: left;
  margin-bottom: 15px;
  user-select: none;
}

.song-title {
  font-size: clamp(18px, 3vw, 30px);
  font-weight: bold;
  color: #9925BA;
  margin-bottom: 5px;
  word-break: break-word;
  user-select: none;
}

.song-artist {
  font-size: clamp(14px, 2vw, 20px);
  color: #935DA2;
}

.progress-container {
  width: 100%;
  margin: 15px 0;
}

.volume-container {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: auto;
  padding: 20px 0;
}

/* Адаптивные стили */
@media (max-width: 1024px) {
  .volume-container {
    padding: 15px 0;
  }
}

@media (max-width: 768px) {
  .volume-container {
    padding: 10px 0;
  }
}

@media (max-width: 480px) {
  .volume-container {
    padding: 5px 0;
  }
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: min(2vw, 20px);
  margin: min(1vh, 10px) 0;
}

.volume-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: min(1vh, 10px) 0;
}

/* Адаптация для разных соотношений сторон */
/* @media (max-aspect-ratio: 1/1) {
  .player-grid {
    grid-template-areas: 
      "cover"
      "content";
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }
  
  .frame {
    max-width: 300px;
    margin: 0 auto;
  }
} */

@media (max-width: 768px) {
  .music-player {
    padding: 15px;
    border-radius: 50px;
  }
  
  .player-grid {
    gap: 15px;
  }
  
  .controls {
    gap: 10px;
    margin: 15px 0;
  }
}

@media (max-width: 480px) {
  .frame {
    max-width: 250px;
  }
  
  .song-title {
    font-size: clamp(16px, 5vw, 24px);
  }
  
  .song-artist {
    font-size: clamp(12px, 4vw, 18px);
  }
}

/* Специфичные медиа-запросы для разных соотношений */
/* @media (aspect-ratio: 16/10) {
  .player-grid {
    grid-template-columns: minmax(180px, 1fr) 2fr;
  }
} */

@media (aspect-ratio: 3/2) {
  .player-grid {
    grid-template-columns: minmax(160px, 1fr) 2fr;
  }
  
  .controls {
    flex-wrap: wrap;
  }
}
</style>
