from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """项目配置"""
    
    # ========== 项目信息 ==========
    PROJECT_NAME: str = "StarJi API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "智能旅行规划助手后端接口"
    
    # ========== 数据库配置 ==========
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "starji"
    SILICONFLOW_API_KEY: str
    QWEATHER_API_KEY: str
    # ========== JWT 配置（新增）==========
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时过期
    
    @property
    def DATABASE_URL(self) -> str:
        """生成数据库连接URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# 创建全局配置对象
settings = Settings()
