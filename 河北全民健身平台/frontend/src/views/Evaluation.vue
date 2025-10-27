<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getBalanceEvaluation, getAccessibilityEvaluation, getAHPEvaluation, getComprehensiveEvaluation } from '../api/evaluation'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const selectedCity = ref('石家庄市')
const cities = ['石家庄市', '保定市', '唐山市']
const balanceData = ref<any>({})
const accessibilityData = ref<any>({})
const ahpData = ref<any>({})
const comprehensiveData = ref<any>({})

const loadEvaluationData = async () => {
  loading.value = true
  try {
    balanceData.value = await getBalanceEvaluation({ city: selectedCity.value })
    accessibilityData.value = await getAccessibilityEvaluation({ city: selectedCity.value })
    ahpData.value = await getAHPEvaluation()
    comprehensiveData.value = await getComprehensiveEvaluation(selectedCity.value)
    
    setTimeout(() => {
      initCharts()
    }, 100)
  } catch (error) {
    ElMessage.error('加载评价数据失败')
  } finally {
    loading.value = false
  }
}

const initCharts = () => {
  // 均衡性雷达图
  const balanceChart = echarts.init(document.getElementById('balanceChart')!)
  balanceChart.setOption({
    title: { text: '均衡性评价', left: 'center' },
    tooltip: {},
    radar: {
      indicator: [
        { name: '设施分布', max: 100 },
        { name: '资源投入', max: 100 },
        { name: '服务项目', max: 100 },
        { name: '人均面积', max: 100 }
      ]
    },
    series: [{
      type: 'radar',
      data: [{
        value: [78, 82, 75, 80],
        name: selectedCity.value
      }]
    }]
  })

  // AHP排名柱状图
  const ahpChart = echarts.init(document.getElementById('ahpChart')!)
  if (ahpData.value.ranking) {
    ahpChart.setOption({
      title: { text: 'AHP综合评价排名', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: ahpData.value.ranking.map((item: any) => item.city)
      },
      yAxis: { type: 'value', name: '得分' },
      series: [{
        type: 'bar',
        data: ahpData.value.ranking.map((item: any) => (item.score * 100).toFixed(1)),
        itemStyle: {
          color: (params: any) => {
            const colors = ['#5470c6', '#91cc75', '#fac858']
            return colors[params.dataIndex]
          }
        }
      }]
    })
  }

  // 综合评价仪表盘
  const gaugeChart = echarts.init(document.getElementById('gaugeChart')!)
  gaugeChart.setOption({
    title: { text: '综合评价得分', left: 'center' },
    series: [{
      type: 'gauge',
      progress: { show: true, width: 18 },
      axisLine: { lineStyle: { width: 18 } },
      axisTick: { show: false },
      splitLine: { length: 15, lineStyle: { width: 2, color: '#999' } },
      axisLabel: { distance: 25, color: '#999', fontSize: 14 },
      anchor: { show: true, showAbove: true, size: 25, itemStyle: { borderWidth: 10 } },
      title: { show: false },
      detail: {
        valueAnimation: true,
        fontSize: 40,
        offsetCenter: [0, '70%']
      },
      data: [{ value: comprehensiveData.value.overall_score || 0 }]
    }]
  })
}

onMounted(() => {
  loadEvaluationData()
})
</script>

<template>
  <div class="evaluation-container">
    <el-card class="header-card" shadow="never">
      <div class="header-content">
        <div>
          <h2>评价分析</h2>
          <p>均衡性与可及性智能评价模型</p>
        </div>
        <el-select v-model="selectedCity" @change="loadEvaluationData" size="large">
          <el-option v-for="city in cities" :key="city" :label="city" :value="city" />
        </el-select>
      </div>
    </el-card>

    <!-- 评价指标卡片 -->
    <el-row :gutter="20" class="metrics-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="metric-card">
          <el-statistic title="基尼系数" :value="balanceData.gini_coefficient?.per_capita_area || 0" :precision="3">
            <template #suffix>
              <el-tag :type="balanceData.gini_coefficient?.per_capita_area < 0.3 ? 'success' : 'warning'" size="small">
                {{ balanceData.gini_coefficient?.interpretation || '-' }}
              </el-tag>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="metric-card">
          <el-statistic title="集中指数" :value="balanceData.concentration_index?.value || 0" :precision="3">
            <template #suffix>
              <el-tag type="info" size="small">
                {{ balanceData.concentration_index?.interpretation?.slice(0, 10) || '-' }}
              </el-tag>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="metric-card">
          <el-statistic title="地理可及性" :value="(accessibilityData.geographic_accessibility * 100) || 0" :precision="1">
            <template #suffix>%</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="metric-card">
          <el-statistic title="综合得分" :value="comprehensiveData.overall_score || 0" :precision="1">
            <template #suffix>
              <el-tag :type="comprehensiveData.grade === '优秀' ? 'success' : 'primary'" size="small">
                {{ comprehensiveData.grade || '-' }}
              </el-tag>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="8">
        <el-card shadow="hover">
          <div id="balanceChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card shadow="hover">
          <div id="ahpChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card shadow="hover">
          <div id="gaugeChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细评价 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="detail-card">
          <template #header>
            <span>优势分析</span>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in comprehensiveData.strengths"
              :key="index"
              type="success"
            >
              {{ item }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="detail-card">
          <template #header>
            <span>改进建议</span>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in comprehensiveData.recommendations"
              :key="index"
              type="primary"
            >
              {{ item }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>

    <!-- 区位商列表 -->
    <el-card shadow="hover" v-if="balanceData.location_quotients">
      <template #header>
        <span>区位商分析</span>
      </template>
      <el-table :data="balanceData.location_quotients" stripe>
        <el-table-column prop="city" label="城市" />
        <el-table-column prop="location_quotient" label="区位商" width="120">
          <template #default="{ row }">
            {{ row.location_quotient.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="interpretation" label="解释" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.location_quotient > 1 ? 'success' : 'warning'" size="small">
              {{ row.location_quotient > 1 ? '高于平均' : '低于平均' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.evaluation-container {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0 0 10px 0;
}

.header-content p {
  margin: 0;
  opacity: 0.9;
}

.metrics-row {
  margin-bottom: 20px;
}

.metric-card {
  margin-bottom: 20px;
}

.charts-row {
  margin-bottom: 20px;
}

.detail-card {
  margin-bottom: 20px;
  min-height: 300px;
}
</style>
