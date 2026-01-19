<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-space-900/80 backdrop-blur-sm border-b border-white/5">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        
        <!-- Logo（不动） -->
        <router-link to="/" class="flex items-center space-x-2">
          <span class="text-2xl text-star">✦</span>
          <span class="text-xl font-bold gradient-text">星迹</span>
        </router-link>

        <!-- 菜单区域 -->
        <div class="flex items-center space-x-8">
          <!-- 前 3 项固定菜单 -->
          <router-link
            v-for="item in fixedMenuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ 'nav-item-active': isActive(item.path) }"
          >
            {{ item.name }}
          </router-link>

          <!-- ✨ 最后一项：根据登录态切换 -->
          <router-link
            v-if="isLoggedIn"
            to="/profile"
            class="nav-item"
            :class="{ 'nav-item-active': isActive('/profile') }"
          >
            我的
          </router-link>
          <router-link
            v-else
            to="/login"
            class="nav-item"
            :class="{ 'nav-item-active': isActive('/login') }"
          >
            登录
          </router-link>
        </div>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// ✨ 前 3 项固定不变
const fixedMenuItems = [
  { name: '首页', path: '/' },
  { name: '旅行规划', path: '/travel-plan' },
  { name: '搜图识景', path: '/search' }
]

const isActive = (path) => route.path === path

// ✨ 登录状态判断
const isLoggedIn = ref(false)

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

onMounted(checkLoginStatus)
watch(() => route.path, checkLoginStatus)
</script>

<style scoped>
/* ✅ 样式完全不动 */
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
</style>
