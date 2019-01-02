import request from '@/utils/request'
import { getToken } from '@/utils/auth' // getToken from cookie

export function fetchEvents() {
  return request({
    url: '/events_list/',
    method: 'get',
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

export function delAttendance(attend_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/attendance/' + attend_id + '/',
    method: 'delete'
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
 
export function rate(event_id, rate) {
  const content_type = "event";
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    "content_type": content_type,
    "object_id": event_id,
    "vote": rate
  }
  return request({
    headers,
    url: '/vote/',
    method: 'post',
    data
  })
}

export function delrate(rate_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/vote/' + rate_id + '/',
    method: 'delete'
  })
}

export function delEvent(event_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/events/' + event_id + '/',
    method: 'delete'
  })
}

export function getTags() {
  return request({
    url: '/tags/',
    method: 'get'
  })
}

export function createComment(event_id, comment) {
  const content_type = "event";
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    "content_type": content_type,
    "object_id": event_id,
    "content": comment
  }
  return request({
    headers,
    url: '/comments/',
    method: 'post',
    data
  })
}

export function delComment(comment_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/comments/' + comment_id + '/',
    method: 'delete'
  })
}

export function editEvent(data, event_id) {
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

export function searchByTitle(tag) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/events_list/?search=' + tag,
    method: 'get'
  })
}

export function searchByLocation(location) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/events_location/?search=' + location,
    method: 'get'
  })
}

export function share(event_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    "event": event_id
  }
  return request({
    headers,
    url: '/share/',
    method: 'post',
    data
  })
}

export function unshare(share_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/share/' + share_id + '/',
    method: 'delete'
  })
}

export function fetchRecommendations() {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/events_recommended_list/',
    method: 'get'
  })
}