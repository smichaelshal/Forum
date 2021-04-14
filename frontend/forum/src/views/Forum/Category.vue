<template>
  <div class="category-page">
    <el-row>
      <HeadForum
        v-for="fourm in listFourms"
        :key="fourm.id"
        :name="fourm.name"
        :id="fourm.id_forum"
        :permission="fourm.permission"
      />
    </el-row>

    <div>
      <AddForum :idCategory="id" />
    </div>
  </div>
</template>

<script>
import HeadForum from "@/components/HeadForum.vue";
import SendApi from "@/mixins/SendApi.js";
import AddForum from "@/components/AddForum.vue";

export default {
  name: "CategoryPage",
  mixins: [SendApi],

  components: {
    HeadForum,
    AddForum,
  },
  computed: {},
  data() {
    return {
      id: null,
      listFourms: [],
    };
  },
  methods: {
    getListFourms() {
      this.sendToServer({
        url: "forum/get_category/",
        args: { id: this.id },
        type: "post",
        isAuth: false,
      })
        .then((data) => {
          this.listFourms = data.category.forums;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.id = this.$route.query.category;
    if (this.id === null || this.id === undefined) {
      // page not found
    } else {
      this.getListFourms();
    }
  },
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
