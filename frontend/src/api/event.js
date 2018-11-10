import request from '@/utils/request'

export function fetchEvents() {
  return request({
    url: '/events_list',
    method: 'get',
    // params: 
  })
}
