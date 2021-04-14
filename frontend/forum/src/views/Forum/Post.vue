<template>
  <div class="post">
    <el-row>
      <BodyPost
        :title="title"
        :data="data"
        :date="date"
        :user="user"
        :id="id"
      />
    </el-row>
    <el-row>
      <Message
        v-for="(message, counter) in listMessages"
        :key="message.id_message"
        :title="message.title"
        :user="message.user"
        :date="message.create_date"
        :data="message.data"
        :id="message.id_message"
        :evenSum="counter % 2 == 0"
      />
    </el-row>

    <div>
      <AddMessage :idPost="id" />
    </div>
  </div>
</template>

<script>
import Message from "@/components/Message.vue";
import BodyPost from "@/components/BodyPost.vue";
import AddMessage from "@/components/AddMessage.vue";
import SendApi from "@/mixins/SendApi.js";

export default {
  name: "Post",
  mixins: [SendApi],

  components: {
    Message,
    AddMessage,
    BodyPost,
  },
  data() {
    return {
      title: null,
      data: null,
      user: null,
      date: null,

      listMessages: [],
      id: null,
    };
  },
  methods: {
    getPost() {
      console.log(this.id);
      this.sendToServer({
        url: "forum/get_post/",
        args: { id: this.id, page: 1 },
      })
        .then((data) => {
          console.log(data);
          this.listMessages = data.post.messages;
          this.title = data.post.title;
          this.user = data.post.user;
          this.date = data.post.create_date;
          this.data = data.post.data;
          this.id = data.post.post_id;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.id = this.$route.query.post;
    if (this.id === null || this.id === undefined) {
      // page not found
    } else {
      this.getPost();
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
