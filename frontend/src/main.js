import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './assets/main.css'

import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Dashboard from './views/Dashboard.vue'
import Admin from './views/Admin.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/admin', component: Admin, meta: { requiresAuth: true, requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const pinia = createPinia()

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin && user?.role !== 'admin') {
    next('/')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')