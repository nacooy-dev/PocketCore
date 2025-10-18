"""
概念验证：基于PocketCore的改进智能助手
解决MCP系统中的任务链中断问题
"""
from pocketflow import Flow, Node
from typing import Dict, Any, List
import asyncio
import time

# 模拟工具类
class BrowserTool:
    async def search_weather(self, location: str) -> str:
        """模拟搜索天气信息"""
        print(f"正在搜索 {location} 的天气信息...")
        await asyncio.sleep(1)  # 模拟网络延迟
        return f"{location}今天晴朗，温度25°C，湿度60%"

class FileTool:
    async def write_to_obsidian(self, content: str, filename: str) -> str:
        """模拟写入Obsidian文件"""
        print(f"正在将内容写入 {filename}...")
        await asyncio.sleep(0.5)  # 模拟文件操作
        return f"成功将天气信息写入 {filename}"

# 任务规划节点
class TaskPlannerNode(Node):
    def prep(self, shared):
        query = shared.get("query", "")
        context = shared.get("context", {})
        return query, context
    
    def exec(self, inputs):
        query, context = inputs
        # 简单的任务规划逻辑
        if "天气" in query and "保存" in query:
            plan = [
                {"type": "search_weather", "location": "北京"},
                {"type": "write_file", "filename": "daily_weather.md"}
            ]
        else:
            plan = [{"type": "simple_response", "content": "已收到请求"}]
        return plan
    
    def post(self, shared, prep_res, exec_res):
        shared["task_plan"] = exec_res
        print(f"任务计划: {exec_res}")
        return "planned"

# 任务执行节点
class TaskExecutorNode(Node):
    def __init__(self):
        super().__init__()
        self.browser_tool = BrowserTool()
        self.file_tool = FileTool()
    
    def prep(self, shared):
        plan = shared.get("task_plan", [])
        context = shared.get("context", {})
        return plan, context
    
    async def execute_step(self, step: Dict[str, Any]) -> str:
        """执行单个步骤"""
        if step["type"] == "search_weather":
            result = await self.browser_tool.search_weather(step["location"])
            return result
        elif step["type"] == "write_file":
            # 获取之前步骤的结果
            weather_info = self.params.get("weather_info", "未找到天气信息")
            content = f"# 天气日报\n\n{weather_info}\n\n> 日期: {time.strftime('%Y-%m-%d')}"
            result = await self.file_tool.write_to_obsidian(content, step["filename"])
            return result
        elif step["type"] == "simple_response":
            return step["content"]
        return "未知任务类型"
    
    def exec(self, inputs):
        plan, context = inputs
        results = []
        
        # 顺序执行所有步骤
        for i, step in enumerate(plan):
            # 这里简化处理，实际应该使用异步执行
            if step["type"] == "search_weather":
                result = asyncio.run(self.browser_tool.search_weather(step["location"]))
                # 将天气信息保存到参数中，供后续步骤使用
                self.params["weather_info"] = result
                results.append(result)
            elif step["type"] == "write_file":
                weather_info = self.params.get("weather_info", "未找到天气信息")
                content = f"# 天气日报\n\n{weather_info}\n\n> 日期: {time.strftime('%Y-%m-%d')}"
                result = asyncio.run(self.file_tool.write_to_obsidian(content, step["filename"]))
                results.append(result)
            else:
                result = "已完成简单响应任务"
                results.append(result)
                
        return results
    
    def post(self, shared, prep_res, exec_res):
        shared["task_results"] = exec_res
        print(f"任务执行结果: {exec_res}")
        return "executed"

# 结果整合节点
class ResultIntegrationNode(Node):
    def prep(self, shared):
        results = shared.get("task_results", [])
        original_query = shared.get("query", "")
        return results, original_query
    
    def exec(self, inputs):
        results, original_query = inputs
        # 整合结果
        if results:
            final_result = f"已完成您的请求: {original_query}\n\n执行步骤:\n"
            for i, result in enumerate(results, 1):
                final_result += f"{i}. {result}\n"
        else:
            final_result = "未执行任何任务"
        return final_result
    
    def post(self, shared, prep_res, exec_res):
        shared["final_result"] = exec_res
        return "completed"

# 改进的智能助手类
class ImprovedAssistant:
    def __init__(self):
        self.flow = self._build_flow()
    
    def _build_flow(self):
        """构建任务流程"""
        # 创建节点
        planner = TaskPlannerNode()
        executor = TaskExecutorNode()
        integrator = ResultIntegrationNode()
        
        # 构建流程
        flow = Flow(planner)
        planner.next(executor, "planned")
        executor.next(integrator, "executed")
        
        return flow
    
    def process_request(self, query: str) -> str:
        """处理用户请求"""
        shared = {
            "query": query,
            "context": {}
        }
        
        # 执行流程
        self.flow._run(shared)
        
        return shared.get("final_result", "处理完成")

# 模拟MCP系统的问题
class MCPSimulator:
    """模拟原有MCP系统的问题"""
    
    @staticmethod
    def mcp_weather_search(location: str) -> str:
        """模拟MCP天气搜索"""
        print(f"[MCP] 搜索 {location} 天气...")
        time.sleep(1)
        return f"{location}天气晴朗"
    
    @staticmethod
    def mcp_write_file(content: str, filename: str) -> str:
        """模拟MCP文件写入"""
        print(f"[MCP] 写入文件 {filename}...")
        time.sleep(0.5)
        return f"写入完成: {filename}"
    
    @staticmethod
    def mcp_approach(query: str) -> str:
        """模拟MCP处理方式"""
        print("[MCP] 开始处理请求...")
        
        if "天气" in query and "保存" in query:
            # 第一个MCP执行完后可能就停止了
            weather = MCPSimulator.mcp_weather_search("北京")
            print(f"[MCP] 天气信息: {weather}")
            print("[MCP] 第一个任务完成，但流程可能中断...")
            # 这里模拟中断问题
            return f"部分完成: 获取了天气信息 - {weather}"
        
        return "MCP处理完成"

# 演示函数
def demo():
    """演示改进效果"""
    print("=== 智能助手改进演示 ===\n")
    
    # 用户请求
    user_query = "查找北京今天的天气信息，并将信息保存到obsidian的daily note中"
    
    print("1. 原MCP系统处理:")
    mcp_result = MCPSimulator.mcp_approach(user_query)
    print(f"结果: {mcp_result}\n")
    
    print("2. 改进的PocketCore系统处理:")
    assistant = ImprovedAssistant()
    pocketcore_result = assistant.process_request(user_query)
    print(f"结果: {pocketcore_result}\n")
    
    print("=== 对比分析 ===")
    print("原MCP问题:")
    print("- 任务链容易中断")
    print("- 无法完整执行多步骤任务")
    print("- 上下文传递困难")
    print("\nPocketCore优势:")
    print("- 连续执行多步骤任务")
    print("- 统一的上下文管理")
    print("- 完整的任务状态跟踪")
    print("- 更好的错误处理机制")

if __name__ == "__main__":
    demo()