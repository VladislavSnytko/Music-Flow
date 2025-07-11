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
.volume-control {
  display: flex;
  align-items: center;
  width: 50%;
  max-width: min(80vw, 300px);
  color: white;
  gap: min(1vw, 10px);
}

input[type="range"] {
  flex: 1;
  min-width: 50px;
  margin: 0;
  background: linear-gradient(to right, #00CED1, #008fee);
  height: min(0.8vh, 5px);
  border-radius: 5px;
  outline: none;
  -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: min(1.5vh, 15px);
  height: min(1.5vh, 15px);
  background: white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

input[type="range"]:hover::-webkit-slider-thumb {
  opacity: 1;
}

/* Для Firefox */
input[type="range"]::-moz-range-thumb {
  width: min(1.5vh, 15px);
  height: min(1.5vh, 15px);
  background: white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

input[type="range"]:hover::-moz-range-thumb {
  opacity: 1;
}

/* Всегда показывать ползунок на мобильных */
@media (hover: none) {
  input[type="range"]::-webkit-slider-thumb {
    opacity: 1 !important;
  }
  input[type="range"]::-moz-range-thumb {
    opacity: 1 !important;
  }
}

/* Адаптация для маленьких высот */
@media (max-height: 600px) {
  input[type="range"] {
    height: min(0.7vh, 4px);
  }
  
  input[type="range"]::-webkit-slider-thumb {
    width: min(1.3vh, 12px);
    height: min(1.3vh, 12px);
  }
}

@media (max-height: 500px) {
  input[type="range"] {
    height: min(0.6vh, 3px);
  }
  
  input[type="range"]::-webkit-slider-thumb {
    width: min(1.1vh, 10px);
    height: min(1.1vh, 10px);
  }
}

@media (max-height: 400px) {
  .volume-control {
    max-width: min(75vw, 200px);
  }
  
  input[type="range"] {
    height: min(0.5vh, 2px);
  }
}
</style>