import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import store from './store'
import router from './router'
// import 'bootstrap/dist/css/bootstrap.css'

createApp(App).use(store).use(store).use(router).mount('#app')
