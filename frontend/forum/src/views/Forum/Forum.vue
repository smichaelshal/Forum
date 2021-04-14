<template>
  <div class="forum">
    <!-- <el-row> -->
    <HeadPost
      v-for="(post, counter) in listPosts"
      :key="post.post_id"
      :title="post.title"
      :user="post.user"
      :date="post.create_date"
      :id="post.post_id"
      :isEven="counter % 2 == 0"
    />
    <!-- </el-row> -->

    <div>
      <AddPost :idForum="id" />
    </div>
  </div>
</template>

<script>
import HeadPost from "@/components/HeadPost.vue";
import AddPost from "@/components/AddPost.vue";
import SendApi from "@/mixins/SendApi.js";

export default {
  name: "Forum",
  mixins: [SendApi],

  components: {
    HeadPost,
    AddPost,
  },
  data() {
    return {
      listPosts: [],
      id: null,
    };
  },
  methods: {
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    getListPosts() {
      this.sendToServer({
        url: "forum/get_forum/",
        args: { id: this.id, page: 1 },
      })
        .then((data) => {
          this.listPosts = data.forum.posts;
          console.log(this.listPosts);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.id = this.$route.query.forum;
    if (this.id === null || this.id === undefined) {
      // page not found
    } else {
      this.getListPosts();
    }
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
