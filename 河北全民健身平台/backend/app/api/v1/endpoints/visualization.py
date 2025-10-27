"""
数据可视化API端点
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from loguru import logger

router = APIRouter()


@router.get("/map-data")
async def get_map_data(city: Optional[str] = None):
    """获取地图数据"""
    try:
        map_data = {
            "facilities": [
                {
                    "id": 1,
                    "name": "石家庄市体育馆",
                    "latitude": 38.0428,
                    "longitude": 114.5149,
                    "type": "综合体育馆",
                    "capacity": 8000
                },
                {
                    "id": 2,
                    "name": "保定市全民健身中心",
                    "latitude": 38.8738,
                    "longitude": 115.4645,
                    "type": "健身中心",
                    "capacity": 5000
                }
            ],
            "coverage_areas": [
                {
                    "facility_id": 1,
                    "center": [38.0428, 114.5149],
                    "radius": 1250  # 米
                }
            ]
        }
        
        if city:
            # 过滤特定城市
            pass
        
        return map_data
    except Exception as e:
        logger.error(f"获取地图数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/charts/participation")
async def get_participation_chart():
    """获取参与率图表数据"""
    try:
        chart_data = {
            "cities": ["石家庄", "保定", "唐山", "秦皇岛", "邯郸"],
            "participation_rates": [31.8, 29.8, 31.2, 33.5, 28.9],
            "target_rate": 38.5
        }
        
        return chart_data
    except Exception as e:
        logger.error(f"获取参与率图表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/charts/facility-distribution")
async def get_facility_distribution():
    """获取设施分布图表数据"""
    try:
        chart_data = {
            "types": ["综合体育馆", "健身中心", "体育公园", "社区健身点", "其他"],
            "counts": [85, 320, 156, 580, 117],
            "percentages": [6.8, 25.4, 12.4, 46.1, 9.3]
        }
        
        return chart_data
    except Exception as e:
        logger.error(f"获取设施分布图表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/charts/activity-popularity")
async def get_activity_popularity():
    """获取运动项目热度"""
    try:
        chart_data = {
            "activities": ["跑步", "健走", "广场舞", "羽毛球", "游泳", "篮球", "太极拳", "瑜伽"],
            "participants": [15000, 12000, 10000, 8500, 7000, 6500, 5000, 4500]
        }
        
        return chart_data
    except Exception as e:
        logger.error(f"获取活动热度失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/charts/trends")
async def get_trends_chart(indicator: str = "participation_rate"):
    """获取趋势图表数据"""
    try:
        chart_data = {
            "years": [2019, 2020, 2021, 2022, 2023, 2024],
            "values": [25.5, 27.2, 28.8, 30.1, 31.5, 33.2],
            "indicator": indicator,
            "target": 38.5
        }
        
        return chart_data
    except Exception as e:
        logger.error(f"获取趋势图表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heatmap")
async def get_heatmap_data():
    """获取热力图数据"""
    try:
        heatmap_data = {
            "points": [
                {"lat": 38.0428, "lng": 114.5149, "intensity": 0.9},
                {"lat": 38.8738, "lng": 115.4645, "intensity": 0.7},
                {"lat": 39.6304, "lng": 118.1803, "intensity": 0.8}
            ]
        }
        
        return heatmap_data
    except Exception as e:
        logger.error(f"获取热力图数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
