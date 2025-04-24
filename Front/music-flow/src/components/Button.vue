<template>
    <button class="button font-nunito font-semibold" :style="{ fontSize: textSize }">
      <span class="button-text">
        <!-- Белый слой -->
        <span class="text-white-layer">{{ text }}</span>
        <!-- Градиентный слой -->
        <span class="text-gradient-layer">{{ text }}</span>
      </span>
    </button>
  </template>
  
  
  <script setup>
  
  const props = defineProps({
    text: {
      type: String,
      default: 'Приступить'
    },
    textSize: {
      type: String,
      default: '20px'
    }
  })
  </script>
  
  <style scoped>
/* Стили для кнопки */
.button {
  @apply flex items-center justify-center gap-2
         bg-[#2EA48C]
         rounded-full
         shadow-[0px_0px_40px_5px_rgba(255,255,255,0.2)];
  padding: 0.25em 1em;  
  transition:
    background-color 0.5s cubic-bezier(0.4,0,0.2,1),
    box-shadow      0.5s cubic-bezier(0.4,0,0.2,1);
}

.button:hover {
  background-color: #296456;
  box-shadow: 0 0 40px 5px rgba(255,255,255,0.2);
}

/* Обёртка для текста, чтобы наложить слои */
.button-text {
  position: relative;
  display: inline-block;
}

/* Общие свойства для обоих слоёв */
.button-text span {
  display: block;
  transition: opacity 0.5s cubic-bezier(0.4,0,0.2,1);
}

/* Белый слой */
.text-white-layer {
  opacity: 1;
  color: white;
}

/* Градиентный слой (скрыт по умолчанию) */
.text-gradient-layer {
  position: absolute;
  top: 0; left: 0;
  opacity: 0;
  background-image: linear-gradient(90deg, #1fdeb1, #e45cfc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* При ховере — кроссфейд */
.button:hover .text-white-layer {
  opacity: 0;
}
.button:hover .text-gradient-layer {
  opacity: 1;
}

  </style>
  