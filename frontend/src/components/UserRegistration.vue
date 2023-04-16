<template>
    <nav>
        <ul>
            <li><a href="/">回到首页</a></li>
        </ul>
    </nav>
    <div class="mobile-container">
        <h2>方言调查</h2>
        <form @submit.prevent="registerUser" class="needs-validation" novalidate>
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
                <label for="language">方言</label>
                <select id="language" v-model="language" class="form-control" required>
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
                    <option value="Unsure">我不确定自己的方言类型</option>
                </select>
                <div class="invalid-feedback">
                    Please select a dialect category.
                </div>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="!isFormValid() || submitIsDisabled" >确认</button>
        </form>

    </div>
</template>

<style scoped>
.mobile-container {
    max-width: 100%;
    padding: 16px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-size: 16px;
}

select {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ced4da;
    background-color: #fff;
    font-size: 16px;
}

option[disabled] {
    color: #a5a5a5;
}

.form-group {
    margin-bottom: 16px;
}

button[type="submit"] {
    width: 100%;
    margin-top: 16px;
    font-size: 16px;
    padding: 12px;
    border-radius: 4px;
    border: none;
    background-color: #007bff;
    color: #fff;
}

/* navibar temp */
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


<script>
import axios from 'axios';
// import 'bootstrap/dist/css/bootstrap.min.css';


export default {

    data() {
        return {
            province: '',
            city: '',
            county: '',
            town: '',
            language: '',
            submitIsDisabled: false,
            hasTown: false,
            provinces: [],
            cities: [],
            counties: [],
            towns: [],
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
        async registerUser() {
            try {
                console.log(typeof this.city)
                const townName = this.town.name === undefined ? '' : this.town.name
                this.submitIsDisabled = true;
                const response = await axios.post(`/api/userRecord/autoregister`, {
                    location: this.province.name + ',' + this.city.name + ',' + this.county.name + ',' + townName,
                    language: this.language,
                });

                if (response.data.message === 'success') {
                    this.$store.dispatch('setAccessToken', response.data.access_token);
                    this.$router.replace('/record-audio');
                }
            } catch (error) {
                console.error('Error registering user:', error);
            }
        },
        isFormValid() {

            return this.language && (this.hasTown && this.town || !this.hasTown);
        },
    },
};
</script>
  