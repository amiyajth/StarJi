<template>
  <nav class="fixed top-0 left-0 right-0 z-50 backdrop-blur-sm border-b transition-colors duration-500"
       :class="isDark ? 'bg-space-900/80 border-white/5' : 'bg-white/70 border-gray-200/50'">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        
        <!-- 左侧：返回按钮 + Logo -->
        <div class="flex items-center space-x-4">
          <!-- 返回按钮（首页时隐藏） -->
          <button
            v-if="showBackButton"
            @click="goBack"
            class="back-btn group"
            title="返回上一页"
          >
            <svg 
              class="w-5 h-5 transition-all duration-300 group-hover:-translate-x-0.5" 
              :class="isDark ? 'text-gray-500 group-hover:text-white' : 'text-gray-400 group-hover:text-gray-800'"
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <!-- Logo -->
          <router-link to="/" class="flex items-center space-x-2">
            <span class="text-2xl" :class="isDark ? 'text-star' : 'text-amber-500'">✦</span>
            <span class="text-xl font-bold" :class="isDark ? 'gradient-text' : 'text-gray-800'">星迹</span>
          </router-link>
        </div>

        <!-- 右侧：菜单 + 主题切换 -->
        <div class="flex items-center space-x-6">
          <!-- 菜单项 -->
          <div class="flex items-center space-x-8">
            <router-link
              v-for="item in fixedMenuItems"
              :key="item.path"
              :to="item.path"
              class="nav-item"
              :class="{ 
                'nav-item-active': isActive(item.path),
                'nav-item-light': !isDark
              }"
            >
              {{ item.name }}
            </router-link>

            <router-link
              v-if="isLoggedIn"
              to="/profile"
              class="nav-item"
              :class="{ 
                'nav-item-active': isActive('/profile'),
                'nav-item-light': !isDark
              }"
            >
              我的
            </router-link>
            <router-link
              v-else
              to="/login"
              class="nav-item"
              :class="{ 
                'nav-item-active': isActive('/login'),
                'nav-item-light': !isDark
              }"
            >
              登录
            </router-link>
          </div>

          <!-- ✨ 主题切换按钮 -->
          <ThemeToggle />
        </div>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTheme } from '../composables/useTheme'
import ThemeToggle from './ThemeToggle.vue'

const route = useRoute()
const router = useRouter()
const { isDark } = useTheme()

const fixedMenuItems = [
  { name: '首页', path: '/' },
  { name: '旅行规划', path: '/travel-plan' },
  { name: '搜图识景', path: '/search' }
]

const isActive = (path) => route.path === path

const isLoggedIn = ref(false)

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

onMounted(checkLoginStatus)
watch(() => route.path, checkLoginStatus)

const showBackButton = computed(() => {
  return route.path !== '/'
})

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
/* 深色模式样式 */
.nav-item {
  @apply text-gray-400 text-sm tracking-wide;
  @apply transition-all duration-300;
  @apply hover:text-white;
  position: relative;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, #a78bfa, #fef3c7);
  transition: width 0.3s ease;
}

.nav-item:hover::after {
  width: 100%;
}

.nav-item-active {
  @apply text-white;
}

.nav-item-active::after {
  width: 100%;
}

/* ✨ 浅色模式样式 */
.nav-item-light {
  @apply text-gray-500;
  @apply hover:text-gray-900;
}

.nav-item-light::after {
  background: linear-gradient(90deg, #6366f1, #f59e0b);
}

.nav-item-light.nav-item-active {
  @apply text-gray-900;
}

/* 返回按钮 */
.back-btn {
  @apply p-2 -ml-2 rounded-lg;
  @apply hover:bg-white/5;
  @apply transition-all duration-300;
  @apply flex items-center justify-center;
}

.back-btn:active {
  @apply scale-95;
}
</style>
