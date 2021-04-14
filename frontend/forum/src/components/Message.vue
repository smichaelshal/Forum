<template>
  <div class="message">
    <el-row>
      <el-col :span="4"><div class="grid-content"></div></el-col>
      <el-col :span="16">
        <el-card v-bind:class="{ even: evenSum, noteven: !evenSum }">
          <!-- <div>
            <div class="content ql-editor" v-html="data"></div>
          </div> -->

          <el-container>
            <!-- <el-header>Header</el-header> -->
            <el-main
              ><div class="content ql-editor" v-html="data"></div
            ></el-main>
            <el-footer>
              <el-row>
                <el-col :span="2">
                  <div class="grid-content">{{ user }}</div>
                </el-col>
                <el-col :span="12"><div class="grid-content"></div></el-col>

                <el-col :span="10">
                  <div class="grid-content">{{ date }}</div>
                </el-col>
              </el-row></el-footer
            >
          </el-container>
        </el-card>
      </el-col>
      <el-col :span="4"><div class="grid-content"></div></el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "HeadCategory",
  props: {
    permission: {
      type: Number,
    },
    data: {
      type: String,
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
    evenSum: {
      type: Boolean,
    },
  },

  components: {},
  methods: {},
  data() {
    return {};
  },
};
</script>

<style scoped>
.message {
  margin-top: 10px;
}

.even {
  background-color: #d3dce6;
}
.noteven {
  background-color: #b3c0d1;
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
</style>
