<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-6xl mx-auto">
      
      <!-- 头部 -->
      <header class="text-center mb-20">
        <h1 class="text-6xl md:text-7xl font-bold mb-6">
          <span class="gradient-text">星迹</span>
        </h1>
        <p class="text-lg text-gray-400 font-light tracking-wider mb-4">
          万籁尽收眼底，众星皆是归途
        </p>
        <p class="text-sm text-gray-600 max-w-md mx-auto leading-relaxed">
          在群星的俯瞰下，交付独属你的那一行诗
        </p>
      </header>

      <!-- 搜索区 -->
      <section id="planner" class="mb-24">
        <div class="glass rounded-2xl p-8 max-w-2xl mx-auto">
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1">
              <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">出发地</label>
              <input 
                v-model="origin" 
                type="text" 
                placeholder="你在哪里" 
                class="search-input" 
              />
            </div>
            <div class="hidden md:flex items-end pb-3 text-gray-600">→</div>
            <div class="flex-1">
              <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">目的地</label>
              <input 
                v-model="destination" 
                type="text" 
                placeholder="想去哪里" 
                class="search-input" 
              />
            </div>
            <div class="flex items-end">
              <button class="search-btn" @click="handleExplore">开始探索</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 热门城市 -->
      <section>
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-xl font-medium text-gray-300">热门目的地</h2>
          <a href="#" class="text-gray-500 hover:text-gray-300 text-sm transition-colors">查看更多 →</a>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CityCard v-for="city in hotCities" :key="city.id" :city="city" @select="handleCitySelect" />
        </div>
      </section>

      <!-- ✨ 优化后的功能介绍 -->
      <section class="mt-32">
        <div class="text-center mb-16">
          <h2 class="text-xl font-medium text-gray-300 mb-3">星迹能为你做什么</h2>
          <p class="text-sm text-gray-600">每一次旅行，都是在星空下留下自己的足迹</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="feature.title"
            class="feature-card group cursor-pointer"
            @click="handleFeatureClick(feature)"
          >
            <!-- 图标容器 -->
            <div class="icon-wrapper">
              <!-- 背景光晕 -->
              <div class="icon-glow" :class="`glow-${index + 1}`"></div>
              <!-- 外圈 -->
              <div class="icon-ring">
                <!-- SVG 图标 -->
                <svg v-if="index === 0" class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <!-- 指南针 -->
                  <circle cx="12" cy="12" r="10" stroke-width="1"/>
                  <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke-width="1"/>
                  <path d="M12 8l2 4-2 4-2-4 2-4z" fill="currentColor" stroke="none"/>
                </svg>
                <svg v-else-if="index === 1" class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <!-- 眼睛/视觉 -->
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="1"/>
                  <circle cx="12" cy="12" r="3" stroke-width="1"/>
                  <circle cx="12" cy="12" r="1" fill="currentColor"/>
                </svg>
                <svg v-else class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <!-- 用户/画像 -->
                  <circle cx="12" cy="8" r="4" stroke-width="1"/>
                  <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke-width="1"/>
                  <path d="M12 14v2M9 18h6" stroke-width="1" opacity="0.5"/>
                </svg>
              </div>
            </div>

            <!-- 文字内容 -->
            <div class="text-center mt-8">
              <p class="text-xs text-gray-600 uppercase tracking-widest mb-2">{{ feature.subtitle }}</p>
              <h3 class="text-lg font-medium text-gray-200 mb-4 group-hover:text-white transition-colors">
                {{ feature.title }}
              </h3>
              <p class="text-gray-500 text-sm leading-relaxed">{{ feature.poetic }}</p>
            </div>

            <!-- 底部装饰线 -->
            <div class="card-line"></div>
          </div>
        </div>
      </section>

      <!-- 底部留白装饰 -->
      <footer class="mt-32 text-center">
        <div class="flex justify-center space-x-3 text-gray-700">
          <span>✦</span>
          <span>✧</span>
          <span>✦</span>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import CityCard from '../components/CityCard.vue'
import { getCities } from '../api/city'

const router = useRouter()

const hotCities = ref([])
const origin = ref('')
const destination = ref('')
const loading = ref(false)
const isLoggedIn = computed(() => !!localStorage.getItem('token'))

