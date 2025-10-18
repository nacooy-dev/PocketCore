"""
改进的对话助手模块
即使在没有LLM的情况下也能正常工作
"""
from typing import Dict, Any, List, Optional
from core.tools import ToolManager
import json
import re

class ImprovedDialogueAssistant:
    """改进的对话助手类"""
    
    def __init__(self):
        self.tool_manager = ToolManager()
        self.conversation_history = []
        
    def _parse_user_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
        """解析用户意图并直接匹配工具"""
        user_input = user_input.lower()
        
        # 计算器工具匹配
        if any(keyword in user_input for keyword in ["计算", "加", "减", "乘", "除", "+", "-", "*", "/", "="]):
            # 提取数学表达式
            math_expr = re.search(r'[\d\+\-\*\/\(\)\.\s]+', user_input)
            if math_expr:
                return {
                    "action": "calculator",
                    "parameters": {"query": math_expr.group().strip()}
                }
        
        # 翻译工具匹配
        if any(keyword in user_input for keyword in ["翻译", "translate", "中文", "英文", "english", "chinese"]):
            # 提取需要翻译的文本
            return {
                "action": "translator",
                "parameters": {"query": user_input}
            }
        
        # 搜索工具匹配
        if any(keyword in user_input for keyword in ["搜索", "查找", "天气", "新闻", "信息"]):
            return {
                "action": "web_search",
                "parameters": {"query": user_input}
            }
        
        # 模型发现工具匹配
        if any(keyword in user_input for keyword in ["模型", "model", "models"]):
            return {
                "action": "model_discovery",
                "parameters": {"query": user_input}
            }
        
        return None
    
    def _execute_tool(self, tool_call: Dict[str, Any]) -> str:
        """执行工具调用"""
        try:
            tool_name = tool_call.get("action")
            if not tool_name or not isinstance(tool_name, str):
                return "错误：工具名称无效"
            
            parameters = tool_call.get("parameters", {})
            
            # 获取工具
            tool = self.tool_manager.get_tool(tool_name)
            if not tool:
                return f"错误：未找到工具 '{tool_name}'"
            
            # 执行工具
            query = parameters.get("query", "")
            context = parameters.get("context", {})
            result = tool.execute(query, context)
            return result
        except Exception as e:
            return f"工具执行错误：{str(e)}"
    
    def chat(self, user_input: str) -> str:
        """对话接口"""
        # 添加用户输入到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 尝试直接解析用户意图
        tool_call = self._parse_user_intent(user_input)
        
        if tool_call:
            # 执行工具调用
            tool_result = self._execute_tool(tool_call)
            
            # 将工具结果添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": json.dumps(tool_call)})
            self.conversation_history.append({"role": "tool", "content": tool_result})
            
            # 生成最终回复
            final_response = f"工具执行结果: {tool_result}"
            self.conversation_history.append({"role": "assistant", "content": final_response})
            return final_response
        else:
            # 默认回复
            default_response = "你好！我是PocketCore智能对话助手。我可以帮你：\n1. 计算数学表达式\n2. 翻译文本\n3. 搜索信息\n4. 查看可用模型\n请告诉我你想要做什么？"
            self.conversation_history.append({"role": "assistant", "content": default_response})
            return default_response
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """获取可用工具列表"""
        return self.tool_manager.list_tools()
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

# 测试改进的对话助手
def test_improved_dialogue():
    """测试改进的对话助手"""
    print("=== 测试改进的对话助手 ===")
    
    assistant = ImprovedDialogueAssistant()
    
    # 测试用例
    test_cases = [
        "你好",
        "计算 123 + 456",
        "翻译 Hello, how are you?",
        "查找北京天气",
        "显示可用模型"
    ]
    
    for test_case in test_cases:
        print(f"\n用户: {test_case}")
        response = assistant.chat(test_case)
        print(f"助手: {response}")

if __name__ == "__main__":
    test_improved_dialogue()