import request from '@/utils/request'
import { getToken } from '@/utils/auth' // getToken from cookie

export function fetchEvents() {
  return request({
    url: '/events_list',
    method: 'get',
    // params: 
  })
}

export function getEventDetail(event_id) {
    return request({
      url: '/events/' + event_id + '/',
      method: 'get'
    })
  }


export function createEvent(data) {
    const headers = {
        //ContentType: 'application/json',
        Authorization: 'Token ' + getToken(),
    }
    return request({
        headers,
        url: '/events/',
        method: 'post',
        data
    })
}
 