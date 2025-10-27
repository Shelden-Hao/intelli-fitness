<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref([
  { title: '健身设施总数', value: '1,258', unit: '个', icon: 'Location', color: '#409EFF' },
  { title: '覆盖人口', value: '2,800', unit: '万人', icon: 'User', color: '#67C23A' },
  { title: '参与率', value: '31.5', unit: '%', icon: 'TrendCharts', color: '#E6A23C' },
  { title: '知识图谱实体', value: '15,432', unit: '个', icon: 'Share', color: '#F56C6C' }
])

const features = ref([
  {
    title: '时空知识图谱',
    description: '构建全民健身公共服务七维度知识表示体系,实现多源异构数据融合与智能查询',
    icon: 'Share',
    route: '/knowledge-graph',
    color: '#409EFF'
  },
  {
    title: '智能评价模型',
    description: '基于AHP、基尼系数、GIS空间分析的均衡性与可及性综合评价体系',
    icon: 'TrendCharts',
    route: '/evaluation',
    color: '#67C23A'
  },
  {
    title: '动作捕捉指导',
    description: '基于MediaPipe的人体姿态检测,提供实时动作分析与智能纠正反馈',
    icon: 'VideoCamera',
    route: '/motion-capture',
    color: '#E6A23C'
  },
  {
    title: '智能推荐系统',
    description: '协同过滤与深度学习融合,个性化健身活动与设施推荐',
    icon: 'Star',
    route: '/recommendation',
    color: '#F56C6C'
  }
])

const navigateTo = (route: string) => {
  router.push(route)
}
</script>

<template>
  <div class="home-container">
    <!-- 欢迎横幅 -->
    <el-card class="welcome-banner" shadow="never">
      <div class="banner-content">
        <div class="banner-text">
          <h1>数智驱动河北全民健身公共服务体系研究</h1>
          <p class="banner-subtitle">
            融合人工智能、大数据、知识图谱技术,构建智能化全民健身公共服务平台
          </p>
          <div class="banner-tags">
            <el-tag type="primary">知识图谱</el-tag>
            <el-tag type="success">大数据分析</el-tag>
            <el-tag type="warning">AI评价模型</el-tag>
            <el-tag type="danger">动作捕捉</el-tag>
          </div>
        </div>
        <div class="banner-image">
          <el-icon :size="200" color="#409EFF"><DataAnalysis /></el-icon>
        </div>
      </div>
    </el-card>

    <!-- 统计数据 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color + '20' }">
              <el-icon :size="40" :color="stat.color">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}<span class="stat-unit">{{ stat.unit }}</span></div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 核心功能 -->
    <div class="section-title">
      <h2>核心功能模块</h2>
      <p>基于前沿AI技术的全民健身智能化服务</p>
    </div>

    <el-row :gutter="20" class="features-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="feature in features" :key="feature.title">
        <el-card class="feature-card" shadow="hover" @click="navigateTo(feature.route)">
          <div class="feature-icon" :style="{ backgroundColor: feature.color + '20' }">
            <el-icon :size="50" :color="feature.color">
              <component :is="feature.icon" />
            </el-icon>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <el-button type="primary" link>
            了解更多 <el-icon><ArrowRight /></el-icon>
          </el-button>
        </el-card>
      </el-col>
    </el-row>

    <!-- 技术亮点 -->
    <div class="section-title">
      <h2>创新亮点</h2>
      <p>多项技术创新,引领全民健身智能化发展</p>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card class="highlight-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon color="#409EFF"><Cpu /></el-icon>
              <span>多源数据融合</span>
            </div>
          </template>
          <ul class="highlight-list">
            <li>国家统计局、体育总局等官方数据源</li>
            <li>社交媒体与用户行为数据挖掘</li>
            <li>政策文件NLP智能分析</li>
            <li>实时数据采集与预处理</li>
          </ul>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card class="highlight-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon color="#67C23A"><Connection /></el-icon>
              <span>知识图谱技术</span>
            </div>
          </template>
          <ul class="highlight-list">
            <li>七维度概念模型设计</li>
            <li>Neo4j图数据库存储</li>
            <li>TransE模型知识补全</li>
            <li>智能查询与推理</li>
          </ul>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card class="highlight-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon color="#E6A23C"><DataAnalysis /></el-icon>
              <span>智能评价算法</span>
            </div>
          </template>
          <ul class="highlight-list">
            <li>基尼系数均衡性分析</li>
            <li>GIS空间可及性评估</li>
            <li>AHP层次分析法</li>
            <li>遗传算法与粒子群优化</li>
          </ul>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card class="highlight-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon color="#F56C6C"><VideoCamera /></el-icon>
              <span>AI动作识别</span>
            </div>
          </template>
          <ul class="highlight-list">
            <li>MediaPipe姿态检测</li>
            <li>BVH格式动作数据</li>
            <li>Three.js 3D可视化</li>
            <li>实时动作纠正反馈</li>
          </ul>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-banner {
  margin-bottom: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.banner-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.banner-text h1 {
  font-size: 32px;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.banner-subtitle {
  font-size: 16px;
  margin-bottom: 20px;
  opacity: 0.95;
}

.banner-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.banner-image {
  opacity: 0.3;
}

.stats-row {
  margin-bottom: 40px;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.stat-unit {
  font-size: 16px;
  font-weight: normal;
  margin-left: 5px;
  color: #909399;
}

.stat-title {
  font-size: 14px;
  color: #606266;
  margin-top: 5px;
}

.section-title {
  text-align: center;
  margin: 40px 0 30px;
}

.section-title h2 {
  font-size: 28px;
  color: #303133;
  margin: 0 0 10px 0;
}

.section-title p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.features-row {
  margin-bottom: 40px;
}

.feature-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.feature-card h3 {
  font-size: 18px;
  color: #303133;
  margin: 0 0 15px 0;
}

.feature-card p {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
  min-height: 80px;
}

.highlight-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.highlight-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.highlight-list li {
  padding: 10px 0;
  border-bottom: 1px solid #EBEEF5;
  color: #606266;
}

.highlight-list li:last-child {
  border-bottom: none;
}

.highlight-list li:before {
  content: "✓";
  color: #67C23A;
  font-weight: bold;
  margin-right: 10px;
}
</style>
