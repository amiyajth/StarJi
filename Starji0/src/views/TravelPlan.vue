<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto">
      <!-- 头部 -->
      <div class="text-center mb-12">
        <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">The Compass</p>
        <h1 class="text-2xl font-medium text-gray-200 mb-4">旅行规划</h1>
        <p class="text-gray-500 text-sm">
          {{ origin }} → {{ destination }}
        </p>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="rounded-xl border border-white/[0.06] p-16 text-center">
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

      <!-- 空状态（不应该出现） -->
      <div v-else class="rounded-xl border border-white/[0.06] p-16 text-center">
        <p class="text-gray-600 text-sm">正在准备...</p>
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

// 从 URL 参数读取出发地和目的地
const origin = ref(route.query.origin || '')
const destination = ref(route.query.destination || '')

// 状态
const loading = ref(false)
const error = ref('')
const tripContent = ref('')

// 简单的 Markdown 渲染（把 # 标题和换行处理一下）
const renderedContent = computed(() => {
  if (!tripContent.value) return ''
  
  return tripContent.value
    // 标题
    .replace(/^### (.+)$/gm, '<h3 class="text-lg font-medium text-gray-200 mt-6 mb-3">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="text-xl font-medium text-gray-100 mt-8 mb-4">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="text-2xl font-bold text-white mt-8 mb-4">$1</h1>')
    // 粗体
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-gray-200">$1</strong>')
    // 列表
    .replace(/^\* (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    .replace(/^- (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li class="text-gray-400 ml-4">$1</li>')
    // 换行
    .replace(/\n\n/g, '</p><p class="text-gray-400 mb-4">')
    .replace(/\n/g, '<br>')
})

// 生成行程
const handleGenerate = async () => {
  if (!origin.value || !destination.value) {
    error.value = '缺少出发地或目的地信息'
    return
  }

  loading.value = true
  error.value = ''
  tripContent.value = ''

  try {
    // 计算默认日期（明天开始，3天后结束）
    const today = new Date()
    const startDate = new Date(today)
    startDate.setDate(today.getDate() + 1)
    const endDate = new Date(startDate)
    endDate.setDate(startDate.getDate() + 2)

    const formatDate = (date) => date.toISOString().split('T')[0]

    // 第一步：创建 Trip
    console.log('正在创建行程...')
    const trip = await createTrip({
      title: `${origin.value} → ${destination.value} 之旅`,
      origin: origin.value,
      destination: destination.value,
      start_date: formatDate(startDate),
      end_date: formatDate(endDate)
    })
    console.log('行程创建成功：', trip)

    // 第二步：调用 AI 生成
    console.log('正在调用 AI 生成行程内容...')
    const result = await generateTrip(trip.id, 'agent')
    console.log('AI 生成完成：', result)

    // 保存内容
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

// 页面加载时自动开始生成
onMounted(() => {
  handleGenerate()
})
</script>

<style scoped>
.prose h1, .prose h2, .prose h3 {
  color: inherit;
}
.prose li {
  list-style-type: disc;
}
</style>
