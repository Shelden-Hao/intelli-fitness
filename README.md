# 数智驱动河北全民健身公共服务体系研究平台

> 河北经贸大学大学生创新训练计划项目  
> 项目作者：郝秀功  
> 指导教师：曹玉辉、王卫红

---

## 📖 项目简介

本项目是一个基于人工智能和大数据技术的全民健身公共服务体系研究平台，旨在通过数据采集、NLP分析、知识图谱构建、智能推荐等技术手段，为河北省全民健身事业提供数据支撑和决策参考。

### 核心特点

- 🔄 **完整数据闭环**：从数据爬取到前端展示的全流程自动化
- 🤖 **智能分析**：集成NLP、知识图谱、协同过滤等多种AI技术
- 📊 **可视化展示**：基于ECharts的专业数据可视化
- 🎯 **个性化推荐**：基于深度学习的智能推荐系统
- 📈 **实时监控**：数据质量监控和流水线状态追踪

---

## 🛠️ 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 主要开发语言 |
| **FastAPI** | 0.104+ | Web框架 |
| **jieba** | 0.42+ | 中文分词 |
| **scikit-learn** | 1.3+ | 机器学习 |
| **PyTorch** | 2.0+ | 深度学习 |
| **loguru** | 0.7+ | 日志管理 |

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue 3** | 3.3+ | 前端框架 |
| **TypeScript** | 5.0+ | 类型安全 |
| **Element Plus** | 2.4+ | UI组件库 |
| **ECharts** | 5.4+ | 数据可视化 |
| **Axios** | 1.6+ | HTTP客户端 |
| **Vite** | 5.0+ | 构建工具 |

### 核心算法

- **NLP技术**：TF-IDF关键词提取、命名实体识别、情感分析
- **知识图谱**：TransE模型、图谱可视化
- **推荐系统**：协同过滤、深度学习推荐
- **数据处理**：爬虫、数据清洗、流水线处理

---

## 🎯 功能介绍

### 1. 数据管理
- ✅ 设施数据管理（8个真实设施）
- ✅ 人口数据管理（3个城市）
- ✅ 参与数据管理
- ✅ 政策文件管理

### 2. 知识图谱
- ✅ 知识图谱可视化（力导向布局）
- ✅ 实体搜索和详情查看
- ✅ 关系网络展示
- ✅ TransE模型训练

### 3. 智能推荐
- ✅ 基于协同过滤的推荐
- ✅ 深度学习推荐模型
- ✅ 个性化推荐结果

### 4. 数据洞察
- ✅ 数据爬取（新闻、设施、政策）
- ✅ NLP文本分析
- ✅ 热门关键词提取
- ✅ 智能推荐生成
- ✅ 数据质量监控

### 5. 数据可视化
- ✅ 数据看板
- ✅ 统计图表
- ✅ 地图可视化
- ✅ 趋势分析

---

## 🚀 项目启动

### 前置要求

- **Python**: 3.8 或更高版本
- **Node.js**: 18.0 或更高版本

### 第一步：克隆项目

```bash
# git clone <repository-url>
```

### 第二步：启动后端

```bash
# 进入项目目录
cd 河北全民健身平台

# 安装 Python 依赖
pip3 install fastapi uvicorn loguru jieba scikit-learn

# 启动后端服务
cd backend
python3 main.py
```

**后端启动成功标志**：
```
🚀 应用启动中...
📝 项目名称: 河北全民健身公共服务体系平台
🌍 环境: development
🔗 API文档: http://0.0.0.0:8001/api/docs
```

**后端地址**：http://localhost:8001  
**API文档**：http://localhost:8001/api/docs

### 第三步：启动前端

**打开新的终端窗口**，执行：

```bash
# 进入前端目录
cd 河北全民健身平台/frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

**前端启动成功标志**：
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**前端地址**：http://localhost:5173

---

## 📁 项目结构

```
nlp/
├── 河北全民健身平台/              # 主项目目录
│   ├── backend/                   # 后端服务
│   │   ├── app/
│   │   │   ├── api/v1/           # API路由
│   │   │   │   └── endpoints/    # API端点
│   │   │   └── core/             # 核心配置
│   │   └── main.py               # 后端入口
│   │
│   ├── frontend/                  # 前端应用
│   │   ├── src/
│   │   │   ├── views/            # 页面组件
│   │   │   ├── components/       # 公共组件
│   │   │   ├── router/           # 路由配置
│   │   │   └── api/              # API接口
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   ├── data_processing/           # 数据处理模块
│   │   ├── crawler/              # 爬虫
│   │   ├── nlp/                  # NLP分析
│   │   ├── preprocessor/         # 数据清洗
│   │   └── pipeline/             # 数据流水线
│   │
│   ├── ml_models/                 # 机器学习模型
│   │   ├── knowledge_graph/      # 知识图谱
│   │   └── recommendation/       # 推荐系统
│   │
│   └── data/                      # 数据目录
│       ├── raw/                  # 原始数据
│       ├── crawled/              # 爬取数据
│       ├── processed/            # 处理数据
│       └── api/                  # API数据
│
├── .gitignore                     # Git忽略配置
└── README.md                      # 项目说明（本文件）
```

---

## 🌐 访问地址

启动成功后，可以访问以下地址：

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端应用** | http://localhost:5173 | 主界面 |
| **后端API** | http://localhost:8001 | API服务 |
| **API文档** | http://localhost:8001/api/docs | API文档 |

---

## 📊 主要功能页面

### 1. 数据看板 (Dashboard)
- 统计概览
- 数据可视化图表
- 实时数据展示

### 2. 知识图谱 (Knowledge Graph)
- 交互式图谱可视化
- 实体搜索
- 关系查看

### 3. 智能推荐 (Recommendation)
- 个性化推荐
- 推荐解释
- 用户反馈

### 4. 数据洞察 (Data Insights)
- 热门关键词
- 数据质量监控
- 智能推荐
- 流水线控制

### 5. 数据管理 (Data Management)
- 设施管理
- 数据上传
- 数据导出

---

## 🔧 常见问题

### Q1: 后端启动失败？

**问题**：提示缺少模块

**解决**：
```bash
pip3 install -r backend/requirements-min.txt
```

### Q2: 前端启动失败？

**问题**：`npm install` 失败

**解决**：
```bash
# 清除缓存
npm cache clean --force

# 重新安装
rm -rf node_modules package-lock.json
npm install
```

### Q3: 端口被占用？

**问题**：8001或5173端口已被占用

**解决**：
```bash
# 查找占用端口的进程
lsof -i :8001
lsof -i :5173

# 杀死进程
kill -9 <PID>
```

### Q4: 数据文件不存在？

**问题**：提示找不到数据文件

**解决**：
```bash
# 运行数据初始化脚本
cd 河北全民健身平台
python3 scripts/init_real_data.py
```

---

## 📚 API文档

启动后端后，访问 http://localhost:8001/api/docs 查看完整的API文档。

### 主要API端点

- `GET /api/v1/data/facilities` - 获取设施数据
- `GET /api/v1/data/population` - 获取人口数据
- `GET /api/v1/kg/entities` - 获取知识图谱实体
- `GET /api/v1/kg/graph` - 获取完整图谱
- `POST /api/v1/recommend/predict` - 获取推荐结果
- `GET /api/v1/insights/latest` - 获取最新洞察
- `POST /api/v1/insights/run-pipeline` - 运行数据流水线

---

## 📄 许可证

本项目为河北经贸大学大学生创新训练计划项目，仅供学习和研究使用。
