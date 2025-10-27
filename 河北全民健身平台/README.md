# 数智驱动河北全民健身公共服务体系研究

## 项目概述

本项目以新时代河北全民健身公共服务为研究对象,围绕河北全民健身公共服务的健身资源配置、全民健身公共服务均衡性与可及性等,借助于新一代人工智能、大数据技术等探索新时代河北全民健身公共服务体系的智能化建设问题。

## 核心功能模块

### 1. 数据采集与预处理模块
- 多源数据采集(政府网站、体育局、统计局等)
- 数据清洗与标准化
- 数据特征提取与转换
- NLP文本分析与语义理解

### 2. 时空知识图谱构建模块
- 概念层模型构建
- 本体技术应用(Protégé)
- 图数据库存储(OrientDB/Neo4j)
- 实体关系抽取
- 知识图谱补全(TransE模型)

### 3. 均衡性与可及性智能评价模型
- 基尼系数计算
- 集中指数分析
- 区位商计算
- GIS空间分析
- AHP层次分析法
- 模糊综合评价
- 遗传算法优化
- 粒子群优化算法

### 4. 健身动作捕捉与指导系统
- 人体动作捕捉(BVH格式)
- 人体节点检测模型
- Three.js 3D可视化
- 动作纠正与反馈

### 5. 智能推荐系统
- 协同过滤算法
- 基于内容的推荐
- FIT-UTCF-VGG算法
- 个性化健身方案推荐

### 6. 数据可视化与分析平台
- 多维数据展示
- ECharts图表分析
- 地理信息可视化
- 实时数据监控

## 技术栈

### 前端技术栈
```
- Vue 3 (组件化框架)
- Vite (构建工具)
- Element Plus (UI组件库)
- Sass/SCSS (样式预处理)
- ECharts (数据可视化)
- Three.js (3D图形库)
- Axios (HTTP客户端)
- Vue Router (路由管理)
- Pinia (状态管理)
- TypeScript (类型系统)
```

### 后端技术栈
```
- Python 3.10+ (主要开发语言)
- FastAPI (Web框架)
- Django (可选,用于管理后台)
- Flask (轻量级服务)
- SQLAlchemy (ORM)
- Pydantic (数据验证)
```

### 数据库技术栈
```
- PostgreSQL (关系型数据库)
- MongoDB (文档数据库)
- Neo4j/OrientDB (图数据库)
- Elasticsearch (搜索引擎)
```

### AI/ML技术栈
```
- PyTorch (深度学习框架)
- TensorFlow (机器学习)
- Scikit-learn (传统ML算法)
- OpenCV (计算机视觉)
- MediaPipe (人体姿态检测)
- Transformers (NLP模型)
- spaCy (NLP处理)
- NLTK (自然语言工具包)
```

### 知识图谱技术栈
```
- Protégé (本体编辑器)
- Neo4j (图数据库)
- OrientDB (多模型数据库)
- RDFLib (RDF处理)
- py2neo (Python Neo4j驱动)
```

### 数据分析技术栈
```
- NumPy (数值计算)
- Pandas (数据分析)
- SciPy (科学计算)
- SPSS (统计分析)
- GeoPandas (地理数据)
- Shapely (几何操作)
```

### DevOps技术栈
```
- Docker (容器化)
- Docker Compose (容器编排)
- Nginx (反向代理)
- Git (版本控制)
- GitHub Actions (CI/CD)
```

## 项目结构

