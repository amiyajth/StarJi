from database import engine
from sqlalchemy import text

def test_connection():
    """测试数据库连接"""
    try:
        with engine.connect() as conn:
            # 测试查询
            result = conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功！")
            print(f"测试查询结果: {result.fetchone()}")
            
            # 查看当前数据库
            result = conn.execute(text("SELECT DATABASE()"))
            print(f"当前数据库: {result.fetchone()[0]}")
            
            # 查看数据库版本
            result = conn.execute(text("SELECT VERSION()"))
            print(f"MySQL版本: {result.fetchone()[0]}")
            
    except Exception as e:
        print(f"❌ 数据库连接失败!")
        print(f"错误信息: {e}")

if __name__ == "__main__":
    test_connection()
