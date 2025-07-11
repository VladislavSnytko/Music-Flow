





<template>
  <div class="participants-container">
    <h3 class="participants-title">Участники ({{ participants.length }})</h3>
    <ul class="participants-list">
      <li 
        v-for="participant in participants" 
        :key="participant.id"
        :class="['participant-item', { 'you': participant.id === userId }]"
      >
        <div class="participant-avatar">
          {{ participant.name.charAt(0).toUpperCase() }}
        </div>
        <span class="participant-name">
          {{ participant.name}}
        </span>
        <span class="status-badge status-online">online</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    participants: {
      type: Array,
      required: true,
      default: () => []
    },
    userId: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
/* .participants-container {
  @apply fixed left-0 top-0 bottom-0 p-6 backdrop-blur flex flex-col;
  width: 400px;
  background: rgba(23, 18, 34, 0.5); 
  border-radius: 0 2rem 2rem 0;
  z-index: 1000;
} */

.participants-container {
  width: 100%;
  height: 100%;
  background: rgba(23, 18, 34, 0.5);
  border-radius: 2rem;
  padding: 1.5rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.participants-list {
  flex: 1;
  overflow-y: auto;
}

.participants-title {
  @apply text-2xl font-bold text-white mb-4 text-center;
  text-shadow: 0 0 10px rgba(0, 217, 231, 0.5);
  flex-shrink: 0;
}

.participants-list {
  @apply list-none p-0 m-0;
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px; /* или только по бокам: padding: 0 10px; */
}

.participant-item {
  @apply flex items-center py-3 px-4 mb-3 rounded-full transition-all duration-300;
  background: rgba(208, 188, 255, 0.08);
}

.participant-item.you {
  background: rgba(208, 188, 255, 0.2);
  box-shadow: 0 0 10px rgba(208, 188, 255, 0.2);
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
}
</style>