"""
PocketCore Web API 接口
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import os

from core.engine import PocketCoreEngine
from core.tools import ToolManager
from core.memory import MemoryManager
from core.tools import LLMClient
from core.dialogue_assistant import DialogueAssistant
from config import Config

app = FastAPI(title="PocketCore API", description="个人智能助手中枢API")

# 初始化核心组件
tool_manager = ToolManager()
memory_manager = MemoryManager()
engine = PocketCoreEngine(tool_manager, memory_manager)
dialogue_assistant = DialogueAssistant()

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[Any, Any]] = None

class QueryResponse(BaseModel):
    result: str
    context: Optional[Dict[Any, Any]] = None

class ModelInfo(BaseModel):
    provider: str
    models: List[str]

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

class DialogueRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = None

class DialogueResponse(BaseModel):
    response: str
    conversation_id: str

@app.get("/")
async def root():
    """根路径"""
    # 如果存在静态文件，返回静态首页
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    # 否则返回JSON响应
    return {"message": "PocketCore 智能助手中枢API已启动"}

@app.get("/chat")
async def chat_page():
    """对话助手页面"""
    chat_path = os.path.join(static_dir, "chat.html")
    if os.path.exists(chat_path):
        return FileResponse(chat_path)
    return {"message": "对话助手页面未找到"}

@app.get("/settings")
async def settings_page():
    """设置页面"""
    settings_path = os.path.join(static_dir, "settings.html")
    if os.path.exists(settings_path):
        return FileResponse(settings_path)
    return {"message": "设置页面未找到"}

@app.get("/tools")
async def list_tools():
    """列出所有可用工具"""
    return {"tools": tool_manager.list_tools()}

@app.get("/models")
async def list_models():
    """列出所有可用模型"""
    llm_client = LLMClient()
    models_dict = llm_client.discover_models()
    
    models_list = [
        ModelInfo(provider=provider, models=models)
        for provider, models in models_dict.items()
    ]
    
    return ModelsResponse(models=models_list)

@app.post("/query")
async def process_query(request: QueryRequest):
    """处理查询请求"""
    try:
        result = await engine.run_async(request.query, request.context)
        return QueryResponse(
            result=result,
            context=request.context
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/memory")
async def get_memory(limit: int = 10):
    """获取交互历史"""
    interactions = memory_manager.get_recent_interactions(limit)
    return {"interactions": interactions}

@app.post("/dialogue")
async def chat_dialogue(request: DialogueRequest):
    """对话接口"""
    try:
        # 如果请求中指定了模型，则使用指定的模型
        if request.model:
            # 保存当前默认模型
            original_model = Config.DEFAULT_MODEL
            # 临时设置指定模型
            Config.DEFAULT_MODEL = request.model
            response = dialogue_assistant.chat(request.message)
            # 恢复原始模型设置
            Config.DEFAULT_MODEL = original_model
        else:
            response = dialogue_assistant.chat(request.message)
            
        return DialogueResponse(
            response=response,
            conversation_id=request.conversation_id or "default"
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)