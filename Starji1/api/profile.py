from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from core.deps import get_current_user
from models.user import User
from models.user_event import UserEvent

router = APIRouter()


@router.get("/profile/me", summary="获取我的用户画像（统计型）")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    uid = current_user.id

    # 1) 目的地 Top
    dest_rows = (
        db.query(UserEvent.payload["destination"].as_string(), func.count(UserEvent.id))
        .filter(UserEvent.user_id == uid)
        .filter(UserEvent.event_type.in_(["trip_create", "trip_generate"]))
        .group_by(UserEvent.payload["destination"].as_string())
        .order_by(func.count(UserEvent.id).desc())
        .limit(10)
        .all()
    )

    destinations_top = [{"destination": r[0], "count": int(r[1])} for r in dest_rows if r[0]]

    # 2) 生成模式统计
    mode_rows = (
        db.query(UserEvent.payload["mode"].as_string(), func.count(UserEvent.id))
        .filter(UserEvent.user_id == uid)
        .filter(UserEvent.event_type == "trip_generate")
        .group_by(UserEvent.payload["mode"].as_string())
        .all()
    )
    modes = {r[0] or "unknown": int(r[1]) for r in mode_rows}

    # 3) 最近事件
    recent = (
        db.query(UserEvent)
        .filter(UserEvent.user_id == uid)
        .order_by(UserEvent.created_at.desc())
        .limit(20)
        .all()
    )
    recent_events = [
        {
            "event_type": e.event_type,
            "trip_id": e.trip_id,
            "payload": e.payload,
            "created_at": e.created_at.isoformat()
        }
        for e in recent
    ]

    # 4) 标签偏好：从 vision_identify 的 tags 统计（简单做法）
    tag_counts = {}
    vision_events = (
        db.query(UserEvent)
        .filter(UserEvent.user_id == uid)
        .filter(UserEvent.event_type == "vision_identify")
        .all()
    )
    for ev in vision_events:
        tags = (ev.payload or {}).get("result", {}).get("tags", [])
        for t in tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    tags_top = sorted(
        [{"tag": k, "count": v} for k, v in tag_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:10]

    return {
        "user": {"id": uid, "username": current_user.username},
        "destinations_top": destinations_top,
        "modes": modes,
        "tags_top": tags_top,
        "recent_events": recent_events
    }
