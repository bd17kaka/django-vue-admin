import { getToken } from '@/utils/auth'
import request from '@/utils/request'

export function getDatasetList(query) {
  return request({
    url: '/system/dataset/',
    method: 'get',
    params: query
  })
}

export function createDataset(data) {         
  return request({
    url: '/system/dataset/',
    method: 'post',
    data
  })
}

export function updateDataset(id, data) {
  return request({
    url: `/system/dataset/${id}/`,
    method: 'put',
    data
  })
}

export function deleteDataset(id) {        
  return request({
    url: `/system/dataset/${id}/`,
    method: 'delete'
  })
}
