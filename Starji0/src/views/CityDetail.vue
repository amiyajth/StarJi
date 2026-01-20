<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto">
      
      <!-- 加载中 -->
      <div v-if="loading" class="text-center text-gray-400">
        <div class="w-12 h-12 mx-auto mb-4 rounded-full border border-white/10 flex items-center justify-center animate-pulse">
          <span class="text-gray-500">◇</span>
        </div>
        加载中...
      </div>

      <!-- 城市详情 -->
      <div v-else-if="city" class="glass rounded-2xl overflow-hidden">
        <!-- 城市图片 -->
        <div class="relative h-64 md:h-80 overflow-hidden">
          <img 
            :src="cityImage" 
            :alt="city.name"
            class="w-full h-full object-cover"
          />
          <!-- 加强遮罩 -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
          
          <!-- 城市名称叠加在图片上 -->
          <div class="absolute bottom-6 left-8">
            <h1 class="text-4xl font-bold text-white drop-shadow-lg">{{ city.name }}</h1>
            <p class="text-gray-200 mt-2">{{ city.province }}</p>
          </div>
        </div>
        
        <!-- 城市信息 -->
        <div class="p-8">
          <!-- 评分和热度 -->
          <div class="flex items-center gap-6 mb-6">
            <div class="flex items-center gap-2">
              <span class="text-yellow-400">★</span>
              <span class="text-white font-medium">{{ city.rating }}</span>
            </div>
            <div class="h-4 w-px bg-white/20"></div>
            <div class="text-gray-400">
              热度: {{ city.popularity }}
            </div>
          </div>

          <!-- 标签 -->
          <div class="flex flex-wrap gap-2 mb-6">
            <span 
              v-for="tag in cityTags" 
              :key="tag"
              class="px-3 py-1.5 rounded-full text-sm bg-nebula-500/20 text-nebula-300 border border-nebula-500/30"
            >
              {{ tag }}
            </span>
          </div>

          <!-- 描述 -->
          <p class="text-gray-300 leading-relaxed mb-8 text-lg">
            {{ city.description }}
          </p>

          <!-- 操作按钮 -->
          <div class="flex gap-4">
            <button 
              @click="goBack"
              class="px-6 py-3 rounded-lg border border-white/20 text-gray-300 hover:bg-white/10 transition-colors"
            >
              ← 返回
            </button>
            <button 
              @click="startPlan"
              class="px-6 py-3 rounded-lg bg-gradient-to-r from-nebula-600 to-nebula-500 text-white hover:from-nebula-500 hover:to-nebula-400 transition-all"
            >
              开始规划旅行 →
            </button>
          </div>
        </div>
      </div>

      <!-- 未找到 -->
      <div v-else class="text-center text-gray-400">
        <div class="text-4xl mb-4">🗺️</div>
        未找到该城市
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCityById } from '../api/city'

const route = useRoute()
const router = useRouter()

const city = ref(null)
const loading = ref(true)

// ✨ 处理图片URL，确保加载正常
const processImageUrl = (url) => {
  if (!url) {
    return 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80'
  }
  
  // 如果是 Unsplash 图片，确保有参数
  if (url.includes('unsplash.com') && !url.includes('?')) {
    return `${url}?w=800&q=80`
  }
  
  // 如果是 picsum 随机图，替换成默认图
  if (url.includes('picsum.photos') || url.includes('random')) {
    return 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80'
  }
  
  return url
}

// ✨ 获取城市图片
const cityImage = computed(() => {
  if (!city.value) return ''
  return processImageUrl(city.value.image)
})

// 解析标签
const cityTags = computed(() => {
  if (!city.value || !city.value.tags) return []
  return city.value.tags.split(',')
})

// 获取城市详情
const fetchCity = async () => {
  const cityId = route.params.id
  loading.value = true
  
  try {
    const data = await getCityById(cityId)
    city.value = data
    console.log('获取城市详情：', data)
  } catch (error) {
    console.error('获取城市详情失败：', error)
    city.value = null
  } finally {
    loading.value = false
  }
}

// 返回首页
const goBack = () => {
  router.push('/')
}

// 开始规划
const startPlan = () => {
  router.push({
    path: '/travel-plan',
    query: { 
      origin: '',
      destination: city.value?.name 
    }
  })
}

onMounted(() => {
  fetchCity()
})
</script>
