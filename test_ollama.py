"""
测试Ollama集成
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tools import LLMClient

def test_ollama():
    """测试Ollama集成"""
    print("测试Ollama集成...")
    print("请确保Ollama服务正在运行 (默认地址: http://localhost:11434)")
    print("如果没有安装Ollama，请访问 https://ollama.com/ 下载安装")
    print("安装后运行: ollama run llama3.1")
    print("-" * 50)
    
    # 初始化LLM客户端
    client = LLMClient()
    
    # 测试消息
    messages = [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好，这是Ollama集成测试"}
    ]
    
    # 调用Ollama
    result = client.call_llm(messages)
    print(f"Ollama响应: {result}")
    
    print("Ollama集成测试完成")

if __name__ == "__main__":
    test_ollama()