"""
核心调度引擎
基于PocketFlow框架实现
"""
from pocketflow import Flow, Node
from typing import Dict, Any, Optional
import asyncio

class DecisionNode(Node):
    """决策节点 - 决定下一步执行哪个工具"""
    
    def prep(self, shared):
        """准备决策所需信息"""
        context = shared.get("context", {})
        query = shared.get("query", "")
        available_tools = shared.get("available_tools", [])
        return context, query, available_tools
    
    def exec(self, inputs):
        """执行决策逻辑"""
        context, query, available_tools = inputs
        
        # 简单决策逻辑 - 在实际应用中可以使用LLM来决策
        if not query:
            return "idle"
            
        # 基于查询内容决定使用哪个工具
        if "搜索" in query or "查找" in query:
            return "web_search"
        elif "计算" in query or "数学" in query:
            return "calculator"
        elif "翻译" in query:
            return "translator"
        else:
            return "general_chat"
    
    def post(self, shared, prep_res, exec_res):
        """后处理 - 保存决策结果"""
        shared["next_action"] = exec_res
        return exec_res

class ToolExecutorNode(Node):
    """工具执行节点"""
    
    def __init__(self, tool_manager):
        super().__init__()
        self.tool_manager = tool_manager
    
    def prep(self, shared):
        """准备执行工具所需信息"""
        next_action = shared.get("next_action", "general_chat")
        query = shared.get("query", "")
        context = shared.get("context", {})
        return next_action, query, context
    
    def exec(self, inputs):
        """执行工具"""
        action, query, context = inputs
        
        # 调用相应的工具
        if action in self.tool_manager.tools:
            tool = self.tool_manager.tools[action]
            return tool.execute(query, context)
        else:
            # 默认聊天工具
            return self.tool_manager.tools["general_chat"].execute(query, context)
    
    def post(self, shared, prep_res, exec_res):
        """后处理 - 保存执行结果"""
        shared["result"] = exec_res
        return "complete"

class MemoryNode(Node):
    """内存管理节点"""
    
    def __init__(self, memory_manager):
        super().__init__()
        self.memory_manager = memory_manager
    
    def prep(self, shared):
        """准备内存操作所需信息"""
        query = shared.get("query", "")
        result = shared.get("result", "")
        context = shared.get("context", {})
        return query, result, context
    
    def exec(self, inputs):
        """执行内存操作"""
        query, result, context = inputs
        
        # 保存对话历史
        self.memory_manager.save_interaction(query, result)
        
        # 更新上下文
        context["last_query"] = query
        context["last_result"] = result
        
        return context
    
    def post(self, shared, prep_res, exec_res):
        """后处理 - 更新共享上下文"""
        shared["context"] = exec_res
        return "updated"

class PocketCoreEngine:
    """PocketCore核心引擎"""
    
    def __init__(self, tool_manager, memory_manager):
        self.tool_manager = tool_manager
        self.memory_manager = memory_manager
        self.flow = self._build_flow()
    
    def _build_flow(self):
        """构建执行流程"""
        # 创建节点
        decision_node = DecisionNode()
        tool_executor_node = ToolExecutorNode(self.tool_manager)
        memory_node = MemoryNode(self.memory_manager)
        
        # 构建流程图
        flow = Flow(decision_node)
        decision_node.next(tool_executor_node)
        tool_executor_node.next(memory_node)
        memory_node.next(decision_node)  # 循环回到决策节点
        
        return flow
    
    def run(self, query: str, context: Optional[Dict[Any, Any]] = None):
        """运行引擎处理查询"""
        # 初始化共享状态
        shared = {
            "query": query,
            "context": context or {},
            "available_tools": list(self.tool_manager.tools.keys())
        }
        
        # 执行流程
        result = self.flow._run(shared)
        
        # 返回结果
        return shared.get("result", "处理完成")
    
    async def run_async(self, query: str, context: Optional[Dict[Any, Any]] = None):
        """异步运行引擎处理查询"""
        # 初始化共享状态
        shared = {
            "query": query,
            "context": context or {},
            "available_tools": list(self.tool_manager.tools.keys())
        }
        
        # 执行流程
        result = await self.flow._run_async(shared)
        
        # 返回结果
        return shared.get("result", "处理完成")