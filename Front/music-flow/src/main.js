import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './main.css'
import { gsap } from "gsap/dist/gsap";
import { Flip } from "gsap/dist/Flip";


gsap.registerPlugin(Flip);

const app = createApp(App)
app.use(router)
app.mount('#app')
