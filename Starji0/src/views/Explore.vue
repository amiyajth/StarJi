<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-6xl mx-auto">
      
      <!-- 页面标题 -->
      <header class="text-center mb-12">
        <h1 class="text-4xl font-bold text-white mb-4">
          探索目的地
        </h1>
        <p class="text-gray-400 text-lg">
          发现你的下一段旅程，让星迹为你指引方向
        </p>
      </header>

      <!-- 搜索和筛选区 -->
      <div class="glass rounded-2xl p-6 mb-10">
        <div class="flex flex-col lg:flex-row gap-4">
          
          <!-- 搜索框 -->
          <div class="flex-1">
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="搜索城市名称..."
                class="search-input pl-10"
              />
              <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
          </div>

          <!-- 地区筛选 -->
          <div class="flex gap-2 flex-wrap">
            <button 
              v-for="region in regions" 
              :key="region.value"
              @click="selectedRegion = region.value"
              class="filter-btn"
              :class="selectedRegion === region.value ? 'filter-btn-active' : ''"
            >
              {{ region.label }}
            </button>
          </div>

          <!-- 排序 -->
          <select v-model="sortBy" class="sort-select">
            <option value="popularity">按热度</option>
            <option value="rating">按评分</option>
            <option value="name">按名称</option>
          </select>
        </div>

        <!-- 标签筛选 -->
        <div class="mt-4 pt-4 border-t border-white/10">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-gray-500 text-sm">标签：</span>
            <button 
              v-for="tag in allTags" 
              :key="tag"
              @click="toggleTag(tag)"
              class="tag-btn"
              :class="selectedTags.includes(tag) ? 'tag-btn-active' : ''"
            >
              {{ tag }}
            </button>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="flex items-center justify-between mb-6">
        <p class="text-gray-400 text-sm">
          共找到 <span class="text-white font-medium">{{ filteredCities.length }}</span> 个目的地
        </p>
        <button 
          v-if="hasFilters"
          @click="clearFilters"
          class="text-nebula-400 hover:text-nebula-300 text-sm transition-colors"
        >
          清除筛选
        </button>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="text-center py-20">
        <div class="w-12 h-12 mx-auto mb-4 rounded-full border border-white/10 flex items-center justify-center animate-pulse">
          <span class="text-gray-500">◇</span>
        </div>
        <p class="text-gray-400">加载中...</p>
      </div>

      <!-- 城市网格 -->
      <div v-else-if="filteredCities.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CityCard 
          v-for="city in filteredCities" 
          :key="city.id" 
          :city="city" 
          @select="handleCitySelect"
        />
      </div>

      <!-- 无结果 -->
      <div v-else class="text-center py-20">
        <div class="text-5xl mb-4">🔍</div>
        <p class="text-gray-400 mb-2">没有找到匹配的城市</p>
        <p class="text-gray-600 text-sm">试试其他关键词或筛选条件</p>
      </div>

      <!-- 返回首页 -->
      <div class="text-center mt-16">
        <router-link 
          to="/"
          class="inline-flex items-center gap-2 text-gray-500 hover:text-gray-300 transition-colors"
        >
          <span>←</span>
          <span>返回首页</span>
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CityCard from '../components/CityCard.vue'
import { getCities } from '../api/city'

const router = useRouter()

// 状态
const allCities = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedRegion = ref('all')
const selectedTags = ref([])
const sortBy = ref('popularity')

// 地区选项
const regions = [
  { label: '全部', value: 'all' },
  { label: '华东', value: '华东' },
  { label: '华南', value: '华南' },
  { label: '华北', value: '华北' },
  { label: '西南', value: '西南' },
  { label: '西北', value: '西北' },
  { label: '东北', value: '东北' },
]

// 省份到地区的映射
const provinceToRegion = {
  // 华东
  '上海市': '华东', '江苏省': '华东', '浙江省': '华东', 
  '安徽省': '华东', '福建省': '华东', '江西省': '华东', '山东省': '华东',
  // 华南
  '广东省': '华南', '广西壮族自治区': '华南', '海南省': '华南',
  // 华北
  '北京市': '华北', '天津市': '华北', '河北省': '华北', 
  '山西省': '华北', '内蒙古自治区': '华北',
  // 西南
  '重庆市': '西南', '四川省': '西南', '贵州省': '西南', 
  '云南省': '西南', '西藏自治区': '西南',
  // 西北
  '陕西省': '西北', '甘肃省': '西北', '青海省': '西北', 
  '宁夏回族自治区': '西北', '新疆维吾尔自治区': '西北',
  // 东北
  '辽宁省': '东北', '吉林省': '东北', '黑龙江省': '东北',
  // 中部（归入华东）
  '河南省': '华东', '湖北省': '华东', '湖南省': '华南',
}

