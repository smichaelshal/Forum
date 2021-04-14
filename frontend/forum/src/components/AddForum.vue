<template>
  <div class="add-forum">
    <div v-if="getPermission >= ceo_code">
      <el-row>
        <el-col :span="22"><div class="grid-content"></div></el-col>
        <el-col :span="2"
          ><div class="grid-content">
            <el-button
              style="margin-top:20px"
              type="primary"
              icon="el-icon-plus"
              circle
              @click="isOpenCreateForum = true"
            ></el-button></div
        ></el-col>
        <div
          style="margin-top:50px"
          v-if="isOpenCreateForum && getPermission >= ceo_code"
        >
          <el-col :span="8"><div class="grid-content"></div></el-col>
          <el-col :span="8"
            ><div class="grid-content">
              <el-input
                placeholder="Please input name"
                v-model="newName"
              ></el-input>
              <el-input
                placeholder="Please input permission"
                v-model="newPermission"
                style="margin-top:20px"
              ></el-input>
              <el-button
                type="primary"
                style="margin-top:20px"
                @click="createForum"
                >Create a new forum</el-button
              >
            </div></el-col
          >
          <el-col :span="8"><div class="grid-content"></div></el-col>
        </div>
      </el-row>
    </div>
  </div>
</template>

<script>
import SendApi from "@/mixins/SendApi.js";
import { mapGetters } from "vuex";

export default {
  name: "home",
  mixins: [SendApi],
  props: {
    idCategory: {
      type: String,
    },
  },
  components: {},
  computed: {
    ...mapGetters(["getPermission"]),
  },
  data() {
    return {
      isOpenCreateForum: false,
      newName: null,
      newPermission: null,
      ceo_code: 100,
    };
  },
  methods: {
    createForum() {
      this.sendToServer({
        url: "forum/create_forum/",
        args: {
          name: this.newName,
          permission: this.newPermission,
          category_id: this.idCategory,
        },
      })
        .then((data) => {
          console.log(data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style>
/* .el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
} */
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
