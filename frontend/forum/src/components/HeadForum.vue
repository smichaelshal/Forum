<template>
  <div class="head-forum box-card file-box">
    <el-card class="box-card">
      <div class="text item" @click="toForum">{{ name }}</div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "HeadForum",
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
    toForum() {
      this.$router.push({
        path: `/forum?forum=${this.id}`,
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
