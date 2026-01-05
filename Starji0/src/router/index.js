// 引入Vue Router的创建函数
import { createRouter, createWebHistory } from 'vue-router'

// 引入页面组件
import Home from '../views/Home.vue'
import TravelPlan from '../views/TravelPlan.vue'
import ImageSearch from '../views/ImageSearch.vue'
import MyProfile from '../views/MyProfile.vue'
import CityDetail from '../views/CityDetail.vue'

// 定义路由规则：什么路径显示什么组件
const routes = [
  {
    path: '/',           // 根路径
    name: 'Home',        // 路由名称
    component: Home      // 对应的组件
  },
  {
    path: '/travel',
    name: 'TravelPlan',
    component: TravelPlan
  },
  {
    path: '/search',
    name: 'ImageSearch',
    component: ImageSearch
  },
  {
    path: '/profile',
    name: 'MyProfile',
    component: MyProfile
  },
  { path: '/city/:id',
    name: 'CityDetail', 
    component: CityDetail
  }
]

// 创建路由实例
const router = createRouter({
  // 使用HTML5 History模式，URL更美观（没有#号）
  history: createWebHistory(),
  routes
})

export default router
