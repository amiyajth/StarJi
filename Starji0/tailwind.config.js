/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 深色主题 - 星空
        'space': {
          900: '#0a0a1a',
          800: '#12122a',
          700: '#1a1a3a',
        },
        // 浅色主题 - 天空
        'sky': {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
        },
        // 星星颜色
        'star': {
          DEFAULT: '#fef3c7',
          bright: '#fef9c3',
        },
        // 紫色渐变
        'nebula': {
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
        },
        // ✨ 新增：主题适应色
        'adaptive': {
          'text': 'var(--color-text-primary)',
          'text-secondary': 'var(--color-text-secondary)',
          'text-muted': 'var(--color-text-muted)',
          'bg': 'var(--color-bg-primary)',
          'bg-card': 'var(--color-bg-card)',
          'border': 'var(--color-border)',
        }
      },
      animation: {
        'twinkle': 'twinkle 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        twinkle: {
          '0%, 100%': { opacity: 0.3 },
          '50%': { opacity: 1 },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
