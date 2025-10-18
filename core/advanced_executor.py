"""
增强版任务执行器
解决MCP系统中的任务链中断问题
"""
from pocketflow import Node, AsyncNode
from typing import Dict, Any, List, Optional
import asyncio
import aiohttp
import json
import os
from datetime import datetime

class ToolRegistry:
    """工具注册表"""
    def __init__(self):
        self.tools = {}
    
    def register(self, name: str, tool_class):
        """注册工具"""
        self.tools[name] = tool_class
    
    def get(self, name: str):
        """获取工具实例"""
        if name not in self.tools:
            raise ValueError(f"未找到工具: {name}")
        return self.tools[name]()

# 工具基类
class BaseTool:
    def __init__(self, name: str):
        self.name = name
    
    async def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具操作"""
        raise NotImplementedError

# 浏览器工具
class BrowserTool(BaseTool):
    def __init__(self):
        super().__init__("browser")
        self.session = None
    
    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行浏览器相关操作"""
        operation = action.get("operation")
        result = {"tool": self.name, "operation": operation}
        
        if operation == "search_weather":
            location = action.get("location", "北京")
            # 模拟天气搜索
            result["data"] = {
                "location": location,
                "temperature": "25°C",
                "condition": "晴朗",
                "humidity": "60%",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            print(f"[BrowserTool] 搜索 {location} 天气信息完成")
            
        elif operation == "navigate":
            url = action.get("url")
            result["data"] = {"url": url, "status": "navigated"}
            print(f"[BrowserTool] 导航到 {url}")
            
        elif operation == "extract":
            selector = action.get("selector")
            # 模拟数据提取
            result["data"] = {"extracted": f"从 {selector} 提取的数据"}
            print(f"[BrowserTool] 提取数据完成")
        
        return result

# 文件系统工具
class FileSystemTool(BaseTool):
    def __init__(self):
        super().__init__("filesystem")
        # 确保目录存在
        os.makedirs("notes", exist_ok=True)
    
    async def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行文件系统操作"""
        operation = action.get("operation")
        result = {"tool": self.name, "operation": operation}
        
        if operation == "write_markdown":
            filename = action.get("filename", "default.md")
            content = action.get("content", "")
            filepath = os.path.join("notes", filename)
            
            # 写入文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            result["data"] = {"filepath": filepath, "status": "written"}
            print(f"[FileSystemTool] 写入文件 {filepath}")
            
        elif operation == "read_markdown":
            filename = action.get("filename", "default.md")
            filepath = os.path.join("notes", filename)
            
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                result["data"] = {"filepath": filepath, "content": content}
            else:
                result["data"] = {"filepath": filepath, "content": "", "error": "文件不存在"}
            print(f"[FileSystemTool] 读取文件 {filepath}")
        
        return result

# 网络工具
class NetworkTool(BaseTool):
    def __init__(self):
        super().__init__("network")
        self.session = None
    
    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行网络操作"""
        operation = action.get("operation")
        result = {"tool": self.name, "operation": operation}
        
        session = await self._get_session()
        
        if operation == "get":
            url = action.get("url")
            try:
                async with session.get(url) as response:
                    content = await response.text()
                    result["data"] = {"url": url, "status": response.status, "content": content[:200] + "..."}
                    print(f"[NetworkTool] GET请求 {url} 完成")
            except Exception as e:
                result["data"] = {"url": url, "error": str(e)}
                print(f"[NetworkTool] GET请求 {url} 失败: {e}")
        
        return result

# LLM工具
class LLMTool(BaseTool):
    def __init__(self):
        super().__init__("llm")
        # 这里可以集成实际的LLM调用
        # 为简化演示，使用模拟响应
    
    async def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行LLM操作"""
        operation = action.get("operation")
        result = {"tool": self.name, "operation": operation}
        
        if operation == "analyze":
            prompt = action.get("prompt", "")
            # 模拟LLM分析
            result["data"] = {
                "prompt": prompt,
                "response": f"经过分析 '{prompt}'，我建议采取以下行动..."
            }
            print(f"[LLMTool] 分析完成")
        
        elif operation == "summarize":
            content = action.get("content", "")
            result["data"] = {
                "content": content[:50] + "...",
                "summary": f"这是 '{content[:20]}...' 的摘要"
            }
            print(f"[LLMTool] 摘要完成")
        
        return result

# 注册工具
tool_registry = ToolRegistry()
tool_registry.register("browser", BrowserTool)
tool_registry.register("filesystem", FileSystemTool)
tool_registry.register("network", NetworkTool)
tool_registry.register("llm", LLMTool)

class TaskPlannerNode(Node):
    """任务规划节点"""
    
    def prep(self, shared):
        query = shared.get("query", "")
        context = shared.get("context", {})
        return query, context
    
    def exec(self, inputs):
        query, context = inputs
        # 使用LLM进行任务规划（这里简化处理）
        plan = self._generate_plan(query)
        return plan
    
    def _generate_plan(self, query: str) -> List[Dict[str, Any]]:
        """生成任务计划"""
        # 简化的任务规划逻辑
        if "天气" in query and "保存" in query:
            return [
                {
                    "step": 1,
                    "tool": "browser",
                    "action": {
                        "operation": "search_weather",
                        "location": "北京"
                    },
                    "description": "搜索北京天气信息"
                },
                {
                    "step": 2,
                    "tool": "llm",
                    "action": {
                        "operation": "analyze",
                        "prompt": "请将以下天气信息格式化为Markdown格式"
                    },
                    "description": "格式化天气信息"
                },
                {
                    "step": 3,
                    "tool": "filesystem",
                    "action": {
                        "operation": "write_markdown",
                        "filename": f"weather_{datetime.now().strftime('%Y%m%d')}.md",
                        "content": "# 天气报告\n\n待填充内容"
                    },
                    "description": "保存到Markdown文件"
                }
            ]
        elif "搜索" in query and "总结" in query:
            return [
                {
                    "step": 1,
                    "tool": "network",
                    "action": {
                        "operation": "get",
                        "url": "https://httpbin.org/json"
                    },
                    "description": "获取网络数据"
                },
                {
                    "step": 2,
                    "tool": "llm",
                    "action": {
                        "operation": "summarize",
                        "content": "网络数据内容"
                    },
                    "description": "总结内容"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "tool": "llm",
                    "action": {
                        "operation": "analyze",
                        "prompt": query
                    },
                    "description": "分析用户请求"
                }
            ]
    
    def post(self, shared, prep_res, exec_res):
        shared["task_plan"] = exec_res
        print(f"[TaskPlannerNode] 生成任务计划: {len(exec_res)} 个步骤")
        return "planned"

class TaskExecutorNode(AsyncNode):
    """任务执行节点"""
    
    def __init__(self):
        super().__init__()
        self.tool_registry = tool_registry
    
    async def prep_async(self, shared):
        plan = shared.get("task_plan", [])
        context = shared.get("context", {})
        return plan, context
    
    async def exec_async(self, inputs):
        plan, context = inputs
        results = []
        
        # 顺序执行所有步骤
        for step in plan:
            try:
                tool_name = step["tool"]
                action = step["action"]
                
                # 获取工具实例
                tool = self.tool_registry.get(tool_name)
                
                # 执行工具操作
                result = await tool.execute(action, context)
                results.append({
                    "step": step["step"],
                    "description": step["description"],
                    "result": result
                })
                
                # 更新上下文
                context[f"step_{step['step']}_result"] = result
                
                print(f"[TaskExecutorNode] 完成步骤 {step['step']}: {step['description']}")
                
            except Exception as e:
                error_result = {
                    "step": step["step"],
                    "description": step["description"],
                    "error": str(e)
                }
                results.append(error_result)
                print(f"[TaskExecutorNode] 步骤 {step['step']} 执行失败: {e}")
        
        return results
    
    async def post_async(self, shared, prep_res, exec_res):
        shared["task_results"] = exec_res
        shared["context"] = shared.get("context", {})
        print(f"[TaskExecutorNode] 所有任务执行完成，共 {len(exec_res)} 个步骤")
        return "executed"

class ResultIntegrationNode(Node):
    """结果整合节点"""
    
    def prep(self, shared):
        results = shared.get("task_results", [])
        original_query = shared.get("query", "")
        return results, original_query
    
    def exec(self, inputs):
        results, original_query = inputs
        
        # 整合结果
        if not results:
            return "未执行任何任务"
        
        # 构建详细的执行报告
        report = f"# 任务执行报告\n\n"
        report += f"**原始请求**: {original_query}\n\n"
        report += f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"## 执行详情\n\n"
        
        successful_steps = 0
        for result in results:
            step_num = result.get("step", "未知")
            description = result.get("description", "未知操作")
            
            if "error" in result:
                report += f"### 步骤 {step_num}: {description}\n"
                report += f"- 状态: ❌ 失败\n"
                report += f"- 错误: {result['error']}\n\n"
            else:
                report += f"### 步骤 {step_num}: {description}\n"
                report += f"- 状态: ✅ 成功\n"
                successful_steps += 1
                
                # 添加详细结果
                result_data = result.get("result", {})
                if "data" in result_data:
                    data = result_data["data"]
                    report += f"- 结果: {json.dumps(data, ensure_ascii=False, indent=2)}\n"
                report += "\n"
        
        report += f"## 总结\n\n"
        report += f"- 总步骤数: {len(results)}\n"
        report += f"- 成功步骤: {successful_steps}\n"
        report += f"- 失败步骤: {len(results) - successful_steps}\n"
        
        if successful_steps == len(results):
            report += "- 整体状态: ✅ 全部成功\n"
        elif successful_steps > 0:
            report += "- 整体状态: ⚠️ 部分成功\n"
        else:
            report += "- 整体状态: ❌ 全部失败\n"
        
        return report
    
    def post(self, shared, prep_res, exec_res):
        shared["final_result"] = exec_res
        print("[ResultIntegrationNode] 结果整合完成")
        return "completed"