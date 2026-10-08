FROM python:3.9-slim

WORKDIR /app

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY test02.py .

# 暴露端口
EXPOSE 3527

# 运行应用
CMD ["python", "test02.py"]