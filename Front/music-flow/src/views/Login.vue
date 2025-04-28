<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'
import LogoInLogin from '@/assets/logo-in-login.vue'
import AuthForm from '@/components/auth-form.vue'

const isLogin = ref(true)
const formContainer = ref(null)

function toggleForm() {
  // Ждём 100ms чтобы кнопка Яндекс успела исчезнуть
  setTimeout(() => {
    gsap.to(formContainer.value, {
      duration: 0.3,
      scale: 0.95 ,
      opacity: 0.8,
      ease: 'power2.in',
      onComplete: () => {
        isLogin.value = !isLogin.value
        gsap.fromTo(formContainer.value,
          { scale: 1.05, opacity: 0.8 },
          { 
            duration: 0.4,
            scale: 1,
            opacity: 1,
            ease: 'power2.out'
          }
        )
      }
    })
  }, 100)
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
      </div>
    </div>
  </div>
</template>