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
        <button class="text-gray-400 text-sm hover:text-white transition" @click="$router.push('/login')">
  登录
        </button>
      </header>

      <!-- 搜索区 -->
      <section class="mb-24">
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

      <!-- 功能介绍：使用你的文案 -->
      <section class="mt-32">
        <div class="text-center mb-16">
          <h2 class="text-xl font-medium text-gray-300 mb-3">星迹能为你做什么</h2>
          <p class="text-sm text-gray-600">每一次旅行，都是在星空下留下自己的足迹</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div v-for="feature in features" :key="feature.title" class="feature-item text-center group">
            <!-- 图标 -->
            <div class="w-16 h-16 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center group-hover:border-nebula-400/30 transition-all duration-500">
              <span class="text-gray-400 text-xl group-hover:text-nebula-400 transition-colors duration-500">{{ feature.icon }}</span>
            </div>
            <!-- 英文小标 -->
            <p class="text-xs text-gray-600 uppercase tracking-widest mb-2">{{ feature.subtitle }}</p>
            <!-- 中文标题 -->
            <h3 class="text-base font-medium text-gray-200 mb-4">{{ feature.title }}</h3>
            <!-- 诗意文案 -->
            <p class="text-gray-500 text-sm leading-relaxed">{{ feature.poetic }}</p>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CityCard from '../components/CityCard.vue'
import { getCities } from '../api/city'
const router = useRouter()

// 城市列表（从后端获取）
const hotCities = ref([])
const origin = ref('')
const destination = ref('')
// 加载状态
const loading = ref(false)

// 获取城市数据
const fetchCities = async () => {
  loading.value = true
  try {
    const data = await getCities()
    // 转换数据格式，适配CityCard组件
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
    // 失败时用备用数据
    hotCities.value = [
      { id: 1, name: '重庆', image: 'https://picsum.photos/400/300?random=1', description: '数据加载失败', tags: ['暂无'] }
    ]
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCities()
})

// 功能介绍
const features = [
  { 
    icon: '◇', 
    title: '旅行规划', 
    subtitle: 'The Compass',
    poetic: '执笔经纬，在时空的平仄里，裁出最合身的归途。'
  },
  { 
    icon: '○', 
    title: '搜图识景', 
    subtitle: 'The Vision',
    poetic: '指尖触碰流光，让每一场不期而遇，都有迹可循。'
  },
  { 
    icon: '△', 
    title: '我的画像', 
    subtitle: 'The Echo',
    poetic: '拾起散落的星屑，于万千偏好中，回响出你的灵魂轮廓。'
  }
]

const handleCitySelect = (city) => {
  console.log('选中城市:', city.name)
  router.push(`/city/${city.id}`)  
}
// 开始探索 → 跳转到旅行规划页
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

.feature-item {
  @apply p-6 rounded-2xl;
  @apply hover:bg-white/[0.02];
  @apply transition-all duration-500;
}
</style>
