<template>
  <div class="login">
    <h1>Login</h1>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input
            placeholder="Please input username"
            v-model="username"
          ></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input
            placeholder="Please input password"
            v-model="password"
            show-password
          ></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-button type="primary" @click="sendLogin">Login</el-button>
        </div>
      </el-col>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8"><div class="grid-content"></div></el-col>

      <el-col :span="24"
        ><el-link
          type="primary"
          class="links"
          @click="$router.push('/register')"
          >To register, click here</el-link
        ></el-col
      >
      <el-col :span="24" class="links"
        ><el-link type="primary" @click="$router.push('/reset-password')"
          >I forgot the password</el-link
        ></el-col
      >
    </el-row>
  </div>
</template>

<script>
import SendApi from "@/mixins/SendApi.js";
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
  mixins: [SendApi],
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    ...mapMutations([
      "setIsLogin",
      "setUsername",
      "setAccessToken",
      "setRefreshToken",
    ]),
    sendLogin() {
      const _this = this;
      _this
        .sendToServer({
          url: "users/login/",
          args: {
            username: _this.username,
            password: _this.password,
          },
          type: "post",
          isAuth: false,
        })
        .then((data) => {
          _this.isLogin = true;
          _this.setUsername(_this.username);
          _this.saveLogin(data);
          _this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveLogin(data) {
      this.refreshToken = data.refresh;
      this.accessToken = data.access;
      localStorage.refreshToken = data.refresh;
      localStorage.accessToken = data.refresh;
    },
  },
};
</script>

<style>
.inputs {
  margin-top: 10px;
  /* min-width: 200px; */
}
.links {
  margin-top: 10px;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
