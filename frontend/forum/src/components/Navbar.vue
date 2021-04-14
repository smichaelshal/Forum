<template>
  <div id="nav">
    <el-menu
      :default-active="getNamePage()"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="home" @click="ChangePage('/')">Home</el-menu-item>

      <el-menu-item index="login" v-if="!isLogin" @click="ChangePage('/login')"
        >Login</el-menu-item
      >
      <el-menu-item
        index="register"
        v-if="!isLogin"
        @click="ChangePage('/register')"
        >Register</el-menu-item
      >

      <el-submenu index="user" v-if="isLogin">
        <template slot="title">{{ username }}</template>
        <el-menu-item index="logout" @click="logout">Logout</el-menu-item>
        <el-menu-item
          index="change-password"
          @click="ChangePage('/change-password')"
          >Change Password</el-menu-item
        >
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

export default {
  computed: {
    ...mapGetters([
      "getIsLogin",
      "getUsername",
      "getAccessToken",
      "getRefreshToken",
    ]),
  },
  name: "Navbar",
  data() {
    return {
      isLogin: false,
      username: "",
      pathPage: "",
    };
  },
  methods: {
    ...mapMutations([
      "setIsLogin",
      "setUsername",
      "setAccessToken",
      "setRefreshToken",
    ]),
    logout() {
      this.setIsLogin(false);
      this.setUsername(null);
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    ChangePage(path) {
      if (this.$route.path != path) {
        this.$router.push(path);
      }
    },
    getNamePage() {
      const namesJson = {
        "/": "home",
        "/login": "login",
        "/register": "register",
        "/change-password": "change-password",
      };
      const pathNow = this.$route.path;
      if (namesJson[pathNow]) return namesJson[pathNow];
      // return namesJson["/"];
      return null;
    },
  },
  watch: {
    getUsername: function(val) {
      if (val === null) {
        this.isLogin = false;
        this.username = null;
      } else {
        this.isLogin = true;
        this.username = val;
      }
    },
  },
};
</script>
