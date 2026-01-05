from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from schemas.user import TokenData
from services import user_service

# 告诉 FastAPI：token 从哪个接口获取（登录接口）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    从请求头的 Token 中解析出当前用户
    
    - 如果 token 无效或过期 → 返回 401
    - 如果用户不存在 → 返回 401
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解码 token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
        
    except JWTError:
        raise credentials_exception
    
    # 查数据库确认用户存在
    user = user_service.get_user_by_username(db, username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user
