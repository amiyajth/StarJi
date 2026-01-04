// 从vue库引入创建应用的函数
import { createApp } from 'vue'

// 引入全局样式
import './style.css'

// 引入根组件
import App from './App.vue'

// 引入路由配置
import router from './router'

// 创建Vue应用实例
const app = createApp(App)

// 使用路由插件
app.use(router)

// 把应用挂载到index.html中id为app的元素上
app.mount('#app')
