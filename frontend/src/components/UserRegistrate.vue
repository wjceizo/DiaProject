<template>
        <form @submit.prevent="register" class="needs-validation" novalidate>
                <div class="form-group">
                        <label for="username">用户名</label>
                        <input id="username" v-model="form.username" type="text" class="form-control" required>
                        <div class="invalid-feedback">请填写用户名</div>
                </div>
                <div class="form-group">
                        <label for="email">电子邮箱</label>
                        <input id="email" v-model="form.email" type="email" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="password">密码</label>
                        <input id="password" v-model="form.password" type="password" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="confirm-password">确认密码</label>
                        <input id="confirm-password" v-model="confirmPassword" type="password" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="name">姓名</label>
                        <input id="name" v-model="form.name" type="text" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="work">工作</label>
                        <input id="work" v-model="form.work" type="text" class="form-control" required>
                </div>
                <div class="form-group">
                        <label for="sex">性别</label>
                        <select id="sex" v-model="form.sex" class="form-control" required>
                                <option value="" disabled>请选择你的性别</option>
                                <option value="男">男</option>
                                <option value="女">女</option>
                                <option value="我不确认">我不确认</option>
                        </select>
                </div>
                <div class="form-group">
                        <label for="province">省</label>
                        <select id="province" v-model="province" class="form-control" required>
                                <option value="" disabled>请选择你所在的省</option>
                                <option v-for="p in provinces" :key="p.id" :value="p">{{ p.name }}</option>
                        </select>
                        <div class="invalid-feedback">
                                Please select a province.
                        </div>
                </div>
                <div class="form-group">
                        <label for="city">市</label>
                        <select id="city" v-model="city" class="form-control" required>
                                <option value="" disabled>请选择你所在的市</option>
                                <option v-for="c in selectedProvinceCities" :key="c.name" :value="c">{{ c.name }}</option>
                        </select>
                        <div class="invalid-feedback">
                                Please select a city.
                        </div>
                </div>

                <div class="form-group">
                        <label for="county">区</label>
                        <select id="county" v-model="county" class="form-control" required>
                                <option value="" disabled>请选择你所在的区</option>
                                <option v-for="c in selectedCityCounties" :key="c" :value="c">{{ c.name }}</option>
                        </select>
                        <div class="invalid-feedback">
                                Please select a county.
                        </div>
                </div>

                <div class="form-group">
                        <label for="town">街道</label>
                        <select id="town" v-model="town" class="form-control" required :disabled="!hasTown">
                                <option value="" disabled>请选择你所在的街道</option>
                                <option v-for="t in selectedCountyTowns" :key="t.id" :value="t">{{ t.name }}</option>
                        </select>
                        <div class="invalid-feedback">
                                Please select a town.
                        </div>
                </div>
                <div class="form-group">
                        <label for="lang">方言</label>
                        <select id="lang" v-model="form.lang" class="form-control" required>
                                <option value="" disabled>请选择你的方言</option>
                                <option value="Jin">晋方言</option>
                                <option value="Wu">吴方言</option>
                                <option value="Min">闽方言</option>
                                <option value="Hakka">客家方言</option>
                                <option value="Cantonese">粤方言</option>
                                <option value="Xiang">湘方言</option>
                                <option value="Gan">赣方言</option>
                                <option value="Hui">徽方言</option>
                                <option value="Ping">平话</option>
                                <option value="Northeast">东北官话</option>
                                <option value="Beijing">北京官话</option>
                                <option value="Jilu">冀鲁官话</option>
                                <option value="JiaoLiao">胶辽官话</option>
                                <option value="CentralPlains">中原官话</option>
                                <option value="LanYin">兰银官话</option>
                                <option value="Jianghuai">江淮官话</option>
                                <option value="Southwest">西南官话</option>
                        </select>
                </div>
                <div v-if="message" class="alert alert-danger">{{ message }}</div>
                <div class="form-group">
                        <button type="submit" class="btn btn-primary">注册</button>
                </div>

        </form>
</template>
      



<script>
import { ref, reactive } from 'vue';
import axios from 'axios';

