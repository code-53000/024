import request from '@/utils/request'

export const getSpecimenIdentifications = (specimenId) => {
  return request({
    url: `/identifications/specimen/${specimenId}`,
    method: 'get'
  })
}

export const getPendingIdentifications = (params) => {
  return request({
    url: '/identifications/pending',
    method: 'get',
    params
  })
}

export const getIdentificationById = (id) => {
  return request({
    url: `/identifications/${id}`,
    method: 'get'
  })
}

export const createIdentification = (data) => {
  return request({
    url: '/identifications',
    method: 'post',
    data
  })
}

export const deleteIdentification = (id) => {
  return request({
    url: `/identifications/${id}`,
    method: 'delete'
  })
}

export const getAllowedTransitions = (currentStatus) => {
  return request({
    url: `/identifications/allowed-transitions/${currentStatus}`,
    method: 'get'
  })
}
