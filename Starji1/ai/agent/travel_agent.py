from ai.client import chat_completion
from models.trip import Trip

from ai.agent.tools.weather import get_weather, format_weather_for_prompt
from ai.agent.tools.route_kb import find_route_record, format_route_record_for_prompt


def build_trip_prompt_agent(trip: Trip, weather_text: str, route_text: str | None = None) -> list:
    system_prompt = (
        "你是专业旅行规划助手。"
        "请用 Markdown 输出，结构清晰、可直接渲染。"
        "必须按天拆分（Day 1, Day 2...），并包含交通/时间建议、购票提示、避坑提示。"
        "不要输出 JSON。"
        "你必须结合【天气信息】给出穿搭/携带物品/行程调整建议。"
    )

    # ✅ 关键：先算好 route_block，再塞进 prompt（不要在 f-string {} 里写复杂拼接）
    route_block = ""
    if route_text:
        route_block = f"""
【路线票价 / 攻略知识库（命中参考）】
{route_text}
"""

    user_prompt = f"""
请为我生成一份旅行行程（Markdown）：

- 出发地：{trip.origin}
- 目的地：{trip.destination}
- 日期：{trip.start_date} 到 {trip.end_date}

【天气信息（工具返回，可信）】
{weather_text}
{route_block}

输出格式要求（必须遵守）：
1) 先给一个《行程总览》（3-6条要点）
2) 再给一个《每日行程》（Day 1...）：
   - 上午 / 下午 / 晚上
   - 推荐景点与理由
   - 预计耗时、交通方式建议
   - 必须结合天气给出当天提醒（如下雨/降温/紫外线等）
   - 若提供了票价/攻略知识库，请合理利用并提示“以实际为准”
3) 《购票与预约建议》：列出可能需要预约/买票的项目
4) 《预算粗估》：按“交通/住宿/餐饮/门票/其它”给区间
5) 《小贴士》：至少5条（需包含天气相关建议）

请使用中文输出。
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]



async def generate_trip_content_agent(trip: Trip) -> str:
    weather_raw = await get_weather(trip.destination, days=3)
    weather_text = format_weather_for_prompt(weather_raw)

    # ✅ 查路线知识库（命中才加）
    record = find_route_record(trip.origin, trip.destination)
    route_text = format_route_record_for_prompt(record) if record else None

    return chat_completion(build_trip_prompt_agent(trip, weather_text, route_text))

