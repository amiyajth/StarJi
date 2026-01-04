from sqlalchemy import Column, Integer, String, Text, Float
from database import Base

class City(Base):
    """城市模型"""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="城市ID")
    name = Column(String(50), nullable=False, unique=True, comment="城市名称")
    province = Column(String(50), nullable=False, comment="所属省份")
    description = Column(Text, comment="城市描述")
    image = Column(String(500), comment="城市图片URL")
    tags = Column(String(200), comment="标签，逗号分隔")
    rating = Column(Float, default=0.0, comment="评分")
    popularity = Column(Integer, default=0, comment="热度")
    
    def __repr__(self):
        return f"<City {self.name}>"
