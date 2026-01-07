<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto text-center">
      <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">The Echo</p>
      <h1 class="text-2xl font-medium text-gray-200 mb-4">我的画像</h1>
      <p class="text-gray-500 text-sm mb-12">拾起散落的星屑，于万千偏好中，回响出你的灵魂轮廓</p>
      
      <!-- 加载中 -->
      <div v-if="loading" class="rounded-xl border border-white/[0.06] p-16">
        <div class="w-16 h-16 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center animate-pulse">
          <span class="text-gray-500 text-xl">△</span>
        </div>
        <p class="text-gray-600 text-sm">正在读取你的星迹...</p>
      </div>

      <!-- 未登录 -->
      <div v-else-if="!user" class="rounded-xl border border-white/[0.06] p-16">
        <div class="w-16 h-16 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center">
          <span class="text-gray-500 text-xl">△</span>
        </div>
        <p class="text-gray-600 text-sm mb-6">你还没有登录，无法查看画像</p>
        <button 
          @click="$router.push('/login')" 
          class="px-6 py-2 rounded-lg bg-white/10 text-gray-300 text-sm hover:bg-white/20 transition"
        >
          去登录
        </button>
      </div>

      <!-- 已登录：显示用户信息 -->
      <div v-else class="rounded-xl border border-white/[0.06] p-12">
        <!-- 头像区域 -->
        <div class="w-20 h-20 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center bg-white/[0.03]">
          <span class="text-gray-300 text-2xl">{{ userInitial }}</span>
        </div>

        <!-- 用户信息 -->
        <div class="space-y-4 mb-8">
          <div class="flex justify-center items-center gap-3">
            <span class="text-gray-500 text-sm">用户名</span>
            <span class="text-gray-200">{{ user.username }}</span>
          </div>
          <div class="flex justify-center items-center gap-3">
            <span class="text-gray-500 text-sm">邮箱</span>
            <span class="text-gray-200">{{ user.email }}</span>
          </div>
          <div class="flex justify-center items-center gap-3">
            <span class="text-gray-500 text-sm">注册时间</span>
            <span class="text-gray-200">{{ formatDate(user.created_at) }}</span>
          </div>
        </div>

        <!-- 分割线 -->
        <div class="border-t border-white/[0.06] my-8"></div>

        <!-- 个人偏好（占位，未来扩展） -->
        <div class="mb-8">
          <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">旅行偏好</p>
          <p class="text-gray-500 text-sm">暂无数据，快去规划你的第一次旅行吧 ✨</p>
        </div>

        <!-- 退出登录 -->
        <button 
          @click="handleLogout" 
          class="px-6 py-2 rounded-lg bg-white/[0.05] text-gray-400 text-sm hover:bg-white/10 hover:text-gray-200 transition"
        >
          退出登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMe, logout } from '../api/auth'

const router = useRouter()

// 状态
const loading = ref(true)
const user = ref(null)

// 用户名首字母（作为简易头像）
const userInitial = computed(() => {
  if (!user.value?.username) return '?'
  return user.value.username.charAt(0).toUpperCase()
})

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 获取用户信息
const fetchUser = async () => {
  loading.value = true
  try {
    const data = await getMe()
    user.value = data
  } catch (e) {
    console.log('未登录或 token 失效')
    user.value = null
  } finally {
    loading.value = false
  }
}

// 退出登录
const handleLogout = () => {
  logout()  // 清除 localStorage 中的 token
  user.value = null
  router.push('/')
}

// 页面加载时获取用户信息
onMounted(() => {
  fetchUser()
})
</script>
