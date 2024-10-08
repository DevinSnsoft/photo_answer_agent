import json
import os
import base64
import requests
import yaml
from httpx import stream

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)  # 安全地加载 YAML 文件
    return config

config = load_config(os.getcwd() + '\\config.yml')
openai_api_key = config['api_key']['gpt4o_key']
kuangtu_service = config['services']['kuangtu']

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def nlg_service(text, image_path, history):
    payload = {"data":json.dumps({"url":image_path})}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'zhixingyun.yuntim.com',
        'Connection': 'keep-alive'
    }
    # 接入框图旋转模型判断，辅助判断传入图片是作答题目
    # flag = 1000 ：正常下载url图片，框图模型判定该图片是题目
    # flag = 1001 ：无法正常下载url图片
    # flag = 1002 ：正常下载url图片，框图模型判定该图片不是题目
    response = requests.request("POST", kuangtu_service, headers=headers, data=payload)
    # if response.status_code == 200 and json.loads(response.text)['data']['flag'] == 1000 and image_path is not None:
    if response.status_code == 200 and image_path is not None:
        base64_image = encode_image(image_path)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {openai_api_key}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": text
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 4096,
           # "stream": True,
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'], history
        else:
            print("多模态信息处理任务响应异常，请重新发送请求！")
    else:
        return "图片不是作答题目，请重新上传！"

if __name__ == '__main__':
    text = "这道题怎么做？"
    image_path = 'E:\\PythonProjects\\photo_answer_agent\\test_data\\20240926-105630.jpg'
    # image_path = 'https://cdnbj.bookln.cn/homeworkCorrect/20240921/310451757_spWlQajAfUSQ4D64PavG.jpg'
    # image_path = "https://cdnbj.bookln.cn/correct/v2/20240829/155448417_cac21590-659e-11ef-adae-39dde55bd0c9.jpg"
    print(nlg_service(text, image_path))