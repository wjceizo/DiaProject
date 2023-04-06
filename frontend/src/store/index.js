import { createStore } from 'vuex';

export default createStore({
  state: {
    accessToken: localStorage.getItem('accessToken') || '',
    wordId: localStorage.getItem('wordId') || 1,
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('accessToken', token); // Save accessToken to local storage
    },
    setWordId(state, Id) {
        state.wordId = Id;
        localStorage.setItem('wordId', Id);
      },
  },
  actions: {
    setAccessToken({ commit }, token) {
      commit('setAccessToken', token);
    },
    setWordId({ commit }, Id) {
        commit('setWordId', Id);
      },
  },
  getters: {
    accessToken: (state) => state.accessToken,
    wordId: (state) => state.wordId,
  },
});
