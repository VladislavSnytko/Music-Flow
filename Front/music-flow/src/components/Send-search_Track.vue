<template>
  <div class="send-container">
    <input 
      type="text" 
      v-model="trackUrl" 
      placeholder="Вставьте ссылку на трек из Яндекс.Музыки" 
      class="send-input"
      @keyup.enter="handleSend"
    >
    <Send class="send-button" @click="handleSend"/>
  </div>
</template>

<script>
import Send from '@/assets/Send.vue';

export default {
  components: {
    Send
  },
  data() {
    return {
      trackUrl: ''
    };
  },
  methods: {
    handleSend() {
      if (this.trackUrl.trim()) {
        this.$emit('send', this.trackUrl.trim());
        this.trackUrl = '';
      }
    }
  }
};
</script>

<style scoped>
.send-container {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(23, 18, 34, 0.7);
  border-radius: 50px;
  /* border-top: 1px solid rgba(208, 188, 255, 0.2); */
}

.send-input {
  flex-grow: 1;
  background-color: rgba(160, 85, 245, 0.15);
  min-height: 20px;
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 50px;
  padding: 12px 20px;
  color: white;
  outline: none;
  font-size: 16px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.send-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.send-button {
  width: 36px;
  height: 36px;
  cursor: pointer;
  transition: all 0.3s ease;
  fill: #D0BCFF;
}

.send-button:hover {
  transform: scale(1.1);
  fill: #ffffff;
}
</style>
[file content end]