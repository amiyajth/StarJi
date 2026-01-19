from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from core.deps import get_current_user
from models.user import User
from services import event_service
from ai.vision import identify_image  # 你下面要新建这个

router = APIRouter()


@router.post("/vision/identify", summary="上传图片识别地点/景点（视觉 MVP）")
async def identify(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    content = await image.read()

    # 调用视觉识别（模型/规则都行，接口不变）
    result = await identify_image(content)

    # 记录事件
    event_service.log_event(
        db,
        user_id=current_user.id,
        event_type="vision_identify",
        payload={
            "filename": image.filename,
            "result": result
        }
    )

    return result
