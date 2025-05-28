<script setup>
import { computed } from 'vue';
import play_button_pause from '@/assets/play_button_pause.vue';
import play_button_active from '@/assets/play_button_active.vue';
import play_past_button from '@/assets/play_past_button.vue';
import play_next_button from '@/assets/play_next_button.vue';

const props = defineProps({
  isPlaying: Boolean
});

const emit = defineEmits(['play', 'pause', 'prev', 'next']);

const togglePlayPause = () => {
  if (props.isPlaying) {
    emit('pause');
  } else {
    emit('play');
  }
};
</script>

<template>
  <div class="controls control-block" :class="{ 'play-active': isPlaying }">
    <button class="play-btn-past control-button past-button" @click="emit('prev')">
      <play_past_button />
    </button>

    <button class="play-btn play-button-wrapper" @click="togglePlayPause">
      <component 
        :is="isPlaying ? play_button_active : play_button_pause" 
        class="control-button play-button" 
      />
    </button>

    <button class="play-btn-next control-button next-button" @click="emit('next')">
      <play_next_button />
    </button>
  </div>
</template>







<style>
.control-block {
  @apply flex items-center justify-center p-0 relative;
  width: 240px;
  height: 80px;
}

/* Базовые стили кнопок */
.play-btn-past, .play-btn-next {
  @apply w-[40px] h-[40px] transition-all duration-500 ease-in-out;
  filter: drop-shadow(0px 4px 10.5px rgba(0, 0, 0, 0.5));
}

.play-btn {
  @apply w-[80px] h-[80px] transition-transform duration-300 ease-in-out;
}

/* Состояние по умолчанию (пауза) */
.play-btn-past {
  @apply mr-[20px];
}

.play-btn-next {
  @apply ml-[20px];
}

/* Анимация при воспроизведении */
.play-active .play-btn-past {
  @apply mr-[25px] -translate-x-[3px];
}

.play-active .play-btn {
  @apply scale-110;
}

.play-active .play-btn-next {
  @apply ml-[25px] translate-x-[3px];
}

/* Общие стили */
.control-button {
  @apply cursor-pointer transition-all duration-300 bg-transparent border-none p-0;
}

.control-button:active {
  @apply scale-95;
}

.play-button {
  @apply w-[80px] h-[80px];
}
</style>

<!-- <style>
.control-block {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  position: relative;
  width: 240px;
  height: 80px;
}

/* Базовые стили кнопок */
.play-btn-past, .play-btn-next {
  width: 41px;
  height: 40px;
  filter: drop-shadow(0px 4px 10.5px rgba(0, 0, 0, 0.5));
  transition: transform 0.3s ease, margin 0.3s ease;
}

.play-btn {
  width: 80px;
  height: 80px;
  transition: transform 0.3s ease;
}

/* Состояние по умолчанию (пауза) */
.play-btn-past {
  margin-right: 35px;
}

.play-btn-next {
  margin-left: 35px;
}

/* Анимация при воспроизведении */
.play-active .play-btn-past {
  margin-right: 40px;
  transform: translateX(-5px);
}

.play-active .play-btn {
  transform: scale(1.1);
}

.play-active .play-btn-next {
  margin-left: 40px;
  transform: translateX(5px);
}

/* Общие стили */
.control-button {
  cursor: pointer;
  transition: all 0.2s;
  background: transparent;
  border: none;
  padding: 0;
}

.control-button:active {
  transform: scale(0.95);
}

.play-button {
  width: 80px;
  height: 80px;
}
</style> -->