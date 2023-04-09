import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/record-complete',
    name: 'RecordComplete',
    component: () => import("../components/RecordComplete.vue")
  },
  {
    path: '/record-audio',
    name: 'RecordAudio',
    component: () => import("../components/RecordAudio.vue")
  },
  {
    path: '/user-registration',
    name: 'UserRegistration',
    component: () => import("../components/UserRegistration.vue")
  },
  {
    path: '/',
    name: 'UserInfo',
    component: () => import("../components/UserInfo.vue")
  }
]

const router = createRouter ({
  history: createWebHistory("/"),
  routes: routes,
})



export default router;
