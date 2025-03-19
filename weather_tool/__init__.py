from .core import get_now_weather as w_tool
from .core import get_n_weather as w_n_tool
from .core import schema
from .core import extract_pattern


def get_weather(city_name: str):
    if isinstance(city_name, dict):
        if 'action_input' in city_name:
            input = city_name['action_input']
            city_name = input.get('city_name')
    try:
        return w_tool(city_name)
    except ValueError:
        city_name = extract_pattern(city_name,
            r'city_?[nN]?ame=?["\']?([\u4e00-\u9fa5\w\s]+)["\']?', group_index=1)
        return w_tool(city_name)


def get_n_weather(city_name: str, n: int=1):
    if isinstance(city_name, dict):
        if 'action_input' in city_name:
            input = city_name['action_input']
            city_name = input.get('city_name')
            n = int(input.get('n'))
    try:
        return w_n_tool(city_name, n=n)
    except ValueError:
        city_name = extract_pattern(city_name,
            r'city_?[nN]?ame=?["\']?([\u4e00-\u9fa5\w\s]+)["\']?', group_index=1)
        return w_n_tool(city_name, n=n)


if __name__ == '__main__':
    re.sub(r'city_?[nN]?ame\s*=?\s*"?([\u4e00-\u9fa5\w\s]+)"?', '', 'city_name = 北京')
    get_weather('city_name = 北京')
