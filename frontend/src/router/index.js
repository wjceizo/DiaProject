import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("../views/HomeView.vue") },
    {
      path: "/questionnaire",
      component: () => import("../views/QuestionnaireView.vue"),
    },
    {
      path: "/auto-registration",
      component: () => import("../components/AutoRegistration.vue"),
    },
    {
      path: "/record-audio",
      component: () => import("../components/RecordAudio.vue"),
    },
    {
      path: "/record-complete",
      component: () => import("../components/RecordComplete.vue"),
    },

    {
      path: "/method-introduction",
      component: () => import("../views/MethodView.vue"),
    },
    {
      path: "/map",
      component: () => import("../views/MapView.vue"),
      beforeEnter: (to, from, next) => {
        const accessToken = localStorage.getItem("accessToken"); // 从本地存储中获取accessToken，你可以根据实际情况修改存储和获取accessToken的逻辑
        if (accessToken) {
          next(); // 允许用户访问
        } else {
          next("/login"); // 重定向到登录页面或其他适当的处理方式
        }
      },
    },
    { path: "/about", component: () => import("../views/AboutView.vue") },
    { path: "/profile", component: () => import("../views/ProfileView.vue") },
    { path: "/login", component: () => import("../components/UserLogin.vue") },
    {
      path: "/register",
      component: () => import("../components/UserRegistrate.vue"),
    },
    {
      path: "/change-password",
      component: () => import("../components/ChangePassword.vue"),
    }
  ],
});

export default router;
