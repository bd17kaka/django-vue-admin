import request from '@/utils/request'

export function getChannelAll() {
  return request({
    url: '/fabric/channel/queryAll/',
    method: 'get'
  })
}

export function getChaincodeAll() {
  return request({
    url: '/fabric/chaincode/queryAll/',
    method: 'get',
  })
}
