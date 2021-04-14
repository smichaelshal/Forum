<template>
  <div class="home">
    <el-row>
      <Categories />
    </el-row>
  </div>
</template>

<script>
import Categories from "@/components/Categories.vue";

export default {
  name: "home",
  components: {
    Categories,
  },
  computed: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
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
