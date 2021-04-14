import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

import Category from "../views/Forum/Category.vue";
import Forum from "../views/Forum/Forum.vue";
import Post from "../views/Forum/Post.vue";

import Login from "../views/User/Login.vue";
import Register from "../views/User/Register.vue";
import ResetPassword from "../views/User/ResetPassword.vue";
import EmailConfirmation from "../views/User/EmailConfirmation.vue";
import ChangePassword from "../views/User/ChangePassword.vue";

import NotAuthorized from "../views/NotAuthorized.vue";
import NotFound from "../views/NotFound.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    // list categories
  },
  {
    path: "/category",
    name: "Category",
    component: Category,
    // list forums
  },
  {
    path: "/forum",
    name: "Forum",
    component: Forum,
    // list posts
  },
  {
    path: "/post",
    name: "Post",
    component: Post,
    // list messages
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/reset-password",
    name: "ResetPassword",
    component: ResetPassword,
  },
  {
    path: "/email-confirmation",
    name: "EmailConfirmation",
    component: EmailConfirmation,
  },
  {
    path: "/not-authorized",
    name: "NotAuthorized",
    component: NotAuthorized,
  },
  {
    path: "/change-password",
    name: "ChangePassword",
    component: ChangePassword,
  },
  {
    path: "*",
    name: "NotFound",
    component: NotFound,
  },
  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/About.vue"),
  // },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
