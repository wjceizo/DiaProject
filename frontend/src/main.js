import { createApp } from 'vue';
import App from './App.vue';
import router from './router'
import store from './store';

router.beforeEach((to, from, next) => {
  const isAuthenticated = (store.getters.accessToken !== '');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ path: '/' });
  } else if (to.path === '/' && isAuthenticated) {
    next({ path: '/record-audio' });
  } else {
    next();
  }
});

createApp(App)
  .use(store)
  .use(router)
  .mount('#app');