const fetchCities = async () => {
  loading.value = true
  try {
    const data = await getCities()
    hotCities.value = data.map(city => ({
      id: city.id,
      name: city.name,
      image: city.image || 'https://picsum.photos/400/300?random=' + city.id,
      description: city.description,
      tags: city.tags ? city.tags.split(',') : []
    }))
    console.log('成功获取城市数据：', hotCities.value)
  } catch (error) {
    console.error('获取城市失败：', error)
    hotCities.value = [
      { id: 1, name: '重庆', image: 'https://picsum.photos/400/300?random=1', description: '数据加载失败', tags: ['暂无'] }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCities()
})

const features = [
  { 
    title: '旅行规划', 
    subtitle: 'The Compass',
    poetic: '执笔经纬，在时空的平仄里，裁出最合身的归途。'
  },
  { 
    title: '搜图识景', 
    subtitle: 'The Vision',
    poetic: '指尖触碰流光，让每一场不期而遇，都有迹可循。'
  },
  { 
    title: '我的画像', 
    subtitle: 'The Echo',
    poetic: '拾起散落的星屑，于万千偏好中，回响出你的灵魂轮廓。'
  }
]

const handleCitySelect = (city) => {
  console.log('选中城市:', city.name)
  router.push(`/city/${city.id}`)  
}

const handleExplore = () => {
  if (!origin.value.trim() || !destination.value.trim()) {
    alert('请输入出发地和目的地')
    return
  }
  
  router.push({
    path: '/travel-plan',
    query: {
      origin: origin.value,
      destination: destination.value
    }
  })
}

const handleFeatureClick = (feature) => {
  if (feature?.title === '旅行规划') {
    const el = document.getElementById('planner')
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }
  if (feature?.title === '搜图识景') {
    router.push('/search')
    return
  }
  if (feature?.title === '我的画像') {
    router.push('/profile')
    return
  }
}
</script>

<style scoped>
.search-input {
  @apply w-full px-4 py-3 rounded-lg;
  @apply bg-white/[0.03] border border-white/[0.06];
  @apply text-white placeholder-gray-600;
  @apply focus:outline-none focus:border-white/20 focus:bg-white/[0.05];
  @apply transition-all duration-300;
}

.search-btn {
  @apply px-8 py-3 rounded-lg;
  @apply bg-gradient-to-r from-nebula-600 to-nebula-500;
  @apply text-white text-sm font-medium tracking-wide;
  @apply hover:from-nebula-500 hover:to-nebula-400;
  @apply transition-all duration-300;
}

/* ✨ 功能卡片 */
.feature-card {
  @apply relative p-8 rounded-2xl;
  @apply bg-white/[0.01] border border-white/[0.04];
  @apply hover:bg-white/[0.03] hover:border-white/[0.08];
  @apply transition-all duration-500;
  @apply hover:-translate-y-2;
}

/* 图标容器 */
.icon-wrapper {
  @apply relative w-24 h-24 mx-auto;
}

/* 背景光晕 */
.icon-glow {
  @apply absolute inset-0 rounded-full opacity-0;
  @apply group-hover:opacity-100;
  @apply transition-opacity duration-700;
  filter: blur(20px);
}

.glow-1 {
  background: radial-gradient(circle, rgba(167, 139, 250, 0.3) 0%, transparent 70%);
}

.glow-2 {
  background: radial-gradient(circle, rgba(96, 165, 250, 0.3) 0%, transparent 70%);
}

.glow-3 {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.2) 0%, transparent 70%);
}

/* 图标外圈 */
.icon-ring {
  @apply absolute inset-2;
  @apply rounded-full;
  @apply border border-white/10;
  @apply flex items-center justify-center;
  @apply group-hover:border-white/20;
  @apply transition-all duration-500;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.05) 0%, transparent 60%);
}

.feature-card:hover .icon-ring {
  @apply scale-110;
  box-shadow: 
    0 0 20px rgba(167, 139, 250, 0.1),
    inset 0 0 20px rgba(255, 255, 255, 0.02);
}

/* SVG 图标 */
.icon-svg {
  @apply w-10 h-10;
  @apply text-gray-500;
  @apply group-hover:text-gray-300;
  @apply transition-all duration-500;
}

.feature-card:nth-child(1):hover .icon-svg {
  @apply text-purple-400;
}

.feature-card:nth-child(2):hover .icon-svg {
  @apply text-blue-400;
}

.feature-card:nth-child(3):hover .icon-svg {
  @apply text-amber-400;
}

/* 底部装饰线 */
.card-line {
  @apply absolute bottom-0 left-1/2 -translate-x-1/2;
  @apply w-0 h-[1px];
  @apply group-hover:w-1/2;
  @apply transition-all duration-500;
  background: linear-gradient(90deg, transparent, rgba(167, 139, 250, 0.5), transparent);
}

/* 呼吸动画 */
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

.feature-card:hover .icon-glow {
  animation: breathe 3s ease-in-out infinite;
}
</style>
