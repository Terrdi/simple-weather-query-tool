# 轻量级的天气信息查询工具
只需要安装就可以使用
数据来源于[中国气象网](https://weather.cma.cn/web/weather/54511.html)

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
from langchain.agents import initialize_agent
from langchain.tools import Tool
from weather_tool import weather_tool

# 定义获取天气的工具
weather_agent_tool = Tool(
    name="GetWeather",
    func=weather_tool,
    description="获取指定城市的天气信息，参数是城市名称, 返回值中_schema包含字段描述"
)


# 初始化 LLM
llm = OllamaLLM(model="llama3")


# 定义 agent
agent = initialize_agent(
    tools=[weather_tool],  # 使用自定义工具
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True,
    agent_kwargs={"handle_parsing_errors": True}
)


# 用户问题
user_question = "北京的天气怎么样？"
print(f"用户问题：{user_question}")


# 执行并打印结果
response = agent.run(user_question)
print(response)
```
