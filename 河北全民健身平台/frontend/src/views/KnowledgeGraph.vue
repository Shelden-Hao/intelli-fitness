<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEntities, getGraphStatistics, searchGraph, getVisualizationData } from '../api/knowledgeGraph'
import { ElMessage } from 'element-plus'
import KnowledgeGraphViz from '../components/KnowledgeGraphViz.vue'

const loading = ref(false)
const searchQuery = ref('')
const statistics = ref<any>({})
const entities = ref<any[]>([])
const searchResults = ref<any[]>([])
const selectedEntity = ref('')
const graphData = ref<any>({ nodes: [], edges: [] })
const showGraph = ref(true)

// 获取统计信息
const loadStatistics = async () => {
  try {
    statistics.value = await getGraphStatistics()
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

// 加载实体列表
const loadEntities = async (entityType?: string) => {
  loading.value = true
  try {
    const params = entityType ? { entity_type: entityType } : {}
    entities.value = await getEntities(params)
  } catch (error) {
    ElMessage.error('加载实体失败')
  } finally {
    loading.value = false
  }
}

// 搜索图谱
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  
  loading.value = true
  try {
    searchResults.value = await searchGraph(searchQuery.value)
    if (searchResults.value.length === 0) {
      ElMessage.info('未找到相关结果')
    }
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

// 可视化实体关系
const visualizeEntity = async (entityName: string) => {
  selectedEntity.value = entityName
  loading.value = true
  try {
    graphData.value = await getVisualizationData(entityName, 2)
    ElMessage.success(`已加载 ${entityName} 的关系网络`)
  } catch (error) {
    ElMessage.error('加载可视化数据失败')
  } finally {
    loading.value = false
  }
}

// 加载完整图谱
const loadFullGraph = async () => {
  loading.value = true
  try {
    // 加载完整的知识图谱数据
    graphData.value = await getVisualizationData('石家庄市', 3)
    ElMessage.success('完整图谱加载成功')
  } catch (error) {
    ElMessage.error('加载完整图谱失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStatistics()
  loadEntities()
  // 自动加载完整图谱
  loadFullGraph()
})
</script>

<template>
  <div class="kg-container">
    <el-card class="header-card" shadow="never">
      <h2>时空知识图谱</h2>
      <p>七维度全民健身公共服务知识表示</p>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="实体总数" :value="statistics.total_entities || 0">
            <template #prefix>
              <el-icon color="#409EFF"><Share /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="关系总数" :value="statistics.total_relations || 0">
            <template #prefix>
              <el-icon color="#67C23A"><Connection /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="实体类型" :value="Object.keys(statistics.entity_types || {}).length">
            <template #prefix>
              <el-icon color="#E6A23C"><Grid /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="关系类型" :value="Object.keys(statistics.relation_types || {}).length">
            <template #prefix>
              <el-icon color="#F56C6C"><Link /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索区域 -->
    <el-card shadow="hover" class="search-card">
      <el-input
        v-model="searchQuery"
        placeholder="搜索实体、关系..."
        size="large"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
        <template #append>
          <el-button :icon="Search" @click="handleSearch" :loading="loading">搜索</el-button>
        </template>
      </el-input>

      <!-- 搜索结果 -->
      <div v-if="searchResults.length > 0" class="search-results">
        <h4>搜索结果</h4>
        <el-table :data="searchResults" stripe>
          <el-table-column prop="entity" label="实体名称" />
          <el-table-column prop="type" label="类型" width="120" />
          <el-table-column prop="score" label="相关度" width="100">
            <template #default="{ row }">
              <el-progress :percentage="row.score * 100" :show-text="false" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="visualizeEntity(row.entity)">
                可视化
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 知识图谱可视化 -->
    <el-card shadow="hover" class="graph-viz-card">
      <template #header>
        <div class="card-header">
          <span>知识图谱可视化</span>
          <el-button type="primary" size="small" @click="loadFullGraph">
            加载完整图谱
          </el-button>
        </div>
      </template>
      <div v-if="graphData.nodes.length === 0" class="empty-state">
        <el-empty description="点击上方按钮加载知识图谱" />
      </div>
      <KnowledgeGraphViz v-else :graphData="graphData" />
    </el-card>

    <!-- 实体列表 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="entity-card">
          <template #header>
            <div class="card-header">
              <span>实体列表</span>
              <el-select v-model="selectedEntity" placeholder="选择实体类型" @change="loadEntities" clearable>
                <el-option label="全部" value="" />
                <el-option label="城市" value="City" />
                <el-option label="设施" value="Facility" />
                <el-option label="活动" value="Activity" />
                <el-option label="政策" value="Policy" />
              </el-select>
            </div>
          </template>
          <el-table :data="entities" height="400" v-loading="loading">
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button size="small" type="primary" link @click="visualizeEntity(row.name)">
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="viz-card">
          <template #header>
            <div class="card-header">
              <span>实体详情</span>
              <el-tag v-if="selectedEntity" type="success">{{ selectedEntity }}</el-tag>
            </div>
          </template>
          <div class="graph-viz">
            <div v-if="graphData.nodes.length === 0" class="empty-state">
              <el-empty description="选择实体查看详细信息" />
            </div>
            <div v-else class="graph-display">
              <div class="graph-info">
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item label="节点数">{{ graphData.nodes.length }}</el-descriptions-item>
                  <el-descriptions-item label="边数">{{ graphData.edges.length }}</el-descriptions-item>
                </el-descriptions>
              </div>
              <div class="nodes-list">
                <h4>关联节点</h4>
                <el-tag
                  v-for="node in graphData.nodes"
                  :key="node.id"
                  :type="node.type === 'City' ? 'primary' : node.type === 'Facility' ? 'success' : 'info'"
                  style="margin: 5px"
                >
                  {{ node.label }}
                </el-tag>
              </div>
              <div class="edges-list">
                <h4>关系列表</h4>
                <el-timeline>
                  <el-timeline-item
                    v-for="(edge, index) in graphData.edges.slice(0, 5)"
                    :key="index"
                    :timestamp="edge.label"
                  >
                    {{ graphData.nodes.find((n: any) => n.id === edge.source)?.label }} → 
                    {{ graphData.nodes.find((n: any) => n.id === edge.target)?.label }}
                  </el-timeline-item>
                </el-timeline>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 实体类型分布 -->
    <el-card shadow="hover" class="distribution-card">
      <template #header>
        <span>实体类型分布</span>
      </template>
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6" v-for="(count, type) in statistics.entity_types" :key="type">
          <div class="type-item">
            <div class="type-count">{{ count }}</div>
            <div class="type-name">{{ type }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<style scoped>
.kg-container {
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

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-results {
  margin-top: 20px;
}

.search-results h4 {
  margin: 0 0 15px 0;
}

.entity-card, .viz-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.graph-viz {
  min-height: 400px;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.graph-display {
  padding: 10px;
}

.graph-info {
  margin-bottom: 20px;
}

.nodes-list, .edges-list {
  margin-top: 20px;
}

.nodes-list h4, .edges-list h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #606266;
}

.distribution-card {
  margin-bottom: 20px;
}

.type-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 10px;
}

.type-count {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
}

.type-name {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
