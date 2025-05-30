<template>
  <div class="main-container">
    <!-- Левый блок: Список участников -->
    <ParticipantsList
      :participants="participants"
      :userId="userId"
    />
    
    <!-- Центральный блок: Очередь треков и поле ввода -->
    <div class="center-section">
      <div class="Trackqueue">
        <TrackQueue 
        :tracks="tracks" 
        :currentTrackIndex="currentTrackIndex"
      />
      </div>
      <div class="SendBlock">
        <SendTrack @send="handleSendTrack"/>
      </div>
      <!-- <SendTrack class="SendBlock" @send="handleSendTrack"/> -->
      
    </div>

    <!-- Правый блок: Плеер -->
    <AudioPlayer
      ref="audioPlayer"
      :song="currentSong"
      @participants-update="updateParticipantsList"
      @update-tracks="updateTracksList"
    />
  </div>
</template>

<script>
import AudioPlayer from '@/components/player.vue';
import ParticipantsList from '@/components/Participants-list.vue';
import TrackQueue from '@/components/Track_queue.vue';
import SendTrack from '@/components/Send-search_Track.vue';

export default {
  components: {
    AudioPlayer,
    ParticipantsList,
    TrackQueue,
    SendTrack
  },
  data() {
    return {
      currentSong: {
        name: 'Name of song',
        artist: 'Songer',
        src: 'path/to/your/audio/file.mp3'
      },
      tracks: [],
      currentTrackIndex: 0,
      isPlayerVisible: false,
      participants: [],
      userId: this.getCookie('user_id'),
      // trackUrl удален отсюда
    };
  },
  methods: {
    updateParticipantsList(participantsArray) {
      this.participants = participantsArray;
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    },
    updateTracksList(tracksArray, currentIndex) {
      this.tracks = tracksArray;
      this.currentTrackIndex = currentIndex;
    },
    handleSendTrack(url) {
      if (url && this.$refs.audioPlayer) {
        this.$refs.audioPlayer.playTrack(url);
      }
    }
  }
};
</script>

<style scoped>
.main-container {
  display: flex;
  justify-content: center; /* центрирует по горизонтали */
  align-items: stretch;    /* чтобы блоки тянулись на всю высоту */
  height: 100vh;           /* чтобы занять весь экран */
  gap: 20px;               /* отступы между колонками */
  padding: 20px;
  box-sizing: border-box;
}

/* Стили для левой колонки (участники) */
.participants-container {
  width: 400px;
  height: calc(100% - 40px);
  margin-top: 20px;
  border-radius: 30px;
}

/* Центральная секция: очередь треков + поле ввода */

.center-section {
  display: flex;
  flex-direction: column;
  border-radius: 30px;
  backdrop-filter: blur(10px);
  flex: 0 1 800px;
  overflow: hidden;
  min-height: 0;
  height: 100%;
}

.Trackqueue {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 7px;
  box-sizing: border-box;
}


/* .SendBlock {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(23, 18, 34, 0.7);
} */

ParticipantsList,
.player-wrapper {
  width: 300px;
  flex-shrink: 0;
}

/* Стили для очереди треков */
.queue-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>