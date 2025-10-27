# 快速开始指南

## 环境要求

### 必需软件

- **Python**: 3.10 或更高版本
- **Node.js**: 18.0 或更高版本
- **Git**: 最新版本

### 可选软件(用于完整功能)

- **Docker**: 20.10+ (用于容器化部署)
- **PostgreSQL**: 14+ (或使用Docker)
- **Neo4j**: 5+ (或使用Docker)
- **Redis**: 7+ (或使用Docker)

---

## 方式一: 本地开发环境(推荐初学者)

### 1. 克隆项目

```bash
git clone <repository-url>
cd 河北全民健身平台
```

### 2. 初始化数据

```bash
# 创建必要的目录和生成示例数据
python3 scripts/init_data.py
```

### 3. 启动后端服务

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动

API文档: `http://localhost:8000/api/docs`

### 4. 启动前端服务

打开新的终端窗口:

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 5. 访问应用

在浏览器中打开: `http://localhost:5173`

---

## 方式二: 使用启动脚本(推荐)

### macOS/Linux

```bash
# 赋予执行权限
chmod +x scripts/start.sh

# 运行启动脚本
./scripts/start.sh
```

### Windows

```bash
# 使用PowerShell
.\scripts\start.ps1
```

脚本会自动:
1. 检查环境
2. 初始化数据
3. 启动后端服务
4. 启动前端服务

---

## 方式三: Docker容器化部署(推荐生产环境)

### 前提条件

确保已安装Docker和Docker Compose

### 启动所有服务

```bash
cd docker
docker-compose up -d
```

这将启动:
- PostgreSQL (端口 5432)
- MongoDB (端口 27017)
- Neo4j (端口 7474, 7687)
- Redis (端口 6379)
- Elasticsearch (端口 9200)
- 后端API (端口 8000)
- 前端应用 (端口 5173)
- Nginx (端口 80)

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 停止服务

```bash
docker-compose down
```

### 完全清理(包括数据卷)

```bash
docker-compose down -v
```

---

## 功能模块测试

### 1. 测试数据采集

```bash
cd data_processing/crawler
python sports_crawler.py
```

### 2. 测试数据预处理

```bash
cd data_processing/preprocessor
python data_cleaner.py
```

### 3. 测试NLP文本分析

```bash
cd data_processing/nlp
python text_analyzer.py
```

### 4. 测试知识图谱构建

```bash
# 需要先启动Neo4j
cd knowledge_graph
python graph_builder.py
```

### 5. 测试评价模型

```bash
# 均衡性评价
cd evaluation_model/balance
python balance_evaluator.py

# 可及性评价
cd evaluation_model/accessibility
python accessibility_evaluator.py

# AHP分析
cd evaluation_model/ahp
python ahp_model.py
```

### 6. 测试动作捕捉

```bash
cd motion_capture/pose_detection
python pose_analyzer.py
```

### 7. 测试推荐系统

```bash
cd recommendation/collaborative
python cf_recommender.py
```

---

## API接口测试

### 使用Swagger UI

访问: `http://localhost:8000/api/docs`

在Swagger UI中可以:
- 查看所有API接口
- 测试接口功能
- 查看请求/响应格式

### 使用curl测试

```bash
# 获取统计数据
curl http://localhost:8000/api/v1/data/statistics

# 获取健身设施
curl http://localhost:8000/api/v1/data/facilities

# 获取知识图谱实体
curl http://localhost:8000/api/v1/kg/entities

# 获取均衡性评价
curl http://localhost:8000/api/v1/evaluation/balance

# 获取推荐活动
curl http://localhost:8000/api/v1/recommend/activities?user_id=1
```

---

## 常见问题

### Q1: 端口被占用

**问题**: 启动时提示端口8000或5173被占用

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :5173

# 杀死进程
kill -9 <PID>
```

### Q2: Python依赖安装失败

**问题**: pip install失败

**解决**:
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: Neo4j连接失败

**问题**: 知识图谱模块无法连接Neo4j

**解决**:
1. 确保Neo4j服务已启动
2. 检查连接配置(默认: bolt://localhost:7687)
3. 验证用户名密码(默认: neo4j/password)

### Q4: 前端页面空白

**问题**: 访问localhost:5173显示空白页

**解决**:
1. 检查浏览器控制台错误
2. 确保后端服务已启动
3. 检查CORS配置
4. 清除浏览器缓存

### Q5: 数据文件不存在

**问题**: 运行时提示找不到数据文件

**解决**:
```bash
# 重新初始化数据
python3 scripts/init_data.py
```

---

## 开发建议

### 推荐的开发工具

- **IDE**: VSCode / PyCharm / WebStorm
- **API测试**: Postman / Insomnia
- **数据库管理**: DBeaver / Neo4j Browser
- **Git客户端**: GitKraken / SourceTree

### VSCode推荐插件

- Python
- Pylance
- Vue Language Features (Volar)
- TypeScript Vue Plugin (Volar)
- ESLint
- Prettier
- Docker

### 代码规范

- Python: 遵循PEP 8
- JavaScript/TypeScript: 使用ESLint + Prettier
- 提交信息: 遵循Conventional Commits

---

## 下一步

1. 📖 阅读 [README.md](./README.md) 了解项目详情
2. 📚 查看 [技术实现方案](./docs/技术实现方案.md) 了解技术细节
3. 📊 查看 [实施进度](./docs/实施进度.md) 了解开发进度
4. 🎯 开始开发新功能或修复Bug

---

## 获取帮助

- 📧 Email: 1603199246@qq.com
- 📝 Issues: 在GitHub仓库提交Issue
- 💬 讨论: 加入项目讨论组

---

**祝您使用愉快! 🎉**
