<template>
  <div class="categories">
    <div>
      <el-row>
        <HeadCategory
          v-for="category in listCategories"
          :key="category.id"
          :name="category.name"
          :permission="category.permission"
          :id="category.id"
        />
      </el-row>
    </div>

    <div>
      <AddCategory />
    </div>
  </div>
</template>

<script>
import HeadCategory from "@/components/HeadCategory.vue";
import AddCategory from "@/components/AddCategory.vue";
import SendApi from "@/mixins/SendApi.js";
import { mapGetters } from "vuex";

export default {
  name: "categories",
  mixins: [SendApi],
  components: {
    HeadCategory,
    AddCategory,
  },
  computed: {
    ...mapGetters(["getPermission"]),
  },
  data() {
    return {
      listCategories: [],
      isOpenCreateCategory: false,
      newName: null,
      newPermission: null,
    };
  },
  methods: {
    getListCategories() {
      const _this = this;
      this.sendToServer({
        url: "forum/get_list_categories/",
        args: {},
        type: "post",
        isAuth: false,
      })
        .then((data) => {
          _this.listCategories = data.listCategory;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    createCategory() {
      this.sendToServer({
        url: "forum/create_category/",
        args: { name: this.newName, permission: this.newPermission },
      })
        .then((data) => {
          console.log(data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.getListCategories();
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
