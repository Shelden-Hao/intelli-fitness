<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeMenu = ref('/')

const handleMenuSelect = (key: string) => {
  router.push(key)
}
</script>

<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="header-content">
        <div class="logo-section">
          <el-icon :size="32" color="#409EFF"><DataAnalysis /></el-icon>
          <h1>河北全民健身公共服务体系平台</h1>
        </div>
        <div class="subtitle">数智驱动 · 健康河北</div>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="200px" class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          @select="handleMenuSelect"
          router
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/dashboard">
            <el-icon><DataLine /></el-icon>
            <span>数据看板</span>
          </el-menu-item>
          <el-menu-item index="/knowledge-graph">
            <el-icon><Share /></el-icon>
            <span>知识图谱</span>
          </el-menu-item>
          <el-menu-item index="/evaluation">
            <el-icon><TrendCharts /></el-icon>
            <span>评价分析</span>
          </el-menu-item>
          <el-menu-item index="/motion-capture">
            <el-icon><VideoCamera /></el-icon>
            <span>动作捕捉</span>
          </el-menu-item>
          <el-menu-item index="/recommendation">
            <el-icon><Star /></el-icon>
            <span>智能推荐</span>
          </el-menu-item>
          <el-menu-item index="/data-management">
            <el-icon><FolderOpened /></el-icon>
            <span>数据管理</span>
          </el-menu-item>
          <el-menu-item index="/policy">
            <el-icon><Document /></el-icon>
            <span>政策文件</span>
          </el-menu-item>
          <el-menu-item index="/data-insights">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据洞察</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  width: 100%;
  overflow: hidden;
}
</style>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 60px !important;
}

.header-content {
  width: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 5px;
}

.logo-section h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin-left: 47px;
}

.sidebar {
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.el-menu-vertical {
  border-right: none;
  height: 100%;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}
</style>
