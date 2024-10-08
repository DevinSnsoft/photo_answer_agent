import base64
import requests
import gradio as gr
import os

# OpenAI API Key
api_key = '******'

def encode_image(image_path):
    # 将二进制数据（图片内容）编码为 base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def chat_with_image(input_data, history):
    image_path = input_data['files'][0]['path']

    # if image_path is not None:
        # 使用 value 属性从 NamedString 获取图像内容
    image_base64 = encode_image(image_path)
        # image_base64 = encode_image(user_image['files'][0])

    # 构造请求体，包括 base64 编码的图片和用户问题
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": input_data['text']
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            },
        ],
        "max_tokens": 4096
    }

    proxies = {
        'http': 'http://127.0.0.1:7897',
        'https': 'http://127.0.0.1:7897',
    }

    # 发送请求到 OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies=proxies)

    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response from the model.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# with gr.Blocks() as demo:
demo = gr.ChatInterface(
        fn=chat_with_image,
        examples=[{"text": "这道题怎么做？"}, {"text": "这道题怎么解答？"}, {"text": "这道题的解题步骤是？"}],
        title='拍照解答智能体',
        multimodal=True
    )


demo.launch(share=True)