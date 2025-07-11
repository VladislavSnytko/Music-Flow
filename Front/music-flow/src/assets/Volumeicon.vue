<template>
  <button @click="toggleMute" class="volume-icon">
    <!-- Иконка "звук выключен" -->
    <svg
      v-if="volume === 0"
      width="30"
      height="30"
      viewBox="0 0 30 30"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      
    >
      <path
        d="M20.1176 16.6511L26 10.3489M26 16.6511L20.1176 10.3489M5.41176 8.77339H2.47059C2.08056 8.77339 1.70651 8.93939 1.43073 9.23486C1.15494 9.53033 1 9.93107 1 10.3489V16.6511C1 17.0689 1.15494 17.4697 1.43073 17.7651C1.70651 18.0606 2.08056 18.2266 2.47059 18.2266H5.41176L10.5588 25.3165C10.6874 25.584 10.901 25.7934 11.161 25.9069C11.4211 26.0204 11.7104 26.0305 11.9768 25.9353C12.2432 25.8402 12.4691 25.6461 12.6136 25.3881C12.7581 25.1302 12.8117 24.8254 12.7647 24.5287V2.47125C12.8117 2.17465 12.7581 1.86982 12.6136 1.61186C12.4691 1.3539 12.2432 1.15982 11.9768 1.06468C11.7104 0.969546 11.4211 0.979632 11.161 1.09312C10.901 1.2066 10.6874 1.41601 10.5588 1.68349L5.41176 8.77339Z"
        stroke="white"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>

    
    <!-- Иконка "звук включен" -->
    <svg
      v-else
      width="30"
      height="30"
      viewBox="0 0 30 30"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M20.7143 19.8021C21.7345 19.0684 22.5625 18.1169 23.1328 17.023C23.7031 15.9291 24 14.723 24 13.5C24 12.277 23.7031 11.0709 23.1328 9.977C22.5625 8.88314 21.7345 7.93164 20.7143 7.19786M5.92857 8.77339H2.64286C2.20714 8.77339 1.78928 8.93939 1.48118 9.23486C1.17309 9.53033 1 9.93107 1 10.3489V16.6511C1 17.0689 1.17309 17.4697 1.48118 17.7651C1.78928 18.0606 2.20714 18.2266 2.64286 18.2266H5.92857L11.6786 25.3165C11.8222 25.584 12.0608 25.7934 12.3513 25.9069C12.6418 26.0204 12.9651 26.0305 13.2627 25.9353C13.5603 25.8402 13.8126 25.6461 13.974 25.3881C14.1354 25.1302 14.1953 24.8254 14.1429 24.5287V2.47125C14.1953 2.17465 14.1354 1.86982 13.974 1.61186C13.8126 1.3539 13.5603 1.15982 13.2627 1.06468C12.9651 0.969547 12.6418 0.979633 12.3513 1.09312C12.0608 1.20661 11.8222 1.41601 11.6786 1.68349L5.92857 8.77339Z"
        stroke="white"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </button>
</template>

<script>
export default {
  name: 'VolumeIcon',
  props: {
    volume: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      previousVolume: this.volume > 0 ? this.volume : 1,
    };
  },
  watch: {
    volume(newVolume) {
      if (newVolume > 0) {
        this.previousVolume = newVolume;
      }
    },
  },
  methods: {
    toggleMute() {
      const newVolume = this.volume === 0 ? this.previousVolume : 0;
      this.$emit('update:volume', newVolume);
    },
  },
};
</script>

<style scoped>
/* Основные стили компонента громкости */
.volume-control {
  display: flex;
  align-items: center;
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  z-index: 1000; /* Чтобы компонент был выше других элементов */
  gap: 10px; /* Расстояние между иконкой и слайдером */
}

/* Слайдер громкости */
input[type="range"] {
  width: 150px;
  margin: 0 10px;
  background: linear-gradient(to right, #00CED1, #008fee);
  height: 5px;
  border-radius: 5px;
  outline: none;
  -webkit-appearance: none;
  position: relative;
  z-index: 1;
}

/* Стилизация тумблера слайдера */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 15px;
  height: 15px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0; /* скрыт по умолчанию */
  transition: opacity 0.2s ease;
}

/* Показываем тумблер при наведении на слайдер */
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

/* Иконка громкости */
.volume-icon {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 1024px) {
  .volume-control {
    bottom: 4%;
    gap: 8px; /* Уменьшаем промежуток */
    transform: translateX(-50%);
  }

  input[type="range"] {
    width: 120px; /* Уменьшаем ширину слайдера */
  }

  .volume-icon {
    font-size: 18px; /* Уменьшаем размер иконки */
  }
}

@media (max-width: 768px) {
  .volume-control {
    bottom: 3%;
    gap: 6px;
  }

  input[type="range"] {
    width: 100px; /* Еще меньше для экрана 768px */
  }

  .volume-icon {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .volume-control {
    bottom: 2%;
    gap: 5px; /* Уменьшаем промежуток */
  }

  input[type="range"] {
    width: 80px; /* Уменьшаем ширину слайдера */
  }

  .volume-icon {
    font-size: 14px;
  }
}


</style>
