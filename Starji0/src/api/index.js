import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // ✅ 加上 /api
  timeout: 10000  // 默认 10 秒（普通接口够用）
})

// ✅ 请求拦截器：自动带上 token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    console.error('请求失败：', error)
    return Promise.reject(error)
  }
)

export default request
