<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const videoFile = ref<File | null>(null)
const actionType = ref('squat')
const analysisResult = ref<any>(null)
const previewUrl = ref('')

const actionTypes = [
  { value: 'squat', label: '深蹲', icon: '🏋️' },
  { value: 'plank', label: '平板支撑', icon: '🧘' },
  { value: 'push_up', label: '俯卧撑', icon: '💪' }
]

const handleFileChange = (file: any) => {
  videoFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
  return false
}

const analyzeMotion = async () => {
  if (!videoFile.value) {
    ElMessage.warning('请先上传视频文件')
    return
  }

  loading.value = true
  try {
    // 模拟分析结果
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    analysisResult.value = {
      action_type: actionType.value,
      average_score: 85.5,
      total_frames: 150,
      analyzed_frames: 145,
      overall_feedback: [
        '整体动作较为标准',
        '建议膝关节弯曲角度再深一些',
        '注意保持背部挺直'
      ],
      frame_results: [
        { frame: 0, score: 88, status: '优秀' },
        { frame: 30, score: 85, status: '良好' },
        { frame: 60, score: 82, status: '良好' },
        { frame: 90, score: 87, status: '优秀' },
        { frame: 120, score: 84, status: '良好' }
      ]
    }
    
    ElMessage.success('分析完成')
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="motion-container">
    <el-card class="header-card" shadow="never">
      <h2>动作捕捉与分析</h2>
      <p>基于MediaPipe的实时姿态检测与智能纠正</p>
    </el-card>

    <el-row :gutter="20">
      <!-- 上传区域 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="upload-card">
          <template #header>
            <span>上传视频</span>
          </template>
          
          <el-form label-width="100px">
            <el-form-item label="动作类型">
              <el-radio-group v-model="actionType">
                <el-radio-button
                  v-for="action in actionTypes"
                  :key="action.value"
                  :label="action.value"
                >
                  {{ action.icon }} {{ action.label }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="视频文件">
              <el-upload
                class="upload-demo"
                drag
                :auto-upload="false"
                :on-change="handleFileChange"
                :limit="1"
                accept="video/*"
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  拖拽文件到此处或<em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    支持mp4, avi, mov等格式，文件大小不超过100MB
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                @click="analyzeMotion"
                :loading="loading"
                :disabled="!videoFile"
                size="large"
              >
                <el-icon><VideoCamera /></el-icon>
                开始分析
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 视频预览 -->
          <div v-if="previewUrl" class="video-preview">
            <h4>视频预览</h4>
            <video :src="previewUrl" controls style="width: 100%; max-height: 300px"></video>
          </div>
        </el-card>
      </el-col>

      <!-- 分析结果 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="result-card">
          <template #header>
            <span>分析结果</span>
          </template>

          <div v-if="!analysisResult" class="empty-state">
            <el-empty description="上传视频后查看分析结果" />
          </div>

          <div v-else class="result-content">
            <!-- 总体评分 -->
            <div class="score-section">
              <el-statistic title="综合得分" :value="analysisResult.average_score">
                <template #suffix>/100</template>
              </el-statistic>
              <el-progress
                :percentage="analysisResult.average_score"
                :stroke-width="20"
                :color="analysisResult.average_score >= 90 ? '#67C23A' : '#409EFF'"
              />
            </div>

            <el-divider />

            <!-- 分析统计 -->
            <el-descriptions :column="2" border size="small">
              <el-descriptions-item label="总帧数">
                {{ analysisResult.total_frames }}
              </el-descriptions-item>
              <el-descriptions-item label="分析帧数">
                {{ analysisResult.analyzed_frames }}
              </el-descriptions-item>
              <el-descriptions-item label="动作类型" :span="2">
                {{ actionTypes.find(a => a.value === analysisResult.action_type)?.label }}
              </el-descriptions-item>
            </el-descriptions>

            <el-divider />

            <!-- 反馈建议 -->
            <h4>改进建议</h4>
            <el-alert
              v-for="(feedback, index) in analysisResult.overall_feedback"
              :key="index"
              :title="feedback"
              type="info"
              :closable="false"
              style="margin-bottom: 10px"
            />

            <el-divider />

            <!-- 帧分析 -->
            <h4>关键帧分析</h4>
            <el-table :data="analysisResult.frame_results" size="small">
              <el-table-column prop="frame" label="帧号" width="80" />
              <el-table-column prop="score" label="得分" width="80" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="row.status === '优秀' ? 'success' : 'primary'"
                    size="small"
                  >
                    {{ row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 动作指南 -->
    <el-card shadow="hover" class="guide-card">
      <template #header>
        <span>动作指南</span>
      </template>
      <el-row :gutter="20">
        <el-col :xs="24" :md="8" v-for="action in actionTypes" :key="action.value">
          <el-card shadow="hover" class="action-guide">
            <h3>{{ action.icon }} {{ action.label }}</h3>
            <el-divider />
            <div v-if="action.value === 'squat'">
              <p><strong>要点：</strong></p>
              <ul>
                <li>双脚与肩同宽</li>
                <li>膝盖不要超过脚尖</li>
                <li>背部保持挺直</li>
                <li>下蹲至大腿与地面平行</li>
              </ul>
            </div>
            <div v-else-if="action.value === 'plank'">
              <p><strong>要点：</strong></p>
              <ul>
                <li>身体呈一条直线</li>
                <li>臀部不要抬高或下沉</li>
                <li>收紧核心肌群</li>
                <li>保持自然呼吸</li>
              </ul>
            </div>
            <div v-else>
              <p><strong>要点：</strong></p>
              <ul>
                <li>双手与肩同宽</li>
                <li>身体保持一条直线</li>
                <li>下降至肘关节90度</li>
                <li>推起时保持控制</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<style scoped>
.motion-container {
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

.upload-card, .result-card {
  margin-bottom: 20px;
  min-height: 600px;
}

.video-preview {
  margin-top: 20px;
}

.video-preview h4 {
  margin: 0 0 10px 0;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.result-content {
  padding: 10px;
}

.score-section {
  text-align: center;
  margin-bottom: 20px;
}

.result-content h4 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.guide-card {
  margin-bottom: 20px;
}

.action-guide {
  margin-bottom: 10px;
}

.action-guide h3 {
  margin: 0;
  text-align: center;
  color: #409EFF;
}

.action-guide ul {
  padding-left: 20px;
  margin: 10px 0;
}

.action-guide li {
  margin: 8px 0;
  color: #606266;
}
</style>
