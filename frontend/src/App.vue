<template>
  <div id="app" class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light px-2">
      <div class="navbar-nav me-auto">
        <router-link class="nav-link" to="/">主页</router-link>
        <router-link class="nav-link" to="/questionnaire">调查问卷</router-link>
        <router-link class="nav-link" to="/method-introduction">方法介绍</router-link>
        <router-link class="nav-link" to="/map" v-if="accessToken">方言地图</router-link>
        <router-link class="nav-link" to="/about">关于</router-link>
      </div>
      <div class="navbar-nav" v-if="!accessToken">
        <router-link class="btn btn-primary nav-link mx-2" to="/register">注册</router-link>
        <router-link class="btn btn-secondary nav-link" to="/login">登录</router-link>
      </div>
      <div class="navbar-nav" v-else>
        <router-link class="nav-link" to="/profile">个人信息</router-link>
        <button class="btn btn-danger nav-link mx-2" @click="handleLogout">注销</button>
      </div>
    </nav>
    <router-view></router-view>
  </div>
  <div>

  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import { mapActions, mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['accessToken'])
  },
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      this.logout(); // Dispatch the logout action to clear the session
      this.$router.push('/');
    }
  },
  // mounted() {
  //   this.fetchProfile()
  // }
}
</script>
