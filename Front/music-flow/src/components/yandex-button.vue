<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoading = ref(true);
const error = ref(null);
const isSdkLoaded = ref(false);

onMounted(() => {
  initYandexAuth();
});

const initYandexAuth = () => {
  // Проверяем, может SDK уже загружен
  if (window.YaAuthSuggest) {
    initYandexButton();
    return;
  }

  const script = document.createElement('script');
  script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js';
  script.async = true;
  
  script.onload = () => {
    if (!window.YaAuthSuggest) {
      error.value = 'Yandex SDK не загрузился';
      return;
    }
    initYandexButton();
  };

  script.onerror = () => {
    error.value = 'Не удалось загрузить Yandex SDK';
    isLoading.value = false;
  };

  document.head.appendChild(script);
};

const initYandexButton = () => {
  try {
    window.YaAuthSuggest.init(
      {
        client_id: import.meta.env.VITE_CLIENT_ID,
        response_type: 'token',
        redirect_uri: `${window.location.origin}/yandex-callback`,
      },
      `${window.location.origin}/yandex-callback`,
      {
        view: 'button',
        parentId: 'yandex-auth-button',
        buttonView: 'additional',
        buttonTheme: 'dark',
        buttonSize: 'm',
        buttonBorderRadius: 22,
      }
    )
    .then(({ handler }) => handler())
    .then(data => {
      console.log('Yandex auth success:', data);
      window.postMessage({
        type: 'yandex_auth_success',
        token: data.access_token
      }, window.location.origin);
    })
    .catch(err => {
      error.value = `Ошибка авторизации: ${err.message}`;
      console.error('Yandex auth error:', err);
    })
    .finally(() => {
      isLoading.value = false;
    });
  } catch (e) {
    error.value = `Ошибка инициализации: ${e.message}`;
    console.error('Yandex init error:', e);
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="yandex-auth-wrapper">
    <div v-if="isLoading" class="loading-state">
      Загрузка кнопки Yandex ID...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div id="yandex-auth-button" class="yandex-button-container"></div>
  </div>
</template>

<style scoped>
.yandex-auth-wrapper {
  margin: 20px auto;
  min-height: 42px;
  position: relative;
}

.yandex-button-container {
  display: flex;
  justify-content: center;
}

.loading-state {
  text-align: center;
  color: #999;
}

.error-message {
  color: #ff3333;
  font-size: 14px;
  text-align: center;
}
</style>