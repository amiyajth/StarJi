import request from './index'

export function identifyImage(file) {
  const form = new FormData()
  form.append('image', file)

  return request({
    url: '/vision/identify',
    method: 'post',
    data: form,
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000
  })
}
