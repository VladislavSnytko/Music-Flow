<template>
  <div class="progress-container" @click="seekFromClick">
    <!-- Время слева -->
    <div class="time current-time">{{ formatTime(currentTime) }}</div>
    
    <!-- Прогресс-бар с динамическим градиентом -->
    <div
      class="progress-line"
      :style="gradientStyle"
    ></div>
    
    <!-- Время справа -->
    <div class="time duration">{{ formatTime(duration) }}</div>
    
    <!-- Точка прогресса -->
    <div
      id="progress"
      class="progress-dot"
      :style="{ left: dotPosition }"
      @mousedown="startDrag"
    ></div>
  </div>
</template>


<script>
export default {
  props: {
    currentTime: {
      type: Number,
      required: true,
    },
    duration: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isDragging: false,
    };
  },
  computed: {
    // Позиция точки на прогресс-баре в процентах
    dotPosition() {
      if (!this.duration) return '0%';
      return `${(this.currentTime / this.duration) * 100}%`;
    },
    // Динамическое вычисление градиента
    gradientStyle() {
      const position = (this.currentTime / this.duration) * 100; // В процентах
      const transitionWidth = 50; // Увеличенная ширина перехода
      return {
        background: `linear-gradient(to right,
          #00CED1 0%,
          #00CED1 calc(${position}% - ${transitionWidth}px),
          color-mix(in srgb, #00CED1 75%, #8A2BE2 25%) calc(${position}% - ${transitionWidth * 0.66}px),
          color-mix(in srgb, #00CED1 50%, #8A2BE2 50%) calc(${position}% - ${transitionWidth * 0.33}px),
          color-mix(in srgb, #00CED1 25%, #8A2BE2 75%) ${position}%,
          #8A2BE2 calc(${position}% + 5px),
          #8A2BE2 100%)`,
        width: '100%',
        height: '5px',
        borderRadius: '5px',
        position: 'absolute',
      };
    },
  },
  methods: {
    // Форматируем время в формате mm:ss
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    },
    // При клике на прогресс-бар вычисляем новое время
    seekFromClick(e) {
      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const newTime = (clickX / rect.width) * this.duration;
      this.$emit('seek', newTime); // Отправляем новое время в родительский компонент
    },
    // Начало перетаскивания
    startDrag() {
      this.isDragging = true;
      document.addEventListener('mousemove', this.handleDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    // Обработка перетаскивания
    handleDrag(e) {
      if (!this.isDragging) return;

      const progressBar = this.$el;
      const rect = progressBar.getBoundingClientRect();
      const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const newTime = (x / rect.width) * this.duration;

      this.$emit('seek', newTime); // Отправляем новое время в родительский компонент
    },
    // Завершение перетаскивания
    stopDrag() {
      if (!this.isDragging) return;
      this.isDragging = false;
      document.removeEventListener('mousemove', this.handleDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
  },
};
</script>


<style scoped>
.progress-container {
  position: relative;
  width: 100%;
  height: 5px;
  /* background: rgba(255, 255, 255, 0.2); */
  border-radius: 4px;
  cursor: pointer;
}

.progress-line {
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: 4px;
  z-index: 1;
}

.progress-dot {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  background-color: #deb8ff;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  cursor: grab;
  z-index: 2;
}

.progress-dot:active {
  cursor: grabbing;
  transform: translate(-50%, -50%) scale(1.25);
}

/* Стили для времени */
.time {
  padding: 10px;
  position: absolute;
  font-size: 15px;
  user-select: none;
}

.current-time {
  /* left: 5px; */
  top: 10px;
  color: #94F6F6;
  text-shadow: 0px 0px 7.5px #00FFD4;
  pointer-events: none
}

.duration {
  right: 5px;
  top: 10px;
  color: #D794F3;
  text-shadow: 0px 0px 7.5px #EF149F;
  pointer-events: none
}
</style>
