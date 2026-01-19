from sqlalchemy.orm import Session
from models.user_event import UserEvent


def log_event(
    db: Session,
    user_id: int,
    event_type: str,
    trip_id: int | None = None,
    payload: dict | None = None
):
    event = UserEvent(
        user_id=user_id,
        event_type=event_type,
        trip_id=trip_id,
        payload=payload or {}
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
