<template>
  <div class="fixed inset-0 overflow-hidden pointer-events-none">
    <!-- 渐变背景 -->
    <div class="absolute inset-0 bg-gradient-to-b from-space-900 via-space-700 to-space-800"></div>
    
    <!-- 星云光斑 -->
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-nebula-600/20 rounded-full blur-3xl"></div>
    <div class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-nebula-400/20 rounded-full blur-3xl"></div>
    <div class="absolute top-1/2 right-1/3 w-64 h-64 bg-star/10 rounded-full blur-3xl"></div>
    
    <!-- 动态星星 -->
    <div
      v-for="star in stars"
      :key="star.id"
      class="absolute rounded-full bg-white"
      :style="{
        left: star.x + '%',
        top: star.y + '%',
        width: star.size + 'px',
        height: star.size + 'px',
        opacity: star.opacity,
        animation: `twinkle ${star.duration}s ease-in-out infinite`,
        animationDelay: star.delay + 's'
      }"
    ></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const stars = ref([])

for (let i = 0; i < 50; i++) {
  stars.value.push({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 2 + 1,
    opacity: Math.random() * 0.7 + 0.3,
    duration: Math.random() * 3 + 2,
    delay: Math.random() * 3
  })
}
</script>
