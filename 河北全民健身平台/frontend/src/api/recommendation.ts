import request from './index'

// 推荐健身活动
export const recommendActivities = (userId: number, method: string = 'collaborative', topN: number = 5) => {
  return request({
    url: '/api/v1/recommend/activities',
    method: 'get',
    params: { user_id: userId, method, top_n: topN }
  })
}

// 推荐健身设施
export const recommendFacilities = (userId: number, latitude: number, longitude: number, topN: number = 5) => {
  return request({
    url: '/api/v1/recommend/facilities',
    method: 'get',
    params: { user_id: userId, latitude, longitude, top_n: topN }
  })
}

// 生成个性化方案
export const getPersonalizedPlan = (profile: any) => {
  return request({
    url: '/api/v1/recommend/personalized',
    method: 'post',
    data: profile
  })
}

// 获取相似用户
export const getSimilarUsers = (userId: number, topN: number = 10) => {
  return request({
    url: '/api/v1/recommend/similar-users',
    method: 'get',
    params: { user_id: userId, top_n: topN }
  })
}

// 获取热门活动
export const getTrendingActivities = (city?: string, limit: number = 10) => {
  return request({
    url: '/api/v1/recommend/trending',
    method: 'get',
    params: { city, limit }
  })
}
