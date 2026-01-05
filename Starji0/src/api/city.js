import request from './index'

export function getCities() {
  return request({
    url: '/api/cities',
    method: 'get'
  })
}

export function getCityById(id) {
  return request({
    url: `/api/cities/${id}`,
    method: 'get'
  })
}
