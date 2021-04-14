<template>
  <div class="category">
    <HeadForum v-for="forum in listForums" :key="forum.id" />
  </div>
</template>

<script>
import HeadForum from "@/components/HeadForum.vue";
import SendApi from "@/mixins/SendApi.js";

export default {
  name: "Category",
  mixins: [SendApi],

  props: {
    name: {
      type: String,
    },
    id: {
      type: String,
    },
  },

  components: {
    HeadForum,
  },
  data() {
    return {
      listForums: [],
    };
  },
  methods: {
    getListFourms() {
      console.log(this.id);
      this.sendToServer({
        url: "forum/get_category/",
        args: { id: this.id },
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
    this.getListFourms();
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
