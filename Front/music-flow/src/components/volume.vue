<template>
  <div class="volume-control">
    <VolumeIcon :volume="volume" @update:volume="$emit('update:volume', $event)" />
    <input
      type="range"
      min="0"
      max="1"
      step="0.01"
      :value="volume"
      @input="$emit('update:volume', parseFloat($event.target.value))"
    />
  </div>
</template>

<script>
import VolumeIcon from '@/assets/VolumeIcon.vue';

export default {
  name: 'Volume',
  props: {
    volume: {
      type: Number,
      required: true,
    },
  },
  components: {
    VolumeIcon,
  },
};
</script>

<style scoped>
/* Стили остаются без изменений */
.volume-control {
  display: flex;
  align-items: center;
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  color: white;
}

input[type="range"] {
  margin: 0 10px;
  width: 150px;
  background: linear-gradient(to right, #00CED1, #008fee);
  /* background-color: white; */
  opacity: 1;
  height: 5px;
  border-radius: 5px;
  outline: none;
  -webkit-appearance: none;
  position: relative;
  z-index: 1;
}

/* Стилизация тумблера: скрыт по умолчанию */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 15px;
  height: 15px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0; /* скрыт */
  transition: opacity 0.2s ease;
}

/* Показываем тумблер при наведении на сам input */
input[type="range"]:hover::-webkit-slider-thumb {
  opacity: 1;
}

/* Для Firefox */
input[type="range"]::-moz-range-thumb {
  width: 15px;
  height: 15px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

input[type="range"]:hover::-moz-range-thumb {
  opacity: 1;
}

.volume-icon {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}
</style>