<template>
    <div class="progress-container" @click="seekFromClick">
      <div class="progress-line"></div>
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
      dotPosition() {
        if (!this.duration) return '0%';
        return `${(this.currentTime / this.duration) * 100}%`;
      },
    },
    methods: {
      seekFromClick(e) {
        const rect = e.currentTarget.getBoundingClientRect();
        const clickX = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
        const newTime = (clickX / rect.width) * this.duration;
        this.$emit('seek', newTime);
      },
      startDrag() {
        this.isDragging = true;
        document.addEventListener('mousemove', this.handleDrag);
        document.addEventListener('mouseup', this.stopDrag);
      },
      handleDrag(e) {
        if (!this.isDragging) return;
  
        const progressBar = this.$el;
        const rect = progressBar.getBoundingClientRect();
        const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
        const newTime = (x / rect.width) * this.duration;
  
        this.$emit('seek', newTime);
      },
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
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    cursor: pointer;
  }
  
  .progress-line {
    position: absolute;
    height: 100%;
    width: 100%;
    background: linear-gradient(to right, #00ced1 0%, #8a2be2 100%);
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
  </style>
  