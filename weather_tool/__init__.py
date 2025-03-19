from .core import get_now_weather as w_tool
from .core import get_n_weather as w_n_tool
from .core import schema


def get_weather(city_name: str):
    return w_tool(city_name)


def get_n_weather(city_name: str, n: int=1):
    return w_n_tool(city_name, n=n)
