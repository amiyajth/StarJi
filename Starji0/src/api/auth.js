import request from './index'

export function registerUser(data) {
  return request({
    url: '/users/register',
    method: 'post',
    data
  })
}

// 注意：后端是 OAuth2PasswordRequestForm，所以这里要 x-www-form-urlencoded
export function loginUser(username, password) {
  const body = new URLSearchParams()
  body.append('username', username)
  body.append('password', password)

  return request({
    url: '/users/login',
    method: 'post',
    data: body,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

export function getMe() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export function logout() {
  localStorage.removeItem('token')
}
