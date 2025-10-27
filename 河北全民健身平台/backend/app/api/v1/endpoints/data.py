"""
数据管理API端点
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Optional
from pydantic import BaseModel
import json
from loguru import logger

router = APIRouter()


class FacilityData(BaseModel):
    """健身设施数据模型"""
    id: Optional[int] = None
    name: str
    type: str
    city: str
    district: str
    address: str
    area: float
    capacity: int
    latitude: float
    longitude: float
    build_year: int
    investment: float
    annual_visitors: int
    open_hours: str


class PopulationData(BaseModel):
    """人口数据模型"""
    city: str
    total_population: int
    urban_population: int
    rural_population: int
    age_0_14: int
    age_15_64: int
    age_65_plus: int
    year: int


@router.get("/facilities", response_model=List[Dict])
async def get_facilities(city: Optional[str] = None, type: Optional[str] = None):
    """获取健身设施数据"""
    try:
        import os
        # 读取真实数据
        data_file = "data/raw/facilities.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                facilities = json.load(f)
        else:
            facilities = []
        
        # 过滤
        if city:
            facilities = [f for f in facilities if f["city"] == city]
        if type:
            facilities = [f for f in facilities if f["type"] == type]
        
        return facilities
    except Exception as e:
        logger.error(f"获取设施数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/population", response_model=List[Dict])
async def get_population(city: Optional[str] = None):
    """获取人口数据"""
    try:
        import os
        data_file = "data/raw/population.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                population_data = json.load(f)
        else:
            population_data = []
        
        if city:
            population_data = [p for p in population_data if p["city"] == city]
        
        return population_data
    except Exception as e:
        logger.error(f"获取人口数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/participation", response_model=List[Dict])
async def get_participation():
    """获取健身参与数据"""
    try:
        import os
        data_file = "data/raw/participation.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                participation_data = json.load(f)
        else:
            participation_data = []
        
        return participation_data
    except Exception as e:
        logger.error(f"获取参与数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics():
    """获取统计概览"""
    try:
        import os
        data_file = "data/processed/data_report.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_facilities": 0,
                "total_population": 0,
                "coverage_rate": 0,
                "kg_entities": 0,
                "cities_count": 0,
                "avg_participation_rate": 0
            }
        return stats
    except Exception as e:
        logger.error(f"获取统计数据失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """上传数据文件"""
    try:
        contents = await file.read()
        
        # 解析文件
        if file.filename.endswith('.json'):
            data = json.loads(contents)
        elif file.filename.endswith('.csv'):
            # 处理CSV文件
            pass
        else:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        logger.info(f"上传文件: {file.filename}, 大小: {len(contents)} bytes")
        
        return {
            "filename": file.filename,
            "size": len(contents),
            "status": "success",
            "message": "文件上传成功"
        }
    except Exception as e:
        logger.error(f"文件上传失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
