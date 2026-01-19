<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto text-center">
      <!-- 头部 -->
      <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">The Vision</p>
      <h1 class="text-2xl font-medium text-gray-200 mb-4">搜图识景</h1>
      <p class="text-gray-500 text-sm mb-12">指尖触碰流光，让每一场不期而遇，都有迹可循</p>

      <!-- 上传区域 -->
      <div class="glass rounded-2xl p-8 max-w-2xl mx-auto mb-8">
        <!-- 拖拽上传区 -->
        <div
          class="upload-zone"
          :class="{ 'upload-zone-active': isDragging, 'upload-zone-has-file': previewUrl }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <!-- 图片预览 -->
          <div v-if="previewUrl" class="preview-container">
            <img :src="previewUrl" alt="预览" class="preview-image" />
            <button @click.stop="clearFile" class="clear-btn">✕</button>
          </div>
          
          <!-- 上传提示 -->
          <div v-else class="upload-placeholder">
            <div class="w-16 h-16 mx-auto mb-4 rounded-full border border-white/10 flex items-center justify-center">
              <span class="text-gray-500 text-2xl">○</span>
            </div>
            <p class="text-gray-400 text-sm mb-2">点击或拖拽图片到这里</p>
            <p class="text-gray-600 text-xs">支持 JPG、PNG 格式</p>
          </div>
          
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onFileChange"
          />
        </div>

        <!-- 识别按钮 -->
        <button
          :disabled="!file || loading"
          @click="submit"
          class="search-btn w-full mt-6"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
            <span class="animate-pulse">◇</span>
            识别中...
          </span>
          <span v-else>开始识别</span>
        </button>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="max-w-2xl mx-auto mb-8 rounded-xl border border-red-500/20 bg-red-500/5 p-4">
        <p class="text-red-300 text-sm">{{ error }}</p>
      </div>

      <!-- 识别结果 -->
      <div v-if="result" class="glass rounded-2xl p-8 max-w-2xl mx-auto text-left">
        <!-- 推荐目的地 -->
        <div class="text-center mb-8">
          <p class="text-xs text-gray-600 uppercase tracking-widest mb-2">推荐目的地</p>
          <h2 class="text-2xl font-medium text-gray-100">{{ result.suggested_destination }}</h2>
          <div class="flex justify-center gap-2 mt-4">
            <span
              v-for="tag in (result.tags || [])"
              :key="tag"
              class="px-3 py-1 rounded-full bg-white/[0.05] text-gray-400 text-xs"
            >
              {{ tag }}
            </span>
          </div>
        </div>

        <div class="border-t border-white/[0.06] my-6"></div>

        <!-- 候选结果 -->
        <div class="mb-8">
          <p class="text-xs text-gray-600 uppercase tracking-widest mb-4">候选结果</p>
          <div class="space-y-3">
            <div
              v-for="(c, idx) in result.top_candidates"
              :key="idx"
              class="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/[0.04]"
            >
              <div>
                <span class="text-gray-200">{{ c.city }}</span>
                <span class="text-gray-500 mx-2">·</span>
                <span class="text-gray-400">{{ c.landmark }}</span>
              </div>
              <div class="flex items-center gap-3">
                <span v-if="c.tags" class="text-gray-600 text-xs">{{ c.tags.join(', ') }}</span>
                <span class="text-nebula-400 text-sm">{{ (c.confidence * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 生成行程按钮 -->
        <button
          :disabled="generating"
          @click="goGenerate(result.suggested_destination)"
          class="search-btn w-full"
        >
          <span v-if="generating" class="flex items-center justify-center gap-2">
            <span class="animate-pulse">◇</span>
            正在生成行程...
          </span>
          <span v-else>去规划 {{ result.suggested_destination }} 之旅 →</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import request from '../api/index'
import { createTrip, generateTrip } from '../api/trip'
import { useRouter } from 'vue-router'

const router = useRouter()

const fileInput = ref(null)
const file = ref(null)
const previewUrl = ref('')
const isDragging = ref(false)
const loading = ref(false)
const generating = ref(false)
const result = ref(null)
const error = ref('')

function triggerFileInput() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const selected = e.target.files?.[0]
  if (selected) {
    setFile(selected)
  }
}

function handleDrop(e) {
  isDragging.value = false
  const dropped = e.dataTransfer.files?.[0]
  if (dropped && dropped.type.startsWith('image/')) {
    setFile(dropped)
  }
}

function setFile(f) {
  file.value = f
  previewUrl.value = URL.createObjectURL(f)
  result.value = null
  error.value = ''
}

function clearFile() {
  file.value = null
  previewUrl.value = ''
  result.value = null
  error.value = ''
}

async function submit() {
  if (!file.value) return

  loading.value = true
  error.value = ''
  result.value = null

  try {
    const form = new FormData()
    form.append('image', file.value)

    const res = await request({
      url: '/vision/identify',
      method: 'post',
      data: form,
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    })

    result.value = res
  } catch (e) {
    console.error(e)
    if (e.response?.status === 401) {
      error.value = '请先登录后再使用此功能'
    } else {
      error.value = '识别失败，请检查网络或稍后重试'
    }
  } finally {
    loading.value = false
  }
}

async function goGenerate(destination) {
  if (!destination) return

  generating.value = true
  error.value = ''

  try {
    const today = new Date()
    const start = today.toISOString().slice(0, 10)
    const end = new Date(today.getTime() + 2 * 86400000).toISOString().slice(0, 10)

    const created = await createTrip({
      title: `以图搜旅 → ${destination}`,
      origin: '本地',
      destination,
      start_date: start,
      end_date: end
    })

    await generateTrip(created.id, 'agent')
    router.push(`/trips/${created.id}`)
  } catch (e) {
    console.error(e)
    error.value = '生成失败，请稍后重试'
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.glass {
  @apply bg-white/[0.02] border border-white/[0.06];
  @apply backdrop-blur;
}

.upload-zone {
  @apply relative p-8 rounded-xl border-2 border-dashed border-white/10;
  @apply cursor-pointer transition-all duration-300;
  @apply hover:border-white/20 hover:bg-white/[0.02];
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone-active {
  @apply border-nebula-500/50 bg-nebula-500/5;
}

.upload-zone-has-file {
  @apply border-solid border-white/10 p-4;
}

.upload-placeholder {
  @apply text-center;
}

.preview-container {
  @apply relative w-full;
}

.preview-image {
  @apply w-full max-h-64 object-contain rounded-lg;
}

.clear-btn {
  @apply absolute top-2 right-2;
  @apply w-8 h-8 rounded-full;
  @apply bg-black/50 text-gray-300 text-sm;
  @apply hover:bg-black/70 hover:text-white;
  @apply transition-all duration-200;
}

.search-btn {
  @apply px-8 py-3 rounded-lg;
  @apply bg-gradient-to-r from-nebula-600 to-nebula-500;
  @apply text-white text-sm font-medium tracking-wide;
  @apply hover:from-nebula-500 hover:to-nebula-400;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
  @apply transition-all duration-300;
}
</style>
