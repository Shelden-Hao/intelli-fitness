import request from './index'

// 获取健身设施数据
export const getFacilities = (params?: any) => {
  return request({
    url: '/api/v1/data/facilities',
    method: 'get',
    params
  })
}

// 获取人口数据
export const getPopulation = (params?: any) => {
  return request({
    url: '/api/v1/data/population',
    method: 'get',
    params
  })
}

// 获取参与数据
export const getParticipation = () => {
  return request({
    url: '/api/v1/data/participation',
    method: 'get'
  })
}

// 获取统计数据
export const getStatistics = () => {
  return request({
    url: '/api/v1/data/statistics',
    method: 'get'
  })
}

// 上传数据文件
export const uploadData = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/v1/data/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
