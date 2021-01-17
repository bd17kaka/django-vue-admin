import request from '@/utils/request'

export function getTracename(data) {
  return request({
    url: '/system/trace/',
    method: 'post',
    data
  })
}

export function getRepresentation(data) {
  return request({
    url: '/system/representation/',
    method: 'post',
    data
  })
}

export function getClassifier(data) {
  return request({
    url: '/system/classifier/',
    method: 'post',
    data
  })
}

export function getTraining(data) {
  return request({
    url: '/system/training/',
    method: 'post',
    data
  })
}

export function getResult(data) {
  return request({
    url: '/system/result/',
    method: 'post',
    data
  })
}

export function getRepresentationResult(data) {
  return request({
    url: '/system/represult/',
    method: 'post',
    data
  })
}