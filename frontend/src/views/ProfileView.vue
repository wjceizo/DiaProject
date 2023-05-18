<template>
  <div>
    <h2>用户信息</h2>
    <p>用户名: {{ userInfo.username }}</p>
    <p>电子邮箱: {{ userInfo.email }}</p>
    <p>姓名: {{ userInfo.name }}</p>
    <p>性别: {{ userInfo.sex }}</p>
    <p>地点: {{ userInfo.location }}</p>
    <p>工作: {{ userInfo.work }}</p>

    <button type="btn-submit" class="btn btn-primary" @click="isEditing = true; isChangePassVisible = false">修改个人信息</button>

    <form v-if="isEditing" @submit.prevent="updateInfo">
      <div class="form-group">
        <label for="name">姓名</label>
        <input id="name" v-model="form.name" type="text" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="email">电子邮箱</label>
        <input id="email" v-model="form.email" type="email" class="form-control" required>
      </div>
      <button type="btn-submit" class="btn btn-primary">提交</button>
    </form>
    <button id="btn-submit" class="btn btn-primary" @click="changePass" v-if="isChangePassVisible">更改密码</button>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const isEditing = ref(false);
    const isChangePassVisible = ref(true);
    const form = reactive({
      name: '',
      email: '',
      lang: null,
      location: null,
    });
    const userInfo = reactive({
      username: '',
      email: '',
      name: '',
      sex: '',
      location: '',
      work: '',
    });

    onMounted(async () => {
      try {
        const response = await axios.get('/api/auth/info', {
          headers: { Authorization: `Bearer ${store.state.accessToken}` },
        });
        Object.assign(userInfo, response.data);
        Object.assign(form, response.data);
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    });

    const updateInfo = async () => {
      try {
        await axios.put('/api/auth/update/info', {
          name: form.name,
          email: form.email,
          lang:null,
          location: null,
        }, {
          headers: { Authorization: `Bearer ${store.state.accessToken}` },
        });
        Object.assign(userInfo, form);
        isEditing.value = false;
        isChangePassVisible.value = true; // Show the "Change Password" button again
      } catch (error) {
        console.error('更新用户信息失败:', error);
      }
    };

    return {
      isEditing,
      form,
      userInfo,
      updateInfo,
      isChangePassVisible,
    };
  },
  methods: {
    changePass() {
      this.$router.replace('/change-password');
    },
  }
};
</script>
