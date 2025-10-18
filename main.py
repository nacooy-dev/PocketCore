"""
PocketCore 主程序
"""
import asyncio
import os
from core.engine import PocketCoreEngine
from core.tools import ToolManager
from core.memory import MemoryManager
from core.tools import LLMClient
from config import Config

def main():
    """主函数"""
    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        return
    
    # 初始化核心组件
    tool_manager = ToolManager()
    memory_manager = MemoryManager()
    
    # 创建引擎
    engine = PocketCoreEngine(tool_manager, memory_manager)
    
    # 简单的命令行交互界面
    print("PocketCore 智能助手中枢已启动")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'tools' 查看可用工具")
    print("输入 'models' 查看可用模型")
    print("输入 'memory' 查看最近的交互历史")
    print("-" * 40)
    
    while True:
        try:
            query = input("\n> ")
            
            if query.lower() in ['quit', 'exit']:
                print("再见！")
                break
            elif query.lower() == 'tools':
                tools = tool_manager.list_tools()
                print("可用工具:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
                continue
            elif query.lower() == 'models':
                llm_client = LLMClient()
                models = llm_client.discover_models()
                print("可用的LLM模型:")
                for provider, model_list in models.items():
                    print(f"\n{provider.upper()}:")
                    for model in model_list:
                        print(f"  - {model}")
                continue
            elif query.lower() == 'memory':
                interactions = memory_manager.get_recent_interactions(5)
                print("最近的交互历史:")
                for interaction in interactions:
                    print(f"  Q: {interaction['query']}")
                    print(f"  A: {interaction['response']}")
                    print(f"  时间: {interaction['timestamp']}")
                    print()
                continue
            elif not query.strip():
                continue
            
            # 处理查询
            print("正在处理...")
            result = engine.run(query)
            print(f"助手: {result}")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"处理出错: {e}")

if __name__ == "__main__":
    main()