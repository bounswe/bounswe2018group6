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
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/events/' + event_id + '/',
    method: 'get'
  })
  }

export function attendance(event, status) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  let attend;
  attend = {
    "Attend": "Y",
    "Won't attend": "N",
    "Maybe": "M",
    "Block": "B",
  }
  status = attend[status]

  const data = {
    event,
    status
  }
  return request({
    headers,
    url: '/attendance/',
    method: 'post',
    data
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
 