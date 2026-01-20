<template>
  <!-- ✨ 添加主题 class -->
  <div 
    class="min-h-screen relative transition-colors duration-500"
    :class="isDark ? 'theme-dark' : 'theme-light'"
  >
    
    <!-- 星空背景组件 -->
    <StarBackground />
    
    <!-- 导航栏 -->
    <Navbar />
    
    <!-- 主要内容区域 -->
    <main class="relative z-10">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import StarBackground from './components/StarBackground.vue'
import { useTheme } from './composables/useTheme'

const { isDark } = useTheme()
</script>

<style>
/* 页面切换动画 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
