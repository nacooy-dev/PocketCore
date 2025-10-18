#!/bin/bash

# PocketCore 启动脚本

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "未找到 requirements.txt 文件"
    exit 1
fi

# 安装依赖
echo "检查并安装依赖..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "创建 .env 配置文件..."
    cp .env.example .env
    echo "请编辑 .env 文件配置您的API密钥和其他设置"
fi

# 显示使用选项
echo "PocketCore 启动选项:"
echo "1. 命令行模式: python main.py"
echo "2. Web服务模式: python api.py"
echo "3. 直接运行Web服务: uvicorn api:app --host 0.0.0.0 --port 8000"
echo ""
echo "请选择运行模式 (1/2/3): "
read -r choice

case $choice in
    1)
        echo "启动命令行模式..."
        python main.py
        ;;
    2)
        echo "启动Web服务模式..."
        python api.py
        ;;
    3)
        echo "直接运行Web服务..."
        uvicorn api:app --host 0.0.0.0 --port 8000
        ;;
    *)
        echo "无效选择，启动默认命令行模式..."
        python main.py
        ;;
esac