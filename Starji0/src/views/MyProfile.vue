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

      <!-- 已登录 -->
      <div v-else class="rounded-xl border border-white/[0.06] p-12 text-left">
        <!-- 头像区域 -->
        <div class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full border border-white/10 flex items-center justify-center bg-white/[0.03]">
            <span class="text-gray-300 text-2xl">{{ userInitial }}</span>
          </div>

          <!-- 用户信息 -->
          <div class="space-y-2 mb-8">
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
        </div>

        <div class="border-t border-white/[0.06] my-8"></div>

        <!-- 画像加载失败提示 -->
        <div v-if="profileError" class="rounded-lg border border-red-500/20 bg-red-500/5 p-4 mb-8">
          <p class="text-red-300 text-sm">{{ profileError }}</p>
          <p class="text-gray-500 text-xs mt-1">提示：请确认后端 /api/profile/me 已上线，并且你已产生行程创建/生成/识别等事件。</p>
        </div>

        <!-- 用户画像（统计型） -->
        <div class="space-y-10">
          <div>
            <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">目的地偏好 Top</p>
            <div v-if="!profile?.destinations_top?.length" class="text-gray-500 text-sm">
              暂无数据，先去创建并生成几次行程吧 ✨
            </div>
            <ul v-else class="space-y-2">
              <li v-for="d in profile.destinations_top" :key="d.destination" class="text-gray-300 text-sm flex justify-between">
                <span>{{ d.destination }}</span>
                <span class="text-gray-500">{{ d.count }} 次</span>
              </li>
            </ul>
          </div>

          <div>
            <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">生成模式统计</p>
            <div v-if="!modeEntries.length" class="text-gray-500 text-sm">
              暂无生成记录
            </div>
            <ul v-else class="space-y-2">
              <li v-for="m in modeEntries" :key="m.mode" class="text-gray-300 text-sm flex justify-between">
                <span>{{ m.mode }}</span>
                <span class="text-gray-500">{{ m.count }} 次</span>
              </li>
            </ul>
          </div>

          <div>
            <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">标签偏好 Top</p>
            <div v-if="!profile?.tags_top?.length" class="text-gray-500 text-sm">
              暂无标签偏好（试试去"以图搜旅"识别几张图，会产生标签统计）
            </div>
            <ul v-else class="space-y-2">
              <li v-for="t in profile.tags_top" :key="t.tag" class="text-gray-300 text-sm flex justify-between">
                <span>{{ t.tag }}</span>
                <span class="text-gray-500">{{ t.count }} 次</span>
              </li>
            </ul>
          </div>

          <div>
            <p class="text-xs text-gray-600 uppercase tracking-widest mb-3">最近事件</p>
            <div v-if="!profile?.recent_events?.length" class="text-gray-500 text-sm">
              暂无事件记录
            </div>
            <ul v-else class="space-y-2">
              <li v-for="(e, idx) in profile.recent_events" :key="idx" class="text-gray-400 text-xs flex justify-between">
                <span>{{ formatDateTime(e.created_at) }}</span>
                <span>{{ e.event_type }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="border-t border-white/[0.06] my-8"></div>

        <!-- 退出登录 -->
        <div class="text-center">
          <button
            @click="handleLogout"
            class="px-6 py-2 rounded-lg bg-white/[0.05] text-gray-400 text-sm hover:bg-white/10 hover:text-gray-200 transition"
          >
            退出登录
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/index'
import { getMe, logout } from '../api/auth'

const router = useRouter()

const loading = ref(true)
const user = ref(null)

const profile = ref(null)
const profileError = ref('')

const userInitial = computed(() => {
  if (!user.value?.username) return '?'
  return user.value.username.charAt(0).toUpperCase()
})

const modeEntries = computed(() => {
  const modes = profile.value?.modes || {}
  return Object.keys(modes).map(k => ({ mode: k, count: modes[k] }))
})

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function fetchUserAndProfile() {
  // ✨ 先检查 token，没有就直接返回"未登录"
  const token = localStorage.getItem('token')
  if (!token) {
    loading.value = false
    user.value = null
    return
  }

  loading.value = true
  profileError.value = ''
  profile.value = null

  try {
    // 1) 先判断登录态
    const me = await getMe()
    user.value = me

    // 2) 再拉画像（统计）
    try {
      const p = await request({
        url: '/profile/me',
        method: 'get',
        timeout: 30000
      })
      profile.value = p
    } catch (e) {
      console.error(e)
      profileError.value = '画像加载失败：后端 /api/profile/me 不可用或暂无权限'
    }
  } catch (e) {
    console.log('未登录或 token 失效')
    user.value = null
    // ✨ token 失效时也清除本地存储
    localStorage.removeItem('token')
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  logout()
  user.value = null
  profile.value = null
  router.push('/')
}

onMounted(() => {
  fetchUserAndProfile()
})
</script>
