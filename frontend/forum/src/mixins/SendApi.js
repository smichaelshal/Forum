import axios from "axios";

export default {
  name: "SendApi",
  data() {
    return {
      accessToken: "gg1",
      host: "http://localhost:8000/",
    };
  },
  methods: {
    setToken(token) {
      this.accessToken = token;
    },
    sendToServer(kwargs) {
      const url = this.host + kwargs["url"];
      const args = kwargs["args"] ? kwargs["args"] : {};
      const type = kwargs["type"] ? kwargs["type"] : "post";
      let isAuth;

      if (kwargs["isAuth"] === undefined) {
        isAuth = true;
      } else {
        isAuth = kwargs["isAuth"];
      }
      let config = {};

      if (isAuth) {
        config = {
          Authorization: `Bearer ${localStorage.accessToken}`,
        };
      }

      return axios({
        method: type,
        url: url,
        data: args,
        headers: config,
      })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          if (error.response.status === 403) {
            // 401
            // this.$router.push("not-authorized/");
          } else if (error.response.status === 404) {
            // this.$router.push("not-found/");
          }
          throw error.response;
        });
    },
  },

  watch: {
    // question: function(val) {
    //   this.accessToken = val;
    // },
  },
};
