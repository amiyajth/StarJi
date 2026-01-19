import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import TravelPlan from '../views/TravelPlan.vue'
import ImageSearch from '../views/ImageSearch.vue'
import MyProfile from '../views/MyProfile.vue'
import CityDetail from '../views/CityDetail.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/travel-plan', name: 'TravelPlan', component: TravelPlan },

  // ✅ 视觉 MVP：以图搜旅
  { path: '/search', name: 'ImageSearch', component: ImageSearch },

  // ✅ 用户画像
  { path: '/profile', name: 'MyProfile', component: MyProfile },

  { path: '/city/:id', name: 'CityDetail', component: CityDetail },

  // ✅ 登录/注册
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
