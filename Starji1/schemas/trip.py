from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class TripBase(BaseModel):
    title: str = Field(..., description="行程标题")
    origin: str = Field(..., description="出发地")
    destination: str = Field(..., description="目的地")
    start_date: Optional[date] = Field(None, description="出发日期")
    end_date: Optional[date] = Field(None, description="返回日期")
    content: Optional[str] = Field(None, description="行程内容")


class TripCreate(TripBase):
    """创建行程（用户手动创建或 AI 生成后保存）"""
    pass


class TripUpdate(BaseModel):
    """更新行程（所有字段可选）"""
    title: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None


class TripResponse(TripBase):
    """返回给前端的行程数据"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
