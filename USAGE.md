# PocketCore 使用指南

## 快速开始

### 1. 启动服务

确保你已经按照 README.md 中的说明安装了所有依赖并配置了环境变量。

```bash
python api.py
```

服务将在 `http://127.0.0.1:8000` 启动。

### 2. 访问Web界面

打开浏览器访问以下URL：

- **主页**：`http://127.0.0.1:8000/`
- **对话助手**：`http://127.0.0.1:8000/chat`
- **设置**：`http://127.0.0.1:8000/settings`

## 使用对话助手

### 基本对话

在对话界面中，你可以与AI助手进行自然语言对话。助手可以回答问题、提供信息和执行任务。

### 数学计算

直接输入数学表达式，助手会自动计算结果：

```
用户：计算 123 + 456
助手：123加456等于579。
```

### 语言翻译

请求翻译服务：

```
用户：翻译 "Hello, how are you?" 成中文
助手：翻译结果: 你好，你好吗？
```

### 信息搜索

请求搜索信息：

```
用户：查找北京的天气
助手：正在为您搜索北京的天气信息...
```

## 配置管理

### 模型配置

在设置页面中，你可以：

1. 选择默认的LLM提供商
2. 设置默认模型
3. 配置各种云服务的API密钥
4. 查看可用的模型列表

### API密钥配置

为使用云服务的LLM模型，你需要配置相应的API密钥：

- **OpenAI**：在 [OpenAI](https://platform.openai.com/) 获取API密钥
- **Anthropic**：在 [Anthropic](https://www.anthropic.com/) 获取API密钥
- **智谱**：在 [智谱](https://open.bigmodel.cn/) 获取API密钥
- **OpenRouter**：在 [OpenRouter](https://openrouter.ai/) 获取API密钥

## API使用

### 获取工具列表

```bash
curl http://127.0.0.1:8000/tools
```

### 获取模型列表

```bash
curl http://127.0.0.1:8000/models
```

### 对话接口

```bash
curl -X POST http://127.0.0.1:8000/dialogue \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "model": "qwen3:4b"}'
```

### 查询接口

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "计算 123 + 456"}'
```

## 高级功能

### 模型选择

在对话界面中，你可以通过下拉菜单选择不同的模型进行对话。支持的本地模型包括：

- qwen3:4b
- gemma3:4b
- llama3:latest
- 等其他Ollama支持的模型

### 聊天历史

对话界面会自动保存聊天历史，你可以在侧边栏中查看和切换历史对话。

### 工具调用

对话助手可以自动识别需要使用工具的任务并调用相应的工具，例如：

```
用户：计算 123 * 456
助手：{"action": "calculator", "parameters": {"query": "123 * 456"}}
```

## 故障排除

### 服务无法启动

1. 检查端口是否被占用：`lsof -i :8000`
2. 确保所有依赖已正确安装
3. 检查环境变量配置

### LLM调用失败

1. 检查Ollama服务是否运行：`ollama list`
2. 确认API密钥是否正确配置
3. 检查网络连接

### 模型不可用

1. 确认模型是否已下载到本地：`ollama list`
2. 检查模型名称是否正确
3. 尝试重新拉取模型：`ollama pull qwen3:4b`

## 常见问题

### Q: 如何添加新的工具？

A: 在 `core/tools.py` 中创建新的工具类并注册到 `ToolManager`。

### Q: 如何支持新的LLM提供商？

A: 在 `core/tools.py` 的 `LLMClient` 类中添加新的调用方法和模型发现逻辑。

### Q: 聊天历史保存在哪里？

A: 聊天历史保存在浏览器的本地存储中，不会发送到服务器。

### Q: 如何更改默认端口？

A: 在 `.env` 文件中修改 `PORT` 参数，或在启动时指定端口。

## 联系和支持

如有问题，请：
1. 查看README.md和USAGE.md文档
2. 提交GitHub Issue
3. 联系项目维护者