import request from '@/utils/request'

export function getTaskList(query) {
  return request({
    url: '/system/task/',
    method: 'get',
    params: query
  })
}

export function getTaskAll() {
  return request({
    url: '/system/task/',
    method: 'get'
  })
}

export function createTask(data) {
  return request({
    url: '/system/task/',
    method: 'post',
    data
  })
}

export function updateTask(id, data) {
  return request({
    url: `/system/task/${id}/`,
    method: 'put',
    data
  })
}

export function deleteTask(id) {
  return request({
    url: `/system/task/${id}/`,
    method: 'delete'
  })
}
