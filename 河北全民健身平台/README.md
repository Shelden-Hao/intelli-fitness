# 河北全民健身公共服务体系智能平台

## 🎯 项目简介

基于AI和大数据技术的河北省全民健身公共服务体系研究平台，集成数据采集、知识图谱、智能评价、推荐系统等核心功能。

## ✨ 核心功能

### 🔍 数据处理
- 多源数据自动采集爬虫
- NLP文本语义分析
- 数据清洗与标准化

### 🕸️ 知识图谱
- 七维度知识建模 (时间、区域、政策、指标、设施、运动、个人)
- 254个实体 + 634个关系
- OWL本体设计，支持Protégé可视化

### 📊 智能评价
- AHP层次分析法
- 均衡性与可及性评价
- 多指标综合评估

### 🎯 推荐系统
- 协同过滤算法
- 深度学习推荐
- 个性化健身方案

### 📈 客流预测
- 时间序列预测模型
- 智能调度优化

## 🛠️ 技术栈

**前端**: Vue 3 + TypeScript + Element Plus + ECharts + Three.js  
**后端**: Python + FastAPI + SQLAlchemy  
**数据库**: PostgreSQL + Neo4j + MongoDB  
**AI/ML**: PyTorch + Scikit-learn + spaCy + MediaPipe  
**容器化**: Docker + Docker Compose

## 📁 项目结构

```
河北全民健身平台/
├── 📂 backend/              # FastAPI后端服务
├── 📂 frontend/             # Vue3前端应用  
├── 📂 data_processing/      # 数据处理(爬虫+NLP)
├── 📂 knowledge_graph/      # 知识图谱构建
├── 📂 evaluation_model/     # 智能评价模型
├── 📂 ml_models/           # 机器学习模型
├── 📂 recommendation/       # 推荐系统
├── 📂 motion_capture/       # 动作捕捉
├── 📂 traffic_prediction/   # 客流预测
├── 📂 data/                # 数据存储
├── 📂 docker/              # 容器化配置
└── 📄 核心数据文件
```

详细结构请查看 [项目结构说明.md](./项目结构说明.md)

## 💡 技术亮点

### 🕸️ 知识图谱创新
- 七维度知识建模 (T-A-L-I-P-F-S)
- 254个实体 + 634个关系
- OWL本体设计，支持Protégé可视化

### 📊 智能评价创新  
- AHP层次分析法
- 多指标综合评价
- 均衡性与可及性分析

### 🎯 推荐系统创新
- 协同过滤 + 深度学习
- 个性化健身方案推荐

## 📊 数据资产

- **场馆数据**: 158个体育设施
- **覆盖范围**: 河北省11个地级市  
- **知识图谱**: 254实体 + 634关系
- **时间跨度**: 1970-2024年

## 🚀 快速启动

### 环境要求
- Node.js 18+ / Python 3.10+
- Docker & Docker Compose

### 启动命令
```bash
# 后端启动
cd backend && pip install -r requirements.txt && python main.py

# 前端启动  
cd frontend && npm install && npm run dev

# Docker启动
cd docker && docker-compose up -d
```

## 📄 许可证

河北经贸大学大学生创新训练计划项目，仅供学习研究使用。

**项目负责人**: 郝秀功  
**指导教师**: 曹玉辉、王卫红
