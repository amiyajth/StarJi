<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto">
      <!-- 头部 -->
      <div class="text-center mb-12">
        <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">The Compass</p>
        <h1 class="text-2xl font-medium text-gray-200 mb-4">旅行规划</h1>
        <p class="text-gray-500 text-sm" v-if="origin && destination">
          {{ origin }} → {{ destination }}
        </p>
        <p class="text-gray-500 text-sm" v-else>
          执笔经纬，在时空的平仄里，裁出最合身的归途
        </p>
      </div>

      <!-- 无参数时显示输入框 -->
      <div v-if="showInputForm" class="glass rounded-2xl p-8 max-w-2xl mx-auto mb-12">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">出发地</label>
            <input 
              v-model="inputOrigin" 
              type="text" 
              placeholder="你在哪里" 
              class="search-input" 
            />
          </div>
          <div class="hidden md:flex items-end pb-3 text-gray-600">→</div>
          <div class="flex-1">
            <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">目的地</label>
            <input 
              v-model="inputDestination" 
              type="text" 
              placeholder="想去哪里" 
              class="search-input" 
            />
          </div>
          <div class="flex items-end">
            <button class="search-btn" @click="startPlan">开始规划</button>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else-if="loading" class="rounded-xl border border-white/[0.06] p-16 text-center">
        <div class="w-16 h-16 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center animate-pulse">
          <span class="text-gray-500 text-xl">◇</span>
        </div>
        <p class="text-gray-400 text-sm mb-2">AI 正在为你规划行程...</p>
        <p class="text-gray-600 text-xs">这可能需要 1~3 分钟，请耐心等待</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="rounded-xl border border-red-500/20 p-8 text-center">
        <p class="text-red-400 text-sm mb-4">{{ error }}</p>
        <button @click="handleGenerate" class="px-6 py-2 rounded-lg bg-white/10 text-gray-300 text-sm hover:bg-white/20 transition">
          重新生成
        </button>
      </div>

      <!-- 行程内容 -->
      <div v-else-if="tripContent" class="rounded-xl border border-white/[0.06] p-8">
        <div class="prose prose-invert prose-sm max-w-none" v-html="renderedContent"></div>
      </div>

      <!-- 返回按钮 -->
      <div class="mt-8 text-center">
        <button @click="$router.push('/')" class="text-gray-500 text-sm hover:text-gray-300 transition">
          ← 返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { createTrip, generateTrip } from '../api/trip'

const route = useRoute()

const origin = ref(route.query.origin || '')
const destination = ref(route.query.destination || '')
const inputOrigin = ref('')
const inputDestination = ref('')

const loading = ref(false)
const error = ref('')
const tripContent = ref('')

const showInputForm = computed(() => {
  return !origin.value && !destination.value && !loading.value && !tripContent.value && !error.value
})

const startPlan = () => {
  if (!inputOrigin.value.trim() || !inputDestination.value.trim()) {
    error.value = '请输入出发地和目的地'
    return
  }
  origin.value = inputOrigin.value.trim()
  destination.value = inputDestination.value.trim()
  handleGenerate()
}

const renderedContent = computed(() => {
  if (!tripContent.value) return ''
  
  return tripContent.value
    .replace(/^### (.+)$/gm, '<h3 class="text-lg font-medium text-gray-200 mt-6 mb-3">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="text-xl font-medium text-gray-100 mt-8 mb-4">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="text-2xl font-bold text-white mt-8 mb-4">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-gray-200">$1</strong>')
    .replace(/^\* (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    .replace(/^- (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    .replace(/\n\n/g, '</p><p class="text-gray-400 mb-4">')
    .replace(/\n/g, '<br>')
})

const handleGenerate = async () => {
  if (!origin.value || !destination.value) {
    error.value = '缺少出发地或目的地信息'
    return
  }

  loading.value = true
  error.value = ''
  tripContent.value = ''

  try {
    const today = new Date()
    const startDate = new Date(today)
    startDate.setDate(today.getDate() + 1)
    const endDate = new Date(startDate)
    endDate.setDate(startDate.getDate() + 2)

    const formatDate = (date) => date.toISOString().split('T')[0]

    console.log('正在创建行程...')
    const trip = await createTrip({
      title: `${origin.value} → ${destination.value} 之旅`,
      origin: origin.value,
      destination: destination.value,
      start_date: formatDate(startDate),
      end_date: formatDate(endDate)
    })
    console.log('行程创建成功：', trip)

    console.log('正在调用 AI 生成行程内容...')
    const result = await generateTrip(trip.id, 'agent')
    console.log('AI 生成完成：', result)

    tripContent.value = result.content || ''

  } catch (err) {
    console.error('生成失败：', err)
    if (err.response?.status === 401) {
      error.value = '请先登录后再使用此功能'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = '生成行程失败，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (origin.value && destination.value) {
    handleGenerate()
  }
})
</script>

<style scoped>
.prose h1, .prose h2, .prose h3 {
  color: inherit;
}

.prose li {
  list-style-type: disc;
}

.glass {
  @apply bg-white/[0.02] border border-white/[0.06];
  @apply backdrop-blur;
}

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
</style>
