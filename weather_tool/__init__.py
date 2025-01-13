from .core import get_weather as w_tool


def get_weather(city_name: str):
    return w_tool(city_name)
