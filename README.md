# PocketCore 智能助手中枢

PocketCore 是一个基于 PocketFlow 框架构建的轻量级个人智能助手系统，用于高效调度和使用各种 AI 工具。

## 功能特性

- **多LLM支持**：支持 Ollama、OpenAI、Anthropic、智谱、OpenRouter 等多种LLM提供商
- **工具调度**：智能调度各种AI工具，包括计算器、翻译器、网络搜索等
- **模型发现**：自动发现可用的AI模型
- **对话助手**：基于LLM的智能对话助手，支持工具调用
- **Web界面**：现代化的Web界面，支持聊天历史和模型选择

## 系统要求

- Python 3.8+
- Ollama (用于本地模型支持)
- 虚拟环境 (推荐)

## 安装步骤

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd PocketCore
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加必要的API密钥
   ```

## 启动服务

```bash
python api.py
```

服务将在 `http://127.0.0.1:8000` 启动。

## 使用说明

### Web界面

- **主页**：`http://127.0.0.1:8000/` - 系统概览和API测试
- **对话助手**：`http://127.0.0.1:8000/chat` - 智能对话界面
- **设置**：`http://127.0.0.1:8000/settings` - 模型和API密钥配置

### API端点

- `GET /` - 系统状态
- `GET /tools` - 可用工具列表
- `GET /models` - 可用模型列表
- `POST /query` - 处理查询请求
- `GET /memory` - 交互历史
- `POST /dialogue` - 对话接口

### 对话助手功能

对话助手可以执行以下操作：

1. **数学计算**：自动识别数学表达式并计算结果
2. **语言翻译**：提供多语言翻译服务
3. **信息搜索**：搜索网络信息
4. **模型管理**：查看和管理可用AI模型

## 配置说明

在 `.env` 文件中配置以下参数：

```env
# LLM API密钥（至少配置一个）
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b

# 智谱配置
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_MODEL=glm-4

# OpenRouter配置
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct

# 默认LLM提供商 (openai, anthropic, ollama, zhipu, openrouter)
DEFAULT_LLM_PROVIDER=ollama
DEFAULT_MODEL=qwen3:4b

# 服务器配置
HOST=127.0.0.1
PORT=8000
```

## 开发指南

### 项目结构

```
PocketCore/
├── api.py              # Web API接口
├── config.py           # 配置管理
├── core/               # 核心模块
│   ├── engine.py       # 调度引擎
│   ├── tools.py        # 工具管理
│   ├── memory.py       # 内存管理
│   └── dialogue_assistant.py  # 对话助手
├── static/             # 静态文件
│   ├── chat.html       # 对话界面
│   ├── settings.html   # 设置界面
│   └── index.html      # 主页
├── requirements.txt    # 依赖包
├── .env.example        # 环境变量示例
└── README.md           # 说明文档
```

### 添加新工具

1. 在 `core/tools.py` 中创建新的工具类，继承 `BaseTool`
2. 实现 `execute` 方法
3. 在 `ToolManager` 中注册工具

### 扩展LLM提供商

1. 在 `core/tools.py` 的 `LLMClient` 类中添加新的调用方法
2. 在 `discover_models` 方法中添加模型发现逻辑
3. 更新 `config.py` 和 `.env` 文件中的配置

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。