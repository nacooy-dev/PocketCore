"""
PocketCore 核心模块测试
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tools import ToolManager
from core.memory import MemoryManager
from core.engine import PocketCoreEngine

def test_tool_manager():
    """测试工具管理器"""
    print("测试工具管理器...")
    tool_manager = ToolManager()
    
    # 列出所有工具
    tools = tool_manager.list_tools()
    print(f"注册的工具数量: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # 测试获取工具
    chat_tool = tool_manager.get_tool("general_chat")
    if chat_tool:
        print(f"成功获取工具: {chat_tool.name}")
    else:
        print("获取工具失败")
    
    print("工具管理器测试完成\n")

def test_memory_manager():
    """测试内存管理器"""
    print("测试内存管理器...")
    memory_manager = MemoryManager()
    
    # 保存交互历史
    memory_manager.save_interaction("你好", "你好！有什么我可以帮助你的吗？")
    memory_manager.save_interaction("今天天气怎么样？", "我无法获取实时天气信息，请查看天气应用或网站。")
    
    # 获取最近交互
    recent = memory_manager.get_recent_interactions(2)
    print(f"最近交互数量: {len(recent)}")
    for interaction in recent:
        print(f"  Q: {interaction['query']}")
        print(f"  A: {interaction['response']}")
    
    # 测试上下文
    memory_manager.save_context("user_name", "张三")
    memory_manager.save_context("preferences", {"theme": "dark", "language": "zh"})
    
    user_name = memory_manager.get_context("user_name")
    preferences = memory_manager.get_context("preferences")
    print(f"用户姓名: {user_name}")
    print(f"用户偏好: {preferences}")
    
    print("内存管理器测试完成\n")

def test_engine():
    """测试核心引擎"""
    print("测试核心引擎...")
    
    # 初始化组件
    tool_manager = ToolManager()
    memory_manager = MemoryManager()
    engine = PocketCoreEngine(tool_manager, memory_manager)
    
    # 测试运行
    test_queries = [
        "你好",
        "计算 123 + 456",
        "翻译 Hello, how are you?",
        "搜索人工智能的发展历史"
    ]
    
    for query in test_queries:
        print(f"查询: {query}")
        result = engine.run(query)
        print(f"结果: {result}")
        print()
    
    print("核心引擎测试完成\n")

def main():
    """主测试函数"""
    print("PocketCore 核心模块测试")
    print("=" * 30)
    
    try:
        test_tool_manager()
        test_memory_manager()
        test_engine()
        print("所有测试完成！")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()