"""
测试对话助手功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.dialogue_assistant import DialogueAssistant, AdvancedDialogueAssistant

def test_basic_dialogue():
    """测试基本对话功能"""
    print("=== 测试基本对话助手 ===")
    
    assistant = DialogueAssistant()
    
    # 测试工具列表
    tools = assistant.get_available_tools()
    print(f"可用工具数量: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # 测试简单对话
    print("\n--- 简单对话测试 ---")
    responses = [
        "你好",
        "你能做什么？",
        "计算 123 + 456",
        "翻译 Hello, how are you?",
        "查找人工智能的发展历史"
    ]
    
    for query in responses:
        print(f"\n用户: {query}")
        response = assistant.chat(query)
        print(f"助手: {response}")

def test_advanced_dialogue():
    """测试高级对话功能"""
    print("\n=== 测试高级对话助手 ===")
    
    assistant = AdvancedDialogueAssistant()
    
    # 测试复杂任务
    print("\n--- 复杂任务测试 ---")
    complex_tasks = [
        "查找北京天气",
        "计算 123 * 456 然后翻译结果",
    ]
    
    for task in complex_tasks:
        print(f"\n用户: {task}")
        response = assistant.chat(task)
        print(f"助手: {response}")

def main():
    """主测试函数"""
    print("对话助手功能测试")
    print("=" * 30)
    
    try:
        test_basic_dialogue()
        test_advanced_dialogue()
        print("\n所有测试完成！")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()