from pydantic import BaseModel, Field
from typing import Optional

class CityBase(BaseModel):
    """城市基础信息"""
    name: str = Field(..., description="城市名称")
    province: str = Field(..., description="所属省份")
    description: Optional[str] = Field(None, description="城市描述")
    image: Optional[str] = Field(None, description="城市图片URL")
    tags: Optional[str] = Field(None, description="标签")
    rating: Optional[float] = Field(0.0, ge=0, le=5, description="评分(0-5)")
    popularity: Optional[int] = Field(0, ge=0, description="热度")

class CityCreate(CityBase):
    """创建城市时的数据"""
    pass

class CityUpdate(BaseModel):
    """更新城市时的数据（所有字段可选）"""
    name: Optional[str] = None
    province: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    tags: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    popularity: Optional[int] = Field(None, ge=0)

class CityResponse(CityBase):
    """返回给前端的城市数据"""
    id: int
    
    class Config:
        from_attributes = True  # 允许从ORM模型转换
