<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-md mx-auto">
      <div class="text-center mb-10">
        <h1 class="text-2xl font-medium text-gray-200">登录</h1>
        <p class="text-gray-500 text-sm mt-2">登录后才能生成行程 ✨</p>
      </div>

      <div class="glass rounded-2xl p-8">
        <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">用户名</label>
        <input v-model="username" class="search-input mb-5" placeholder="请输入用户名" />

        <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">密码</label>
        <input v-model="password" type="password" class="search-input mb-6" placeholder="请输入密码" />

        <button class="search-btn w-full" :disabled="loading" @click="handleLogin">
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <p v-if="error" class="text-red-400 text-sm mt-4">{{ error }}</p>

        <div class="mt-6 text-center text-sm text-gray-500">
          还没有账号？
          <a class="text-gray-300 hover:text-white" @click.prevent="goRegister" href="#">去注册 →</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser, getMe } from '../api/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  if (!username.value.trim() || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  try {
    const tokenResp = await loginUser(username.value.trim(), password.value)
    // 后端返回: { access_token, token_type } :contentReference[oaicite:4]{index=4}
    localStorage.setItem('token', tokenResp.access_token)

    // 可选：立刻验证 token 是否可用
    await getMe()

    router.push('/')
  } catch (e) {
    error.value = e?.response?.data?.detail || '登录失败，请检查用户名或密码'
  } finally {
    loading.value = false
  }
}

const goRegister = () => router.push('/register')
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
.glass {
  @apply bg-white/[0.02] border border-white/[0.06];
  @apply backdrop-blur;
}
</style>
