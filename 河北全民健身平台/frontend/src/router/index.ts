import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '数据看板' }
  },
  {
    path: '/knowledge-graph',
    name: 'KnowledgeGraph',
    component: () => import('../views/KnowledgeGraph.vue'),
    meta: { title: '知识图谱' }
  },
  {
    path: '/evaluation',
    name: 'Evaluation',
    component: () => import('../views/Evaluation.vue'),
    meta: { title: '评价分析' }
  },
  {
    path: '/motion-capture',
    name: 'MotionCapture',
    component: () => import('../views/MotionCapture.vue'),
    meta: { title: '动作捕捉' }
  },
  {
    path: '/recommendation',
    name: 'Recommendation',
    component: () => import('../views/Recommendation.vue'),
    meta: { title: '智能推荐' }
  },
  {
    path: '/data-management',
    name: 'DataManagement',
    component: () => import('../views/DataManagement.vue'),
    meta: { title: '数据管理' }
  },
  {
    path: '/policy',
    name: 'Policy',
    component: () => import('../views/Policy.vue'),
    meta: { title: '政策文件' }
  },
  {
    path: '/data-insights',
    name: 'DataInsights',
    component: () => import('../views/DataInsights.vue'),
    meta: { title: '数据洞察' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || '河北全民健身平台'} - 数智驱动全民健身公共服务体系`
  next()
})

export default router
