<!-- <script setup>
import LogoInLogin from '@/components/logo-in-login.vue'
import AuthCard      from '@/components/auth-card.vue'

</script>

<template>
  <div class="login-container">
    <div class="logo-section">
      <LogoInLogin />
    </div>
    <div class="form-section">
      <AuthCard />
    </div>
  </div>
</template> -->


<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from "gsap/dist/gsap"
import { Flip } from 'gsap/Flip';
import LogoInLogin from '@/components/logo-in-login.vue'
import AuthCard from '@/components/auth-card.vue'
import RegistrationCard from '@/components/registration-card.vue'

gsap.registerPlugin(Flip)
import { animateFormTransition } from '@/animations/animateFormTransition'

const currentForm = ref('login')
const authCardRef = ref(null)
const regCardRef = ref(null)

const toggleForm = (type) => {
  if (currentForm.value === type) return

  const current = currentForm.value === 'login' ? authCardRef.value.$el : regCardRef.value.$el
  const next = type === 'login' ? authCardRef.value.$el : regCardRef.value.$el

  animateFormTransition(current, next, () => {
    currentForm.value = type
  })
}
// Инициализация позиций после монтирования

onMounted(() => {
  const buttons = document.querySelectorAll('.auth-button, .register-button');
  if (buttons.length) {
    gsap.set(buttons, { scale: 1 });
  }
})
</script>

<template>
  <div class="login-container">
    <div class="logo-section">
      <LogoInLogin />
    </div>
    
    <div class="form-section" ref="formContainer">
      <AuthCard 
        v-show="currentForm === 'login'"
        ref="authCardRef"
        @toggle="toggleForm('register')"
      />
      <RegistrationCard 
        v-show="currentForm === 'register'"
        ref="regCardRef"
        @toggle="toggleForm('login')"
      />
    </div>
  </div>
</template>