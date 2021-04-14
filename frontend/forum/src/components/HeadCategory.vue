<template>
  <div class="head-category box-card file-box">
    <el-card class="box-card">
      <div class="text item" @click="toCatecory">{{ name }}</div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "HeadCategory",
  props: {
    name: {
      type: String,
    },
    permission: {
      type: Number,
    },
    id: {
      type: String,
    },
  },

  components: {
    // MainDesktop,
  },
  methods: {
    toCatecory() {
      this.$router.push({
        path: `/category?category=${this.id}`,
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
</style>
