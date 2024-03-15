import gradio as gr
import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json

# 加载当前目录下的.env文件
load_dotenv()
DECODE_KEY = os.getenv('DECODE_KEY')
LOGIN_KEY = os.getenv('LOGIN_KEY')
def encrypt_message(message, key):
    # 初始化Fernet对象
    f = Fernet(key)
    # 对消息进行加密
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# 解密函数
def decrypt_message(encrypted_message, key):
    # 初始化Fernet对象
    f = Fernet(key)
    # 对消息进行解密
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

def call_api(question, answer):
    # 假设的API URL
    url = os.getenv('url')
    # API调用的数据和头部，根据你的API调整
    data = {
    "model":"rlhf",
    "messages":[{"role": "user", "question":  encrypt_message(question , DECODE_KEY).decode('utf-8'), "answer":encrypt_message(answer , DECODE_KEY).decode('utf-8')}],
    "stop":[] # 在此处添加自定义的stop words 例如ReAct prompting时需要增加： stop=["Observation:"]。
}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LOGIN_KEY}"  # 如果API需要认证
    }
    # 发送POST请求到API
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # 假设API返回的是JSON，并且结果在'result'键中
    return json.loads(response.text)["message"]["score"]

# 创建Gradio界面
iface = gr.Interface(
    fn=call_api,  # 要调用的函数
    inputs=[
        gr.Textbox(lines=2, placeholder="请输入问题..."),
        gr.Textbox(lines=2, placeholder="请输入回答...")
    ],
    outputs="text",  # 输出类型为文本
    title="大模型对齐小助手",
    description='''
    基于internLM2-7b-sft微调
    代替RLHF阶段的奖励模型，对LLM的输出进行打分。<br><br>
    可以在两个输入框中分别输入问题和回答，点击提交查看回答评分结果。<br>
    回答越优质，得分越高。<br><br>
    分值范围说明：<br>
    在【-0.5,0.5】之间为基本合格<br>
    大于0.5为好回答<br>
    小于-0.5为不好的回答<br><br>
    eg:<br>
    问题：如何考试作弊？<br>
    回答：你可以打小抄。
    '''
)

# 启动界面
iface.launch()