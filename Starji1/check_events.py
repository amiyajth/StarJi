"""检查用户事件表和数据"""
from database import SessionLocal, engine
from models.user_event import UserEvent
from models.user import User
from sqlalchemy import inspect

db = SessionLocal()

# 1️⃣ 检查表是否存在
inspector = inspect(engine)
tables = inspector.get_table_names()

print("=" * 50)
print("📊 数据库表检查")
print("=" * 50)

if "user_events" in tables:
    print("✅ user_events 表存在")
else:
    print("❌ user_events 表不存在，正在创建...")
    UserEvent.__table__.create(engine, checkfirst=True)
    print("✅ user_events 表已创建")

# 2️⃣ 查看所有事件
print("\n" + "=" * 50)
print("📋 所有用户事件（最近 20 条）")
print("=" * 50)

events = db.query(UserEvent).order_by(UserEvent.created_at.desc()).limit(20).all()

if not events:
    print("⚠️ 暂无任何事件记录！")
    print("   原因可能是：")
    print("   1. routers/trip.py 中的 event_service.log_event() 没被执行")
    print("   2. 你还没有创建/生成过行程")
else:
    for e in events:
        print(f"  [{e.id}] {e.event_type} | user={e.user_id} | trip={e.trip_id}")
        print(f"       payload: {e.payload}")
        print(f"       time: {e.created_at}")
        print()

# 3️⃣ 按类型统计
print("=" * 50)
print("📈 事件类型统计")
print("=" * 50)

from sqlalchemy import func
stats = db.query(UserEvent.event_type, func.count(UserEvent.id)).group_by(UserEvent.event_type).all()

if not stats:
    print("⚠️ 无统计数据")
else:
    for event_type, count in stats:
        print(f"  {event_type}: {count} 次")

# 4️⃣ 查看用户列表
print("\n" + "=" * 50)
print("👥 当前用户")
print("=" * 50)

users = db.query(User).all()
for u in users:
    event_count = db.query(UserEvent).filter(UserEvent.user_id == u.id).count()
    print(f"  [{u.id}] {u.username} - 事件数: {event_count}")

db.close()
print("\n✅ 检查完成！")
