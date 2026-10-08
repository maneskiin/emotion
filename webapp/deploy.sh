#!/bin/bash

# 部署脚本 - 情感分析前端应用
echo "========================================="
echo "   情感分析前端应用 Docker 部署脚本"
echo "========================================="
echo ""

# 检查是否在正确的目录
if [ ! -d "frontend" ] || [ ! -d "nginx" ]; then
    echo "错误：请在app目录下运行此脚本"
    echo "当前目录结构应该是："
    echo "webapp/"
    echo "├── frontend/"
    echo "├── nginx/"
    echo "├── docker-compose.yml"
    echo "└── deploy.sh"
    exit 1
fi

# 检查必要文件
echo "检查必要文件..."

# 检查前端文件
if [ ! -f "frontend/Dockerfile" ]; then
    echo "错误：未找到 frontend/Dockerfile"
    exit 1
fi

if [ ! -f "frontend/requirements.txt" ]; then
    echo "错误：未找到 frontend/requirements.txt"
    exit 1
fi

if [ ! -f "frontend/test02.py" ]; then
    echo "错误：未找到 frontend/test02.py"
    exit 1
fi

# 检查nginx配置
if [ ! -f "nginx/nginx.conf" ]; then
    echo "错误：未找到 nginx/nginx.conf"
    exit 1
fi

# 检查docker-compose文件
if [ ! -f "docker-compose.yml" ]; then
    echo "错误：未找到 docker-compose.yml"
    exit 1
fi

echo "✓ 所有必要文件已就绪"
echo ""

# 检查test02.py中的Ajax URL是否已修改
echo "检查Ajax URL配置..."
if grep -q "http://xx.xx.xx.xx:8000/analysis" frontend/test02.py; then
    echo "警告：检测到test02.py中仍使用绝对路径URL"
    echo "请将 'http://xx.xx.xx.xx:8000/analysis' 修改为 '/api/analysis'"
    echo "是否继续部署？(y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "部署已取消"
        exit 1
    fi
else
    echo "✓ Ajax URL配置正确"
fi
echo ""

# 停止并删除旧容器（如果存在）
echo "停止并删除旧容器..."
docker-compose down 2>/dev/null
echo ""

# 构建并启动服务
echo "构建Docker镜像..."
docker-compose build

echo ""
echo "启动服务..."
docker-compose up -d

# 等待服务启动
echo ""
echo "等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "服务状态："
docker-compose ps

# 检查容器是否正常运行
if docker ps | grep -q "emotion-analysis-nginx" && docker ps | grep -q "emotion-analysis-frontend"; then
    echo ""
    echo "========================================="
    echo "✓ 部署成功！"
    echo ""
    echo "常用命令："
    echo "  查看日志：docker-compose logs -f"
    echo "  查看前端日志：docker-compose logs -f frontend"
    echo "  查看Nginx日志：docker-compose logs -f nginx"
    echo "  重启服务：docker-compose restart"
    echo "  停止服务：docker-compose down"
    echo "  重新构建：docker-compose up -d --build"
    echo "========================================="
else
    echo ""
    echo "错误：服务启动失败"
    echo "请查看日志以获取更多信息："
    echo "docker-compose logs"
    exit 1
fi

# 可选：显示最近的日志
echo ""
echo "最近的日志："
docker-compose logs --tail=20