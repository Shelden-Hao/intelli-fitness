<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { recommendActivities, recommendFacilities, getTrendingActivities, getPersonalizedPlan } from '../api/recommendation'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const userId = ref(1)
const activities = ref<any[]>([])
const facilities = ref<any[]>([])
const trending = ref<any[]>([])
const personalizedPlan = ref<any>(null)

const userProfile = ref({
  age: 30,
  gender: 'male',
  fitness_level: 'medium',
  preferences: ['有氧运动', '力量训练']
})

const loadRecommendations = async () => {
  loading.value = true
  try {
    activities.value = await recommendActivities(userId.value, 'collaborative', 5)
    facilities.value = await recommendFacilities(userId.value, 38.0428, 114.5149, 5)
    trending.value = await getTrendingActivities('石家庄市', 10)
  } catch (error) {
    ElMessage.error('加载推荐数据失败')
  } finally {
    loading.value = false
  }
}

const generatePlan = async () => {
  loading.value = true
  try {
    personalizedPlan.value = await getPersonalizedPlan(userProfile.value)
    ElMessage.success('个性化方案生成成功')
  } catch (error) {
    ElMessage.error('生成方案失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRecommendations()
})
</script>

<template>
  <div class="recommendation-container">
    <el-card class="header-card" shadow="never">
      <h2>智能推荐</h2>
      <p>基于协同过滤和深度学习的个性化推荐系统</p>
    </el-card>

    <!-- 用户画像 -->
    <el-card shadow="hover" class="profile-card">
      <template #header>
        <div class="card-header">
          <span>用户画像</span>
          <el-button type="primary" @click="generatePlan" :loading="loading">
            生成个性化方案
          </el-button>
        </div>
      </template>
      <el-form :model="userProfile" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="年龄">
              <el-input-number v-model="userProfile.age" :min="10" :max="100" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="性别">
              <el-select v-model="userProfile.gender">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="健身水平">
              <el-select v-model="userProfile.fitness_level">
                <el-option label="初级" value="low" />
                <el-option label="中级" value="medium" />
                <el-option label="高级" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="运动偏好">
          <el-checkbox-group v-model="userProfile.preferences">
            <el-checkbox label="有氧运动" />
            <el-checkbox label="力量训练" />
            <el-checkbox label="球类运动" />
            <el-checkbox label="柔韧性训练" />
          </el-checkbox-group>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 推荐活动 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="recommend-card">
          <template #header>
            <span>推荐活动</span>
          </template>
          <el-table :data="activities" v-loading="loading">
            <el-table-column prop="activity_name" label="活动名称" />
            <el-table-column prop="category" label="类别" width="120" />
            <el-table-column prop="intensity" label="强度" width="80" />
            <el-table-column label="推荐度" width="120">
              <template #default="{ row }">
                <el-progress :percentage="row.recommendation_score * 100" :stroke-width="8" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="recommend-card">
          <template #header>
            <span>推荐设施</span>
          </template>
          <el-table :data="facilities" v-loading="loading">
            <el-table-column prop="name" label="设施名称" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column label="距离" width="100">
              <template #default="{ row }">
                {{ row.distance_km.toFixed(1) }}km
              </template>
            </el-table-column>
            <el-table-column prop="rating" label="评分" width="80">
              <template #default="{ row }">
                <el-rate v-model="row.rating" disabled show-score text-color="#ff9900" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 热门活动 -->
    <el-card shadow="hover" class="trending-card">
      <template #header>
        <span>热门活动趋势</span>
      </template>
      <el-table :data="trending" v-loading="loading">
        <el-table-column type="index" label="排名" width="60" />
        <el-table-column prop="activity" label="活动名称" />
        <el-table-column label="参与人数" width="150">
          <template #default="{ row }">
            {{ row.participants.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="增长率" width="120">
          <template #default="{ row }">
            <el-tag :type="row.growth_rate > 0.2 ? 'success' : 'info'">
              +{{ (row.growth_rate * 100).toFixed(1) }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="trend" label="趋势" width="100">
          <template #default="{ row }">
            <el-icon v-if="row.trend === '上升'" color="#67C23A"><CaretTop /></el-icon>
            <el-icon v-else color="#909399"><Minus /></el-icon>
            {{ row.trend }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 个性化方案 -->
    <el-card shadow="hover" v-if="personalizedPlan" class="plan-card">
      <template #header>
        <span>个性化健身方案</span>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="每周目标时长">
          {{ personalizedPlan.weekly_target?.total_duration }} 分钟
        </el-descriptions-item>
        <el-descriptions-item label="每周目标消耗">
          {{ personalizedPlan.weekly_target?.total_calories }} 卡路里
        </el-descriptions-item>
        <el-descriptions-item label="锻炼频率">
          每周 {{ personalizedPlan.weekly_target?.frequency }} 次
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h4>每周计划</h4>
      <el-timeline>
        <el-timeline-item
          v-for="(day, index) in personalizedPlan.weekly_plan"
          :key="index"
          :timestamp="day.day"
        >
          <el-tag
            v-for="(activity, idx) in day.activities"
            :key="idx"
            type="success"
            style="margin-right: 10px"
          >
            {{ activity.name }} - {{ activity.duration }}分钟
          </el-tag>
        </el-timeline-item>
      </el-timeline>

      <el-divider />

      <h4>健身建议</h4>
      <ul>
        <li v-for="(tip, index) in personalizedPlan.tips" :key="index">{{ tip }}</li>
      </ul>
    </el-card>
  </div>
</template>

<style scoped>
.recommendation-container {
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

.profile-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recommend-card {
  margin-bottom: 20px;
}

.trending-card {
  margin-bottom: 20px;
}

.plan-card h4 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.plan-card ul {
  padding-left: 20px;
}

.plan-card li {
  margin: 10px 0;
  color: #606266;
}
</style>
