import request from './index'

export function getMyProfile() {
  return request({
    url: '/profile/me',
    method: 'get'
  })
}
