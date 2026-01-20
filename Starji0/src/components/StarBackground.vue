<template>
  <div class="fixed inset-0 overflow-hidden pointer-events-none transition-all duration-1000">
    
    <!-- ============ 夜间背景 ============ -->
    <div 
      class="absolute inset-0 transition-opacity duration-1000"
      :class="isDark ? 'opacity-100' : 'opacity-0'"
    >
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

    <!-- ============ 白天背景 ============ -->
    <div 
      class="absolute inset-0 transition-opacity duration-1000"
      :class="isDark ? 'opacity-0' : 'opacity-100'"
    >
      <!-- 天空渐变 -->
      <div class="absolute inset-0 bg-gradient-to-b from-sky-300 via-sky-200 to-blue-100"></div>
      
      <!-- 太阳 -->
      <div class="sun-glow"></div>
      
      <!-- 阳光光线 -->
      <div class="sun-rays"></div>
      
      <!-- 飘动的云朵 -->
      <div
        v-for="cloud in clouds"
        :key="cloud.id"
        class="cloud"
        :style="{
          left: cloud.x + '%',
          top: cloud.y + '%',
          width: cloud.width + 'px',
          opacity: cloud.opacity,
          animationDuration: cloud.duration + 's',
          animationDelay: cloud.delay + 's'
        }"
      >
        <div class="cloud-body"></div>
      </div>
      
      <!-- 远处的山/地平线装饰（可选） -->
      <div class="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-blue-200/30 to-transparent"></div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTheme } from '../composables/useTheme'

const { isDark } = useTheme()

// 夜间星星
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

// 白天云朵
const clouds = ref([])
for (let i = 0; i < 8; i++) {
  clouds.value.push({
    id: i,
    x: Math.random() * 120 - 10,
    y: Math.random() * 40 + 10,
    width: Math.random() * 100 + 80,
    opacity: Math.random() * 0.4 + 0.4,
    duration: Math.random() * 40 + 60,
    delay: Math.random() * 20
  })
}
</script>

<style scoped>
/* 星星闪烁动画 */
@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* ============ 白天样式 ============ */

/* 太阳光晕 */
.sun-glow {
  position: absolute;
  top: 8%;
  right: 15%;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: radial-gradient(circle, 
    rgba(255, 255, 200, 1) 0%, 
    rgba(255, 220, 100, 0.8) 30%, 
    rgba(255, 200, 50, 0.4) 60%, 
    transparent 100%
  );
  box-shadow: 
    0 0 60px rgba(255, 200, 50, 0.6),
    0 0 120px rgba(255, 200, 50, 0.4),
    0 0 200px rgba(255, 200, 50, 0.2);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
}

/* 太阳光线 */
.sun-rays {
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 60%;
  background: radial-gradient(
    ellipse at top right,
    rgba(255, 255, 200, 0.3) 0%,
    rgba(255, 220, 150, 0.1) 40%,
    transparent 70%
  );
  pointer-events: none;
}

/* 云朵 */
.cloud {
  position: absolute;
  animation: floatCloud linear infinite;
}

@keyframes floatCloud {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(calc(100vw + 100%)); }
}

.cloud-body {
  position: relative;
  width: 100%;
  height: 40px;
  background: white;
  border-radius: 40px;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.05),
    inset 0 -4px 8px rgba(0, 0, 0, 0.02);
}

.cloud-body::before {
  content: '';
  position: absolute;
  top: -20px;
  left: 25%;
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 50%;
}

.cloud-body::after {
  content: '';
  position: absolute;
  top: -30px;
  left: 45%;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
}
</style>
