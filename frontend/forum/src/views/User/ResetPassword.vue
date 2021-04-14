<template>
  <div class="reset-password">
    <h1>Reset Password</h1>

    <el-row>
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input
            placeholder="Please input email"
            v-model="email"
            :disabled="isSend"
          ></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row v-if="!isSend">
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-button type="primary" @click="sendEmail">Send mail</el-button>
        </div>
      </el-col>
      <el-col :span="8"><div class="grid-content"></div></el-col>
    </el-row>

    <el-row v-if="isSend">
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input placeholder="Please input token" v-model="token"></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row v-if="isSend">
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-input
            placeholder="Please input a new password"
            v-model="password"
            show-password
          ></el-input>
        </div>
      </el-col>
    </el-row>

    <el-row v-if="isSend">
      <el-col :span="8"><div class="grid-content"></div></el-col>
      <el-col :span="8">
        <div class="inputs">
          <el-button type="primary">Reset Password</el-button>
        </div>
      </el-col>
      <el-col :span="8"><div class="grid-content"></div></el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      token: "",
      password: "",
      isSend: false,
    };
  },
  methods: {
    sendEmail() {
      this.isSend = true;
      console.log(this.isSend);
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
