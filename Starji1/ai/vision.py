from typing import Any, Dict
import base64


async def identify_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    视觉 MVP 输出格式（稳定！后续换模型也保持这个返回）
    """
    # TODO: 如果你有支持视觉的模型，在这里调用它
    # 下面先给一个“占位策略”：你可以先手动返回一个结构，确保前后端联通
    return {
        "top_candidates": [
            {"city": "北京", "landmark": "故宫/古建筑", "confidence": 0.62, "tags": ["历史", "古建筑", "人文"]},
            {"city": "西安", "landmark": "城墙/古迹", "confidence": 0.21, "tags": ["历史", "古迹"]},
            {"city": "南京", "landmark": "博物馆/古建", "confidence": 0.12, "tags": ["人文", "博物馆"]},
        ],
        "suggested_destination": "北京",
        "tags": ["历史", "古建筑", "人文"],
        "message": "这是视觉 MVP 的占位结果：后续接入真实视觉模型后会更准。"
    }
