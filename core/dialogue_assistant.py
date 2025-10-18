"""
对话助手模块
基于LLM的智能对话助手，能够调用各种工具
"""
from typing import Dict, Any, List, Optional
from core.tools import ToolManager, LLMClient
import json
import re

class DialogueAssistant:
    """对话助手类"""
    
    def __init__(self):
        self.tool_manager = ToolManager()
        self.llm_client = LLMClient()
        self.conversation_history = []
        
    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        tools = self.tool_manager.list_tools()
        
        tool_descriptions = ""
        for tool in tools:
            tool_descriptions += f"- {tool['name']}: {tool['description']}\n"
        
        return f"""
你是一个智能对话助手，可以帮助用户完成各种任务。

你可以使用的工具包括：
{tool_descriptions}

当用户请求需要使用工具时，请按照以下JSON格式回复：
{{"action": "tool_name", "parameters": {{"param1": "value1", "param2": "value2"}}}}

当直接回答用户问题时，请直接回复自然语言，不要使用JSON格式。

示例对话：
用户：计算123+456等于多少？
助手：{{"action": "calculator", "parameters": {{"query": "123 + 456"}}}}

用户：你好
助手：你好！我是智能对话助手，有什么可以帮助你的吗？

用户：查找北京的天气
助手：{{"action": "web_search", "parameters": {{"query": "北京天气"}}}}

请根据用户需求选择合适的工具并提供必要的参数。
"""
    
    def _parse_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """解析工具调用"""
        try:
            # 尝试解析JSON格式的工具调用
            tool_call = json.loads(response)
            if isinstance(tool_call, dict) and "action" in tool_call:
                return tool_call
        except json.JSONDecodeError:
            # 如果不是JSON格式，可能是直接回复
            pass
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
            result = tool.execute(query, parameters)
            return result
        except Exception as e:
            return f"工具执行错误：{str(e)}"
    
    def chat(self, user_input: str, model: Optional[str] = None) -> str:
        """对话接口"""
        # 添加用户输入到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 构建消息历史
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]
        
        # 添加对话历史（限制最近10轮对话）
        for msg in self.conversation_history[-10:]:
            messages.append(msg)
        
        # 调用LLM
        try:
            # 如果指定了模型，则使用指定模型
            if model:
                llm_response = self.llm_client.call_llm(messages, model)
            else:
                llm_response = self.llm_client.call_llm(messages)
        except Exception as e:
            # 如果LLM调用失败，尝试直接解析用户意图并执行工具
            tool_call = self._parse_direct_tool_call(user_input)
            if tool_call:
                tool_result = self._execute_tool(tool_call)
                final_response = f"工具执行完成: {tool_result}"
                self.conversation_history.append({"role": "assistant", "content": final_response})
                return final_response
            else:
                # 如果不是明确的工具调用，使用默认回复
                error_msg = "抱歉，我暂时无法连接到AI服务。您可以尝试以下操作：\n1. 计算数学表达式（如：计算 123 + 456）\n2. 查看可用工具（输入 'tools'）"
                self.conversation_history.append({"role": "assistant", "content": error_msg})
                return error_msg
        
        # 检查是否需要调用工具
        tool_call = self._parse_tool_call(llm_response)
        if tool_call:
            # 执行工具调用
            tool_result = self._execute_tool(tool_call)
            
            # 将工具结果添加到对话历史
            self.conversation_history.append({"role": "assistant", "content": json.dumps(tool_call)})
            self.conversation_history.append({"role": "tool", "content": tool_result})
            
            # 让LLM基于工具结果生成最终回复
            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "tool", "content": tool_result})
            
            try:
                # 如果指定了模型，则使用指定模型
                if model:
                    final_response = self.llm_client.call_llm(messages, model)
                else:
                    final_response = self.llm_client.call_llm(messages)
            except Exception as e:
                final_response = f"工具执行完成: {tool_result}\n\n注：AI服务当前不可用，无法生成详细解释。"
            
            self.conversation_history.append({"role": "assistant", "content": final_response})
            return final_response
        else:
            # 直接回复
            self.conversation_history.append({"role": "assistant", "content": llm_response})
            return llm_response
    
    def _parse_direct_tool_call(self, user_input: str) -> Optional[Dict[str, Any]]:
        """直接解析用户输入中的工具调用"""
        user_input = user_input.lower()
        
        # 计算器工具
        if any(keyword in user_input for keyword in ["计算", "加", "减", "乘", "除", "+", "-", "*", "/", "="]):
            import re
            math_expr = re.search(r'[\d\+\-\*\/\(\)\.\s]+', user_input)
            if math_expr:
                return {
                    "action": "calculator",
                    "parameters": {"query": math_expr.group().strip()}
                }
        
        # 翻译工具
        if any(keyword in user_input for keyword in ["翻译", "translate"]):
            return {
                "action": "translator",
                "parameters": {"query": user_input}
            }
        
        # 搜索工具
        if any(keyword in user_input for keyword in ["搜索", "查找", "天气", "新闻"]):
            return {
                "action": "web_search",
                "parameters": {"query": user_input}
            }
        
        return None
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """获取可用工具列表"""
        return self.tool_manager.list_tools()
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

