from weather_tool import weather_tool as w_tool


def get_weather(city_name: str):
    return w_tool(city_name)
