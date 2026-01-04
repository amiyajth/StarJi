from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """项目配置"""
    
    # 项目信息
    PROJECT_NAME: str = "StarJi API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "智能旅行规划助手后端接口"
    
    # 数据库配置（暂时留空，待会在阶段2配置）
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str  # 待会填你的MySQL密码
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "starji"
    
    @property
    def DATABASE_URL(self) -> str:
        """生成数据库连接URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    class Config:
        case_sensitive = True
        env_file = ".env"  # 可以从.env文件读取配置

# 创建全局配置对象
settings = Settings()
