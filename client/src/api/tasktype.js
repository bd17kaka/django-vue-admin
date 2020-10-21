import request from '@/utils/request'

export function getTasktypeAll() {
  return request({
    url: '/system/tasktype/',
    method: 'get'
  })
}

export function createTasktype(data) {          //TODO
  return request({
    url: '/system/tasktype/',
    method: 'post',
    data
  })
}

export function updateTasktype(id, data) {      //TODO
  return request({
    url: `/system/tasktype/${id}/`,
    method: 'put',
    data
  })
}

export function deleteTasktype(id) {            //TODO
  return request({
    url: `/system/tasktype/${id}/`,
    method: 'delete'
  })
}
