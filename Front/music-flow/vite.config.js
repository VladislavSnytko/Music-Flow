// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import path from 'path';
// import mkcert from 'vite-plugin-mkcert';

// export default defineConfig({
//   plugins: [vue(), mkcert()],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//   },
//   server: {
//     https: true,
//     host: 'localhost',
//     port: 443,
//     http2: false, // Отключаем HTTP/2
//     headers: {
//       'Content-Security-Policy': `
//         default-src 'self';
//         script-src 'self' https://yastatic.net https://mc.yandex.ru;
//         style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
//         style-src-elem 'self' 'unsafe-inline' https://fonts.googleapis.com;
//         font-src 'self' https://fonts.gstatic.com https://yastatic.net;
//         frame-src https://*.yandex.ru;
//         connect-src *;
//         img-src * data:;
//       `.replace(/\s{2,}/g, ' ').trim(),
//     },
//   },
  
// });










// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import path from 'path';
// import mkcert from 'vite-plugin-mkcert';

// export default defineConfig({
//   plugins: [
//     vue(),
//     mkcert() // Генерирует доверенные локальные сертификаты
//   ],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//   },
//   server: {
//     https: true,
//     host: 'localhost',
//     port: 443,
//     strictPort: true, // Запрещаем переключение на другой порт
//     hmr: {
//       protocol: 'wss', // WebSocket для HMR через HTTPS
//       host: 'localhost'
//     },
//     cors: true, // Разрешаем CORS для разработки
//     headers: {
//       'Content-Security-Policy': `
//         default-src 'self';
//         script-src 'self' 'unsafe-inline' https://yastatic.net https://mc.yandex.ru;
//         style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
//         img-src 'self' data: https://*.yandex.net https://yastatic.net;
//         connect-src 'self' https://*.yandex.ru https://*.yandex.net;
//         frame-src 'self' https://oauth.yandex.ru;
//       `.replace(/\n/g, '').trim()
//     }
//   },
//   optimizeDeps: {
//     include: [
//       '@yandex/oauth' // Если используете какие-то Яндекс пакеты
//     ]
//   }
// });






// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import path from 'path';
// import mkcert from 'vite-plugin-mkcert';

// export default defineConfig({
//   plugins: [vue(), mkcert()],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//   },
//   server: {
//     https: true,
//     host: 'localhost',
//     port: 443,
//     strictPort: true,
//     hmr: { protocol: 'wss' },
//     headers: {
//       'Content-Security-Policy': `
//         default-src 'self' https://yastatic.net https://passport.yandex.ru;
//         script-src 'self' 'unsafe-inline' 'unsafe-eval' https://yastatic.net https://mc.yandex.ru https://passport.yandex.ru;
//         style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
//         font-src 'self' https://fonts.gstatic.com https://yastatic.net;
//         media-src 'self' https://*.trycloudflare.com;
//         img-src * data:;
//         frame-src https://*.yandex.ru https://passport.yandex.ru;
//         connect-src *;
//       `.replace(/\s{2,}/g, ' ').trim()
//     }
    
//   }
// });






// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import path from 'path';
// import mkcert from 'vite-plugin-mkcert';



// export default defineConfig({

//   plugins: [vue(), mkcert()],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//   },
//   server: {
//     // proxy: {
//     //   '/api': 'https://localhost:8000', // ваш бекенд
//     // },
//     port: 443,
//     allowedHosts: [
//       // 'hh-statewide-calcium-surely.trycloudflare.com',
//       //  'https://pe-science-determining-hobby.trycloudflare.com'// Разрешаем этот домен (бек)
//       'fs-ag-cage-hold.trycloudflare.com',
//       DOMAIN,
//     ],
//     https: true,
//     // host: 'localhost',
//     // port: 443,
//     strictPort: true,
//     hmr: { protocol: 'wss' },
    // headers: {
    //   'Content-Security-Policy': `
    //     default-src 'self' https://yastatic.net https://passport.yandex.ru;
    //     script-src 'self' 'unsafe-inline' 'unsafe-eval' https://yastatic.net https://mc.yandex.ru https://passport.yandex.ru;
    //     style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    //     font-src 'self' https://fonts.gstatic.com https://yastatic.net;
    //     media-src 'self' https://*.trycloudflare.com https://bottle-deaths-guestbook-kernel.trycloudflare.com;
    //     img-src * data:;
    //     frame-src https://*.yandex.ru https://passport.yandex.ru;
    //     connect-src *;
    //   `.replace(/\s{2,}/g, ' ').trim()
    // }
    
//   }
// });


import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import mkcert from 'vite-plugin-mkcert';

export default defineConfig(({ mode }) => {
  // Загружаем переменные окружения с учётом текущего режима (например, 'development')
  const env = loadEnv(mode, process.cwd());

  const DOMAIN = env.VITE_DOMAIN;

  return {
    plugins: [vue(), mkcert()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 443,
      allowedHosts: [
        'besides-instrument-feeling-conf.trycloudflare.com',
        DOMAIN,
      ],
      https: true,
      strictPort: true,
      hmr: { protocol: 'wss' },
      headers: {
        'Content-Security-Policy': `
          default-src 'self' https://yastatic.net https://passport.yandex.ru;
          script-src 'self' 'unsafe-inline' 'unsafe-eval' https://yastatic.net https://mc.yandex.ru https://passport.yandex.ru;
          style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
          font-src 'self' https://fonts.gstatic.com https://yastatic.net;
          media-src 'self' https://*.trycloudflare.com https://bottle-deaths-guestbook-kernel.trycloudflare.com;
          img-src * data:;
          frame-src https://*.yandex.ru https://passport.yandex.ru;
          connect-src *;
        `.replace(/\s{2,}/g, ' ').trim()
      }
    }
  };
});
