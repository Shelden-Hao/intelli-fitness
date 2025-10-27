#!/bin/bash

echo "======================================"
echo "河北全民健身公共服务体系平台"
echo "======================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python 3.10+"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js 18+"
    exit 1
fi

echo ""
echo "📦 初始化数据..."
cd "$(dirname "$0")/.."
python3 scripts/init_data.py

echo ""
echo "🚀 启动后端服务..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

echo "启动FastAPI服务 (http://localhost:8000)..."
python main.py &
BACKEND_PID=$!

echo ""
echo "🎨 启动前端服务..."
cd ../frontend
npm install -q
echo "启动Vite开发服务器 (http://localhost:5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "✅ 服务启动成功!"
echo "======================================"
echo "前端地址: http://localhost:5173"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/api/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "======================================"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
