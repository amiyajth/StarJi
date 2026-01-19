from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base


class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # event_type: trip_create / trip_generate / vision_identify
    event_type = Column(String(50), nullable=False, index=True)

    # 关联资源（可选）
    trip_id = Column(Integer, nullable=True, index=True)

    # 事件细节（自由扩展）
    payload = Column(JSON, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
