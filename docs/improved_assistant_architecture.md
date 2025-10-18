# 改进的智能助手架构设计

## 概述

基于PocketCore框架设计一个更高效的智能助手，解决之前MCP系统中的运行效率和任务链中断问题。

## 核心改进点

### 1. 统一的任务执行环境

与MCP的分布式调用不同，PocketCore提供统一的任务执行环境：

```
mermaid
graph TD
    A[智能助手核心] --> B[任务调度器]
    B --> C[工具执行器]
    C --> D[浏览器工具]
    C --> E[文件系统工具]
    C --> F[网络工具]
    C --> G[LLM工具]
    
    H[共享内存] --> B
    H --> C
    H --> D
    H --> E
    H --> F
    H --> G
```

### 2. 连续任务执行流程

解决任务链中断问题的关键设计：

1. **状态保持**：通过共享内存保持任务执行状态
2. **上下文传递**：在任务步骤间自动传递上下文信息
3. **错误恢复**：支持任务失败后的恢复机制

### 3. 高效的任务调度

```
mermaid
graph TD
    A[用户请求] --> B[意图识别]
    B --> C[任务规划]
    C --> D[并行执行器]
    D --> E[浏览器操作]
    D --> F[数据处理]
    E --> G[结果整合]
    F --> G
    G --> H[文件写入]
    H --> I[返回结果]
```

## 具体实现方案

### 1. 任务规划节点

```python
class TaskPlannerNode(Node):
    def prep(self, shared):
        # 分析用户请求，识别所需步骤
        query = shared["query"]
        context = shared.get("context", {})
        return query, context
    
    def exec(self, inputs):
        query, context = inputs
        # 使用LLM分析任务，生成执行计划
        # 例如："打开网站查找天气信息，然后将信息写到obsidian文件"
        # 计划: [打开浏览器, 搜索天气, 提取信息, 写入文件]
        plan = self.generate_plan(query)
        return plan
    
    def post(self, shared, prep_res, exec_res):
        shared["task_plan"] = exec_res
        return "planned"
```

### 2. 并行执行节点

```python
class ParallelExecutorNode(AsyncParallelBatchNode):
    def prep(self, shared):
        plan = shared["task_plan"]
        return plan
    
    async def exec_async(self, plan):
        # 并行执行任务计划中的步骤
        results = []
        for step in plan:
            if step["type"] == "browser":
                result = await self.browser_tool.execute(step["action"])
            elif step["type"] == "file":
                result = await self.file_tool.execute(step["action"])
            elif step["type"] == "web":
                result = await self.web_tool.execute(step["action"])
            results.append(result)
        return results
```

### 3. 结果整合节点

```python
class ResultIntegrationNode(Node):
    def prep(self, shared):
        results = shared.get("task_results", [])
        original_query = shared.get("query", "")
        return results, original_query
    
    def exec(self, inputs):
        results, original_query = inputs
        # 整合所有步骤的结果
        final_result = self.integrate_results(results, original_query)
        return final_result
    
    def post(self, shared, prep_res, exec_res):
        shared["final_result"] = exec_res
        return "completed"
```

## 工具系统增强

### 1. 浏览器自动化工具

```python
class BrowserTool(BaseTool):
    def __init__(self):
        super().__init__("browser", "浏览器自动化工具")
        # 初始化浏览器驱动
    
    async def execute(self, action):
        # 执行浏览器操作
        if action["type"] == "navigate":
            await self.navigate_to(action["url"])
        elif action["type"] == "search":
            await self.search_weather(action["location"])
        elif action["type"] == "extract":
            return await self.extract_information(action["selector"])
```

### 2. 文件系统工具

```python
class FileSystemTool(BaseTool):
    def __init__(self):
        super().__init__("filesystem", "文件系统工具")
    
    async def execute(self, action):
        # 执行文件操作
        if action["type"] == "write":
            await self.write_to_obsidian(action["content"], action["filename"])
        elif action["type"] == "read":
            return await self.read_from_file(action["filename"])
```

## 内存管理优化

### 1. 上下文状态管理

```python
class ContextManager:
    def __init__(self):
        self.state = {}
        self.history = []
    
    def update_state(self, key, value):
        self.state[key] = value
        self.history.append({"key": key, "value": value, "timestamp": time.time()})
    
    def get_state(self, key):
        return self.state.get(key)
    
    def get_recent_context(self, minutes=10):
        # 获取最近的上下文信息
        recent_time = time.time() - (minutes * 60)
        return [item for item in self.history if item["timestamp"] > recent_time]
```

## 错误处理与恢复

### 1. 任务重试机制

```python
class ResilientNode(Node):
    def __init__(self, max_retries=3, wait_time=1):
        super().__init__(max_retries=max_retries, wait=wait_time)
    
    def exec_fallback(self, prep_res, exc):
        # 失败回退处理
        logger.error(f"任务执行失败: {exc}")
        # 尝试替代方案或返回错误信息
        return f"任务执行失败: {str(exc)}"
```

## 性能优化策略

### 1. 工具实例复用

```python
class ToolManager:
    def __init__(self):
        self.tool_instances = {}
    
    def get_tool(self, tool_name):
        if tool_name not in self.tool_instances:
            # 按需创建工具实例
            self.tool_instances[tool_name] = self._create_tool(tool_name)
        return self.tool_instances[tool_name]
```

### 2. 缓存机制

```python
class CacheManager:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        if key in self.cache:
            item, timestamp = self.cache[key]
            if time.time() - timestamp < 300:  # 5分钟缓存
                return item
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, time.time())
```

## 使用示例

### 复杂任务执行流程

用户请求："查找北京今天的天气信息，并将信息保存到obsidian的daily note中"

执行流程：
1. **任务解析**：识别为多步骤任务
2. **计划生成**：
   - 步骤1：打开天气网站
   - 步骤2：搜索北京天气
   - 步骤3：提取天气信息
   - 步骤4：写入obsidian文件
3. **并行执行**：
   - 浏览器工具执行步骤1-3
   - 文件系统工具准备步骤4
4. **结果整合**：将提取的天气信息格式化后写入文件
5. **返回结果**：确认任务完成

## 优势对比

| 特性 | 原MCP系统 | PocketCore改进系统 |
|------|-----------|-------------------|
| 任务连续性 | 易中断 | 连续执行 |
| 执行效率 | 较低 | 高效 |
| 上下文保持 | 有限 | 完整 |
| 错误恢复 | 弱 | 强 |
| 扩展性 | 复杂 | 简单 |

## 实施计划

### 阶段1：核心框架搭建
- 实现任务规划节点
- 实现并行执行节点
- 实现结果整合节点

### 阶段2：工具系统开发
- 开发浏览器自动化工具
- 开发文件系统工具
- 开发网络请求工具

### 阶段3：优化与测试
- 实现缓存机制
- 实现错误恢复机制
- 进行性能测试

### 阶段4：集成与部署
- 集成到现有PocketCore系统
- 部署测试环境
- 用户验收测试