export default {
        data() {
                return {
                        form: reactive({
                                username: '',
                                password: '',
                                email: '',
                                name: '',
                                lang: '',
                                sex: '',
                                work: ''
                        }),
                        message: ref(''),
                        provinces: [],
                        cities: [],
                        counties: [],
                        towns: [],
                        province: '',
                        city: '',
                        county: '',
                        town: '',
                        confirmPassword: '',
                };
        },
        computed: {
                selectedProvinceCities() {
                        return this.cities;

                },
                selectedCityCounties() {
                        return this.counties;
                },
                selectedCountyTowns() {
                        return this.towns;
                },
        },
        async created() {
                try {
                        const { data } = await axios.get('/api/location/provinces');
                        this.provinces = data.data;
                } catch (error) {
                        console.error('Error fetchingprovinces:', error);
                }
        },

        watch: {
                async province(newValue) {
                        if (newValue) {
                                try {
                                        const { data } = await axios.get(`/api/location/province/${newValue.id}/cities`);
                                        this.cities = data.data;
                                } catch (error) {
                                        console.error('Error fetching cities:', error);
                                }
                        } else {
                                this.cities = [];
                        }
                        this.city = '';
                        this.county = '';
                        this.town = '';
                },
                async city(newValue) {
                        if (newValue) {
                                try {
                                        const { data } = await axios.get(`/api/location/city/${newValue.id}/counties`);
                                        this.counties = data.data;
                                } catch (error) {
                                        console.error('Error fetching counties:', error);
                                }
                        } else {
                                this.counties = [];
                        }
                        this.county = '';
                        this.town = '';
                },
                async county(newValue) {
                        if (newValue) {
                                try {
                                        const { data } = await axios.get(`/api/location/county/${newValue.id}/towns`);
                                        this.towns = data.data;
                                        console.log(data.data)
                                        this.hasTown = data.data.length > 0 ? true : false
                                        console.log(this.hasTown)

                                } catch (error) {
                                        console.error('Error fetching towns:', error);
                                }
                        } else {
                                this.towns = [];
                        }
                        this.town = '';
                },
        },
        methods: {
                async register() {

                        if (this.form.username == '' || this.form.password == '' || this.form.email == '' || this.form.lang == '' || this.form.name == '' || this.form.sex == '' || this.form.work == '') {
                                this.message = '请完成所有数据填写';
                                return;
                        }
                        // 验证输入
                        if (!this.form.email.match(/^\S+@\S+\.\S+$/)) {
                                this.message = '请输入正确的电子邮件地址';
                                return;
                        }
                        if (this.form.password !== this.confirmPassword) {
                                this.message = '两次输入的密码不一致';
                                return;
                        }
                        // 省略其他验证


                        // 添加地点到表单数据
                        const townName = this.town.name === undefined ? '' : this.town.name;
                        this.form.location = this.province.name + ',' + this.city.name + ',' + this.county.name + ',' + townName;

                        // 提交注册请求
                        try {
                                const response = await axios.post('/api/auth/register', this.form);
                                if (response.status === 201) {
                                        this.message = '注册成功';
                                        this.$router.replace('/');
                                        // 你可以在这里重定向到其他页面或执行其他操作
                                } else if (response.status === 422) {
                                        this.message = '该用户已存在，请重新注册';
                                } else {
                                        this.message = '注册失败';
                                }
                        } catch (error) {
                                console.error('注册失败:', error);
                                this.message = '注册失败';
                        }
                },
        },
};
</script>



      
<style>
/* Add Bootstrap classes and custom styles here */
.form-group label {
        font-weight: bold;
}

.invalid-feedback {
        display: none;
        color: red;
}

.invalid-feedback.show {
        display: block;
}

nav {
        display: block;
        background-color: #2182ea;
        border-bottom: 1px solid #e7e7e7;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        height: 50px;
        line-height: 50px;
        position: relative;
        top: 0;
        width: 100%;
        z-index: 100;
        text-align: start;
}

ul {
        list-style: none;
        margin: 0;
        padding: 0;
}

li {
        display: inline-block;
        margin: 0 10px;
        font: 14px/1.5 "Helvetica Neue", Helvetica, Arial, sans-serif;
}

a {
        color: #ccc;
        text-decoration: none;
}

a:hover {
        color: #ccc;
        text-decoration: none;
}

a:active {
        color: #ccc;
        text-decoration: none;
}

a:visited {
        color: #ccc;
        text-decoration: none;
}

a:link {
        color: #ccc;
        text-decoration: none;
}
</style>
      