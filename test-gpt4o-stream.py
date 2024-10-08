import gradio as gr
import requests
import base64
import json

from click import prompt

# API_URL = "https://api.openai.com/v1/chat/completions"  # 替换为实际的 API URL
API_KEY = "******"  # 替换为你的 API 密钥

prompt ={
    "role": "user",
    "content": [{
        "type":"text",
        "text": "糖尿病应该怎么护理？"
    }]
}

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_gpt4o_response(textbox):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model":"gpt-4o",
        # "prompt": prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": textbox
                    },
                    # {
                    #     "type": "image_url",
                    #     "image_url": {
                    #         "url": f"data:image/jpeg;base64,{base64_image}"
                    #     }
                    # }
                ]
            }
        ],
        # "stream": True,
        "max_tokens": 4096,
    }
    proxies = {
        'http': 'http://127.0.0.1:7897',
        'https': 'http://127.0.0.1:7897',
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies=proxies)

    if response.status_code == 200:
        full_response = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                full_response += chunk.decode('utf-8')
        # chat_history.append((prompt, full_response))
        # return "", chat_history
        return full_response
        # return full_response.json()['choices'][0]['message']['content']
    else:
        # chat_history.append((prompt, "Error: " + str(response.status_code)))
        # return "", chat_history
        return "Error"

with gr.Blocks() as app:
    # chatbot = gr.Chatbot()
    textbox = gr.Textbox(placeholder="输入你的消息...")
    outputbox = gr.Textbox()

    textbox.submit(get_gpt4o_response, inputs=[textbox], outputs=[outputbox])

app.launch(share=True)
