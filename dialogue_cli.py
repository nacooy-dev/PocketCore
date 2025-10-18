#!/usr/bin/env python3
"""
PocketCore 对话助手 CLI 工具
"""

import sys
import os
import argparse
import requests
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.improved_dialogue import ImprovedDialogueAssistant

def interactive_mode(base_url):
    """交互模式"""
    print("=== PocketCore 对话助手 ===")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看帮助")
    print("输入 'tools' 查看可用工具")
    print("-" * 40)
    
    # 创建本地对话助手实例
    assistant = ImprovedDialogueAssistant()
    
    while True:
        try:
            user_input = input("\n> ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("再见！")
                break
            elif user_input.lower() == 'help':
                print("可用命令:")
                print("  quit/exit - 退出程序")
                print("  help - 显示帮助")
                print("  tools - 显示可用工具")
                print("  clear - 清空对话历史")
                continue
            elif user_input.lower() == 'tools':
                tools = assistant.get_available_tools()
                print("可用工具:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
                continue
            elif user_input.lower() == 'clear':
                assistant.clear_history()
                print("对话历史已清空")
                continue
            elif not user_input.strip():
                continue
            
            # 获取助手回复
            response = assistant.chat(user_input)
            print(f"助手: {response}")
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")

def api_mode(base_url, message):
    """API模式"""
    try:
        response = requests.post(
            f"{base_url}/dialogue",
            headers={"Content-Type": "application/json"},
            json={"message": message}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(result["response"])
        else:
            print(f"API错误: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"请求失败: {e}")

def local_mode(message):
    """本地模式（不依赖API）"""
    try:
        assistant = ImprovedDialogueAssistant()
        response = assistant.chat(message)
        print(response)
    except Exception as e:
        print(f"执行失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="PocketCore 对话助手 CLI")
    parser.add_argument("message", nargs="?", help="要发送的消息")
    parser.add_argument("--url", default="http://localhost:8000", help="API基础URL")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--local", "-l", action="store_true", help="本地模式（不依赖API）")
    
    args = parser.parse_args()
    
    if args.local:
        if args.message:
            local_mode(args.message)
        else:
            print("本地模式需要提供消息内容")
    elif args.interactive or not args.message:
        interactive_mode(args.url)
    else:
        api_mode(args.url, args.message)

if __name__ == "__main__":
    main()