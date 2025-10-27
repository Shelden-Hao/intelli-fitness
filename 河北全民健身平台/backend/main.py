"""
河北全民健身公共服务体系平台 - 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import uvicorn

from app.core.config import settings
from app.api.v1 import api_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="数智驱动河北全民健身公共服务体系研究平台",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")

# 静态文件服务
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 应用启动中...")
    logger.info(f"📝 项目名称: {settings.PROJECT_NAME}")
    logger.info(f"🌍 环境: {settings.ENVIRONMENT}")
    logger.info(f"🔗 API文档: http://{settings.HOST}:{settings.PORT}/api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("👋 应用关闭中...")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "河北全民健身公共服务体系平台API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
