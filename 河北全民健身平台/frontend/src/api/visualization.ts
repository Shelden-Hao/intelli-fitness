import request from './index'

// 获取地图数据
export const getMapData = (city?: string) => {
  return request({
    url: '/api/v1/viz/map-data',
    method: 'get',
    params: { city }
  })
}

// 获取参与率图表数据
export const getParticipationChart = () => {
  return request({
    url: '/api/v1/viz/charts/participation',
    method: 'get'
  })
}

// 获取设施分布图表数据
export const getFacilityDistribution = () => {
  return request({
    url: '/api/v1/viz/charts/facility-distribution',
    method: 'get'
  })
}

// 获取活动热度图表数据
export const getActivityPopularity = () => {
  return request({
    url: '/api/v1/viz/charts/activity-popularity',
    method: 'get'
  })
}

// 获取趋势图表数据
export const getTrendsChart = (indicator: string = 'participation_rate') => {
  return request({
    url: '/api/v1/viz/charts/trends',
    method: 'get',
    params: { indicator }
  })
}

// 获取热力图数据
export const getHeatmapData = () => {
  return request({
    url: '/api/v1/viz/heatmap',
    method: 'get'
  })
}
