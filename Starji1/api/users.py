from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserResponse
from services import user_service

router = APIRouter()


@router.post("/users/register", response_model=UserResponse, summary="用户注册")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名（唯一）
    - **email**: 邮箱（唯一）
    - **password**: 密码（至少6位）
    """
    # 检查用户名是否已存在
    if user_service.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已被注册")
    
    # 检查邮箱是否已存在
    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建用户
    new_user = user_service.create_user(db, user)
    
    return new_user
