import request from '@/utils/request'

export const getSpecimens = (params) => {
  return request({
    url: '/specimens',
    method: 'get',
    params
  })
}

export const getSpecimenById = (id) => {
  return request({
    url: `/specimens/${id}`,
    method: 'get'
  })
}

export const createSpecimen = (data) => {
  return request({
    url: '/specimens',
    method: 'post',
    data
  })
}

export const updateSpecimen = (id, data) => {
  return request({
    url: `/specimens/${id}`,
    method: 'put',
    data
  })
}

export const deleteSpecimen = (id) => {
  return request({
    url: `/specimens/${id}`,
    method: 'delete'
  })
}

export const getMineralTypes = () => {
  return request({
    url: '/specimens/mineral-types',
    method: 'get'
  })
}

export const getProvinces = () => {
  return request({
    url: '/specimens/provinces',
    method: 'get'
  })
}

export const getLocalities = () => {
  return request({
    url: '/specimens/localities',
    method: 'get'
  })
}
