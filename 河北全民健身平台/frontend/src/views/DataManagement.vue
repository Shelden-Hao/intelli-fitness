<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFacilities, getPopulation, getParticipation } from '../api/data'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const activeTab = ref('facilities')
const facilities = ref<any[]>([])
const population = ref<any[]>([])
const participation = ref<any[]>([])
const searchQuery = ref('')

const loadData = async () => {
  loading.value = true
  try {
    facilities.value = await getFacilities()
    population.value = await getPopulation()
    participation.value = await getParticipation()
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const filteredFacilities = ref<any[]>([])
const handleSearch = () => {
  if (!searchQuery.value) {
    filteredFacilities.value = facilities.value
  } else {
    filteredFacilities.value = facilities.value.filter((f: any) =>
      f.name.includes(searchQuery.value) || f.city.includes(searchQuery.value)
    )
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="data-container">
    <el-card class="header-card" shadow="never">
      <h2>数据管理</h2>
      <p>全民健身公共服务数据查询与管理</p>
    </el-card>

    <el-card shadow="hover">
      <el-tabs v-model="activeTab">
        <!-- 健身设施 -->
        <el-tab-pane label="健身设施" name="facilities">
          <div class="search-bar">
            <el-input
              v-model="searchQuery"
              placeholder="搜索设施名称或城市..."
              @input="handleSearch"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>

          <el-table :data="facilities" v-loading="loading" stripe>
            <el-table-column prop="name" label="设施名称" min-width="200" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="city" label="城市" width="120" />
            <el-table-column prop="district" label="区域" width="100" />
            <el-table-column prop="area" label="面积(㎡)" width="100" />
            <el-table-column prop="capacity" label="容量(人)" width="100" />
            <el-table-column prop="open_hours" label="开放时间" width="150" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" link>详情</el-button>
                <el-button type="success" size="small" link>编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 人口数据 -->
        <el-tab-pane label="人口数据" name="population">
          <el-table :data="population" v-loading="loading" stripe>
            <el-table-column prop="city" label="城市" width="150" />
            <el-table-column label="总人口" width="120">
              <template #default="{ row }">
                {{ (row.total_population / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="城镇人口" width="120">
              <template #default="{ row }">
                {{ (row.urban_population / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="农村人口" width="120">
              <template #default="{ row }">
                {{ (row.rural_population / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="0-14岁" width="120">
              <template #default="{ row }">
                {{ (row.age_0_14 / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="15-64岁" width="120">
              <template #default="{ row }">
                {{ (row.age_15_64 / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="65岁以上" width="120">
              <template #default="{ row }">
                {{ (row.age_65_plus / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column prop="year" label="年份" width="100" />
          </el-table>
        </el-tab-pane>

        <!-- 参与数据 -->
        <el-tab-pane label="参与数据" name="participation">
          <el-table :data="participation" v-loading="loading" stripe>
            <el-table-column prop="city" label="城市" width="150" />
            <el-table-column label="经常参与人数" width="150">
              <template #default="{ row }">
                {{ (row.regular_participants / 10000).toFixed(0) }}万
              </template>
            </el-table-column>
            <el-table-column label="参与率" width="120">
              <template #default="{ row }">
                <el-tag :type="row.participation_rate >= 0.3 ? 'success' : 'warning'">
                  {{ (row.participation_rate * 100).toFixed(1) }}%
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="weekly_frequency" label="每周频次" width="120" />
            <el-table-column prop="avg_duration" label="平均时长(分)" width="120" />
            <el-table-column label="热门活动" min-width="300">
              <template #default="{ row }">
                <el-tag
                  v-for="(activity, index) in row.popular_activities"
                  :key="index"
                  style="margin-right: 5px"
                  size="small"
                >
                  {{ activity }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 数据统计 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic title="设施总数" :value="facilities.length">
            <template #prefix>
              <el-icon color="#409EFF"><Location /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic title="覆盖城市" :value="population.length">
            <template #prefix>
              <el-icon color="#67C23A"><MapLocation /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic
            title="平均参与率"
            :value="participation.length > 0 ? (participation.reduce((sum: number, p: any) => sum + p.participation_rate, 0) / participation.length * 100) : 0"
            :precision="1"
          >
            <template #suffix>%</template>
            <template #prefix>
              <el-icon color="#E6A23C"><TrendCharts /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.data-container {
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

.search-bar {
  margin-bottom: 20px;
}
</style>
