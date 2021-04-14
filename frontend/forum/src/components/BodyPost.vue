<template>
  <div class="body-post">
    <el-container>
      <el-container>
        <el-header class="title">{{ title }}</el-header>
        <el-main>
          <div class="content ql-editor" v-html="data"></div>
        </el-main>
        <el-footer>
          <el-row>
            <el-col :span="2">
              <div class="grid-content">{{ user }}</div>
            </el-col>
            <el-col :span="17"><div class="grid-content"></div></el-col>

            <el-col :span="5">
              <div class="grid-content">{{ date }}</div>
            </el-col>
          </el-row>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "BodyPost",
  props: {
    title: {
      type: String,
    },
    permission: {
      type: Number,
    },
    views: {
      type: Number,
    },
    id: {
      type: String,
    },
    user: {
      type: String,
    },
    date: {
      type: String,
    },
    data: {
      type: String,
    },
  },

  components: {},
  methods: {},
  data() {
    return {
      content: "",
      dataTest:
        '<h1 class="ql-align-center"><strong>Test</strong></h1><p class="ql-align-center">Hello world</p>',
    };
  },
};
</script>

<style scoped>
.body-post {
}
.date {
  right: 0px;
  float: right;
}

.user {
  right: 0px;
  float: right;
  margin-right: 10px;
  margin-top: 10px;
}
.header {
  right: 0px;
  float: left;
  top: 0px;
}

.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.title {
  font-weight: bold;
  font-size: 25px;
}
</style>
