from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate
from core.security import hash_password


def get_user_by_username(db: Session, username: str):
    """根据用户名查找用户"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """根据邮箱查找用户"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    创建新用户
    - 密码会被加密后存储
    """
    hashed_pwd = hash_password(user.password)
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
