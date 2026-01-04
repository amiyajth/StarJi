from sqlalchemy.orm import Session
from models.city import City
from schemas.city import CityCreate, CityUpdate
from typing import List, Optional

def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[City]:
    """查询城市列表"""
    return db.query(City).offset(skip).limit(limit).all()

def get_city_by_id(db: Session, city_id: int) -> Optional[City]:
    """根据ID查询城市"""
    return db.query(City).filter(City.id == city_id).first()

def get_city_by_name(db: Session, name: str) -> Optional[City]:
    """根据名称查询城市"""
    return db.query(City).filter(City.name == name).first()

def create_city(db: Session, city: CityCreate) -> City:
    """创建新城市"""
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city
