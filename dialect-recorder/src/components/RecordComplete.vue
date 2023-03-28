<template>
    <div >
      <h1>Congratulations!</h1>
      <p>You have completed all recordings!</p>
      <button class="btn btn-primary" @click="resetRecordings">Start a new recording</button>
    </div>
  </template>
  
  <script>
  import { useStore } from 'vuex';
  
  export default {
    data() {
      return {
        wordId: 1
      };
    },

    methods: {
      resetRecordings() {
        // Clear the accessToken and wordId from the Vuex store
        this.$store.commit('setAccessToken', '');
        this.$store.commit('setWordId', 1);
        this.$router.replace('/');
      }
    },
    created() {
      const store = useStore();
      this.wordId = store.getters.wordId;
    }
  };
  </script>
  