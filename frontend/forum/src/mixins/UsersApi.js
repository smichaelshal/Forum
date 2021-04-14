// import axios from "axios";
import SendApi from "@/mixins/SendApi.js";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "UsersApi",
  mixins: [SendApi],
  computed: {
    ...mapGetters([
      "getIsLogin",
      "getUsername",
      "getAccessToken",
      "getRefreshToken",
    ]),
  },
  data() {
    return {
      refreshToken: null,
      host: "http://localhost:8000/",
      username: "",
      password: "",
      isLogin: false,
      timeTokenAccess: 1000 * 60 * 4,
      sumCall: 0,
    };
  },
  methods: {
    ...mapMutations(["setIsLogin", "setUsername", "setPermission"]),
    login() {
      if (localStorage.refreshToken) {
        this.refreshToken = localStorage.refreshToken;
        this.accessToken = localStorage.accessToken;
        this.getMyUsername();
      }
    },
    saveLogin(data) {
      this.refreshToken = data.refresh;
      this.accessToken = data.access;
      localStorage.refreshToken = data.refresh;
      localStorage.accessToken = data.refresh;
    },
    sendLogin() {
      this.sendToServer({
        url: "users/login/",
        args: {
          username: this.username,
          password: this.password,
        },
        type: "post",
        isAuth: false,
      })
        .then((data) => {
          this.isLogin = true;
          this.saveLogin(data);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async sendRefreshToken() {
      try {
        let data = await this.sendToServer({
          url: "users/api/token/refresh/",
          args: {
            refresh: this.refreshToken,
          },
          type: "post",
          isAuth: false,
        });
        this.accessToken = data.access;
        localStorage.accessToken = data.access;
        this.isLogin = true;
        this.setToken(data.access);
        this.getMyUsername();
      } catch (error) {
        console.log(error);
        this.isLogin = false;
      }
    },

    async getMyUsername() {
      try {
        const dataSerevr = await this.sendToServer({
          url: "users/get-username/",
          args: {},
          type: "post",
          isAuth: true,
        });
        this.isLogin = true;
        this.username = dataSerevr.username;
        this.permission = dataSerevr.permission;
        this.setIsLogin(true);
        this.setUsername(this.username);
        this.setPermission(this.permission);
      } catch (error) {
        if (this.sumCall <= 0) {
          this.sendRefreshToken();
          this.sumCall += 1;
        }
      }
    },
  },
  mounted() {
    this.login();

    const _this = this;
    setInterval(() => {
      _this.sendRefreshToken();
    }, _this.timeTokenAccess);
  },
  watch: {
    getUsername: function(val) {
      if (val === null) {
        this.setToken(null);
      }
    },
  },
};
