import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'
const UserIDKey = 'Cultidate-User-Id'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function setUserIDCookie(id){
  return Cookies.set(UserIDKey, id)
}

export function getUserIDCookie() {
  return Cookies.get(UserIDKey)
}

export function removeUserIDCookie() {
  return Cookies.remove(UserIDKey)
}