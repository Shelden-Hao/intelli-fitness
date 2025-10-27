<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getStatistics } from '../api/data'
import { getParticipationChart, getFacilityDistribution, getActivityPopularity, getTrendsChart } from '../api/visualization'

const loading = ref(false)
const stats = ref<any>({})

// 初始化图表
const initCharts = () => {
  // 参与率图表
  const participationChart = echarts.init(document.getElementById('participationChart')!)
  getParticipationChart().then((data: any) => {
    participationChart.setOption({
      title: { text: '各城市参与率对比', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: data.cities },
      yAxis: { type: 'value', name: '参与率(%)' },
      series: [
        {
          name: '参与率',
          type: 'bar',
          data: data.participation_rates.map((v: number) => (v * 100).toFixed(1)),
          itemStyle: { color: '#409EFF' },
          markLine: {
            data: [{ type: 'average', name: '平均值' }, { yAxis: data.target_rate, name: '目标值' }]
          }
        }
      ]
    })
  })

  // 设施分布饼图
  const facilityChart = echarts.init(document.getElementById('facilityChart')!)
  getFacilityDistribution().then((data: any) => {
    facilityChart.setOption({
      title: { text: '健身设施类型分布', left: 'center' },
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [
        {
          name: '设施类型',
          type: 'pie',
          radius: '50%',
          data: data.types.map((type: string, index: number) => ({
            value: data.counts[index],
            name: type
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
  })

  // 活动热度柱状图
  const activityChart = echarts.init(document.getElementById('activityChart')!)
  getActivityPopularity().then((data: any) => {
    activityChart.setOption({
      title: { text: '运动项目参与人数', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: data.activities,
        axisLabel: { rotate: 45 }
      },
      yAxis: { type: 'value', name: '参与人数' },
      series: [
        {
          name: '参与人数',
          type: 'bar',
          data: data.participants,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 1, color: '#188df0' }
            ])
          }
        }
      ]
    })
  })

  // 趋势折线图
  const trendChart = echarts.init(document.getElementById('trendChart')!)
  getTrendsChart('participation_rate').then((data: any) => {
    trendChart.setOption({
      title: { text: '参与率年度趋势', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: data.years },
      yAxis: { type: 'value', name: '参与率(%)' },
      series: [
        {
          name: '参与率',
          type: 'line',
          data: data.values.map((v: number) => (v * 100).toFixed(1)),
          smooth: true,
          itemStyle: { color: '#67C23A' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
              { offset: 1, color: 'rgba(103, 194, 58, 0.1)' }
            ])
          },
          markLine: {
            data: [{ yAxis: data.target, name: '目标值' }]
          }
        }
      ]
    })
  })
}

onMounted(async () => {
  loading.value = true
  try {
    stats.value = await getStatistics()
    setTimeout(() => {
      initCharts()
    }, 100)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="dashboard-container">
    <el-card class="header-card" shadow="never">
      <h2>数据看板</h2>
      <p>实时监控河北省全民健身公共服务数据</p>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409EFF20">
              <el-icon :size="40" color="#409EFF"><Location /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_facilities || 0 }}</div>
              <div class="stat-label">健身设施总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67C23A20">
              <el-icon :size="40" color="#67C23A"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ (stats.total_population / 10000).toFixed(0) }}万</div>
              <div class="stat-label">覆盖人口</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #E6A23C20">
              <el-icon :size="40" color="#E6A23C"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ (stats.coverage_rate * 100).toFixed(1) }}%</div>
              <div class="stat-label">平均参与率</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #F56C6C20">
              <el-icon :size="40" color="#F56C6C"><Share /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.kg_entities || 0 }}</div>
              <div class="stat-label">知识图谱实体</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <div id="participationChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <div id="facilityChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <div id="activityChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <div id="trendChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-card h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
}

.header-card p {
  margin: 0;
  opacity: 0.9;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
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

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.charts-row {
  margin-bottom: 20px;
}
</style>
