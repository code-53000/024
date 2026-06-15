import request from '@/utils/request'

export const login = (data) => {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export const register = (data) => {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

export const logout = () => {
  return new Promise((resolve) => {
    resolve()
  })
}

export const getCurrentUser = () => {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export const updateCurrentUser = (data) => {
  return request({
    url: '/users/me',
    method: 'put',
    data
  })
}
