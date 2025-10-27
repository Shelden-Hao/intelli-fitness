# 系统演示指南

## 🎬 功能演示

### 演示环境

- **前端地址**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/api/docs

---

## 📋 演示流程

### 1. 数据管理模块演示

#### 1.1 查询健身设施

**API**: `GET /api/v1/data/facilities`

```bash
curl http://localhost:8000/api/v1/data/facilities
```

**预期结果**: 返回3条健身设施数据

```json
[
  {
    "id": 1,
    "name": "石家庄市体育馆",
    "type": "综合体育馆",
    "city": "石家庄市",
    "area": 15000,
    "capacity": 8000
  }
]
```

#### 1.2 查询人口数据

**API**: `GET /api/v1/data/population`

```bash
curl http://localhost:8000/api/v1/data/population?city=石家庄市
```

#### 1.3 查询统计概览

**API**: `GET /api/v1/data/statistics`

```bash
curl http://localhost:8000/api/v1/data/statistics
```

**预期结果**:
```json
{
  "total_facilities": 1258,
  "total_population": 28000000,
  "coverage_rate": 0.315,
  "kg_entities": 15432
}
```

---

### 2. 知识图谱模块演示

#### 2.1 查询实体

**API**: `GET /api/v1/kg/entities`

```bash
curl http://localhost:8000/api/v1/kg/entities?entity_type=City
```

**预期结果**: 返回城市实体列表

#### 2.2 查询关系

**API**: `GET /api/v1/kg/relations`

```bash
curl http://localhost:8000/api/v1/kg/relations?source=石家庄市体育馆
```

**预期结果**: 返回设施的关系网络

#### 2.3 图谱搜索

**API**: `GET /api/v1/kg/search?query=石家庄`

```bash
curl http://localhost:8000/api/v1/kg/search?query=石家庄
```

#### 2.4 可视化数据

**API**: `GET /api/v1/kg/visualization?center_entity=石家庄市体育馆`

```bash
curl http://localhost:8000/api/v1/kg/visualization?center_entity=石家庄市体育馆
```

**预期结果**: 返回节点和边数据，可用于前端可视化

---

### 3. 评价模型模块演示

#### 3.1 均衡性评价

**API**: `GET /api/v1/evaluation/balance`

```bash
curl http://localhost:8000/api/v1/evaluation/balance
```

**预期结果**:
```json
{
  "gini_coefficient": {
    "per_capita_area": 0.312,
    "interpretation": "相对均衡"
  },
  "concentration_index": {
    "value": 0.245,
    "interpretation": "设施分布与人口分布较为匹配"
  }
}
```

#### 3.2 可及性评价

**API**: `GET /api/v1/evaluation/accessibility`

```bash
curl http://localhost:8000/api/v1/evaluation/accessibility
```

**预期结果**:
```json
{
  "geographic_accessibility": 0.78,
  "temporal_accessibility": 0.65,
  "comprehensive_score": 0.725,
  "interpretation": "良好"
}
```

#### 3.3 AHP综合评价

**API**: `GET /api/v1/evaluation/ahp`

```bash
curl http://localhost:8000/api/v1/evaluation/ahp
```

**预期结果**: 返回城市排名

```json
{
  "ranking": [
    {"rank": 1, "city": "石家庄市", "score": 0.358},
    {"rank": 2, "city": "唐山市", "score": 0.330},
    {"rank": 3, "city": "保定市", "score": 0.312}
  ]
}
```

#### 3.4 综合评价

**API**: `GET /api/v1/evaluation/comprehensive?city=石家庄市`

```bash
curl http://localhost:8000/api/v1/evaluation/comprehensive?city=石家庄市
```

**预期结果**: 返回详细的评价报告，包括优势、劣势和建议

---

### 4. 动作捕捉模块演示

#### 4.1 获取支持的动作

**API**: `GET /api/v1/motion/actions`

```bash
curl http://localhost:8000/api/v1/motion/actions
```

**预期结果**:
```json
[
  {
    "id": "squat",
    "name": "深蹲",
    "category": "力量训练",
    "difficulty": "中等"
  }
]
```

#### 4.2 分析动作视频

**API**: `POST /api/v1/motion/analyze`

```bash
curl -X POST http://localhost:8000/api/v1/motion/analyze \
  -F "video=@test_video.mp4" \
  -F "action_type=squat"
```

**预期结果**: 返回动作分析结果和反馈

#### 4.3 查询分析历史

**API**: `GET /api/v1/motion/history?user_id=1`

```bash
curl http://localhost:8000/api/v1/motion/history?user_id=1
```

---

### 5. 推荐系统模块演示

#### 5.1 推荐健身活动

**API**: `GET /api/v1/recommend/activities?user_id=1`

```bash
curl http://localhost:8000/api/v1/recommend/activities?user_id=1&top_n=5
```

**预期结果**:
```json
[
  {
    "activity_name": "跑步",
    "category": "有氧运动",
    "recommendation_score": 0.92,
    "reason": "根据您的运动偏好,推荐跑步"
  }
]
```

#### 5.2 推荐健身设施

**API**: `GET /api/v1/recommend/facilities`

```bash
curl "http://localhost:8000/api/v1/recommend/facilities?user_id=1&latitude=38.0428&longitude=114.5149"
```

**预期结果**: 返回附近推荐的健身设施

#### 5.3 生成个性化方案

**API**: `POST /api/v1/recommend/personalized`

```bash
curl -X POST http://localhost:8000/api/v1/recommend/personalized \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "gender": "male",
    "fitness_level": "medium",
    "preferences": ["有氧运动", "力量训练"]
  }'
```

**预期结果**: 返回每周健身计划

