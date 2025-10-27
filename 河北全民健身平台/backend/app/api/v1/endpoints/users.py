"""
用户管理API端点
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from loguru import logger

router = APIRouter()


class User(BaseModel):
    """用户模型"""
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None
    role: str = "user"


@router.get("/me")
async def get_current_user():
    """获取当前用户信息"""
    try:
        user = {
            "id": 1,
            "username": "admin",
            "email": "admin@hebei-fitness.com",
            "full_name": "管理员",
            "role": "admin"
        }
        return user
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}")
async def get_user(user_id: int):
    """获取用户信息"""
    try:
        user = {
            "id": user_id,
            "username": f"user{user_id}",
            "email": f"user{user_id}@example.com",
            "full_name": f"用户{user_id}",
            "role": "user"
        }
        return user
    except Exception as e:
        logger.error(f"获取用户失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
