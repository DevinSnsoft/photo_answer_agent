import logging
import gradio as gr
from gradio.themes.builder_app import chatbot

from modules.asr.asr_service import asr_service
from modules.nlg.nlg_service import nlg_service
from modules.tts.tts_service import tts_service

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    filename='photo_answer_agent.log',
    filemode='a'
)

# 创建一个 StreamHandler，用于将日志输出到控制台，并指定编码
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# 创建一个 logger 对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# 创建一个 FileHandler，用于将日志输出到文件
file_handler = logging.FileHandler('photo_answer_agent.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

def asr_audio2text(audio):
    logger.info("进入语音识别，处理语音识别任务")
    if asr_service(audio) is not None:
        logger.info("语音识别任务正常运行")
        # logger.info("语音识别结果：", str(asr_service(audio)))
        return asr_service(audio)
    else:
        logger.debug("语音识别任务异常，请重新处理")

# def gpt4o_multimodal2text(text, image, history, past_key_values):
#     logger.info("进入gpt4o，处理多模态信息")
#         if nlg_service(text, image, history, past_key_values) is not None:
#             logger.info("多模态信息处理任务正常")
#             # logger.info("多模态信息处理结果为：", str(nlg_service(text, image)))
#             return nlg_service(text, image, history, past_key_values)
#         else:
#             logger.debug("多模态信息处理异常，请重新访问gpt4o")

def gpt4o_multimodal2text(text, image):
    logger.info("进入gpt4o，处理多模态信息")
    if nlg_service(text, image) is not None:
        logger.info("多模态信息处理任务正常")
        # logger.info("多模态信息处理结果为：", str(nlg_service(text, image)))
        return nlg_service(text, image)
    else:
        logger.debug("多模态信息处理异常，请重新访问gpt4o")

def tts_text2audio(gpt4o_response_info):
    logger.info("正在进入语音合成，马上为您处理语音合成任务！")
    if tts_service(gpt4o_response_info) is not None:
        logger.info("语音合成任务正常运行")
        return tts_service(gpt4o_response_info)
    else:
        logger.debug("语音合成异常，请重新处理")

examples = ["这道题怎么做？", "这道题怎么解答？", "这道题的解题步骤是？"]

with gr.Blocks(title="拍照解答智能体") as app:
    with gr.Row():
        with gr.Column():
            # chatbot = gr.Chatbot()
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="语音输入")
            text_input = gr.Textbox(label="文本输入")
            gr.Examples(examples=examples, inputs=text_input)
            image_input = gr.Image(type="filepath", label="图片输入")
            submit_btn = gr.Button("提交")
            gpt4o_response_chatbot = gr.Chatbot()
            # gpt4o_response_box = gr.Textbox(label="GPT-4o 响应")
            audio_output = gr.Audio(label="播放音频")

            # 添加历史记录功能
            history = gr.State([])
            past_key_values = gr.State(None)

        audio_input.change(fn=asr_audio2text, inputs=[audio_input], outputs=text_input)
        submit_btn.click(fn=gpt4o_multimodal2text, inputs=[text_input, image_input], outputs=gpt4o_response_chatbot)
        # submit_btn.click(fn=gpt4o_multimodal2text, inputs=[text_input, image_input, history, past_key_values],
        #                  outputs=[gpt4o_response_box, history, past_key_values], show_progress="full")
        gpt4o_response_chatbot.change(fn=tts_text2audio, inputs=[gpt4o_response_chatbot], outputs=audio_output)

app.launch(share=True)
