"""给 users 表添加 avatar 字段"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN avatar VARCHAR(500) NULL
        """))
        conn.commit()
        print("✅ avatar 字段添加成功！")
    except Exception as e:
        if "Duplicate column" in str(e):
            print("✅ avatar 字段已存在，无需重复添加")
        else:
            print(f"❌ 错误: {e}")
