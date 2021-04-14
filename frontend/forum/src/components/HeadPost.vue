<template>
  <div class="head-post" @click="toPost">
    <el-row v-bind:class="{ even: isEven, noteven: !isEven }">
      <el-col :span="8"
        ><div class="grid-content">{{ title }}</div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content">{{ user }}</div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content">{{ date }}</div></el-col
      >
    </el-row>
    <!-- {{ title }} -->
    <!-- <el-container class="post-heads">
      <el-header>Header</el-header>
      <el-main>Main</el-main>
    </el-container> -->

    <!-- <el-card> -->
    <!-- <div class="text item">title {{ title }}</div> -->
    <!-- <div class="text item">user {{ user }}</div> -->
    <!-- <div class="text item">date {{ date }}</div> -->
    <!-- <div class="text item">id {{ id }}</div> -->
    <!-- </el-card> -->
  </div>
</template>

<script>
export default {
  name: "HeadCategory",
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
    isEven: {
      type: Boolean,
    },
  },

  components: {
    // MainDesktop,
  },
  methods: {
    toPost() {
      this.$router.push({
        path: `/post?post=${this.id}`,
      });
    },
  },
  data() {
    return {};
  },
};
</script>

<style>
.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.box-card {
  width: 200px;
}

.file-box {
  width: 180px;
  float: right;
  margin-left: 40px;
  margin-top: 10px;
}

.post-heads {
  background: red;
  float: right;
}

.even {
  background-color: #d3dce6;
}
.noteven {
  background-color: #b3c0d1;
}

.head-post {
  margin-top: 10px;
}
</style>
