<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  // Парсим токен из URL hash
  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);
  const accessToken = params.get('access_token');

  if (accessToken) {
    // Отправляем токен в родительское окно
    if (window.opener) {
      window.opener.postMessage({
        type: 'yandex_auth_success',
        token: accessToken
      }, window.location.origin);
    }
    
    // Сохраняем токен и закрываем popup
    localStorage.setItem('yandex_token', accessToken);
    window.close();
  } else {
    router.push('/login');
  }
});
</script>

<template>
  <div class="callback-container">
    <p>Завершение авторизации...</p>
  </div>
</template>