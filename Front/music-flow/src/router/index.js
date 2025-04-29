// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/yandex-callback',
    name: 'YandexCallback',
    component: () => import('@/components/YandexCallback.vue')
  },
  // router/index.js
{
  path: '/main',
  name: 'Main',
  component: () => import('../views/Main.vue'),
  meta: { requiresAuth: true }
}

]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
