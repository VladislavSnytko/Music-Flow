<template>
  <form class="auth-form" @submit.prevent="handleSubmit">
    <h2 class="welcome-title">С возвращением!</h2>

    <div class="form-fields">
      <input v-model="email" type="email" placeholder="Email" class="auth-input" />
      <input v-model="password" type="password" placeholder="Пароль" class="auth-input" />
    </div>

    <div class="form-button">
      <Button text="Войти" textSize="37px" />
    </div>

    <!-- <div id="yandex-login" class="yandex-id"></div> -->
    <YandexButton />
    <div class="login-bottom-text cursor-pointer" @click="toggleForm">
        Регистрация
    </div>
  </form>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import Button from '@/components/Button.vue'
import YandexButton from './yandex-button.vue';

const email = ref('')
const password = ref('')
const emit = defineEmits(['toggle'])

function handleSubmit() {
  console.log('Авторизация:', email.value, password.value)
}

function toggleForm() {
  emit('toggle')
}
</script>


<style>
/* .auth-form-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
} */
</style>