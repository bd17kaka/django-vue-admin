import { getToken } from '@/utils/auth'
import request from '@/utils/request'

// export function upUrl() {
//   return process.env.VUE_APP_BASE_API +'/dataset/'
// }

// export function upHeaders() {
//   return { Authorization: "Bearer " + getToken() }
// }

export function getDatasetAll() {
  return request({
    url: '/system/dataset/',
    method: 'get'
  })
}

export function createDataset(data) {         
  return request({
    url: '/system/dataset/',
    method: 'post',
    data
  })
}

export function deleteDataset(id) {        
  return request({
    url: `/system/dataset/${id}/`,
    method: 'delete'
  })
}
