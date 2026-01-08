import json
from pathlib import Path
from typing import Optional, Dict, Any, List


# route_kb.json 的路径（相对 Starji1 根目录）
KB_PATH = Path(__file__).resolve().parents[3] / "data" / "route_kb.json"


def _normalize_city(s: str) -> str:
    """简单归一化：去空格、统一箭头等"""
    if not s:
        return ""
    s = s.strip().replace(" ", "")
    s = s.replace("到", "->").replace("-", "->").replace("—", "->").replace("→", "->")
    return s


def _make_key(origin: str, destination: str) -> str:
    return f"{_normalize_city(origin)}->{_normalize_city(destination)}"


def load_route_kb() -> List[Dict[str, Any]]:
    """加载知识库（不存在/空文件都返回空列表）"""
    if not KB_PATH.exists():
        return []
    try:
        text = KB_PATH.read_text(encoding="utf-8").strip()
        if not text:
            return []
        data = json.loads(text)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def find_route_record(origin: str, destination: str) -> Optional[Dict[str, Any]]:
    """按 origin+destination 查找匹配记录"""
    key = _make_key(origin, destination)
    kb = load_route_kb()

    for item in kb:
        o = item.get("origin", "")
        d = item.get("destination", "")
        if _make_key(o, d) == key:
            return item

    # 允许用户只写 tripline 的情况（兼容）
    for item in kb:
        tripline = item.get("tripline", "")
        if _normalize_city(tripline) == key:
            return item

    return None


def format_route_record_for_prompt(record: Dict[str, Any]) -> str:
    """把记录格式化成适合塞进 Prompt 的文本块"""
    origin = record.get("origin", "")
    destination = record.get("destination", "")
    tripline = record.get("tripline") or f"{origin}->{destination}"

    ticket = record.get("ticket", {})
    tips = record.get("tips", [])

    lines = [f"📌 路线知识库命中：{tripline}"]

    # 票价块
    lines.append("【交通票价参考（区间/经验值，仅供参考，以购票平台为准）】")
    train = (ticket.get("train") or {})
    if train:
        for k, v in train.items():
            lines.append(f"- 火车/高铁 {k}：{v}")
    flight = ticket.get("flight")
    if flight:
        lines.append(f"- 飞机：{flight}")
    notes = ticket.get("notes")
    if notes:
        lines.append(f"- 备注：{notes}")

    # 攻略块
    if tips:
        lines.append("【目的地攻略参考（知识库摘要）】")
        for t in tips[:12]:
            lines.append(f"- {t}")

    return "\n".join(lines)
