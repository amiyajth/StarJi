<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-space-900/80 backdrop-blur-sm border-b border-white/5">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2">
          <span class="text-2xl text-star">✦</span>
          <span class="text-xl font-bold gradient-text">星迹</span>
        </router-link>

        <!-- 菜单：去掉emoji，纯文字 -->
        <div class="flex items-center space-x-8">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ 'nav-item-active': isActive(item.path) }"
          >
            {{ item.name }}
          </router-link>
        </div>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = [
  { name: '首页', path: '/' },
  { name: '旅行规划', path: '/travel' },
  { name: '搜图识景', path: '/search' },
  { name: '我的', path: '/profile' }
]

const isActive = (path) => route.path === path
</script>

<style scoped>
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
