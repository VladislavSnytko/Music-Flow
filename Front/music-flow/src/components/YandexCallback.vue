<script setup>
import { onMounted } from 'vue';

const loadYandexSdk = () => {
  return new Promise((resolve, reject) => {
    if (window.YaSendSuggestToken) {
      resolve(); // SDK уже загружен
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-token-with-polyfills-latest.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Не удалось загрузить Yandex SDK'));
    document.head.appendChild(script);
  });
};

onMounted(async () => {
  console.log('YandexCallback mounted. Parsing token...');

  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);
  const token = params.get('access_token');
  console.log('YandexCallback — token:', token);

  if (!token) {
    console.error('Токен не найден в URL');
    return;
  }

  // Сохраняем токен (по желанию)
  localStorage.setItem('yandex_token', token);

  try {
    await loadYandexSdk();
    console.log('Yandex SDK загружен. Вызываем YaSendSuggestToken...');

    // Передаём токен родителю (origin должен быть точным)
    window.YaSendSuggestToken('https://localhost', {
      token: token
    });

    console.log('YaSendSuggestToken отправлен.');
  } catch (e) {
    console.error('Ошибка при работе с Yandex SDK:', e);
  }

  // Закрываем popup (если открыт в новом окне)
  if (window.opener) {
    setTimeout(() => {
      window.close();
    }, 500); // даём чуть-чуть времени на передачу
  }
});
</script>

<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <p>Авторизация через Яндекс... Подождите</p>
  </div>
</template>

<style scoped>
p {
  font-family: sans-serif;
  color: #333;
  font-size: 1.1rem;
}
</style>
