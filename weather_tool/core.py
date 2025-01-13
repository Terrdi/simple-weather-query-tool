# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json, re, datetime
from bs4 import BeautifulSoup
from bs4 import element

home_url = "https://weather.cma.cn/web/weather/map.html"
headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie': 'Hm_lvt_c758855eca53e5d78186936566552a13=1736666561; HMACCOUNT=F9A4533CE00020EC; _trs_uv=m5tafo34_6252_68nr; _trs_ua_s_1=m5tafo34_6252_980v; Hm_lpvt_c758855eca53e5d78186936566552a13=1736666574',
    'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

schema = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "description": "7日内分时段的天气预报, 第一个元素是最新的天气报告",
            "items": {
                "time": {
                    "type": "string",
                    "description": "时间"
                },
                "timeAlias": {
                    "type": "array",
                    "prefixItems": [
                        {
                            "type": "string"
                        }
                    ],
                    "description": "时间别名",
                    "unevaluatedItems": True
                },
                "humidity": {
                    "type": "number",
                    "description": "湿度",
                    "minimum": 0,
                    "maximum": 100
                },
                "precipitation": {
                    "type": "string",
                    "description": "降水"
                },
                "pressure": {
                    "type": "number",
                    "description": "气压, 单位: hPa"
                },
                "temperature": {
                    "type": "number",
                    "description": "温度, 单位: 摄氏度(℃)"
                },
                "windDirection": {
                    "type": "string",
                    "description": "风向"
                },
                "windDirectionDegree": {
                    "type": "number",
                    "description": "风向角度, 单位: 度"
                },
                "windScale": {
                    "type": "string",
                    "description": "风力等级"
                },
                "windSpeed": {
                    "type": "number",
                    "description": "风速, 单位: 米每秒(m/s)"
                }
            }
        },
        "summarys": {
            "type": "array",
            "description": "7日内每日的天气情况概览, 第一个元素是今日的天气概览",
            "items": {
                "date": {
                    "type": "string",
                    "description": "日期信息, 格式: 月份/天号"
                },
                "dateAlias": {
                    "type": "array",
                    "description": "日期别名",
                    "prefixItems": [
                        {
                            "type": "string"
                        }
                    ],
                    "unevaluatedItems": True
                },
                "dayDescription": {
                    "type": "string",
                    "description": "日间天气情况描述"
                },
                "nightDescription": {
                    "type": "string",
                    "description": "夜间天气情况描述"
                },
                "dayWindDirection": {
                    "type": "string",
                    "description": "日间风向"
                },
                "nightWindDirection": {
                    "type": "string",
                    "description": "夜间风向"
                },
                "dayWindScale": {
                    "type": "string",
                    "description": "日间风力等级"
                },
                "nightWindScale": {
                    "type": "string",
                    "description": "夜间风力等级"
                },
                "minTemperature": {
                    "type": "number",
                    "description": "最低温度, 单位: 摄氏度(℃)"
                },
                "maxTemperature": {
                    "type": "number",
                    "description": "最高温度, 单位: 摄氏度(℃)"
                }
            }
        },
        "code": {
            "type": "integer",
            "description": "返回码, 0代表成功, -1代表未找到, 其它代表未知错误"
        },
        "msg": {
            "type": "string",
            "description": "错误信息, 请求成功为空字符串"
        }
    },
    "requeired": [
        "code", "items"
    ]
}

summary_pattern = re.compile(r'.*?<div class="day-item">\s*(?P<daydesc>.*?)</div>'
                            r'.*?<div class="day-item">\s*(?P<dayDescription>\S*?)\s*</div>'
                            r'.*?<div class="day-item">\s*(?P<dayWindDirection>\S*?)\s*</div>'
                            r'.*?<div class="day-item">\s*(?P<dayWindScale>\S*?)\s*</div>'
                            r'.*?<div class="high">\s*(?P<maxTemperature>\S*?)\s*</div>'
                            r'.*?<div class="low">\s*(?P<minTemperature>\S*?)\s*</div>'
                            r'.*?<div class="day-item">\s*(?P<nightDescription>\S*?)\s*</div>'
                            r'.*?<div class="day-item">\s*(?P<nightWindDirection>\S*?)\s*</div>'
                            r'.*?<div class="day-item">\s*(?P<nightWindScale>\S*?)\s*</div>', re.S)


