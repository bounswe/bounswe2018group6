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

export function follow(event_id) {
  const content_type = "event";
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    "content_type": content_type,
    "object_id": event_id
  }
  return request({
    headers,
    url: '/follow/',
    method: 'post',
    data
  })
}

export function unfollow(follow_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/follow/' + follow_id + '/',
    method: 'delete'
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
 

export function editEvent(data, event_id) {
  console.log(data)
  const headers = {
      //ContentType: 'application/json',
      Authorization: 'Token ' + getToken(),
  }
  return request({
      headers,
      url: '/events/' + event_id + '/',
      method: 'put',
      data
  })
}