```
河北全民健身平台/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── views/          # 页面
│   │   ├── api/            # API接口
│   │   ├── store/          # 状态管理
│   │   ├── router/         # 路由配置
│   │   ├── assets/         # 静态资源
│   │   └── utils/          # 工具函数
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   ├── schemas/        # 数据验证
│   │   └── core/           # 核心配置
│   ├── requirements.txt
│   └── main.py
│
├── data_processing/          # 数据处理模块
│   ├── crawler/            # 数据爬虫
│   ├── cleaner/            # 数据清洗
│   ├── nlp/                # NLP处理
│   └── preprocessor/       # 预处理
│
├── knowledge_graph/          # 知识图谱模块
│   ├── ontology/           # 本体设计
│   ├── entity_extraction/  # 实体抽取
│   ├── relation_extraction/ # 关系抽取
│   ├── graph_builder/      # 图谱构建
│   └── graph_completion/   # 图谱补全
│
├── evaluation_model/         # 评价模型模块
│   ├── balance/            # 均衡性评价
│   ├── accessibility/      # 可及性评价
│   ├── gis_analysis/       # GIS分析
│   ├── ahp/                # 层次分析法
│   ├── fuzzy/              # 模糊评价
│   └── optimization/       # 优化算法
│
├── motion_capture/           # 动作捕捉模块
│   ├── pose_detection/     # 姿态检测
│   ├── bvh_processor/      # BVH处理
│   ├── action_analysis/    # 动作分析
│   └── feedback/           # 反馈系统
│
├── recommendation/           # 推荐系统模块
│   ├── collaborative/      # 协同过滤
│   ├── content_based/      # 基于内容
│   ├── hybrid/             # 混合推荐
│   └── models/             # 推荐模型
│
├── big_data/                 # 大数据处理
│   ├── hdfs/               # HDFS配置
│   ├── hive/               # Hive脚本
│   ├── spark/              # Spark任务
│   └── kafka/              # Kafka配置
│
├── ml_models/                # 机器学习模型
│   ├── training/           # 模型训练
│   ├── inference/          # 模型推理
│   ├── evaluation/         # 模型评估
│   └── saved_models/       # 保存的模型
│
├── data/                     # 数据目录
│   ├── raw/                # 原始数据
│   ├── processed/          # 处理后数据
│   ├── knowledge_graph/    # 知识图谱数据
│   └── models/             # 模型数据
│
├── docs/                     # 文档
│   ├── api/                # API文档
│   ├── design/             # 设计文档
│   └── user_manual/        # 用户手册
│
├── tests/                    # 测试
│   ├── unit/               # 单元测试
│   ├── integration/        # 集成测试
│   └── e2e/                # 端到端测试
│
├── docker/                   # Docker配置
│   ├── frontend/
│   ├── backend/
│   └── docker-compose.yml
│
├── scripts/                  # 脚本工具
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
│
└── README.md
```

## 创新亮点

### 1. 时空知识图谱创新
- 七维度知识表示(时间、区域、政策法规、指标、个人信息等)
- 本体技术与图数据库深度融合
- TransE模型知识图谱补全
- 多源异构数据融合

### 2. 智能评价模型创新
- 多算法融合(基尼系数、集中指数、区位商)
- AHP+模糊综合评价
- 遗传算法与粒子群优化
- GIS空间分析集成

### 3. 动作捕捉与指导创新
- BVH格式动作数据标准化
- Three.js 3D实时可视化
- 智能动作纠正反馈
- 个性化健身指导

### 4. 智能推荐创新
- FIT-UTCF-VGG混合算法
- 标签特征+图片特征融合
- 协同过滤优化
- 个性化方案生成

## 数据来源

### 官方数据源
- 国家统计局
- 河北省统计局
- 国家体育总局
- 河北省体育局
- 中国国民体质监测数据库
- 各市县体育局

### 政策文件
- 国家全民健身政策
- 河北省体育发展规划
- 全民健身实施计划
- 体育设施建设标准

### 社会数据
- 社交媒体数据
- 健身APP数据
- 问卷调查数据
- 用户行为数据

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Neo4j 5+
- Redis 7+

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd 河北全民健身平台
```

2. 安装前端依赖
```bash
cd frontend
npm install
```

3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

4. 启动服务
```bash
# 使用Docker Compose启动所有服务
docker-compose up -d

# 或分别启动
cd frontend && npm run dev
cd backend && python main.py
```

## 许可证

本项目为河北经贸大学大学生创新训练计划项目,仅供学习研究使用。

## 联系方式

- 项目负责人: 郝秀功
- 指导教师: 曹玉辉、王卫红
- 学院: 管理科学与信息工程学院
