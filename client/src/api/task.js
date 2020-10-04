import request from '@/utils/request'

export function getTaskAll() {
  return request({
    url: '/system/task/',
    method: 'get'
  })
}

export function createTask(data) {          //TODO
  return request({
    url: '/system/task/',
    method: 'post',
    data
  })
}

export function updateTask(id, data) {      //TODO
  return request({
    url: `/system/task/${id}/`,
    method: 'put',
    data
  })
}

export function deleteTask(id) {            //TODO
  return request({
    url: `/system/task/${id}/`,
    method: 'delete'
  })
}
