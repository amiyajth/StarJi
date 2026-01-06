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
 * AI 生成行程内容（需要更长的超时时间）
 */
export function generateTrip(tripId) {
  return request({
    url: `/trips/${tripId}/generate`,
    method: 'post',
    timeout: 300000  // ✅ 5 分钟（AI 生成比较慢）
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
