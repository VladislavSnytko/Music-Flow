<script setup>
import { ref, onMounted } from 'vue';
import { gsap } from 'gsap';
import { useRouter } from 'vue-router';
import LogoInLogin from '@/assets/logo-in-login.vue';
import AuthForm from '@/components/auth-form.vue';
import YandexButton from '@/components/yandex-button.vue';

const router = useRouter();
const isLogin = ref(true);
const formContainer = ref(null);





// onMounted(() => {
//   console.log('Ожидаемый origin в родителе:', window.location.origin);
//   const handleYandexAuth = async (token) => {
//     try {
//       console.log('Получен токен от Яндекс:', token);
//       localStorage.setItem('yandex_token', token);
      
//       const response = await fetch(
//         `https://never-mrs-controller-seal.trycloudflare.com/check_token?token=${encodeURIComponent(token)}`, 
//         {
//           method: 'GET',
//           headers: {
//             'Content-Type': 'application/json',
//           }
//         }
//       );
      
//       if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
//       const result = await response.json();
//       console.log('Ответ сервера:', result);
      
//       if (result.success) {
//         router.push('/Main');
//       } else {
//         console.error('Сервер отклонил токен:', result.message);
//         router.push('/login?error=invalid_token');
//       }
//     } catch (error) {
//       console.error('Ошибка при обработке токена:', error);
//       router.push('/login?error=auth_failed');
//     }
//   };

//   // Обработчик сообщений
//   const messageHandler = (event) => {
//     // */ Принимаем сообщения только от нашего origin и от Яндекс callback
//     const allowedOrigins = [
//       window.location.origin,
//       'https://autofill.yandex.ru',
//       'https://oauth.yandex.ru'
//     ];
    
//     if (!allowedOrigins.includes(event.origin)) {
//       console.log('Игнорируем сообщение от origin:', event.origin);
//       return;
//     }
    
//     // Отладочный вывод всех сообщений
//     console.log('Получено сообщение:', event.data);
    
//     // Обрабатываем только сообщения с токеном
//     if (event.data.type === 'yandex_auth_success') {
//       handleYandexAuth(event.data.token);
//     }
//   };

//   window.addEventListener('message', messageHandler);
  
//   return () => {
//     window.removeEventListener('message', messageHandler);
//   };
// });


onMounted(() => {
  window.addEventListener('message', async (event) => {
    // Проверяем origin сообщения для безопасности
    if (event.origin !== window.location.origin) return;
    
    if (event.data.type === 'yandex_auth_success') {
      try {
        const token = event.data.token;
        console.log('Получен токен от Яндекс:', token);
        
        // 1. Сохраняем токен в localStorage
        localStorage.setItem('yandex_token', token);
        
        // 2. Отправляем токен на сервер для валидации
        const response = await fetch(
          `https://hardly-jane-time-functions.trycloudflare.com/check_token?token=${encodeURIComponent(token)}`, 
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            }
          }
        );
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Ответ сервера:', result);
        
        // 3. Проверяем ответ сервера и перенаправляем
        if (result.success) {
          router.push('/Main');
        } else {
          console.error('Сервер отклонил токен:', result.message);
          router.push('/login?error=invalid_token');
        }
        
      } catch (error) {
        console.error('Ошибка при обработке токена:', error);
        router.push('/login?error=auth_failed');
      }
    }
  });
});

function toggleForm() {
  setTimeout(() => {
    gsap.to(formContainer.value, {
      duration: 0.3,
      scale: 0.95,
      opacity: 0.8,
      ease: 'power2.in',
      onComplete: () => {
        isLogin.value = !isLogin.value;
        gsap.fromTo(formContainer.value,
          { scale: 1.05, opacity: 0.8 },
          { 
            duration: 0.4,
            scale: 1,
            opacity: 1,
            ease: 'power2.out'
          }
        );
      }
    });
  }, 100);
}
</script>

<template>
  <div class="login-container">
    <div class="logo-section">
      <LogoInLogin />
    </div>
    <div class="form-section">
      <div ref="formContainer">
        <AuthForm :isLogin="isLogin" @toggle="toggleForm" />
        <!-- <YandexButton></YandexButton> -->
        <!-- <teleport to="body">
            <div id="yandex-auth-button-global"></div>
        </teleport> -->
      </div>
    </div>
  </div>
</template>