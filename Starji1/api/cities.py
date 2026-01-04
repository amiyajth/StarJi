from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.city import CityResponse, CityCreate
from services import city_service

router = APIRouter()

@router.get("/cities", response_model=List[CityResponse], summary="获取城市列表")
def read_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取城市列表
    
    - **skip**: 跳过前N条记录（分页用）
    - **limit**: 最多返回N条记录
    """
    cities = city_service.get_cities(db, skip=skip, limit=limit)
    return cities

@router.get("/cities/{city_id}", response_model=CityResponse, summary="获取单个城市详情")
def read_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    """
    根据城市ID获取详情
    
    - **city_id**: 城市ID
    """
    city = city_service.get_city_by_id(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    return city

@router.post("/cities", response_model=CityResponse, summary="创建新城市")
def create_city(
    city: CityCreate,
    db: Session = Depends(get_db)
):
    """
    创建新城市
    """
    # 检查城市名是否已存在
    existing = city_service.get_city_by_name(db, name=city.name)
    if existing:
        raise HTTPException(status_code=400, detail="城市名称已存在")
    
    return city_service.create_city(db=db, city=city)
