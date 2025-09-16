import requests
import json
from typing import Optional, Dict, List, Any
import asyncio
import aiohttp

prompt = """请你扮演一位图书文案专家，为指定的书籍创作一段具有诗意的短视频分享文案。
## 核心要求：
### 风格与格式： 
文案风格需严格参考用户提供的《文城》范例。采用分行、断句的诗歌体格式，语言精炼且富有哲理和意境。最终输出只要纯文字，不要任何时间轴、序号或额外标记。
### 内容要点： 
文案必须紧扣书籍的核心主题与思想（例如，对于《巴别塔》，需包含“语言、权力、翻译、背叛、殖民、文化冲突、身份认同”等关键词）。
### 结构： 
整体结构应为：首行点明书籍，中间部分展开核心矛盾与意象，最后部分升华主题。保持短句。

---
《文城》范例：
今天分享的是
文城

过度思考未来
无异于杀死现在的自己

言未出，结局已演千百遍
身未动，心中已过万重山
行未果，假象苦难愁不展
事已毕，过往仍在脑中演

生而悦己，而非困于他人
我与我周旋久，宁作我
---
### 输出格式
输出的文案必须是纯文字，不要包含任何时间轴、序号或额外标记。

请基于以上要求，为下面的书籍生成一段介绍。"""


class LLMClient:
    """大语言模型客户端，支持多种AI服务提供商"""
    
    def __init__(self, api_url: str = "https://api.pearktrue.cn/api/aichat/", api_key: Optional[str] = None):
        """
        初始化LLM客户端
        
        Args:
            api_url: API接口地址
            api_key: API密钥（如果需要）
        """
        self.api_url = api_url
        self.api_key = api_key
        self.session = None
    
    def chat(self, 
             message: str, 
             model: str = "glm-4.5", 
             stream: bool = False,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        同步聊天接口
        
        Args:
            message: 用户消息
            model: 模型名称
            stream: 是否流式输出
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            API响应结果
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": stream
        }
        
        if temperature != 0.7:
            payload["temperature"] = temperature
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"请求失败: {str(e)}"
            }
    
    async def chat_async(self, 
                         message: str, 
                         model: str = "glm-4.5", 
                         stream: bool = False,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        异步聊天接口
        
        Args:
            message: 用户消息
            model: 模型名称
            stream: 是否流式输出
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            API响应结果
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": stream
        }
        
        if temperature != 0.7:
            payload["temperature"] = temperature
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.post(self.api_url, json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            return {
                "error": True,
                "message": f"请求失败: {str(e)}"
            }
    

# 使用示例
if __name__ == "__main__":
    # 创建LLM客户端
    llm = LLMClient()
    
    # 简单聊天
    print("=== 简单聊天测试 ===")
    response = llm.chat("{'title': '巴别塔', 'url': 'https://book.douban.com/subject/36463571/', 'pic': 'https://img1.doubanio.com/view/subject/s/public/s34640760.jpg', 'author_name': '[美]匡灵秀', 'year': '2023', 'type': 'b', 'id': '36463571'}")
    if response.get("error"):
        # print(f"错误: {response['message']}")
        content = ""
    else:
        # print(f"回复: {response.get('content', '无内容')}")
        content = response.get('content', '无内容')
    temp = content.split('\n')
    if "今天分享的是" != temp[0]:
        temp[0] = "今天分享的是"
        content = '\n'.join(temp)
    
    print(content)
    
    