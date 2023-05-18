import { createStore } from "vuex";

export default createStore({
  state: {
    accessToken: localStorage.getItem("accessToken") || "",
    refreshToken: localStorage.getItem("refreshToken") || "",
    wordId: localStorage.getItem("wordId") || 1,
    temporaryToken: localStorage.getItem("temporaryToken") || "",
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
      localStorage.setItem("accessToken", token); // Save accessToken to local storage
    },
    setRefreshToken(state, token) {
      state.temporaryToken = token;
      localStorage.setItem("refreshToken", token);
    },
    setWordId(state, Id) {
      state.wordId = Id;
      localStorage.setItem("wordId", Id);
    },
    settemporaryToken(state, token) {
      state.temporaryToken = token;
      localStorage.setItem("temporaryToken", token);
    },
  },
  actions: {
    setAccessToken({ commit }, token) {
      commit("setAccessToken", token);
    },
    setRefreshToken({ commit }, token) {
      commit("setRefreshToken", token);
    },
    setWordId({ commit }, Id) {
      commit("setWordId", Id);
    },
    settemporaryToken({ commit }, token) {
      commit("settemporaryToken", token);
    },
    async logout({ commit }) {
       commit('setAccessToken', null);
       commit('setRefreshToken', null);
       localStorage.removeItem('accessToken');
       localStorage.removeItem('refreshToken');
    },
  },
  getters: {
    accessToken: (state) => state.accessToken,
    refreshToken: (state) => state.refreshToken,
    wordId: (state) => state.wordId,
    temporaryToken: (state) => state.temporaryToken,
  },
});
