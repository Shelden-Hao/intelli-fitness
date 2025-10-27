import request from './index'

// 获取实体列表
export const getEntities = (params?: any) => {
  return request({
    url: '/api/v1/kg/entities',
    method: 'get',
    params
  })
}

// 获取关系
export const getRelations = (params?: any) => {
  return request({
    url: '/api/v1/kg/relations',
    method: 'get',
    params
  })
}

// 搜索图谱
export const searchGraph = (query: string, limit: number = 20) => {
  return request({
    url: '/api/v1/kg/search',
    method: 'get',
    params: { query, limit }
  })
}

// 查找路径
export const findPath = (start: string, end: string, maxDepth: number = 3) => {
  return request({
    url: '/api/v1/kg/path',
    method: 'get',
    params: { start, end, max_depth: maxDepth }
  })
}

// 获取图谱统计
export const getGraphStatistics = () => {
  return request({
    url: '/api/v1/kg/statistics',
    method: 'get'
  })
}

// 获取可视化数据
export const getVisualizationData = (centerEntity: string, depth: number = 2) => {
  return request({
    url: '/api/v1/kg/visualization',
    method: 'get',
    params: { center_entity: centerEntity, depth }
  })
}
