"""
API v1 路由
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    data,
    knowledge_graph,
    evaluation,
    motion_capture,
    recommendation,
    visualization,
    users,
    auth,
    insights
)

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(data.router, prefix="/data", tags=["数据管理"])
api_router.include_router(knowledge_graph.router, prefix="/kg", tags=["知识图谱"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["评价模型"])
api_router.include_router(motion_capture.router, prefix="/motion", tags=["动作捕捉"])
api_router.include_router(recommendation.router, prefix="/recommend", tags=["推荐系统"])
api_router.include_router(visualization.router, prefix="/viz", tags=["数据可视化"])
api_router.include_router(insights.router, prefix="/insights", tags=["数据洞察"])
