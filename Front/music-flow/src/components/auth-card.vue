<template>
    <form class="auth-form" @submit.prevent="handleSubmit">
      <h2 class="welcome-title">С возвращением!</h2>
  
      <div class="form-fields">
        <input v-model="email" type="email" placeholder="Email" class="auth-input" />
        <input v-model="password" type="password" placeholder="Пароль" class="auth-input" />
      </div>
  
      
      <div class="form-button">
        <Button class="auth-button" text="Войти" textSize="37px" />
      </div>
  
      <!-- Контейнер для Яндекс кнопки -->
      <div id="yandex-login" class="yandex-id" />
  
      <div class="login-bottom-text">Регистрация</div>
    </form>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  import Button from '@/components/Button.vue'
  
  const email = ref('')
  const password = ref('')
  
  function handleSubmit() {
    console.log('Авторизация:', email.value, password.value)
  }
  
  onMounted(() => {
    const script = document.createElement('script')
    script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js'
    script.async = true
    script.onload = () => {
      window.YaAuthSuggest.init({
        client_id: 'c46f0c53093440c39f12eff95a9f2f93',
        response_type: 'token',
        redirect_uri: 'https://examplesite.com/suggest/token'
      },
      'https://examplesite.com',
      {
        view: 'button',
        parentId: 'yandex-login',
        buttonView: 'additional',
        buttonTheme: 'dark',
        buttonSize: 'm',
        buttonBorderRadius: 30
      })
      .then(res => res.handler())
      .then(data => console.log('Токен получен:', data))
      .catch(err => console.error('Ошибка авторизации Яндекс:', err))
    }
  
    document.head.appendChild(script)
  })
  </script>
  