<!-- App.vue -->
<template>
  <div id="app">
    <UserRegistration v-if="!accessToken" @registration-success="handleRegistrationSuccess" />
    <RecordAudio v-if="accessToken" @recordings-completed="handleRecordingsCompleted" />
    <p v-if="recordingsCompleted">All recordings are completed. Thank you for your participation!</p>
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import UserRegistration from './components/UserRegistration.vue';
import RecordAudio from './components/RecordAudio.vue';

export default {
  components: {
    UserRegistration,
    RecordAudio,
  },
  computed: {
    ...mapGetters(['accessToken']),
  },
  data() {
    return {
      recordingsCompleted: false,
    };
  },
  methods: {
    handleRegistrationSuccess(token) {
      this.$store.dispatch('setAccessToken', token);
    },
    handleRecordingsCompleted() {
      this.recordingsCompleted = true;
    },
  },
};
</script>
