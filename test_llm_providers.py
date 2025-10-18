"""
测试多LLM提供商集成
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tools import LLMClient

def test_all_providers():
    """测试所有LLM提供商"""
    print("测试多LLM提供商集成...")
    
    # 初始化LLM客户端
    client = LLMClient()
    
    # 测试消息
    messages = [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好，这是多LLM提供商集成测试"}
    ]
    
    # 发现模型
    print("发现可用模型...")
    models = client.discover_models()
    for provider, model_list in models.items():
        print(f"{provider.upper()}: {', '.join(model_list)}")
    
    print("-" * 50)
    
    # 测试Ollama
    print("测试Ollama...")
    original_provider = client.default_provider
    client.default_provider = "ollama"
    result = client.call_llm(messages)
    print(f"Ollama响应: {result}")
    client.default_provider = original_provider
    
    print("多LLM提供商集成测试完成")

if __name__ == "__main__":
    test_all_providers()