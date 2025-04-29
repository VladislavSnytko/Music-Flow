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


// let matches = fetch("https://uniform-connections-scroll-cloud.trycloudflare.com/auth/sign-in?nickname=ch1l&hashed_password=5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5", {method:"GET"});

// async function getCookie(name) {
//                 let matches = await fetch("/https://uniform-connections-scroll-cloud.trycloudflare.com/get_cookie", {method:GET});
//                 return await matches.json();
//             }