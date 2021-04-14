<template>
  <div class="add-message" v-if="getPermission >= regular_code">
    <el-row v-if="getPermission >= regular_code">
      <el-col :span="3"><div class="grid-content"></div></el-col>
      <el-col :span3="18">
        <div>
          <VueEditor v-model="data" />
        </div>
      </el-col>
      <el-col :span="3"><div class="grid-content"></div></el-col>
    </el-row>

    <el-row class="button-send">
      <el-col :span="3"><div class="grid-content"></div></el-col>
      <el-col :span="18">
        <div>
          <el-button type="primary" @click="createMessage"
            >Create a message</el-button
          >

          <!-- <div class="content ql-editor" v-html="content"></div> -->
        </div>
      </el-col>
      <el-col :span="3"><div class="grid-content"></div></el-col>
    </el-row>
  </div>
</template>

<script>
import SendApi from "@/mixins/SendApi.js";
import { mapGetters } from "vuex";
import { VueEditor } from "vue2-editor";

export default {
  name: "AddMessage",
  mixins: [SendApi],
  props: {
    idPost: {
      type: String,
    },
  },
  components: {
    VueEditor,
  },
  computed: {
    ...mapGetters(["getPermission"]),
  },
  data() {
    return {
      isOpenCreateMessage: false,
      data: null,
      regular_code: 100,
      content: "",
    };
  },
  methods: {
    createMessage() {
      this.sendToServer({
        url: "forum/create_message/",
        args: {
          data: this.data,
          post_id: this.idPost,
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

.add-message {
  margin-top: 20px;
}

.button-send {
  margin-top: 20px;
}
</style>