// 所有标签（从城市数据中提取）
const allTags = computed(() => {
  const tags = new Set()
  allCities.value.forEach(city => {
    city.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags).slice(0, 12) // 最多显示12个
})

// 是否有筛选条件
const hasFilters = computed(() => {
  return searchQuery.value || selectedRegion.value !== 'all' || selectedTags.value.length > 0
})

// 处理图片URL
const processImageUrl = (url) => {
  if (!url) {
    return 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80'
  }
  if (url.includes('unsplash.com') && !url.includes('?')) {
    return `${url}?w=800&q=80`
  }
  if (url.includes('picsum.photos') || url.includes('random')) {
    return 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80'
  }
  return url
}

// 筛选后的城市
const filteredCities = computed(() => {
  let result = [...allCities.value]
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(city => 
      city.name.toLowerCase().includes(query) ||
      city.province.toLowerCase().includes(query) ||
      city.description.toLowerCase().includes(query)
    )
  }
  
  // 地区过滤
  if (selectedRegion.value !== 'all') {
    result = result.filter(city => {
      const region = provinceToRegion[city.province]
      return region === selectedRegion.value
    })
  }
  
  // 标签过滤
  if (selectedTags.value.length > 0) {
    result = result.filter(city => 
      selectedTags.value.some(tag => city.tags.includes(tag))
    )
  }
  
  // 排序
  result.sort((a, b) => {
    if (sortBy.value === 'popularity') {
      return b.popularity - a.popularity
    } else if (sortBy.value === 'rating') {
      return b.rating - a.rating
    } else {
      return a.name.localeCompare(b.name, 'zh-CN')
    }
  })
  
  return result
})

// 获取城市数据
const fetchCities = async () => {
  loading.value = true
  try {
    const data = await getCities()
    allCities.value = data.map(city => ({
      id: city.id,
      name: city.name,
      province: city.province,
      image: processImageUrl(city.image),
      description: city.description,
      tags: city.tags ? city.tags.split(',') : [],
      rating: city.rating || 0,
      popularity: city.popularity || 0
    }))
    console.log('获取城市数据：', allCities.value)
  } catch (error) {
    console.error('获取城市失败：', error)
  } finally {
    loading.value = false
  }
}

// 切换标签
const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
}

// 清除筛选
const clearFilters = () => {
  searchQuery.value = ''
  selectedRegion.value = 'all'
  selectedTags.value = []
}

// 选择城市
const handleCitySelect = (city) => {
  router.push(`/city/${city.id}`)
}

onMounted(() => {
  fetchCities()
})
</script>

<style scoped>
.search-input {
  @apply w-full pl-12 pr-4 py-3 rounded-lg; 
  @apply text-white placeholder-gray-600;
  @apply focus:outline-none;
  @apply transition-all duration-300;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.filter-btn {
  @apply px-4 py-2 rounded-lg text-sm;
  @apply text-gray-400 hover:text-white;
  @apply transition-all duration-300;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filter-btn-active {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.4);
  color: #c4b5fd;
}

.tag-btn {
  @apply px-3 py-1 rounded-full text-xs;
  @apply text-gray-500 hover:text-gray-300;
  @apply transition-all duration-300;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.tag-btn:hover {
  background: rgba(255, 255, 255, 0.08);
}

.tag-btn-active {
  background: rgba(251, 191, 36, 0.2);
  border-color: rgba(251, 191, 36, 0.4);
  color: #fbbf24;
}

.sort-select {
  @apply px-4 py-2 rounded-lg text-sm;
  @apply text-gray-300;
  @apply focus:outline-none;
  @apply transition-all duration-300;
  @apply cursor-pointer;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.sort-select:focus {
  border-color: rgba(255, 255, 255, 0.2);
}

.sort-select option {
  background: #1a1a2e;
  color: #d1d5db;
}
</style>