def get_home(url):
    home = requests.get(url, headers=headers)
    home.encoding = 'utf-8'
    return BeautifulSoup(home.text, "html.parser")

def get_cities(home):
    """
    获取所有支持的城市
    """
    for city in home.find_all("div", class_="city"):
        yield next(city.children)


def build_city_url(city_item):
    # base_url = urllib.parse.urlparse(home_url)
    if isinstance(city_item, element.Tag):
        sub_url = city_item['href']
    else:
        sub_url = city_item
    return sub_url if sub_url is None or sub_url.startswith('http') \
        else urllib.parse.urljoin(home_url, sub_url)


def resolve_city_id(city):
    if isinstance(city, element.Tag):
        city = city['href']
    if isinstance(city, str):
        return re.split('\D+', city.rstrip('/').split('/')[-1], 1)[0]
    else:
        return None

def get_now_weather(city_id):
    response = json.loads(requests.get(build_city_url(f"/api/now/{city_id}"),
            headers=headers).text)
    return response.get('data')



def extract_pattern(text:str, pattern, single=True, dictable=False):
    """
    从字符串中根据正则表达式pattern提取出对应子串
    single为True时返回子串, False 返回子串列表迭代器
    dictable为True时返回字典, False 返回字符串
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    if not isinstance(pattern, re.Pattern):
        raise TypeError("不是正则表达式对象")
    ret = re.finditer(pattern, text)
    if dictable:
        return next(ret).groupdict() if single else map(lambda x: x.groupdict(), ret)
    else:
        return next(ret).group(0) if single else map(lambda x: x.group(0), ret)

def extract_number(text:str, single=True):
    return float(extract_pattern(text, re.compile('\-?\d+(?:\.\d+)?')))


def resolve_week_summary(city_detail):
    summary_items = city_detail.find_all('div', class_='day')

    day_alias_list = ['今天', '明天', '后天', '大后天']
    for index, item in enumerate(summary_items):
        item = extract_pattern(item.prettify(), summary_pattern, dictable=True)
        item['date'] = extract_pattern(item['daydesc'], '\d{1,2}\D\d{1,2}')
        day_alias = list(extract_pattern(item['daydesc'], '(?:星期|周)[一二三四五六日]', single=False))
        if index < len(day_alias_list):
            day_alias.append(day_alias_list[index])
        weekday = day_alias[0]
        if weekday.startswith('周'):
            day_alias.append(f"星期{weekday[-1]}")
        else:
            day_alias.append(f"周{weekday[-1]}")
        item['dateAlias'] = day_alias

        item['maxTemperature'] = float(extract_number(item['maxTemperature']))
        item['minTemperature'] = float(extract_number(item['minTemperature']))
        yield item


def resolve_week_detail(city_detail, summarys):
    key_map = {
        '时间': ('time', None),
        '天气': (None, None),
        '气温': ('temperature', extract_number),
        '降水': ('precipitation', None),
        '风速': ('windSpeed', extract_number),
        '风向': ('windDirection', None),
        '气压': ('pressure', extract_number),
        '湿度': ('humidity', extract_number),
        '云量': (None, extract_number)
    }
    ret = []
    for index in range(len(summarys)):
        table_item = city_detail.find_all(id=f'hourTable_{index}')[0]
        # print(table_item)
        tr_items = table_item.find_all('tr')
        last_index = len(ret)

        if index == 0 and datetime.datetime.now().hour >= 23:
            # 23时之后显示的是凌晨的时间
            index=1

        # print(f"开始处理时间 {summarys[index]['date']}")
        for tr_item in tr_items:
            # 获取每一行的数据
            td_items = tr_item.find_all('td')
            title = td_items[0].get_text().strip()
            title = key_map[title]
            if title[0] is None:
                continue
            delta = 0
            for td_index, td_item in enumerate(td_items[1:]):
                td_text = td_item.get_text().strip()
                td_value = title[1](td_text) if title[1] else td_text
                weather_item = {}
                if last_index + td_index >= len(ret):
                    # 判断时间是否是最新的时间
                    # 这里是时间参数
                    if title[0] == 'time':
                        current_hour = extract_pattern(td_value, '\d{1,2}(?=:)')
                        if int(current_hour) < 8:
                            # print(f"开始处理时间 {summarys[index]['date']}, time: {td_value}")
                            delta = 1
                        if index + delta >= len(summarys):
                            continue
                        date = summarys[index + delta]['date']
                        weather_item['timeAlias'] = \
                            [f"{date_alias_item} {td_value}" for date_alias_item in summarys[index + delta]['dateAlias']]

                        td_value = f"{date} {td_value}"
                    weather_item[title[0]] = td_value
                    ret.append(weather_item)
                else:
                    ret[last_index + td_index][title[0]] = td_value
        tr_items = None
        table_item = None

    index = 1
    while index < len(ret):
        last_time = ret[index - 1]['time']
        current_time = ret[index].get('time')
        if current_time is None or last_time >= current_time:
            del ret[index]
        else:
            index+=1
    return ret


def get_weather(city_name: str):
    home = get_home(home_url)
    city_name = extract_pattern(city_name, "[\u4e00-\u9fa5]+")
    try:
        target_city = next(filter(lambda item: item.text==city_name, get_cities(home)))
    except RuntimeError as e:
        print(e.get_msg())
        target_city = None
    if target_city is None:
        return {
            "code": -1,
            "msg": f"不支持的城市: {city_name}",
            "_schema": schema
        }

    # 跳转到当前的城市详情页面
    city_detail = get_home(build_city_url(target_city))
    target_city_id = resolve_city_id(target_city)

    ret = []
    # 首先获取当前最新的天气情况
    now_weather = get_now_weather(target_city_id)
    ret.append({
        "time": now_weather.get('lastUpdate', datetime.datetime.now().\
                    strftime('%Y/%m/%d %H:%M')),
        "timeAlias": ["当前", "现在", "current", "now"],
        "humidity": now_weather.get('now').get('humidity'),
        "precipitation": now_weather.get('now').get('precipitation'),
        "pressure": now_weather.get('now').get('pressure'),
        "temperature": now_weather.get('now').get('temperature'),
        "windDirection": now_weather.get('now').get('windDirection'),
        "windDirectionDegree": now_weather.get('now').get('windDirectionDegree'),
        "windScale": now_weather.get('now').get('windScale'),
        "windSpeed": now_weather.get('now').get('windSpeed')
    })

    # 获取概览信息
    summarys = list(resolve_week_summary(city_detail))

    # 获取详细信息
    ret.extend(resolve_week_detail(city_detail, summarys))

    return {
        "code": 0,
        "msg": "",
        "items": ret,
        "summarys": summarys,
        "_schema": schema
    }


if __name__ == '__main__':
    home = get_home(home_url)

    target_city_name = '北京(Beijing)'
    # target_city = next(filter(lambda item: item.text==target_city_name, get_cities(home)))
    # print(target_city, target_city['href'], resolve_city_id(target_city), build_city_url(target_city))
    # print(get_now_weather(resolve_city_id(target_city)))

    # print(list(extract_pattern('123131jjjj1213i333i1', '\d+', single=False)))
    # resolve_week_summary(get_home(build_city_url(target_city)))
    ret = json.dumps(get_weather(target_city_name), indent=2, \
          ensure_ascii=False)
    from jsonschema import Draft7Validator, exceptions
    print(ret)
    # 使用 Draft7Validator 校验数据
    try:
        # 创建 Draft7Validator 对象
        validator = Draft7Validator(schema)

        # 校验 JSON 数据
        # validator.validate(ret)
        validator.validate(get_weather(target_city_name))
        print("数据符合 JSON Schema！")
    except exceptions.ValidationError as e:
        print(f"校验失败: {e.message}")
