import request from '@/utils/request'

export function getAppAll() {
  return request({
    url: '/system/app/',
    method: 'get'
  })
}

export function createApp(data) {
  return request({
    url: '/system/app/',
    method: 'post',
    data
  })
}

export function updateApp(id, data) {
  return request({
    url: `/system/app/${id}/`,
    method: 'put',
    data
  })
}

export function deleteApp(id) {
  return request({
    url: `/system/app/${id}/`,
    method: 'delete'
  })
}


