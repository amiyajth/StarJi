import request from './index'

export function getCities() {
  return request({
    url: '/cities',
    method: 'get'
  })
}

export function getCityById(id) {
  return request({
    url: `/cities/${id}`,
    method: 'get'
  })
}
