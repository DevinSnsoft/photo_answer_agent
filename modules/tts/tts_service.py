# coding=utf-8
import os
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)  # 安全地加载 YAML 文件
    return config

config = load_config(os.getcwd() + '\\config.yml')
dashscope.api_key = config['api_key']['tts_key']

def tts_service(gpt4o_response_box):
    if gpt4o_response_box is not None:
        result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                        text=gpt4o_response_box,
                                        sample_rate=48000,
                                        format='wav')

        if result.get_response().status_code == 200:
            # 保存语音到本地，需要可解开注释
            # with open('output.wav', 'wb') as f:
            #     f.write(result.get_audio_data())
            return result.get_audio_data()
        else:
            print("语音合成任务响应状态异常，请重新发送请求！")

if __name__ == '__main__':
    output_box = "这道题怎么做？"
    tts_service(output_box)
