"""
和风天气工具 - Agent 的第一个工具
用于获取目的地的天气预报
"""
import httpx
import json
from typing import Optional
from config import settings

# 配置专属域名（添加 https 协议头 + 固定 v7 版本前缀）
BASE_HOST = "https://mt4y3kay4h.re.qweatherapi.com/v7"

async def get_city_id(city_name: str) -> Optional[str]:
    """
    根据城市名获取和风天气的 Location ID
    
    Args:
        city_name: 城市名，如 "成都"、"北京"
    
    Returns:
        城市ID，如 "101270101"
    """
    # Geo 接口单独用 v2 版本路径
    url = f"https://mt4y3kay4h.re.qweatherapi.com/geo/v2/city/lookup"
    params = {
        "location": city_name,
        "range": "cn",
        "key": settings.QWEATHER_API_KEY,
        "number": 1  # 只返回最匹配的一个
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()  # 抛出 HTTP 错误状态码异常
        except httpx.HTTPError as e:
            print(f"城市查询请求异常: {str(e)}")
            return None
        
        print(f"请求 URL: {response.url}")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")  # 只打印前500字符
        
        # 检查响应是否为空
        if not response.text.strip():
            print("⚠️ 响应为空！")
            return None
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"⚠️ JSON解析失败，响应内容: {response.text}")
            return None
        
        if data.get("code") == "200" and data.get("location"):
            return data["location"][0]["id"]
        
        print(f"未找到城市: {city_name}, 返回: {data}")
        return None 


async def get_weather(city_name: str, days: int = 3) -> dict:
    """
    获取城市未来几天的天气预报
    支持 3天/7天 预报，对应接口 /weather/3d /weather/7d
    
    Args:
        city_name: 城市名，如 "成都"
        days: 预报天数，3 或 7
    
    Returns:
        天气信息字典
    """
    # 校验天数参数
    if days not in [3,7]:
        return {"error": "days参数仅支持 3 或 7"}
    
    # 第一步：获取城市 ID
    city_id = await get_city_id(city_name)
    if not city_id:
        return {"error": f"未找到城市: {city_name}"}
    
    # 第二步：获取天气预报 - 修正 v7 版本接口路径
    url = f"{BASE_HOST}/weather/{days}d"
    params = {
        "location": city_id,
        "key": settings.QWEATHER_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPError as e:
            return {"error": f"天气请求异常: {str(e)}"}
        
        # 检查响应内容
        if not response.text.strip():
            return {"error": "天气接口返回内容为空"}
        
        # 防 JSON 解析报错
        try:
            data = response.json()
        except json.JSONDecodeError:
            return {"error": f"JSON解析失败，响应: {response.text[:100]}"}
        
        if data.get("code") == "200":
            return {
                "city": city_name,
                "update_time": data.get("updateTime"),
                "daily": data.get("daily", [])
            }
        
        return {"error": f"获取天气失败: {data.get('code')}, 信息: {data.get('msg','无')}"}


def format_weather_for_prompt(weather_data: dict) -> str:
    """
    把天气数据格式化成适合放进 Prompt 的文本
    
    Args:
        weather_data: get_weather 返回的数据
    
    Returns:
        格式化后的天气描述
    """
    if "error" in weather_data:
        return weather_data["error"]
    
    city = weather_data.get("city", "未知城市")
    daily = weather_data.get("daily", [])
    
    if not daily:
        return f"{city}：暂无天气数据"
    
    lines = [f"📍 {city} 未来天气预报："]
    
    for day in daily[:3]:  # 最多显示3天
        date = day.get("fxDate", "")
        text_day = day.get("textDay", "")
        temp_min = day.get("tempMin", "")
        temp_max = day.get("tempMax", "")
        
        lines.append(f"  • {date}：{text_day}，{temp_min}~{temp_max}°C")
    
    return "\n".join(lines)


# ========== 测试代码 ==========
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("正在测试天气工具...\n")
        
        # 测试获取成都天气
        weather = await get_weather("成都")
        print("原始数据：")
        print(weather)
        print()
        
        # 测试格式化输出
        formatted = format_weather_for_prompt(weather)
        print("格式化后（可以直接放进 Prompt）：")
        print(formatted)
    
    asyncio.run(test())
