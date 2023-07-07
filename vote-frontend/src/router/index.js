import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';
import Results from '@/components/container/Results.vue'
import Ballot from '@/components/container/Ballot.vue'
import Login from '@/components/container/Login.vue'
import App from './App.vue'

const routes = [
  {
    path: '/',
    name: 'App',
    component: App,
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  },
  {
    path: '/ballot',
    name: 'Ballot',
    component: Ballot
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
];

const router = createRouter({
  base: "/vote-frontend/",
  history: createWebHistory(),
  routes,
});

export default router;
