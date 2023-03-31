// import { createApp } from 'vue';
// import App from './App.vue';
// import store from './store';

// createApp(App).use(store).mount('#app');

import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import { createRouter, createWebHistory } from 'vue-router';
// import UserRegistration from './components/UserRegistration.vue';
import RecordComplete from './components/RecordComplete.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // { path: '/', component: UserRegistration },
    { path: '/record-complete', component: RecordComplete },

  ]
});

createApp(App)
  .use(store)
  .use(router)
  .mount('#app');
