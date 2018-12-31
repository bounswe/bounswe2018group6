import request from '@/utils/request'
import { getToken } from '@/utils/auth' // getToken from cookie


export function createConversation(user_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    participant: user_id
  }
  return request({
    headers: headers,
    url: '/conversations/',
    method: 'post',
    data
  })
}

export function getAllConversations() {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers: headers,
    url: '/conversations_list/',
    method: 'get'
  })
}

export function getConversationDetails(conversation_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers: headers,
    url: '/conversations/' + conversation_id + '/',
    method: 'get'
  })
}

export function createMessage(receiver_id, conversation_id, content) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    receiver: receiver_id,
    conversation: conversation_id,
    content: content
  }
  return request({
    headers: headers,
    url:'/messages/',
    method: 'post',
    data
  })  
}

export function deleteConversations(conversation_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers: headers,
    url: '/conversations/' + conversation_id + '/',
    method: 'delete'
  })
}