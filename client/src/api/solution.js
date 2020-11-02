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

// export function getSolution(id) {
//   return request({
//     url: `/system/solution/${id}/`,
//     method: 'get'
//   })
// }

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
  // console.log("这里3")
  return request({
    url: `/system/solution/${id}/`,
    method: 'delete',
  })

}
