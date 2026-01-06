from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.trip import TripCreate, TripUpdate, TripResponse
from services import trip_service
from core.deps import get_current_user
from models.user import User

router = APIRouter()


@router.get("/trips", response_model=List[TripResponse], summary="获取我的行程列表")
def get_my_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前登录用户的所有行程"""
    return trip_service.get_trips_by_user(db, current_user.id)


@router.get("/trips/{trip_id}", response_model=TripResponse, summary="获取行程详情")
def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定行程的详情（只能查看自己的）"""
    trip = trip_service.get_trip_by_id(db, trip_id)
    
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此行程")
    
    return trip


@router.post("/trips", response_model=TripResponse, summary="创建新行程")
def create_trip(
    trip: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新的行程"""
    return trip_service.create_trip(db, trip, current_user.id)


@router.put("/trips/{trip_id}", response_model=TripResponse, summary="更新行程")
def update_trip(
    trip_id: int,
    trip_update: TripUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新指定行程（只能修改自己的）"""
    trip = trip_service.get_trip_by_id(db, trip_id)
    
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此行程")
    
    updated_trip = trip_service.update_trip(db, trip_id, trip_update)
    return updated_trip


@router.delete("/trips/{trip_id}", summary="删除行程")
def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除指定行程（只能删除自己的）"""
    trip = trip_service.get_trip_by_id(db, trip_id)
    
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此行程")
    
    trip_service.delete_trip(db, trip_id)
    
    return {"message": "行程已删除"}
