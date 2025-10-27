"""
推荐系统API端点
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from loguru import logger

router = APIRouter()


class UserProfile(BaseModel):
    """用户画像"""
    age: int
    gender: str
    fitness_level: str  # low, medium, high
    preferences: List[str]
    health_conditions: Optional[List[str]] = []


@router.get("/activities")
async def recommend_activities(
    user_id: int,
    method: str = "collaborative",
    top_n: int = 5
):
    """推荐健身活动"""
    try:
        recommendations = [
            {
                "activity_id": 1,
                "activity_name": "跑步",
                "category": "有氧运动",
                "intensity": "中等",
                "duration": 30,
                "recommendation_score": 0.92,
                "reason": "根据您的运动偏好,推荐跑步"
            },
            {
                "activity_id": 2,
                "activity_name": "游泳",
                "category": "有氧运动",
                "intensity": "中等",
                "duration": 45,
                "recommendation_score": 0.88,
                "reason": "与您喜欢的活动相似,游泳也很适合您"
            },
            {
                "activity_id": 4,
                "activity_name": "瑜伽",
                "category": "柔韧性训练",
                "intensity": "低",
                "duration": 60,
                "recommendation_score": 0.85,
                "reason": "许多和您相似的用户都喜欢瑜伽"
            }
        ]
        
        return recommendations[:top_n]
    except Exception as e:
        logger.error(f"活动推荐失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/facilities")
async def recommend_facilities(
    user_id: int,
    latitude: float,
    longitude: float,
    top_n: int = 5
):
    """推荐健身设施"""
    try:
        recommendations = [
            {
                "facility_id": 1,
                "name": "石家庄市体育馆",
                "type": "综合体育馆",
                "distance_km": 2.5,
                "rating": 4.5,
                "activities": ["篮球", "羽毛球", "游泳"],
                "recommendation_score": 0.95,
                "reason": "距离近,设施完善"
            },
            {
                "facility_id": 3,
                "name": "长安区健身中心",
                "type": "健身中心",
                "distance_km": 1.8,
                "rating": 4.3,
                "activities": ["健身", "瑜伽", "动感单车"],
                "recommendation_score": 0.90,
                "reason": "距离最近,适合日常锻炼"
            }
        ]
        
        return recommendations[:top_n]
    except Exception as e:
        logger.error(f"设施推荐失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personalized")
async def get_personalized_plan(profile: UserProfile):
    """生成个性化健身方案"""
    try:
        plan = {
            "user_profile": profile.dict(),
            "weekly_plan": [
                {
                    "day": "周一",
                    "activities": [
                        {
                            "name": "跑步",
                            "duration": 30,
                            "intensity": "中等",
                            "calories": 250
                        }
                    ]
                },
                {
                    "day": "周三",
                    "activities": [
                        {
                            "name": "游泳",
                            "duration": 45,
                            "intensity": "中等",
                            "calories": 350
                        }
                    ]
                },
                {
                    "day": "周五",
                    "activities": [
                        {
                            "name": "瑜伽",
                            "duration": 60,
                            "intensity": "低",
                            "calories": 180
                        }
                    ]
                }
            ],
            "weekly_target": {
                "total_duration": 135,
                "total_calories": 780,
                "frequency": 3
            },
            "tips": [
                "建议每周锻炼3-5次",
                "注意运动前热身和运动后拉伸",
                "保持充足的水分摄入"
            ]
        }
        
        return plan
    except Exception as e:
        logger.error(f"生成个性化方案失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar-users")
async def get_similar_users(user_id: int, top_n: int = 10):
    """获取相似用户"""
    try:
        similar_users = [
            {
                "user_id": 101,
                "similarity": 0.92,
                "common_activities": ["跑步", "游泳", "瑜伽"],
                "age_group": "25-35"
            },
            {
                "user_id": 102,
                "similarity": 0.88,
                "common_activities": ["跑步", "健身"],
                "age_group": "25-35"
            }
        ]
        
        return similar_users[:top_n]
    except Exception as e:
        logger.error(f"获取相似用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending")
async def get_trending_activities(city: Optional[str] = None, limit: int = 10):
    """获取热门活动"""
    try:
        trending = [
            {
                "activity": "跑步",
                "participants": 15000,
                "growth_rate": 0.25,
                "trend": "上升"
            },
            {
                "activity": "健走",
                "participants": 12000,
                "growth_rate": 0.18,
                "trend": "上升"
            },
            {
                "activity": "广场舞",
                "participants": 10000,
                "growth_rate": 0.12,
                "trend": "稳定"
            }
        ]
        
        return trending[:limit]
    except Exception as e:
        logger.error(f"获取热门活动失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
