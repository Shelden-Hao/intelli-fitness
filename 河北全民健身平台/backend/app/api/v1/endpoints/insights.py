"""
数据洞察API - 连接数据处理流水线
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List
import json
import os
from datetime import datetime
from loguru import logger
import subprocess

router = APIRouter()


@router.get("/latest")
async def get_latest_insights():
    """获取最新的数据洞察"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights = json.load(f)
            return insights
        else:
            return {
                "insights": {
                    "hot_keywords": [],
                    "key_entities": [],
                    "recommendations": []
                },
                "message": "暂无数据，请先运行数据处理流水线"
            }
    except Exception as e:
        logger.error(f"获取洞察数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hot-keywords")
async def get_hot_keywords():
    """获取热门关键词"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights = json.load(f)
            return {
                "keywords": insights.get("insights", {}).get("hot_keywords", []),
                "last_updated": insights.get("last_updated", "")
            }
        return {"keywords": [], "message": "暂无数据"}
    except Exception as e:
        logger.error(f"获取热门关键词失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_recommendations():
    """获取智能推荐"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights = json.load(f)
            return {
                "recommendations": insights.get("insights", {}).get("recommendations", []),
                "last_updated": insights.get("last_updated", "")
            }
        return {"recommendations": [], "message": "暂无数据"}
    except Exception as e:
        logger.error(f"获取推荐失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest-news")
async def get_latest_news():
    """获取最新新闻分析"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights = json.load(f)
            return {
                "news": insights.get("latest_news", []),
                "last_updated": insights.get("last_updated", "")
            }
        return {"news": [], "message": "暂无数据"}
    except Exception as e:
        logger.error(f"获取新闻失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data-quality")
async def get_data_quality():
    """获取数据质量指标"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights = json.load(f)
            return insights.get("data_quality", {})
        return {
            "completeness": 0,
            "accuracy": 0,
            "timeliness": 0,
            "overall_score": 0
        }
    except Exception as e:
        logger.error(f"获取数据质量失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run-pipeline")
async def run_data_pipeline(background_tasks: BackgroundTasks):
    """触发数据处理流水线（后台任务）"""
    try:
        def run_pipeline_task():
            """后台运行流水线"""
            logger.info("开始执行数据处理流水线...")
            try:
                result = subprocess.run(
                    ["python3", "data_processing/pipeline/data_pipeline.py"],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5分钟超时
                )
                if result.returncode == 0:
                    logger.info("流水线执行成功")
                else:
                    logger.error(f"流水线执行失败: {result.stderr}")
            except Exception as e:
                logger.error(f"流水线执行异常: {e}")
        
        background_tasks.add_task(run_pipeline_task)
        
        return {
            "status": "started",
            "message": "数据处理流水线已在后台启动",
            "estimated_time": "2-5分钟"
        }
    except Exception as e:
        logger.error(f"启动流水线失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pipeline-status")
async def get_pipeline_status():
    """获取流水线执行状态"""
    try:
        insights_file = "data/api/insights.json"
        if os.path.exists(insights_file):
            stat = os.stat(insights_file)
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            
            # 判断数据是否新鲜（1小时内）
            time_diff = (datetime.now() - last_modified).total_seconds()
            is_fresh = time_diff < 3600
            
            return {
                "status": "completed" if is_fresh else "outdated",
                "last_run": last_modified.isoformat(),
                "data_age_minutes": int(time_diff / 60),
                "is_fresh": is_fresh
            }
        else:
            return {
                "status": "never_run",
                "message": "流水线尚未执行"
            }
    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
