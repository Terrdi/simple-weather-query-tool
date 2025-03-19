# 轻量级的天气信息查询工具
只需要安装就可以使用
数据来源于[中国气象网](https://www.weather.com.cn/)

* 不要注册
* 不要手机号
* *不要花钱!!!不要花钱！！！不要花钱！！！*

## 快速使用案例
#### 1. 快速安装
```bash
pip install git+https://github.com/Terrdi/simple-weather-query-tool.git
```

#### 2. 通过大模型导入
```python
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.tools import StructuredTool
from langchain.schema import SystemMessage
from pydantic import BaseModel, Field
from weather_tool import get_weather, get_n_weather

class WeatherNDaysSchema(BaseModel):
    city_name: str = Field(..., description='The name of the city.')
    n: int = Field(..., description='How many days from today is the time you need to query?')

class WeatherSchema(BaseModel):
    city_name: str = Field(..., description='The name of the city.')

# 定义获取天气的工具
weather_agent_tool = Tool.from_function(
    name="GetWeather",
    func=get_weather,
    description="当你需要查询自己的天气时，调用该函数, 参数是地点名称, 返回值是一个json,里面包含天气信息",
    args_schema=WeatherSchema
)
weather_n_days_tool = StructuredTool.from_function(
    name="GetNWeather",
    func=get_n_weather,
    description="获取指定城市几天后的天气信息，第一个参数是城市名称, 第二个参数是天数",
    args_schema=WeatherNDaysSchema
)


# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:7b", temperature=0)


# 定义 agent
agent = initialize_agent(
    tools=[weather_agent_tool, weather_n_days_tool],  # 使用自定义工具
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"handle_parsing_errors": True}
)


# 用户问题
user_question = "北京的天气怎么样？"
print(f"用户问题：{user_question}")


# 执行并打印结果
response = agent.run(user_question)
print(response)

print(agent.run("北京明天的天气怎么样？"))
```
