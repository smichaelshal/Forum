<template>
  <div class="add-post">
    <div v-if="getPermission >= regular_code">
      <el-row>
        <el-col :span="22"><div class="grid-content"></div></el-col>
        <el-col :span="2"
          ><div class="grid-content">
            <el-button
              style="margin-top:20px"
              type="primary"
              icon="el-icon-plus"
              circle
              @click="isOpenCreatePost = true"
            ></el-button></div
        ></el-col>
        <div
          style="margin-top:50px"
          v-if="isOpenCreatePost && getPermission >= regular_code"
        >
          <el-col :span="2"><div class="grid-content"></div></el-col>
          <el-col :span="20"
            ><div class="grid-content">
              <el-input
                placeholder="Please input title"
                v-model="title"
              ></el-input>
              <el-row v-if="getPermission >= regular_code">
                <el-col :span="3"><div class="grid-content"></div></el-col>
                <el-col :span3="18">
                  <div>
                    <VueEditor v-model="data" />
                  </div>
                </el-col>
              </el-row>
              <el-button
                type="primary"
                style="margin-top:20px"
                @click="createPost"
                >Create a new Post</el-button
              >
            </div></el-col
          >
          <el-col :span="2"><div class="grid-content"></div></el-col>
        </div>
      </el-row>
    </div>
  </div>
</template>

<script>
import SendApi from "@/mixins/SendApi.js";
import { mapGetters } from "vuex";
import { VueEditor } from "vue2-editor";

export default {
  name: "home",
  mixins: [SendApi],
  props: {
    idForum: {
      type: String,
    },
  },
  components: { VueEditor },
  computed: {
    ...mapGetters(["getPermission"]),
  },
  data() {
    return {
      isOpenCreatePost: false,
      title: null,
      data: null,
      regular_code: 100,
    };
  },
  methods: {
    createPost() {
      this.sendToServer({
        url: "forum/create_post/",
        args: {
          title: this.title,
          data: this.data,
          forum_id: this.idForum,
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
