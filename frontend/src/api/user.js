import request from '@/utils/request'
import { getToken } from '@/utils/auth' // getToken from cookie

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: '/auth/',
    method: 'post',
    data
  })
}

export function getUserInfo(user_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    url: '/user/' + user_id + '/',
    method: 'get'
  })
}

export function signupDate(first_name, last_name, email, username, password) {
  const data = {
    first_name,
    last_name,
    email,
    username,
    password
  }
  return request({
    url: '/signup/',
    method: 'post',
    data
  })
}

export function editUser(user_id, data) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/user/' + user_id + '/',
    method: 'put',
    data
  })
}

