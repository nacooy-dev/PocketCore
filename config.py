"""
配置管理模块
"""
import os
from dotenv import load_dotenv
from typing import Optional

# 加载环境变量
load_dotenv()

class Config:
    # LLM配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ZHIPU_API_KEY: str = os.getenv("ZHIPU_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # Ollama配置
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    # 智谱配置
    ZHIPU_BASE_URL: str = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    ZHIPU_MODEL: str = os.getenv("ZHIPU_MODEL", "glm-4")
    
    # OpenRouter配置
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
    
    # 默认LLM提供商 (openai, anthropic, ollama, zhipu, openrouter)
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "ollama")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3.1")
    
    # 服务器配置
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///pocketcore.db")
    
    # 调试配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 工具配置
    TOOLS_DIR: str = os.getenv("TOOLS_DIR", "./tools")
    
    # 内存配置
    MAX_MEMORY_SIZE: int = int(os.getenv("MAX_MEMORY_SIZE", 1000))
    
    @classmethod
    def validate(cls):
        """验证必要配置"""
        # 现在支持多种LLM提供商，不再强制要求API密钥
        pass
            
    @classmethod
    def get_llm_config(cls):
        """获取LLM配置"""
        return {
            "openai_api_key": cls.OPENAI_API_KEY,
            "anthropic_api_key": cls.ANTHROPIC_API_KEY,
            "zhipu_api_key": cls.ZHIPU_API_KEY,
            "openrouter_api_key": cls.OPENROUTER_API_KEY,
            "ollama_base_url": cls.OLLAMA_BASE_URL,
            "ollama_model": cls.OLLAMA_MODEL,
            "zhipu_base_url": cls.ZHIPU_BASE_URL,
            "zhipu_model": cls.ZHIPU_MODEL,
            "openrouter_base_url": cls.OPENROUTER_BASE_URL,
            "openrouter_model": cls.OPENROUTER_MODEL,
            "default_provider": cls.DEFAULT_LLM_PROVIDER,
            "default_model": cls.DEFAULT_MODEL
        }