import request from '@/utils/request'

export function getInfo() {
  return request({
    url: '/system/solution/info/',
    method: 'get'
  })
}

export function getSolutionAll() {
  return request({
    url: '/system/solution/',
    method: 'get'
  })
}

export function getSolutionList(query) {
  return request({
    url: '/system/solution/',
    method: 'get',
    params: query
  })
}

export function createSolution(data) {
  return request({
    url: '/system/solution/',
    method: 'post',
    data
  })
}

export function updateSolution(id, data) {
  return request({
    url: `/system/solution/${id}/`,
    method: 'put',
    data
  })
}

export function deleteSolution(id) {
  return request({
    url: `/system/solution/${id}/`,
    method: 'delete'
  })
}

export function getSolutionResultAll() {
  return request({
    url: '/system/solution_result/',
    method: 'get'
  })
}
