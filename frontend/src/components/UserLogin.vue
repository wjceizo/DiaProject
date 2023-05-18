<template>
        <form @submit.prevent="login">
                <div class="form-group">
                        <label for="username">用户名</label>
                        <input id="username" v-model="form.username" type="text" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="password">密码</label>
                        <input id="password" v-model="form.password" type="password" class="form-control" required>
                </div>
                <div class="form-group">
                        <button type="submit" class="btn btn-primary">登录</button>
                </div>
                <div v-if="message" class="alert alert-danger">{{ message }}</div>
        </form>
</template>
      

<script>
import { reactive, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
        setup() {
                const store = useStore();
                const router = useRouter();

                const form = reactive({
                        username: '',
                        password: '',
                });
                const message = ref('');

                const login = async () => {
                        try {
                                const response = await axios.post('/api/auth/login', form);

                                if (response.status === 200) {
                                        store.commit('setAccessToken', response.data.access_token);
                                        store.commit('setRefreshToken', response.data.refresh_token);
                                        message.value = '登录成功';
                                        router.replace('/');
                                } else {
                                        if (response.status === 403) {
                                                message.value = '用户名不存在或密码错误';
                                        } else {
                                                message.value = '用户名不存在或密码错误';
                                        }
                                }
                        } catch (error) {
                                console.error('登录失败:', error);
                                message.value = '用户名不存在或密码错误';
                        }
                };
                return {
                        form,
                        message,
                        login,
                };
        },
};
</script>
