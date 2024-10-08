import os
import yaml
import dashscope
from os import PathLike
from dashscope.audio.asr import (Recognition, RecognitionCallback)

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)  # 安全地加载 YAML 文件
    return config

config = load_config(os.getcwd() + '\\config.yml')
dashscope.api_key = config['api_key']['asr_key']

# 重构RecognitionCallback，需要可解开注释
# class Callback(RecognitionCallback):
#     # 识别完成
#     def on_complete(self) -> None:
#         print("识别完成！")
#
#     # 错误处理
#     def on_error(self, result: RecognitionResult) -> None:
#         print("识别出错，请重新识别！")
#
#     # 处理识别结果
#     def on_event(self, result: RecognitionResult) -> None:
#         print(result['output']['sentence'][0]['text'])

def asr_service(audio:PathLike):
    callback = RecognitionCallback()
    recognition = Recognition(model='paraformer-realtime-v2',
                              format='wav',
                              sample_rate=48000,
                              callback=callback)

    if audio is not None:
        result = recognition.call(audio)

        if result['status_code'] == 200:
            return result['output']['sentence'][0]['text']
        else:
            print("语音识别任务响应状态异常，请重新发送请求！")

if __name__ == '__main__':
    audio_path = "E:\\PythonProjects\\photo_answer_agent\\test_data\\test.wav"
    print(asr_service(audio_path))