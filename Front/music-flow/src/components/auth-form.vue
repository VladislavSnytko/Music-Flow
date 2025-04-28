<template>
    <form class="auth-form" @submit.prevent="handleSubmit">
      <h2 class="welcome-title">
        {{ isLogin ? 'С возвращением!' : 'Добро пожаловать!' }}
      </h2>
  
      <div class="form-fields">
        <input
          v-if="!isLogin"
          v-model="username"
          type="text"
          placeholder="Имя пользователя"
          class="auth-input"
          key="username"
        />
        <input v-model="email" type="email" :placeholder="isLogin ? 'Email' : 'Электронная почта'" class="auth-input" />
        <input v-model="password" type="password" placeholder="Пароль" class="auth-input" />
      </div>
  
      <div class="form-button">
        <Button :text="isLogin ? 'Войти' : 'Зарегистрироваться'" textSize="37px" />
      </div>
  
      <!-- <transition name="fast-fade" mode="out-in"> -->
      <YandexButton v-show="isLogin" :key="'yandex-btn'" />
    <!-- </transition> -->
      
      <div class="login-bottom-text cursor-pointer" @click="$emit('toggle')">
        {{ isLogin ? 'Регистрация' : 'Уже есть аккаунт? Войти' }}
      </div>
    </form>
  </template>
  <script setup>
  import { ref, watch } from 'vue'
  import Button from '@/components/Button.vue'
  import YandexButton from './yandex-button.vue'
  
  const props = defineProps({
    isLogin: {
      type: Boolean,
      default: true
    }
  })
  
  const showYandexBtn = ref(true)
  const username = ref('')
  const email = ref('')
  const password = ref('')
  
  watch(() => props.isLogin, (newVal) => {
    if (!newVal) {
      // Сначала скрываем кнопку Яндекс ID
      showYandexBtn.value = false
    } else {
      // Показываем с небольшой задержкой
      setTimeout(() => {
        showYandexBtn.value = true
      }, 150)
    }
  })
  </script>
  
  <!-- <style scoped>
  /* Быстрое исчезновение для Яндекс кнопки
  .fast-fade-enter-active {
    transition: all 0.1s ease-out;
  }
  .fast-fade-leave-active {
    transition: all 0.1s ease-in;
  }
  .fast-fade-enter-from,
  .fast-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  } */
  
  /* Медленное для основного контента */
  /* .fade-enter-active,
  .fade-leave-active {
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  } */
  </style> -->