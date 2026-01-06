from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 行程基本信息
    title = Column(String(100), nullable=False)           # 行程标题
    origin = Column(String(50), nullable=False)           # 出发地
    destination = Column(String(50), nullable=False)      # 目的地
    
    # 日期
    start_date = Column(Date, nullable=True)              # 出发日期
    end_date = Column(Date, nullable=True)                # 返回日期
    
    # AI 生成的行程内容
    content = Column(Text, nullable=True)                 # 详细行程（AI 生成）
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联用户（可选，方便后续查询）
    user = relationship("User", backref="trips")
