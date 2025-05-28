<template>
  <div :class="['player-wrapper', { visible: isPlayerVisible }]">
    <AudioPlayer :song="currentSong" />
  </div>

</template>








<script>
import AudioPlayer from '@/components/player.vue';
import ParticipantsList from '@/components/Participants-list.vue';

export default {
  components: {AudioPlayer},
  ParticipantsList,
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




<!-- <template>
  <div :class="['player-wrapper', { visible: isPlayerVisible }]">
    <AudioPlayer :song="currentSong" />
  </div>

  <div class="participants-container">
    <h3 class="participants-title">Участники ({{ participants.length }})</h3>
    <ul id="participants-list" class="participants-list"></ul>
  </div>
</template>

<script>
import AudioPlayer from '@/components/player.vue';

export default {
  components: {
    AudioPlayer
  },
  data() {
    return {
      currentSong: {
        name: 'Name of song',
        artist: 'Songer',
        src: 'path/to/your/audio/file.mp3'
      },
      isPlayerVisible: false,
      participants: [],
      userId: 'Alex' // Здесь должен быть реальный ID текущего пользователя
    };
  },
  mounted() {
    setTimeout(() => {
      this.isPlayerVisible = true;
    }, 100);
    
    // Имитация получения данных
    this.fetchParticipants();
    socket.on('participants-updated', (newParticipants) => {
    this.updateParticipantsList(newParticipants);
});
  },
  methods: {
    async fetchParticipants() {
      try {
    const response = await axios.get('/api/participants');
    this.updateParticipantsList(response.data);
      } catch (error) {
    console.error('Ошибка получения участников:', error);
      }
    },
    
    // Ваша функция с минимальными изменениями
    updateParticipantsList(participants) {
      this.participants = participants; // Сохраняем данные реактивно
      
      const list = document.getElementById('participants-list');
      list.innerHTML = '';
      
      participants.forEach(participant => {
        const li = document.createElement('li');
        li.className = 'participant-item';
        
        if (participant === this.userId) {
          li.classList.add('you');
        }

        // Аватар с первой буквой имени
        const avatar = document.createElement('div');
        avatar.className = 'participant-avatar';
        avatar.textContent = participant.charAt(0).toUpperCase();
        li.appendChild(avatar);

        // Имя участника
        const nameSpan = document.createElement('span');
        nameSpan.className = 'participant-name';
        nameSpan.textContent = participant + (participant === this.userId ? ' (Вы)' : '');
        li.appendChild(nameSpan);

        // Статус
        const status = document.createElement('span');
        status.className = 'status-badge status-online';
        status.textContent = 'online';
        li.appendChild(status);

        list.appendChild(li);
      });
    }
  }
};
</script> -->

<style>
/* Стили из вашего CSS с дополнениями */
.participants-container {
  @apply bg-[rgba(255,255,255,0.1)] rounded-2xl p-6 border border-[#00d9e7] backdrop-blur;
  max-width: 400px;
  margin-top: 2rem;
}

.participants-title {
  @apply text-2xl font-bold text-white mb-4 text-center;
  text-shadow: 0 0 10px rgba(0, 217, 231, 0.5);
}

.participants-list {
  @apply list-none p-0 m-0;
  max-height: 400px;
  overflow-y: auto;
}

.participant-item {
  @apply flex items-center py-3 px-4 mb-3 rounded-full transition-all duration-300;
  background: rgba(208, 188, 255, 0.08);
  border: 1px solid rgba(208, 188, 255, 0.2);
}

.participant-item.you {
  background: rgba(208, 188, 255, 0.2);
  border-color: rgba(208, 188, 255, 0.4);
  box-shadow: 0 0 15px rgba(208, 188, 255, 0.2);
}

.participant-avatar {
  @apply w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg mr-4;
  background: linear-gradient(135deg, #D0BCFF 0%, #2EA48C 100%);
  color: #1F1431;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.3);
}

.participant-name {
  @apply flex-grow text-white font-medium;
  font-size: 1.1rem;
}

.status-badge {
  @apply py-1 px-3 rounded-full text-xs font-bold uppercase;
}

.status-online {
  background: rgba(46, 164, 79, 0.2);
  color: #2EA44F;
  border: 1px solid rgba(46, 164, 79, 0.4);
}

.parent {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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