import request from './index'

// 获取均衡性评价
export const getBalanceEvaluation = (params?: any) => {
  return request({
    url: '/api/v1/evaluation/balance',
    method: 'get',
    params
  })
}

// 获取可及性评价
export const getAccessibilityEvaluation = (params?: any) => {
  return request({
    url: '/api/v1/evaluation/accessibility',
    method: 'get',
    params
  })
}

// 获取AHP评价
export const getAHPEvaluation = () => {
  return request({
    url: '/api/v1/evaluation/ahp',
    method: 'get'
  })
}

// 获取综合评价
export const getComprehensiveEvaluation = (city: string) => {
  return request({
    url: '/api/v1/evaluation/comprehensive',
    method: 'get',
    params: { city }
  })
}

// 获取评价趋势
export const getEvaluationTrends = (city: string, years: number = 5) => {
  return request({
    url: '/api/v1/evaluation/trends',
    method: 'get',
    params: { city, years }
  })
}
