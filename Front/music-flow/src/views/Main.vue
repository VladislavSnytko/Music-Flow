<template>
  <div v-if="!connected" class="main-container">
    <Rooms @join-room="handleJoinRoom" />
  </div>
  <div v-else class="main-container">
    <!-- Левый блок: Список участников -->
    <div class="participants-column">
      <ParticipantsList
        :participants="participants"
        :userId="userId"
      />
    </div>
    
    <!-- Центральный блок: Очередь треков и поле ввода -->
    <div class="center-column">
      <div class="track-queue-container">
        <TrackQueue 
          :tracks="tracks" 
          :currentTrackIndex="currentTrackIndex"
        />
      </div>
      <div class="send-block">
        <SendTrack @send="handleSendTrack"/>
      </div>
    </div>

    <!-- Правый блок: Плеер -->
    <div class="player-column">
      <AudioPlayer
        v-if="roomId"
        ref="audioPlayer"
        :song="currentSong"
        :roomId="roomId"
        @participants-update="updateParticipantsList"
        @update-tracks="updateTracksList"
      />
    </div>
  </div>
</template>

<script>
import AudioPlayer from '@/components/player.vue';
import ParticipantsList from '@/components/Participants-list.vue';
import TrackQueue from '@/components/Track_queue.vue';
import SendTrack from '@/components/Send-search_Track.vue';
import Rooms from '@/components/Rooms.vue';
import { getCookie } from '@/utils/cookies.js';

export default {
  components: {
    AudioPlayer,
    ParticipantsList,
    TrackQueue,
    SendTrack,
    Rooms
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
      userId: getCookie('user_id'),
      roomId: null,
      connected: false,
      // trackUrl удален отсюда
    };
  },
  methods: {
    updateParticipantsList(participantsArray) {
      this.participants = participantsArray;
    },
    handleJoinRoom(id) {
      this.roomId = id;
      this.connected = true;
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
  display: grid;
  /* grid-template-columns: minmax(250px, 400px) minmax(400px, 1fr) minmax(250px, 450px); */
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

.participants-column {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.center-column {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 30px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.track-queue-container {
  flex: 1;
  overflow-y: auto;
  padding: 7px;
  box-sizing: border-box;
}

.send-block {
  flex-shrink: 0;
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  background: rgba(23, 18, 34, 0.7);
}

.player-column {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* Мобильная версия */
@media (max-width: 1024px) {
  .main-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
    gap: 15px;
    padding: 15px;
  }

  .participants-column,
  .center-column,
  .player-column {
    width: 100%;
    height: auto;
    min-height: 300px; /* Минимальная высота для мобильных */
  }

  .track-queue-container {
    overflow: visible;
    flex: none;
    height: auto;
  }

  .player-column {
    order: 1; /* Плеер первым на мобильных */
  }
  
  .center-column {
    order: 2;
  }
  
  .participants-column {
    order: 3;
  }
}
</style>