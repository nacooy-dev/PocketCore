"""
工具管理模块
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
import json
from config import Config

class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行工具功能"""
        pass

class LLMClient:
    """多LLM客户端管理器"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.default_provider = self.config["default_provider"]
        
    def call_llm(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用LLM"""
        provider = self.default_provider
        
        if provider == "ollama":
            return self._call_ollama(messages, model)
        elif provider == "openai" and Config.OPENAI_API_KEY:
            return self._call_openai(messages, model)
        elif provider == "anthropic" and Config.ANTHROPIC_API_KEY:
            return self._call_anthropic(messages, model)
        elif provider == "zhipu" and Config.ZHIPU_API_KEY:
            return self._call_zhipu(messages, model)
        elif provider == "openrouter" and Config.OPENROUTER_API_KEY:
            return self._call_openrouter(messages, model)
        else:
            # 默认使用Ollama
            return self._call_ollama(messages, model)
    
    def _call_ollama(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用Ollama"""
        try:
            model = model or self.config["ollama_model"]
            url = f"{self.config['ollama_base_url']}/api/chat"
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            response = httpx.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"Ollama调用出错: {str(e)}"
    
    def _call_openai(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用OpenAI"""
        try:
            import openai
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            model = model or self.config["default_model"]
            
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content or "无响应内容"
        except Exception as e:
            return f"OpenAI调用出错: {str(e)}"
    
    def _call_anthropic(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用Anthropic"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            model = model or self.config["default_model"]
            
            # 转换消息格式
            system_message = ""
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    anthropic_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = client.messages.create(
                model=model,
                messages=anthropic_messages,
                system=system_message,
                max_tokens=1024
            )
            return response.content[0].text
        except Exception as e:
            return f"Anthropic调用出错: {str(e)}"
    
    def _call_zhipu(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用智谱"""
        try:
            model = model or self.config["zhipu_model"]
            url = f"{self.config['zhipu_base_url']}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {Config.ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            response = httpx.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"智谱调用出错: {str(e)}"
    
    def _call_openrouter(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """调用OpenRouter"""
        try:
            model = model or self.config["openrouter_model"]
            url = f"{self.config['openrouter_base_url']}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            response = httpx.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"OpenRouter调用出错: {str(e)}"
    
    def discover_models(self) -> Dict[str, List[str]]:
        """自动发现可用模型"""
        models = {}
        
        # Ollama模型发现
        try:
            response = httpx.get(f"{self.config['ollama_base_url']}/api/tags", timeout=30)
            if response.status_code == 200:
                tags = response.json()
                models["ollama"] = [tag["name"] for tag in tags.get("models", [])]
        except Exception:
            models["ollama"] = ["llama3.1"]  # 默认模型
        
        # OpenAI模型发现（静态列表）
        if Config.OPENAI_API_KEY:
            models["openai"] = [
                "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"
            ]
        
        # Anthropic模型发现（静态列表）
        if Config.ANTHROPIC_API_KEY:
            models["anthropic"] = [
                "claude-3-5-sonnet-20240620", "claude-3-opus-20240229", 
                "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
            ]
        
        # 智谱模型发现（静态列表）
        if Config.ZHIPU_API_KEY:
            models["zhipu"] = [
                "glm-4", "glm-4v", "glm-3-turbo"
            ]
        
        # OpenRouter模型发现（静态列表）
        if Config.OPENROUTER_API_KEY:
            models["openrouter"] = [
                "meta-llama/llama-3.1-8b-instruct",
                "meta-llama/llama-3.1-70b-instruct",
                "anthropic/claude-3.5-sonnet",
                "google/gemini-pro-1.5"
            ]
        
        return models

class GeneralChatTool(BaseTool):
    """通用聊天工具"""
    
    def __init__(self):
        super().__init__("general_chat", "通用聊天工具")
        self.llm_client = LLMClient()
    
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行通用聊天"""
        try:
            messages = [
                {"role": "system", "content": "你是一个有用的助手"},
                {"role": "user", "content": query}
            ]
            
            result = self.llm_client.call_llm(messages)
            return result
        except Exception as e:
            return f"执行出错: {str(e)}"

class WebSearchTool(BaseTool):
    """网络搜索工具"""
    
    def __init__(self):
        super().__init__("web_search", "网络搜索工具")
        self.llm_client = LLMClient()
    
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行网络搜索"""
        # 这里应该集成实际的搜索API
        # 为了演示，我们使用LLM生成模拟结果
        try:
            messages = [
                {"role": "system", "content": "你是一个模拟搜索引擎，根据用户查询生成相关的搜索结果。请以以下格式返回：搜索结果: 关于'[查询]'的搜索结果...\n1. 相关链接1\n2. 相关链接2\n3. 相关链接3"},
                {"role": "user", "content": f"搜索: {query}"}
            ]
            
            result = self.llm_client.call_llm(messages)
            return result
        except Exception as e:
            return f"搜索出错: {str(e)}"

class CalculatorTool(BaseTool):
    """计算器工具"""
    
    def __init__(self):
        super().__init__("calculator", "计算器工具")
    
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行计算"""
        try:
            # 简单的安全计算表达式
            import re
            # 只允许数字、运算符和空格
            safe_query = re.sub(r'[^0-9+\-*/(). ]', '', query)
            result = eval(safe_query)
            return f"计算结果: {query} = {result}"
        except Exception as e:
            return f"计算出错: {str(e)}"

class TranslatorTool(BaseTool):
    """翻译工具"""
    
    def __init__(self):
        super().__init__("translator", "翻译工具")
        self.llm_client = LLMClient()
    
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行翻译"""
        try:
            messages = [
                {"role": "system", "content": "你是一个翻译助手，请将用户输入翻译成中文"},
                {"role": "user", "content": query}
            ]
            
            result = self.llm_client.call_llm(messages)
            return f"翻译结果: {result}"
        except Exception as e:
            return f"翻译出错: {str(e)}"

class ModelDiscoveryTool(BaseTool):
    """模型发现工具"""
    
    def __init__(self):
        super().__init__("model_discovery", "发现可用的LLM模型")
        self.llm_client = LLMClient()
    
    def execute(self, query: str, context: Dict[Any, Any]) -> str:
        """执行模型发现"""
        try:
            models = self.llm_client.discover_models()
            result = "可用的LLM模型:\n"
            for provider, model_list in models.items():
                result += f"\n{provider.upper()}:\n"
                for model in model_list:
                    result += f"  - {model}\n"
            return result
        except Exception as e:
            return f"模型发现出错: {str(e)}"

class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        self.register_tool(GeneralChatTool())
        self.register_tool(WebSearchTool())
        self.register_tool(CalculatorTool())
        self.register_tool(TranslatorTool())
        self.register_tool(ModelDiscoveryTool())
    
    def register_tool(self, tool: BaseTool):
        """注册工具"""
        self.tools[tool.name] = tool
    
    def unregister_tool(self, tool_name: str):
        """注销工具"""
        if tool_name in self.tools:
            del self.tools[tool_name]
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """列出所有工具"""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]