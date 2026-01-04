<template>
  <!-- 整个应用的容器 -->
  <div class="min-h-screen relative">
    
    <!-- 星空背景组件 - 放在最底层 -->
    <StarBackground />
    
    <!-- 导航栏 - 固定在顶部 -->
    <Navbar />
    
    <!-- 主要内容区域 -->
    <main class="relative z-10">
      <!-- 
        router-view: 根据当前URL显示对应的页面组件
        v-slot: 获取当前路由信息，用于过渡动画
      -->
      <router-view v-slot="{ Component }">
        <!-- 页面切换时的过渡动画 -->
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
// 引入子组件
import Navbar from './components/Navbar.vue'
import StarBackground from './components/StarBackground.vue'
</script>
