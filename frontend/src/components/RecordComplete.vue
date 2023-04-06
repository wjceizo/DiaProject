<template>
  <div class="mobile-container">
    <h1>恭喜您!</h1>
    <p>您完成了所有的方言调查!</p>
    <button type="complete" class="btn btn-primary" @click="resetRecordings">开始新的录音调查</button>
  </div>
</template>
<style scoped>

button[type="complete"] {
    width: 100%;
    margin-top: 16px;
    font-size: 16px;
    padding: 12px;
    border-radius: 4px;
    border: none;
    background-color: #007bff;
    color: #fff;
}
  .mobile-container {
    max-width: 100%;
    padding: 16px;
    text-align: center;
  }
</style>
  
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
  