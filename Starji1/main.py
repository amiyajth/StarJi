from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "StarJi 后端启动成功！🌟"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
