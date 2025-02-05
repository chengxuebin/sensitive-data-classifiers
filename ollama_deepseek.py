from flask import Flask, render_template, request, jsonify
import requests
import json
import time
from requests.exceptions import RequestException
import os

app = Flask(__name__)

OLLAMA_MODEL = "deepseek-r1:14b"
OLLAMA_API_ENDPOINT = "http://127.0.0.1:11434/api/chat"
OLLAMA_API_VERSION = "http://127.0.0.1:11434/api/version"

# 在应用启动时读取prompt文件
def read_prompt(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filename}")
        return None
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return None

# 读取系统提示和用户提示
system_content = read_prompt(os.path.join('prompts', 'role.txt'))
user_content = read_prompt(os.path.join('prompts', 'personal_info.txt'))

def check_ollama_service():
    try:
        response = requests.get(OLLAMA_API_VERSION)
        return response.status_code == 200
    except RequestException:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if not system_content or not user_content:
        return jsonify({"error": "无法读取必要的提示文件"}), 500
        
    if not check_ollama_service():
        return jsonify({"error": "Ollama服务未运行"}), 503

    content = request.json.get('text', '')
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "model": OLLAMA_MODEL,
        "messages": [{
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": user_content + content
        }],
        "stream": False,
        "options": {"temperature": 0.7}
    }

    try:
        response = requests.post(OLLAMA_API_ENDPOINT, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({"error": f"API调用失败: {response.text}"}), response.status_code
            
    except RequestException as e:
        return jsonify({"error": f"请求异常: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
