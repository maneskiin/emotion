# -*- coding:utf-8 -*-
import requests
import json

url = "http://10.108.16.44:8000/v1/completions"
headers = {
    "Content-Type": "application/json"
}
data = {
    "model": "/app/Qwen2.5-7B-Instruct/",
    "prompt": "示例提示词",
    "max_tokens": 4000,
    "temperature": 0.7,
    "response_format": {"type": "json_object"}
}

try:
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        timeout=180  # 设置超时时间
    )
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.json())
except requests.exceptions.ConnectionError as e:
    print("连接失败，请检查以下问题：")
    print("1. 服务器是否正常运行")
    print("2. 防火墙是否开放80端口")
    print("3. 网络是否连通")
    print("4. IP地址是否正确（10.108.16.44）")
    print(f"错误详情: {e}")