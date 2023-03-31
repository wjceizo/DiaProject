<template>
    <div style="width: 50%; margin: auto;">
        <h2>User Registration</h2>
        <form @submit.prevent="registerUser" class="needs-validation" novalidate>
            <div class="form-group">
                <label for="province">Province:</label>
                <select id="province" v-model="province" class="form-control" required>
                    <option value="" disabled>Select Province</option>
                    <option v-for="p in provinces" :key="p.id" :value="p">{{ p.name }}</option>
                </select>
                <div class="invalid-feedback">
                    Please select a province.
                </div>
            </div>

            <div class="form-group">
                <label for="city">City:</label>
                <select id="city" v-model="city" class="form-control" required>
                    <option value="" disabled>Select City</option>
                    <option v-for="c in selectedProvinceCities" :key="c.name" :value="c">{{ c.name }}</option>
                </select>
                <div class="invalid-feedback">
                    Please select a city.
                </div>
            </div>

            <div class="form-group">
                <label for="county">County:</label>
                <select id="county" v-model="county" class="form-control" required>
                    <option value="" disabled>Select County</option>
                    <option v-for="c in selectedCityCounties" :key="c" :value="c">{{ c.name }}</option>
                </select>
                <div class="invalid-feedback">
                    Please select a county.
                </div>
            </div>

            <div class="form-group">
                <label for="town">Town:</label>
                <select id="town" v-model="town" class="form-control" required :disabled="!hasTown">
                    <option value="" disabled>Select Town</option>
                    <option v-for="t in selectedCountyTowns" :key="t.id" :value="t">{{ t.name }}</option>
                </select>
                <div class="invalid-feedback">
                    Please select a town.
                </div>
            </div>

            <div class="form-group">
                <label for="language">Dialect Category:</label>
                <select id="language" v-model="language" class="form-control" required>
                    <option value="" disabled>Select Dialect Category</option>
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
                <div class="invalid-feedback">
                    Please select a dialect category.
                </div>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="!isFormValid()">Submit</button>
        </form>
    </div>
</template>


<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
    data() {
        return {
            province: '',
            city: '',
            county: '',
            town: '',
            language: '',
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
                const response = await axios.post(`/api/userRecord/autoregister`, {
                    location: this.province.name + ',' + this.city.name + ',' + this.county.name + ',' + townName,
                    language: this.language,
                });

                if (response.data.message === 'success') {
                    this.$store.dispatch('setAccessToken', response.data.access_token);
                }
            } catch (error) {
                console.error('Error registering user:', error);
            }
        },
        isFormValid() {
            
            return this.language && (this.hasTown && this.town || !this.hasTown) ;
        },
    },
};
</script>
  