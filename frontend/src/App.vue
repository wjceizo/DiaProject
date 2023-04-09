<template>
  <div id="app">
    <router-view v-if="recordingsCompleted || accessToken" />
    <router-view v-if="!recordingsCompleted && !accessToken" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['accessToken']),
  },
  data() {
    return {
      recordingsCompleted: false,
    };
  },
};
</script>
