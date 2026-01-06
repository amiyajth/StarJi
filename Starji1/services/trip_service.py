from sqlalchemy.orm import Session
from typing import List, Optional

from models.trip import Trip
from schemas.trip import TripCreate, TripUpdate


def get_trips_by_user(db: Session, user_id: int) -> List[Trip]:
    """获取用户的所有行程"""
    return db.query(Trip).filter(Trip.user_id == user_id).order_by(Trip.created_at.desc()).all()


def get_trip_by_id(db: Session, trip_id: int) -> Optional[Trip]:
    """根据 ID 获取行程"""
    return db.query(Trip).filter(Trip.id == trip_id).first()


def create_trip(db: Session, trip: TripCreate, user_id: int) -> Trip:
    """创建新行程"""
    db_trip = Trip(
        user_id=user_id,
        title=trip.title,
        origin=trip.origin,
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        content=trip.content
    )
    
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    return db_trip


def update_trip(db: Session, trip_id: int, trip_update: TripUpdate) -> Optional[Trip]:
    """更新行程"""
    db_trip = get_trip_by_id(db, trip_id)
    
    if not db_trip:
        return None
    
    update_data = trip_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_trip, field, value)
    
    db.commit()
    db.refresh(db_trip)
    
    return db_trip


def delete_trip(db: Session, trip_id: int) -> bool:
    """删除行程"""
    db_trip = get_trip_by_id(db, trip_id)
    
    if not db_trip:
        return False
    
    db.delete(db_trip)
    db.commit()
    
    return True
