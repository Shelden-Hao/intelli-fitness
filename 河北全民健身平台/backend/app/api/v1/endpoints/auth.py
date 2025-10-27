"""
认证API端点
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

router = APIRouter()


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """用户登录"""
    try:
        # 简化的登录逻辑
        if request.username == "admin" and request.password == "admin":
            return {
                "access_token": "fake-jwt-token",
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout():
    """用户登出"""
    return {"message": "登出成功"}
