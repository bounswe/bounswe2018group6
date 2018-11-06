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

export function logout() {
  // return request({
  //   url: '/login/logout',
  //   method: 'post'
  // })
  // Currently we don't use API for logout.
  return
}

// export function getUserInfo(token) {
export function getUserInfo(user_id) {
  return request({
    url: '/user/' + user_id,
    method: 'get'
    // params: { token }
  })
}

