import request from '@/utils/request'

export function getMeasurementAll() {
  return request({
    url: '/system/measurement/',
    method: 'get'
  })
}

export function createMeasurement(data) {
  return request({
    url: '/system/measurement/',
    method: 'post',
    data
  })
}

export function updateMeasurement(id, data) {
  return request({
    url: `/system/measurement/${id}/`,
    method: 'put',
    data
  })
}

export function deleteMeasurement(id) {
  return request({
    url: `/system/measurement/${id}/`,
    method: 'delete'
  })
}
