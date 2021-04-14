import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
  hostHttp: "http://localhost:8000/",
  isLogin: false,
  username: null,
  permission: null,
  accessToken: null,
  refreshToken: null,
};

const mutations = {
  setUsername(state, username) {
    state.username = username;
  },
  setPermission(state, permission) {
    state.permission = permission;
  },
  setIsLogin(state, isLogin) {
    state.isLogin = isLogin;
  },
  setAccessToken(state, accessToken) {
    state.accessToken = accessToken;
  },
  setRefreshToken(state, refreshToken) {
    state.refreshToken = refreshToken;
  },
};
const actions = {};
const modules = {};
const getters = {
  getHostHttp() {
    return state.hostHttp;
  },
  getPermission() {
    return state.permission;
  },
  getUsername() {
    return state.username;
  },
  getIsLogin() {
    return state.isLogin;
  },
  getAccessToken() {
    return state.accessToken;
  },
  getRefreshToken() {
    return state.refreshToken;
  },
};

export default new Vuex.Store({
  state,
  getters,
  mutations,

  actions,
  modules,
});
