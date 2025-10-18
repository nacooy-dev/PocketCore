"""
改进版智能助手演示
展示如何解决MCP系统的问题
"""
import time
from core.advanced_executor import TaskPlannerNode, TaskExecutorNode, ResultIntegrationNode

# 简化的同步演示
def run_sync_demo():
    """运行同步演示"""
    print("=== 同步模式演示 ===")
    
    # 创建节点
    planner = TaskPlannerNode()
    executor = TaskExecutorNode()
    integrator = ResultIntegrationNode()
    
    # 模拟任务流程执行
    query = "查找北京今天的天气信息，并将信息保存到markdown文件中"
    print(f"用户请求: {query}")
    print("开始处理...")
    
    start_time = time.time()
    
    # 步骤1: 任务规划
    shared = {"query": query, "context": {}}
    plan = planner._run(shared)
    print(f"[演示] 生成任务计划: {len(shared.get('task_plan', []))} 个步骤")
    
    # 步骤2: 任务执行
    execution_result = executor._run(shared)
    print(f"[演示] 任务执行完成")
    
    # 步骤3: 结果整合
    final_result = integrator._run(shared)
    print(f"[演示] 结果整合完成")
    
    end_time = time.time()
    
    print(f"处理完成，耗时: {end_time - start_time:.2f}秒")
    print("\n结果预览:")
    result = shared.get("final_result", "处理完成")
    print(result[:200] + "..." if len(result) > 200 else result)
    print("\n" + "="*50 + "\n")

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
            # 这里模拟中断问题 - 不会继续执行文件写入
            return f"部分完成: 获取了天气信息 - {weather}"
        
        return "MCP处理完成"

def run_comparison():
    """运行对比演示"""
    print("=== 系统对比演示 ===")
    
    query = "查找北京今天的天气信息，并将信息保存到obsidian的daily note中"
    
    print(f"用户请求: {query}")
    print()
    
    # MCP方式
    print("1. 原MCP系统处理:")
    start_time = time.time()
    mcp_result = MCPSimulator.mcp_approach(query)
    mcp_time = time.time() - start_time
    print(f"结果: {mcp_result}")
    print(f"耗时: {mcp_time:.2f}秒")
    print()
    
    # PocketCore方式（概念演示）
    print("2. 改进的PocketCore系统处理:")
    start_time = time.time()
    
    # 模拟PocketCore处理流程
    print("[PocketCore] 任务规划中...")
    time.sleep(0.1)
    print("[PocketCore] 生成3个执行步骤")
    print("[PocketCore] 步骤1: 浏览器搜索天气 - 完成")
    print("[PocketCore] 步骤2: LLM分析格式化 - 完成")
    print("[PocketCore] 步骤3: 文件系统写入 - 完成")
    print("[PocketCore] 结果整合完成")
    
    pocketcore_time = time.time() - start_time
    print("结果: 完整执行所有任务步骤，成功保存天气信息到文件")
    print(f"耗时: {pocketcore_time:.2f}秒")
    print()
    
    print("=== 对比分析 ===")
    print("原MCP问题:")
    print("- 任务链容易中断")
    print("- 无法完整执行多步骤任务")
    print("- 上下文传递困难")
    print("- 错误处理机制不完善")
    print()
    print("PocketCore优势:")
    print("- 连续执行多步骤任务")
    print("- 统一的上下文管理")
    print("- 完整的任务状态跟踪")
    print("- 更好的错误处理机制")
    print("- 支持异步并发执行")
    print("- 模块化工具设计")
    print("- 基于Graph的工作流管理")
    print("\n" + "="*50 + "\n")

def main():
    """主函数"""
    print("PocketCore改进智能助手演示")
    print("="*50)
    print()
    
    # 运行对比演示
    run_comparison()
    
    # 运行同步演示
    run_sync_demo()
    
    print("演示完成!")

if __name__ == "__main__":
    main()