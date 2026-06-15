import request from '@/utils/request'

export const getOverallStats = () => {
  return request({
    url: '/stats',
    method: 'get'
  })
}
