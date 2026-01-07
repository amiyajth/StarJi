import request from './index'

/**
 * 创建新行程
 */
export function createTrip(data) {
  return request({
    url: '/trips',
    method: 'post',
    data
  })
}

/**
 * AI 生成行程内容
 * @param {number} tripId - 行程ID
 * @param {'basic'|'agent'} mode - basic=基础版；agent=天气增强版
 */
export function generateTrip(tripId, mode = 'basic') {
  return request({
    url: `/trips/${tripId}/generate`,
    method: 'post',
    params: { mode },       // ✅ 自动拼成 ?mode=agent
    timeout: 300000         // ✅ 5分钟（AI + 天气工具会比较慢）
  })
}

/**
 * 获取行程详情
 */
export function getTrip(tripId) {
  return request({
    url: `/trips/${tripId}`,
    method: 'get'
  })
}
