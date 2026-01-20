import request from './index'

// 获取城市列表
export function getCities(limit = 100) {
  return request({
    url: '/cities',
    method: 'get',
    params: { limit }
  })
}

// 获取单个城市详情
export function getCityById(id) {
  return request({
    url: `/cities/${id}`,
    method: 'get'
  })
}
