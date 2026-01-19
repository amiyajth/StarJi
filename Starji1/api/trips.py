from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.trip import TripCreate, TripUpdate, TripResponse
from services import trip_service
from core.deps import get_current_user
from models.user import User
from ai.trip_generator import generate_trip_content
from ai.agent.travel_agent import generate_trip_content_agent
from services import event_service

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
    created = trip_service.create_trip(db, trip, current_user.id)

    event_service.log_event(
        db,
        user_id=current_user.id,
        event_type="trip_create",
        trip_id=created.id,
        payload={
            "origin": created.origin,
            "destination": created.destination,
            "start_date": str(created.start_date),
            "end_date": str(created.end_date),
        }
    )

    return created


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


@router.post("/trips/{trip_id}/generate", response_model=TripResponse, summary="AI 生成行程内容")
async def generate_trip(
    trip_id: int,
    mode: str = Query("basic", description="basic=基础版，agent=天气增强版"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI 生成行程内容并写回（只能操作自己的行程）"""
    trip = trip_service.get_trip_by_id(db, trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")

    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权生成此行程内容")

    # ✅ 分支：basic / agent
    if mode == "agent":
        content = await generate_trip_content_agent(trip)
    else:
        content = generate_trip_content(trip)

    updated = trip_service.update_trip_content(db, trip_id, content)
    if not updated:
        raise HTTPException(status_code=404, detail="行程不存在")

    return updated
    event_service.log_event(
        db,
        user_id=current_user.id,
        event_type="trip_generate",
        trip_id=trip_id,
        payload={
            "mode": mode,  # basic/agent
            "origin": trip.origin,
            "destination": trip.destination
        }
    )
