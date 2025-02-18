import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import UserPage from "../views/UserPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/user/:username",
    name: "userPage", // Nome da rota que será chamada ao clicar no nome do usuário
    component: UserPage,
    props: true, // Passa o parâmetro `username` como prop para o componente UserPage
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