class AdvancedDialogueAssistant(DialogueAssistant):
    """高级对话助手"""
    
    def __init__(self):
        super().__init__()
        self.task_context = {}
    
    def _build_advanced_system_prompt(self) -> str:
        """构建高级系统提示"""
        tools = self.tool_manager.list_tools()
        
        tool_descriptions = ""
        for tool in tools:
            tool_descriptions += f"- {tool['name']}: {tool['description']}\n"
        
        return f"""
你是一个高级智能对话助手，具有以下能力：

1. 智能任务理解：能够理解复杂的多步骤任务
2. 工具调用：可以调用以下工具完成任务
3. 上下文管理：能够维护任务执行的上下文
4. 结果整合：能够整合多步骤任务的结果

可用工具：
{tool_descriptions}

任务执行流程：
1. 分析用户请求，识别是否需要执行任务
2. 如果需要执行任务，规划执行步骤
3. 按步骤调用相应工具
4. 整合所有结果，给出最终回答

工具调用格式：
{{"action": "tool_name", "parameters": {{"param1": "value1"}}}}

复杂任务处理：
对于需要多步骤完成的任务，请按以下方式处理：
1. 先调用需要的工具获取信息
2. 基于获取的信息决定下一步操作
3. 继续执行直到任务完成

示例：
用户：查找北京天气并保存到文件
助手：{{"action": "web_search", "parameters": {{"query": "北京天气"}}}}
助手：{{"action": "general_chat", "parameters": {{"query": "请将以下天气信息格式化为报告：[天气信息]"}}}}
助手：{{"action": "filesystem", "parameters": {{"operation": "write", "content": "[格式化后的报告]", "filename": "weather_report.md"}}}}

请根据用户需求智能选择和调用工具。
"""
    
    def _extract_task_sequence(self, response: str) -> List[Dict[str, Any]]:
        """提取任务序列"""
        # 这里可以实现更复杂的任务序列提取逻辑
        tool_call = self._parse_tool_call(response)
        if tool_call:
            return [tool_call]
        return []
    
    def chat(self, user_input: str, model: Optional[str] = None) -> str:
        """高级对话接口"""
        # 添加用户输入到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 构建消息历史
        messages = [
            {"role": "system", "content": self._build_advanced_system_prompt()}
        ]
        
        # 添加对话历史
        for msg in self.conversation_history[-10:]:
            messages.append(msg)
        
        # 调用LLM
        # 如果指定了模型，则使用指定模型
        if model:
            llm_response = self.llm_client.call_llm(messages, model)
        else:
            llm_response = self.llm_client.call_llm(messages)
        
        # 检查是否需要调用工具
        task_sequence = self._extract_task_sequence(llm_response)
        
        if task_sequence:
            # 执行任务序列
            results = []
            for tool_call in task_sequence:
                tool_result = self._execute_tool(tool_call)
                results.append({
                    "tool": tool_call["action"],
                    "parameters": tool_call.get("parameters", {}),
                    "result": tool_result
                })
                
                # 将工具结果添加到对话历史
                self.conversation_history.append({"role": "assistant", "content": json.dumps(tool_call)})
                self.conversation_history.append({"role": "tool", "content": tool_result})
            
            # 整合结果并生成最终回复
            if len(results) == 1:
                final_response = results[0]["result"]
            else:
                # 多步骤任务的结果整合
                summary = "任务执行完成，结果如下：\n"
                for i, result in enumerate(results, 1):
                    summary += f"{i}. {result['tool']} 执行结果: {result['result']}\n"
                final_response = summary
            
            self.conversation_history.append({"role": "assistant", "content": final_response})
            return final_response
        else:
            # 直接回复
            self.conversation_history.append({"role": "assistant", "content": llm_response})
            return llm_response

# 简单的对话助手使用示例
def demo_dialogue_assistant():
    """演示对话助手"""
    print("=== 对话助手演示 ===")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'tools' 查看可用工具")
    print("-" * 40)
    
    # 创建对话助手
    assistant = DialogueAssistant()
    
    while True:
        try:
            user_input = input("\n用户: ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("助手: 再见！")
                break
            elif user_input.lower() == 'tools':
                tools = assistant.get_available_tools()
                print("助手: 可用工具:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description']}")
                continue
            elif not user_input.strip():
                continue
            
            # 获取助手回复
            response = assistant.chat(user_input)
            print(f"助手: {response}")
            
        except KeyboardInterrupt:
            print("\n\n助手: 再见！")
            break
        except Exception as e:
            print(f"助手: 抱歉，处理时出现错误: {e}")

if __name__ == "__main__":
    demo_dialogue_assistant()