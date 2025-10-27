<script setup lang="ts">
import { ref } from 'vue'

const policies = ref([
  {
    id: 1,
    title: '河北省全民健身实施计划(2021-2025年)',
    level: '省级',
    department: '河北省人民政府',
    publish_date: '2021-12-15',
    effective_date: '2022-01-01',
    key_points: [
      '到2025年,经常参加体育锻炼人数比例达到38.5%',
      '人均体育场地面积达到2.6平方米',
      '县(市、区)、乡镇(街道)、行政村(社区)三级公共健身设施和社区15分钟健身圈全覆盖'
    ],
    content: '为深入实施全民健身国家战略，加快体育强省建设，更好满足人民群众的健身和健康需求...',
    url: 'http://example.com/policy1'
  },
  {
    id: 2,
    title: '关于构建更高水平的全民健身公共服务体系的意见',
    level: '国家级',
    department: '中共中央办公厅、国务院办公厅',
    publish_date: '2022-03-23',
    effective_date: '2022-03-23',
    key_points: [
      '推动全民健身公共服务城乡区域均衡发展',
      '提升全民健身公共服务智慧化水平',
      '完善全民健身激励机制'
    ],
    content: '为深入贯彻习近平总书记关于体育工作的重要论述，构建更高水平的全民健身公共服务体系...',
    url: 'http://example.com/policy2'
  }
])

const selectedPolicy = ref<any>(null)
const dialogVisible = ref(false)

const viewPolicy = (policy: any) => {
  selectedPolicy.value = policy
  dialogVisible.value = true
}
</script>

<template>
  <div class="policy-container">
    <el-card class="header-card" shadow="never">
      <h2>政策文件</h2>
      <p>全民健身相关政策法规与文件</p>
    </el-card>

    <!-- 政策列表 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12" v-for="policy in policies" :key="policy.id">
        <el-card shadow="hover" class="policy-card">
          <template #header>
            <div class="card-header">
              <span class="policy-title">{{ policy.title }}</span>
              <el-tag :type="policy.level === '国家级' ? 'danger' : 'primary'" size="small">
                {{ policy.level }}
              </el-tag>
            </div>
          </template>

          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="发布单位">
              {{ policy.department }}
            </el-descriptions-item>
            <el-descriptions-item label="发布日期">
              {{ policy.publish_date }}
            </el-descriptions-item>
            <el-descriptions-item label="生效日期">
              {{ policy.effective_date }}
            </el-descriptions-item>
          </el-descriptions>

          <el-divider />

          <div class="key-points">
            <h4>核心要点</h4>
            <ul>
              <li v-for="(point, index) in policy.key_points" :key="index">
                {{ point }}
              </li>
            </ul>
          </div>

          <div class="policy-actions">
            <el-button type="primary" @click="viewPolicy(policy)">
              <el-icon><View /></el-icon>
              查看详情
            </el-button>
            <el-button type="success" link>
              <el-icon><Download /></el-icon>
              下载文件
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计信息 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic title="政策文件总数" :value="policies.length">
            <template #prefix>
              <el-icon color="#409EFF"><Document /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic title="国家级政策" :value="policies.filter(p => p.level === '国家级').length">
            <template #prefix>
              <el-icon color="#F56C6C"><Flag /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover">
          <el-statistic title="省级政策" :value="policies.filter(p => p.level === '省级').length">
            <template #prefix>
              <el-icon color="#67C23A"><Memo /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 政策详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="selectedPolicy?.title"
      width="80%"
      top="5vh"
    >
      <div v-if="selectedPolicy" class="policy-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="政策级别">
            <el-tag :type="selectedPolicy.level === '国家级' ? 'danger' : 'primary'">
              {{ selectedPolicy.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="发布单位">
            {{ selectedPolicy.department }}
          </el-descriptions-item>
          <el-descriptions-item label="发布日期">
            {{ selectedPolicy.publish_date }}
          </el-descriptions-item>
          <el-descriptions-item label="生效日期">
            {{ selectedPolicy.effective_date }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider />

        <h3>核心要点</h3>
        <el-timeline>
          <el-timeline-item
            v-for="(point, index) in selectedPolicy.key_points"
            :key="index"
            type="primary"
          >
            {{ point }}
          </el-timeline-item>
        </el-timeline>

        <el-divider />

        <h3>政策内容</h3>
        <p class="policy-content">{{ selectedPolicy.content }}</p>

        <el-divider />

        <div class="policy-link">
          <el-button type="primary" :href="selectedPolicy.url" target="_blank">
            <el-icon><Link /></el-icon>
            访问原文
          </el-button>
        </div>
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary">
          <el-icon><Download /></el-icon>
          下载文件
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.policy-container {
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

.policy-card {
  margin-bottom: 20px;
  min-height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.policy-title {
  font-weight: 600;
  font-size: 16px;
}

.key-points {
  margin: 20px 0;
}

.key-points h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.key-points ul {
  padding-left: 20px;
  margin: 0;
}

.key-points li {
  margin: 10px 0;
  color: #606266;
  line-height: 1.6;
}

.policy-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.policy-detail h3 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.policy-content {
  line-height: 1.8;
  color: #606266;
  text-indent: 2em;
}

.policy-link {
  text-align: center;
}
</style>
