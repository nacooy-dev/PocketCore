# PocketCore 快速开始指南

## 系统要求

- Python 3.13+
- pip包管理器
- 至少一个LLM (Ollama、OpenAI、Anthropic、智谱或OpenRouter)

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd PocketCore
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者在Windows上: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置您的API密钥和其他设置：

```bash
# LLM API密钥（至少配置一个）
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# 智谱配置
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_MODEL=glm-4

# OpenRouter配置
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct

# 默认LLM提供商 (openai, anthropic, ollama, zhipu, openrouter)
DEFAULT_LLM_PROVIDER=ollama
DEFAULT_MODEL=llama3.1
```

## LLM配置选项

### 选项1: 使用本地Ollama (推荐)

1. 安装Ollama: 访问 https://ollama.com/ 下载安装
2. 拉取模型: `ollama run llama3.1`
3. 在 `.env` 文件中设置:
   ```
   DEFAULT_LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.1
   ```

### 选项2: 使用OpenAI

1. 获取OpenAI API密钥: https://platform.openai.com/api-keys
2. 在 `.env` 文件中设置:
   ```
   DEFAULT_LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   DEFAULT_MODEL=gpt-4o
   ```

### 选项3: 使用Anthropic

1. 获取Anthropic API密钥: https://console.anthropic.com/settings/keys
2. 在 `.env` 文件中设置:
   ```
   DEFAULT_LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   DEFAULT_MODEL=claude-3-5-sonnet-20240620
   ```

### 选项4: 使用智谱(Zhipu)

1. 获取智谱API密钥: https://open.bigmodel.cn/
2. 在 `.env` 文件中设置:
   ```
   DEFAULT_LLM_PROVIDER=zhipu
   ZHIPU_API_KEY=your_zhipu_api_key_here
   ZHIPU_MODEL=glm-4
   ```

### 选项5: 使用OpenRouter

1. 获取OpenRouter API密钥: https://openrouter.ai/
2. 在 `.env` 文件中设置:
   ```
   DEFAULT_LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
   ```

## 运行系统

### 命令行模式

```bash
python main.py
```

在命令行模式下，您可以：

- 输入问题与助手交互
- 输入 `tools` 查看可用工具
- 输入 `memory` 查看最近的交互历史
- 输入 `models` 查看可用模型（新功能）
- 输入 `quit` 或 `exit` 退出程序

### Web服务模式

```bash
python api.py
```

或者使用uvicorn：

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

Web服务启动后，您可以通过以下API端点访问：

- `GET /` - 系统状态
- `GET /tools` - 可用工具列表
- `GET /models` - 可用模型列表
- `POST /query` - 处理查询请求
- `GET /memory` - 交互历史

## 使用示例

### 命令行交互示例

```
PocketCore 智能助手中枢已启动
输入 'quit' 或 'exit' 退出程序
输入 'tools' 查看可用工具
输入 'memory' 查看最近的交互历史
输入 'models' 查看可用模型
----------------------------------------

> 你好
正在处理...
助手: 你好！有什么我可以帮助你的吗？

> 计算 123 + 456
正在处理...
助手: 计算结果: 123 + 456 = 579

> tools
可用工具:
  - general_chat: 通用聊天工具
  - web_search: 网络搜索工具
  - calculator: 计算器工具
  - translator: 翻译工具
  - model_discovery: 发现可用的LLM模型

> models
可用的LLM模型:
OLLAMA:
  - llama3.1
OPENAI:
  - gpt-4o
  - gpt-4o-mini
  - gpt-4
  - gpt-3.5-turbo
```

### Web API使用示例

```bash
# 获取工具列表
curl http://127.0.0.1:8000/tools

# 获取模型列表
curl http://127.0.0.1:8000/models

# 发送查询请求
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "你好"}'

# 获取交互历史
curl http://127.0.0.1:8000/memory?limit=5
```

## 系统配置

### 环境变量说明

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| OPENAI_API_KEY | 无 | OpenAI API密钥 |
| ANTHROPIC_API_KEY | 无 | Anthropic API密钥 |
| ZHIPU_API_KEY | 无 | 智谱API密钥 |
| OPENROUTER_API_KEY | 无 | OpenRouter API密钥 |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama服务地址 |
| OLLAMA_MODEL | llama3.1 | Ollama使用的模型 |
| ZHIPU_BASE_URL | https://open.bigmodel.cn/api/paas/v4 | 智谱API地址 |
| ZHIPU_MODEL | glm-4 | 智谱使用的模型 |
| OPENROUTER_BASE_URL | https://openrouter.ai/api/v1 | OpenRouter API地址 |
| OPENROUTER_MODEL | meta-llama/llama-3.1-8b-instruct | OpenRouter使用的模型 |
| DEFAULT_LLM_PROVIDER | ollama | 默认LLM提供商 |
| DEFAULT_MODEL | llama3.1 | 默认使用的模型 |
| HOST | 127.0.0.1 | Web服务监听地址 |
| PORT | 8000 | Web服务监听端口 |
| DATABASE_URL | sqlite:///pocketcore.db | 数据库连接URL |
| DEBUG | False | 调试模式 |
| TOOLS_DIR | ./tools | 工具目录 |
| MAX_MEMORY_SIZE | 1000 | 最大内存大小 |

## 常见问题

### 1. 如何添加新的工具？

创建继承自 `BaseTool` 的新工具类，实现 `execute` 方法，然后在 `ToolManager` 中注册。

### 2. 如何扩展系统功能？

可以添加新的节点类型、集成更多LLM提供商、添加插件系统等。

### 3. 如何提高系统性能？

可以启用缓存机制、使用异步处理、优化数据库查询等。

### 4. Ollama连接失败怎么办？

确保Ollama服务正在运行：
1. 安装Ollama: https://ollama.com/
2. 启动Ollama服务
3. 拉取模型: `ollama run llama3.1`

### 5. 如何查看可用的模型？

在命令行模式下输入 `models`，或通过Web API访问 `/models` 端点。

## 故障排除

### API密钥错误

确保在 `.env` 文件中正确配置了API密钥。

### 依赖安装问题

确保使用正确的Python版本，并在虚拟环境中安装依赖。

### 数据库连接问题

检查 `DATABASE_URL` 配置是否正确，确保SQLite数据库文件有读写权限。

### Ollama连接问题

1. 确保Ollama服务正在运行
2. 检查 `OLLAMA_BASE_URL` 配置是否正确
3. 确保指定的模型已拉取

### 模型发现问题

模型发现功能依赖于各提供商的API可用性。如果无法连接到特定提供商的API，系统将返回预定义的模型列表。