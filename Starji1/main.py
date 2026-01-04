from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.cities import router as cities_router
# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# 配置跨域（允许前端调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源，生产环境要改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径：项目信息
@app.get("/", tags=["系统"])
def read_root():
    """欢迎信息"""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs": "/docs",
        "status": "running"
    }

# 健康检查
@app.get("/health", tags=["系统"])
def health_check():
    """健康检查接口，用于监控服务状态"""
    return {"status": "healthy"}

# 后续会在这里注册更多路由
app.include_router(cities_router, prefix="/api", tags=["城市"])
