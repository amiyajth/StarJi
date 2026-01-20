<template>
  <button
    @click="toggleTheme"
    class="theme-toggle"
    :class="{ 'is-light': !isDark }"
    :title="isDark ? '切换到白天模式' : '切换到夜间模式'"
  >
    <!-- 背景装饰层 -->
    <div class="toggle-bg">
      <!-- 夜间装饰（星星 + 月亮） -->
      <div class="night-side">
        <span class="moon">🌙</span>
        <span class="star star-1">✦</span>
        <span class="star star-2">·</span>
        <span class="star star-3">✧</span>
      </div>
      
      <!-- 白天装饰（太阳 + 云朵） -->
      <div class="day-side">
        <span class="sun">☀️</span>
        <span class="cloud cloud-1">☁️</span>
        <span class="cloud cloud-2">☁️</span>
      </div>
    </div>

    <!-- 滑动圆球 -->
    <div class="toggle-knob">
      <div class="knob-face">
        <!-- 夜间：显示月亮表面 -->
        <div class="moon-face" v-if="isDark">
          <span class="crater crater-1"></span>
          <span class="crater crater-2"></span>
        </div>
        <!-- 白天：显示太阳光芒 -->
        <div class="sun-face" v-else>
          <span class="ray"></span>
        </div>
      </div>
    </div>
  </button>
</template>

<script setup>
import { useTheme } from '../composables/useTheme'

const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
.theme-toggle {
  position: relative;
  width: 72px;
  height: 32px;
  border-radius: 16px;
  border: none;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.2);
}

.theme-toggle.is-light {
  background: linear-gradient(135deg, #87CEEB 0%, #98D8E8 50%, #B0E2FF 100%);
  box-shadow: 
    inset 0 2px 4px rgba(255, 255, 255, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 背景装饰层 */
.toggle-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

/* 夜间装饰 */
.night-side {
  position: absolute;
  left: 4px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 24px;
  opacity: 1;
  transition: all 0.5s ease;
}

.is-light .night-side {
  opacity: 0;
  transform: translateY(-150%);
}

.moon {
  position: absolute;
  left: 2px;
  top: 2px;
  font-size: 12px;
  filter: drop-shadow(0 0 4px rgba(255, 255, 200, 0.6));
}

.star {
  position: absolute;
  color: #fff;
  font-size: 8px;
  animation: twinkle 2s ease-in-out infinite;
}

.star-1 {
  right: 2px;
  top: 0;
  animation-delay: 0s;
}

.star-2 {
  right: 10px;
  bottom: 2px;
  font-size: 6px;
  animation-delay: 0.5s;
}

.star-3 {
  right: 0;
  bottom: 4px;
  font-size: 7px;
  animation-delay: 1s;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* 白天装饰 */
.day-side {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(150%);
  width: 32px;
  height: 24px;
  opacity: 0;
  transition: all 0.5s ease;
}

.is-light .day-side {
  opacity: 1;
  transform: translateY(-50%);
}

.sun {
  position: absolute;
  right: 2px;
  top: 2px;
  font-size: 12px;
  filter: drop-shadow(0 0 6px rgba(255, 200, 50, 0.8));
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.cloud {
  position: absolute;
  font-size: 10px;
  opacity: 0.9;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.cloud-1 {
  left: 0;
  top: 4px;
  animation: float 3s ease-in-out infinite;
}

.cloud-2 {
  left: 8px;
  bottom: 0;
  font-size: 8px;
  animation: float 4s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(3px); }
}

/* 滑动圆球 */
.toggle-knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: linear-gradient(145deg, #e8e8e8, #ffffff);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1),
    inset 0 2px 4px rgba(255, 255, 255, 0.8);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 夜间：圆球在右边 */
.theme-toggle:not(.is-light) .toggle-knob {
  left: calc(100% - 29px);
  background: linear-gradient(145deg, #f5f5dc, #fffacd);
  box-shadow: 
    0 0 12px rgba(255, 255, 200, 0.6),
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1);
}

/* 白天：圆球在左边 */
.is-light .toggle-knob {
  left: 3px;
  background: linear-gradient(145deg, #FFD700, #FFA500);
  box-shadow: 
    0 0 16px rgba(255, 200, 50, 0.8),
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.knob-face {
  width: 100%;
  height: 100%;
  position: relative;
}

/* 月亮表面（陨石坑） */
.moon-face {
  width: 100%;
  height: 100%;
  position: relative;
}

.crater {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
}

.crater-1 {
  width: 6px;
  height: 6px;
  top: 6px;
  left: 8px;
}

.crater-2 {
  width: 4px;
  height: 4px;
  bottom: 8px;
  right: 6px;
}

/* 太阳光芒 */
.sun-face {
  width: 100%;
  height: 100%;
  position: relative;
}

.ray {
  position: absolute;
  inset: 4px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
}
</style>
