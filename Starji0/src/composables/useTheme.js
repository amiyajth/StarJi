import { ref, watch } from 'vue'

// 全局响应式状态
const isDark = ref(true)

// 初始化：从 localStorage 读取
const savedTheme = localStorage.getItem('theme')
if (savedTheme) {
  isDark.value = savedTheme === 'dark'
}

// 监听变化，保存到 localStorage
watch(isDark, (val) => {
  localStorage.setItem('theme', val ? 'dark' : 'light')
})

export function useTheme() {
  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  return {
    isDark,
    toggleTheme
  }
}
