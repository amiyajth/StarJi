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
    created_at: datetime

    class Config:
        from_attributes = True