#### 5.4 查看热门活动

**API**: `GET /api/v1/recommend/trending`

```bash
curl http://localhost:8000/api/v1/recommend/trending?city=石家庄市
```

---

### 6. 数据可视化模块演示

#### 6.1 获取地图数据

**API**: `GET /api/v1/viz/map-data`

```bash
curl http://localhost:8000/api/v1/viz/map-data
```

**预期结果**: 返回设施位置和覆盖区域数据

#### 6.2 参与率图表

**API**: `GET /api/v1/viz/charts/participation`

```bash
curl http://localhost:8000/api/v1/viz/charts/participation
```

**预期结果**:
```json
{
  "cities": ["石家庄", "保定", "唐山"],
  "participation_rates": [31.8, 29.8, 31.2],
  "target_rate": 38.5
}
```

#### 6.3 设施分布图表

**API**: `GET /api/v1/viz/charts/facility-distribution`

```bash
curl http://localhost:8000/api/v1/viz/charts/facility-distribution
```

#### 6.4 趋势图表

**API**: `GET /api/v1/viz/charts/trends?indicator=participation_rate`

```bash
curl http://localhost:8000/api/v1/viz/charts/trends?indicator=participation_rate
```

---

## 🖥️ 前端界面演示

### 首页

访问 `http://localhost:5173`

**展示内容**:
- 项目介绍横幅
- 统计数据卡片(设施总数、覆盖人口、参与率、知识图谱实体)
- 核心功能模块卡片
- 创新亮点展示

**交互功能**:
- 点击功能卡片跳转到对应页面
- 响应式布局适配不同屏幕

### 侧边栏导航

**菜单项**:
1. 首页
2. 数据看板
3. 知识图谱
4. 评价分析
5. 动作捕捉
6. 智能推荐
7. 数据管理
8. 政策文件

---

## 🧪 测试场景

### 场景1: 查询城市健身设施分布

1. 访问API: `/api/v1/data/facilities?city=石家庄市`
2. 查看返回的设施列表
3. 访问API: `/api/v1/viz/map-data`
4. 获取地图可视化数据

### 场景2: 评估城市健身服务水平

1. 查询均衡性评价: `/api/v1/evaluation/balance?city=石家庄市`
2. 查询可及性评价: `/api/v1/evaluation/accessibility?city=石家庄市`
3. 查询综合评价: `/api/v1/evaluation/comprehensive?city=石家庄市`
4. 获取评价趋势: `/api/v1/evaluation/trends?city=石家庄市`

### 场景3: 获取个性化健身推荐

1. 推荐活动: `/api/v1/recommend/activities?user_id=1`
2. 推荐设施: `/api/v1/recommend/facilities?user_id=1&latitude=38.0428&longitude=114.5149`
3. 生成计划: `POST /api/v1/recommend/personalized`
4. 查看热门: `/api/v1/recommend/trending`

### 场景4: 知识图谱查询

1. 搜索实体: `/api/v1/kg/search?query=石家庄`
2. 查询关系: `/api/v1/kg/relations?source=石家庄市体育馆`
3. 路径查找: `/api/v1/kg/path?start=石家庄市体育馆&end=石家庄市`
4. 可视化: `/api/v1/kg/visualization?center_entity=石家庄市体育馆`

---

## 📊 数据展示示例

### 统计数据

```
健身设施总数: 1,258 个
覆盖人口: 2,800 万人
平均参与率: 31.5%
知识图谱实体: 15,432 个
知识图谱关系: 28,765 条
```

### 评价结果

```
石家庄市综合评价:
- 总分: 82.5分
- 等级: 良好
- 均衡性: 78.5分 (排名第2)
- 可及性: 85.0分 (排名第1)
- 服务质量: 80.0分
- 参与度: 86.5分
```

### 推荐结果

```
为您推荐的健身活动:
1. 跑步 (推荐度: 92%) - 根据您的运动偏好
2. 游泳 (推荐度: 88%) - 与您喜欢的活动相似
3. 瑜伽 (推荐度: 85%) - 许多相似用户都喜欢
```

---

## 🎯 演示要点

### 技术亮点演示

1. **知识图谱**: 展示七维度知识表示和复杂查询能力
2. **评价模型**: 展示多算法融合的科学评价体系
3. **动作捕捉**: 展示实时姿态检测和智能反馈
4. **推荐系统**: 展示个性化推荐和可解释性

### 业务价值演示

1. **决策支持**: 为政府提供数据驱动的决策依据
2. **资源优化**: 帮助优化健身设施布局
3. **服务提升**: 提高全民健身公共服务水平
4. **用户体验**: 为居民提供智能化健身服务

---

## 🔧 故障排除

### 问题1: API返回404

**原因**: 后端服务未启动  
**解决**: `cd backend && python main.py`

### 问题2: 前端页面空白

**原因**: 前端服务未启动  
**解决**: `cd frontend && npm run dev`

### 问题3: CORS错误

**原因**: 跨域配置问题  
**解决**: 检查backend/app/core/config.py中的CORS配置

### 问题4: 数据文件不存在

**原因**: 未初始化数据  
**解决**: `python3 scripts/quick_init.py`

---

## 📝 演示检查清单

- [ ] 数据已初始化
- [ ] 后端服务已启动
- [ ] 前端服务已启动
- [ ] API文档可访问
- [ ] 所有API端点可正常调用
- [ ] 前端页面可正常访问
- [ ] 演示数据准备完毕
- [ ] 演示脚本准备完毕

---

**演示准备时间**: 10分钟  
**演示时长**: 15-20分钟  
**建议演示顺序**: 首页 → 数据查询 → 知识图谱 → 评价模型 → 推荐系统
