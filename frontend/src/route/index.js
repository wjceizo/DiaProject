import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  // {
  //   path: '/',
  //   name: 'UserRegistration',
  //   component: () => import("../components/UserRegistration.vue")
  // },
  {
    path: '/record-complete',
    name: 'RecordComplete',
    component: () => import("../components/RecordComplete.vue")
  }
]

const router = createRouter ({
  history: createWebHistory("/"),
  routes: routes,
})

export default router;
