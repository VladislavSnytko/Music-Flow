<template>
    <div id="yandex-login" class="yandex-id"></div>
</template>
  
  <script setup>
  import { onMounted } from 'vue';
  
  onMounted(() => {
    const script = document.createElement('script');
    script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js';
    script.async = true;
    script.onload = () => {
      window.YaAuthSuggest.init({
        client_id: import.meta.env.VITE_CLIENT_ID,
        response_type: 'code',
        redirect_uri: 'https://fjxp38df-8000.euw.devtunnels.ms/callback',
      }, 'http://localhost:5173', {
        view: 'button',
        parentId: 'yandex-login',
        buttonView: 'additional',
        buttonTheme: 'dark',
        buttonSize: 'l',
        buttonBorderRadius: 30,
      })
      .then(result => {
        if (!result?.handler) throw new Error('Яндекс не вернул handler()');
        return result.handler();
      })
      .then(data => {
        console.log('Данные:', data);
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
    };
    document.head.appendChild(script);
  });
  </script>
  
  <style scoped>
.yandex-id {
  padding-top: 15px;   /* Отступ сверху */
  padding-bottom: 20px; /* Отступ снизу */
}
  </style>