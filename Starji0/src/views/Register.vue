<template>
  <div class="min-h-screen pt-24 pb-12 px-6">
    <div class="max-w-md mx-auto">
      <div class="text-center mb-10">
        <h1 class="text-2xl font-medium text-gray-200">注册</h1>
        <p class="text-gray-500 text-sm mt-2">创建账号后就能一键生成行程 🧭</p>
      </div>

      <div class="glass rounded-2xl p-8">
        <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">用户名</label>
        <input v-model="username" class="search-input mb-5" placeholder="例如 lizi" />

        <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">邮箱</label>
        <input v-model="email" class="search-input mb-5" placeholder="例如 lizi@example.com" />

        <label class="block text-xs text-gray-500 mb-2 uppercase tracking-wider">密码（至少 6 位）</label>
        <input v-model="password" type="password" class="search-input mb-6" placeholder="请输入密码" />

        <button class="search-btn w-full" :disabled="loading" @click="handleRegister">
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <p v-if="error" class="text-red-400 text-sm mt-4">{{ error }}</p>

        <div class="mt-6 text-center text-sm text-gray-500">
          已有账号？
          <a class="text-gray-300 hover:text-white" @click.prevent="goLogin" href="#">去登录 →</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../api/auth'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  error.value = ''
  if (!username.value.trim() || !email.value.trim() || !password.value) {
    error.value = '请把用户名、邮箱、密码填完整'
    return
  }
  if (password.value.length < 6) {
    error.value = '密码至少 6 位'
    return
  }

  loading.value = true
  try {
    // 后端 UserCreate: username, email, password :contentReference[oaicite:5]{index=5}
    await registerUser({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value
    })
    router.push('/login')
  } catch (e) {
    error.value = e?.response?.data?.detail || '注册失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

const goLogin = () => router.push('/login')
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
