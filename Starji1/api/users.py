from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserResponse, Token
from services import user_service
from core.security import create_access_token
from core.deps import get_current_user
from models.user import User

router = APIRouter()


@router.post("/users/register", response_model=UserResponse, summary="用户注册")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    if user_service.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已被注册")
    
    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    new_user = user_service.create_user(db, user)
    return new_user


@router.post("/users/login", response_model=Token, summary="用户登录")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - 登录成功返回 JWT Token
    - 用这个 Token 访问需要登录的接口
    """
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 token（把用户名编码进去）
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息
    
    - 需要在请求头带上 Token
    - Authorization: Bearer <your_token>
    """
    return current_user
