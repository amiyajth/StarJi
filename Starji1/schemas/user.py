from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="用户密码")


class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 新增：Token 相关 ==========

class Token(BaseModel):
    """登录成功后返回的 Token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 中解码出的数据"""
    username: Optional[str] = None
