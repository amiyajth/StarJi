from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 创建数据库引擎（连接池）
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 自动检测连接是否断开
    echo=True  # 开发阶段打印SQL语句，方便调试
)

# 创建会话工厂（用来操作数据库）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    """
    每次API请求时创建一个数据库会话
    请求结束后自动关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
