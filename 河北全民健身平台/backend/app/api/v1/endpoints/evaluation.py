"""
评价模型API端点
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from loguru import logger

router = APIRouter()


class EvaluationRequest(BaseModel):
    """评价请求模型"""
    cities: List[str]
    indicators: List[str]


@router.get("/balance")
async def get_balance_evaluation(city: Optional[str] = None):
    """获取均衡性评价"""
    try:
        evaluation = {
            "gini_coefficient": {
                "total_area": 0.285,
                "per_capita_area": 0.312,
                "interpretation": "相对均衡"
            },
            "concentration_index": {
                "value": 0.245,
                "interpretation": "设施分布与人口分布较为匹配"
            },
            "location_quotients": [
                {
                    "city": "石家庄市",
                    "location_quotient": 1.15,
                    "interpretation": "设施相对集中,高于平均水平"
                },
                {
                    "city": "保定市",
                    "location_quotient": 0.92,
                    "interpretation": "设施分布适中,接近平均水平"
                },
                {
                    "city": "唐山市",
                    "location_quotient": 1.08,
                    "interpretation": "设施分布适中,接近平均水平"
                }
            ],
            "per_capita_areas": [
                {"city": "石家庄市", "area": 0.045},
                {"city": "保定市", "area": 0.040},
                {"city": "唐山市", "area": 0.055}
            ]
        }
        
        if city:
            # 过滤特定城市
            evaluation["location_quotients"] = [
                lq for lq in evaluation["location_quotients"] if lq["city"] == city
            ]
        
        return evaluation
    except Exception as e:
        logger.error(f"均衡性评价失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accessibility")
async def get_accessibility_evaluation(city: Optional[str] = None):
    """获取可及性评价"""
    try:
        evaluation = {
            "geographic_accessibility": 0.78,
            "temporal_accessibility": 0.65,
            "facility_density_per_10k": 1.85,
            "comprehensive_score": 0.725,
            "interpretation": "良好",
            "coverage_details": {
                "15min_fitness_circle": {
                    "coverage_rate": 0.78,
                    "interpretation": "良好 - 覆盖率较高"
                },
                "service_radius_km": 1.25,
                "total_points": 100,
                "covered_points": 78
            },
            "time_accessibility": {
                "average_daily_hours": 14.5,
                "average_accessibility_score": 0.65,
                "interpretation": "良好 - 开放时间较好"
            }
        }
        
        return evaluation
    except Exception as e:
        logger.error(f"可及性评价失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ahp")
async def get_ahp_evaluation():
    """获取AHP综合评价"""
    try:
        evaluation = {
            "criteria_weights": [0.35, 0.30, 0.20, 0.15],
            "criteria_names": ["均衡性", "可及性", "服务质量", "参与度"],
            "city_names": ["石家庄市", "保定市", "唐山市"],
            "comprehensive_weights": [0.358, 0.312, 0.330],
            "ranking": [
                {
                    "rank": 1,
                    "city": "石家庄市",
                    "score": 0.358,
                    "percentage": "35.80%"
                },
                {
                    "rank": 2,
                    "city": "唐山市",
                    "score": 0.330,
                    "percentage": "33.00%"
                },
                {
                    "rank": 3,
                    "city": "保定市",
                    "score": 0.312,
                    "percentage": "31.20%"
                }
            ],
            "criteria_consistency": {
                "CR": 0.045,
                "is_consistent": True,
                "interpretation": "通过一致性检验"
            }
        }
        
        return evaluation
    except Exception as e:
        logger.error(f"AHP评价失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comprehensive")
async def get_comprehensive_evaluation(city: str):
    """获取综合评价"""
    try:
        evaluation = {
            "city": city,
            "overall_score": 82.5,
            "grade": "良好",
            "dimensions": {
                "balance": {
                    "score": 78.5,
                    "rank": 2,
                    "interpretation": "设施分布相对均衡"
                },
                "accessibility": {
                    "score": 85.0,
                    "rank": 1,
                    "interpretation": "可及性良好"
                },
                "service_quality": {
                    "score": 80.0,
                    "rank": 2,
                    "interpretation": "服务质量较好"
                },
                "participation": {
                    "score": 86.5,
                    "rank": 1,
                    "interpretation": "参与度高"
                }
            },
            "strengths": [
                "15分钟健身圈覆盖率高",
                "居民参与度较高",
                "设施开放时间充足"
            ],
            "weaknesses": [
                "设施分布存在一定不均衡",
                "部分区域设施密度偏低",
                "运动项目多样性有待提升"
            ],
            "recommendations": [
                "加强偏远地区设施建设",
                "优化设施布局,提高均衡性",
                "丰富运动项目种类",
                "延长部分设施开放时间"
            ]
        }
        
        return evaluation
    except Exception as e:
        logger.error(f"综合评价失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calculate")
async def calculate_evaluation(request: EvaluationRequest):
    """计算自定义评价"""
    try:
        # 模拟计算过程
        results = {
            "cities": request.cities,
            "indicators": request.indicators,
            "scores": [
                {"city": city, "score": 75 + i * 5}
                for i, city in enumerate(request.cities)
            ],
            "timestamp": "2024-01-01T00:00:00"
        }
        
        return results
    except Exception as e:
        logger.error(f"评价计算失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_evaluation_trends(city: str, years: int = 5):
    """获取评价趋势"""
    try:
        trends = {
            "city": city,
            "years": list(range(2020, 2020 + years)),
            "balance_scores": [72, 75, 78, 80, 82],
            "accessibility_scores": [70, 73, 77, 82, 85],
            "service_quality_scores": [68, 72, 75, 78, 80],
            "participation_scores": [75, 78, 82, 85, 87]
        }
        
        return trends
    except Exception as e:
        logger.error(f"获取趋势失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
