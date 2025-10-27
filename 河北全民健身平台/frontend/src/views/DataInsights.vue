<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const insights = ref<any>({})
const hotKeywords = ref<string[]>([])
const recommendations = ref<any[]>([])
const latestNews = ref<any[]>([])
const dataQuality = ref<any>({})
const pipelineStatus = ref<any>({})

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001'

// 加载洞察数据
const loadInsights = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE}/api/v1/insights/latest`)
    insights.value = response.data
    hotKeywords.value = response.data.insights?.hot_keywords || []
    recommendations.value = response.data.insights?.recommendations || []
    latestNews.value = response.data.latest_news || []
    dataQuality.value = response.data.data_quality || {}
  } catch (error) {
    console.error('加载洞察数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载流水线状态
const loadPipelineStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/v1/insights/pipeline-status`)
    pipelineStatus.value = response.data
  } catch (error) {
    console.error('加载状态失败:', error)
  }
}

// 运行数据流水线
const runPipeline = async () => {
  loading.value = true
  try {
    const response = await axios.post(`${API_BASE}/api/v1/insights/run-pipeline`)
    ElMessage.success(response.data.message)
    setTimeout(() => {
      loadInsights()
      loadPipelineStatus()
    }, 3000)
  } catch (error) {
    ElMessage.error('启动流水线失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadInsights()
  loadPipelineStatus()
})
</script>

<template>
  <div class="insights-container">
    <el-card class="header-card" shadow="never">
      <h2>🔍 数据洞察中心</h2>
      <p>爬虫 → NLP分析 → 算法处理 → 智能洞察</p>
    </el-card>

    <!-- 流水线控制 -->
    <el-card shadow="hover" class="pipeline-card">
      <template #header>
        <div class="card-header">
          <span>数据处理流水线</span>
          <el-button type="primary" @click="runPipeline" :loading="loading">
            <el-icon><Refresh /></el-icon>
            运行流水线
          </el-button>
        </div>
      </template>
      
      <el-descriptions :column="4" border>
        <el-descriptions-item label="状态">
          <el-tag :type="pipelineStatus.status === 'completed' ? 'success' : 'warning'">
            {{ pipelineStatus.status === 'completed' ? '已完成' : pipelineStatus.status === 'never_run' ? '未运行' : '数据过期' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最后运行">
          {{ pipelineStatus.last_run ? new Date(pipelineStatus.last_run).toLocaleString() : '从未运行' }}
        </el-descriptions-item>
        <el-descriptions-item label="数据年龄">
          {{ pipelineStatus.data_age_minutes || 0 }} 分钟
        </el-descriptions-item>
        <el-descriptions-item label="数据新鲜度">
          <el-tag :type="pipelineStatus.is_fresh ? 'success' : 'danger'">
            {{ pipelineStatus.is_fresh ? '新鲜' : '过期' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="pipeline-steps">
        <el-steps :active="5" finish-status="success">
          <el-step title="数据爬取" description="从官网爬取数据" />
          <el-step title="NLP分析" description="文本分析与实体识别" />
          <el-step title="数据清洗" description="标准化与去重" />
          <el-step title="算法分析" description="趋势挖掘与推荐" />
          <el-step title="API生成" description="生成前端数据" />
        </el-steps>
      </div>
    </el-card>

    <!-- 热门关键词 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <template #header>
            <span>🔥 热门关键词</span>
          </template>
          <div v-if="hotKeywords.length > 0" class="keywords-cloud">
            <el-tag
              v-for="(keyword, index) in hotKeywords"
              :key="index"
              :type="index < 3 ? 'danger' : index < 6 ? 'warning' : 'info'"
              size="large"
              style="margin: 8px"
            >
              {{ keyword }}
            </el-tag>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <template #header>
            <span>📊 数据质量</span>
          </template>
          <div v-if="dataQuality.overall_score" class="quality-metrics">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-statistic title="完整性" :value="dataQuality.completeness * 100" :precision="1">
                  <template #suffix>%</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="准确性" :value="dataQuality.accuracy * 100" :precision="1">
                  <template #suffix>%</template>
                </el-statistic>
              </el-col>
            </el-row>
            <el-divider />
            <el-row :gutter="20">
              <el-col :span="12">
                <el-statistic title="时效性" :value="dataQuality.timeliness * 100" :precision="1">
                  <template #suffix>%</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="综合得分" :value="dataQuality.overall_score * 100" :precision="1">
                  <template #suffix>%</template>
                </el-statistic>
              </el-col>
            </el-row>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 智能推荐 -->
    <el-card shadow="hover" class="recommendations-card">
      <template #header>
        <span>💡 智能推荐</span>
      </template>
      <el-timeline v-if="recommendations.length > 0">
        <el-timeline-item
          v-for="(rec, index) in recommendations"
          :key="index"
          :timestamp="rec.keyword"
          placement="top"
        >
          <el-card>
            <h4>{{ rec.recommendation }}</h4>
            <p>基于关键词: <el-tag size="small">{{ rec.keyword }}</el-tag></p>
            <p>出现频次: {{ rec.frequency }} 次</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      <el-empty v-else description="暂无推荐" />
    </el-card>

    <!-- 最新新闻分析 -->
    <el-card shadow="hover">
      <template #header>
        <span>📰 最新新闻分析</span>
      </template>
      <el-table :data="latestNews" v-loading="loading">
        <el-table-column prop="title" label="标题" min-width="300" />
        <el-table-column label="关键词" width="300">
          <template #default="{ row }">
            <el-tag
              v-for="(kw, index) in row.keywords"
              :key="index"
              size="small"
              style="margin: 2px"
            >
              {{ kw }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="情感" width="120">
          <template #default="{ row }">
            <el-tag :type="row.sentiment === 'positive' ? 'success' : 'info'">
              {{ row.sentiment === 'positive' ? '积极' : row.sentiment === 'negative' ? '消极' : '中性' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.insights-container {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-card h2 {
  margin: 0 0 10px 0;
}

.header-card p {
  margin: 0;
  opacity: 0.9;
}

.pipeline-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pipeline-steps {
  margin-top: 20px;
}

.keywords-cloud {
  min-height: 200px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
}

.quality-metrics {
  padding: 20px;
}

.recommendations-card {
  margin: 20px 0;
}
</style>
