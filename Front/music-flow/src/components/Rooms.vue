<template>
  <div class="rooms-container">
    <input
      v-model="roomIdInput"
      type="text"
      placeholder="Введите ID комнаты"
      class="rooms-input"
      @keyup.enter="joinRoom"
    />
    <Button text="Подключиться" @click="joinRoom" />
  </div>
</template>

<script>
import Button from '@/components/Button.vue';

export default {
  components: { Button },
  data() {
    return { roomIdInput: '' };
  },
  methods: {
    joinRoom() {
      const value = this.roomIdInput.trim();
      if (value) {
        this.$emit('join-room', value);
      }
    }
  }
};
</script>

<style scoped>
.rooms-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: 100%;
  height: 100%;
}

.rooms-input {
  width: 100%;
  max-width: 400px;
  padding: 12px 20px;
  border-radius: 50px;
  border: none;
  background: rgba(160, 85, 245, 0.15);
  color: white;
  outline: none;
}
</style>
