import request from '@/utils/request'

export function getEventsList() {
  return request({
    url: '/events_list/',
    method: 'get'
  })
}

export function getEventsDetails(event_id) {
  return request({
    url: '/events/' + event_id,
    method: 'get'
  })
}

