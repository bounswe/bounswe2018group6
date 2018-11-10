import request from '@/utils/request'

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
  return request({
    url: '/user/' + user_id,
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

