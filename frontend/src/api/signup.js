import request from '@/utils/request'

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

