/** @type {import('tailwindcss').Config} */
export default {
  // 告诉Tailwind去哪些文件里找class名
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 自定义颜色 - 星空主题
      colors: {
        // 主背景色：深蓝到紫的渐变会用到这些
        'space': {
          900: '#0a0a1a',  // 最深的夜空
          800: '#12122a',  // 深空
          700: '#1a1a3a',  // 星空背景
        },
        // 强调色：星星和高亮
        'star': {
          DEFAULT: '#fef3c7', // 星星的颜色（暖黄）
          bright: '#fef9c3',  // 更亮的星星
        },
        // 渐变用的紫色
        'nebula': {
          400: '#a78bfa',  // 浅紫
          500: '#8b5cf6',  // 中紫
          600: '#7c3aed',  // 深紫
        }
      },
      // 自定义动画
      animation: {
        'twinkle': 'twinkle 3s ease-in-out infinite',  // 星星闪烁
        'float': 'float 6s ease-in-out infinite',       // 漂浮效果
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
