<template>
  <form class="auth-form" @submit.prevent="handleSubmit">
    <transition name="fade">
      <h2 key="title" class="welcome-title">
        Добро пожаловать!
      </h2>
    </transition>

    <div class="form-fields">
      <transition name="fade">
        <input
          v-model="username"
          type="text"
          placeholder="Имя пользователя"
          class="auth-input"
          key="username"
        />
      </transition>
      <input v-model="email" type="email" placeholder="Электронная почта" class="auth-input" />
      <input v-model="password" type="password" placeholder="Пароль" class="auth-input" />
    </div>

    <div class="form-button">
      <Button text="Зарегистрироваться" textSize="37px" />
    </div>

    <!-- Добавляем компонент кнопки Яндекса -->
    <!-- <YandexButton /> -->

    <div class="login-bottom-text cursor-pointer" @click="toggleForm">
      Уже есть аккаунт? Войти
    </div>
  </form>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import Button from '@/components/Button.vue'
import YandexButton from './yandex-button.vue'; // импортируем компонент кнопки Яндекса
const username = ref('')
const email = ref('')
const password = ref('')

function handleSubmit() {
  console.log('Регистрация:', username.value, email.value, password.value)
}

const emit = defineEmits(['toggle']) // теперь используем emit

function toggleForm() {
  emit('toggle') // теперь используем emit
}
</script>

<style scoped>
/* .auth-form-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
} */
</style>
