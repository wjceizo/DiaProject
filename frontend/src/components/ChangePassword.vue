<template>
        <form @submit.prevent="changePassword">
                <div class="form-group">
                        <label for="password">原密码</label>
                        <input id="password" v-model="form.password" type="password" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="newpassword">新密码</label>
                        <input id="new password" v-model="form.newpassword" type="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary mt-3">修改密码</button>
        </form>
</template>
      
<script>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
        setup() {
                const store = useStore();
                const router = useRouter();
                const form = reactive({
                        password: '',
                        newpassword: '',
                });

                const changePassword = async () => {
                        try {
                                await axios.put('/api/auth/update/password', form, {
                                        headers: { Authorization: `Bearer ${store.state.accessToken}` },
                                });
                                form.password = '';
                                form.newpassword = '';
                                alert('修改密码成功, 请重新登录');
                                handleLogout(); // Call handleLogout after password change
                        } catch (error) {
                                console.error('修改密码失败:', error);
                        }
                };

                const handleLogout = () => {
                        store.dispatch('logout'); // Dispatch the logout action to clear the session
                        router.push('/');
                };

                return {
                        form,
                        changePassword,
                };
        },
};
</script>
      