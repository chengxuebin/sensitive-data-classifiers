import requests
import json

# 替换为你的 DeepSeek API 密钥和端点
API_KEY = 'your_deepseek_api_key'
API_ENDPOINT = 'https://api.deepseek.com/v1/your_endpoint'

# 请求头，包含 API 密钥
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 请求体，根据 API 文档填写
data = {
    'prompt': 'Python3实现的，调用DeepSeek API的示例代码。',
    'max_tokens': 100,
    'temperature': 0.7
}

# 发送 POST 请求
response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

# 检查响应状态码
if response.status_code == 200:
    # 解析响应内容
    result = response.json()
    print('API 调用成功:')
    print(json.dumps(result, indent=4, ensure_ascii=False))
else:
    print(f'API 调用失败，状态码: {response.status_code}')
    print(response.text)