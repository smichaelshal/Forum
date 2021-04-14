<template>
  <div class="email-confirmation">
    <h1>Email Confirmation</h1>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input placeholder="Please input token" v-model="token"></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-button type="primary" @click="sendToken">Send Token</el-button>
        </div>
      </el-col>
      <el-col :span="8"><div class="grid-content"></div></el-col>
    </el-row>
  </div>
</template>

<script>
import SendApi from "@/mixins/SendApi.js";

export default {
  mixins: [SendApi],

  data() {
    return {
      token: "",
    };
  },
  methods: {
    sendToken() {
      this.sendToServer({
        url: "users/confirmed-email/",
        args: {
          token: this.token,
        },
        type: "post",
        isAuth: false,
      })
        .then((data) => {
          console.log(data);
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
        });
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
