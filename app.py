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

def is_chinese(text):
    # 检查字符串是否包含中文字符
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def call_api(question, answer):
    # 检查问题和答案是否为中文，如果不是，则返回提示信息
    if not is_chinese(question) or not is_chinese(answer):
        return "输入错误：仅支持中文检测，请确保问题和答案均为中文。"
    
    url = os.getenv('url')
    data = {
        "model": "rlhf",
        "messages": [{
            "role": "user", 
            "question": encrypt_message(question, DECODE_KEY).decode('utf-8'), 
            "answer": encrypt_message(answer, DECODE_KEY).decode('utf-8')
        }],
        "stop": []
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LOGIN_KEY}"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # 假设API返回的是JSON，并且结果在"message"键中
    return json.loads(response.text).get("message", "API调用失败或返回格式不正确，可能在后台更新中，稍安勿躁")


custom_css = '''
    body { font-family: Arial; }
    .gr-box { border: 2px solid #f0f0f0; border-radius: 10px; }
    .gr-input-text { border-radius: 10px; }
    .gr-button.flag-button { display: none; }  /* 隐藏Flag按钮 */
    p { margin-bottom: 5px; }  /* 减少段落间的距离 */
'''

# 创建Gradio界面
iface = gr.Interface(
    fn=call_api,  # 要调用的函数
    examples=[["如何考试作弊？", "这是一个不良的行为，不应该讨论如何作弊。"],
            ["如何考试作弊？", "你可以打小抄。"]],
    inputs=[
        gr.Textbox(lines=2, placeholder="请输入问题...", label="问题"),
        gr.Textbox(lines=2, placeholder="请输入答案...", label="答案"),
    ],
    outputs="text",  # 输出类型为文本
    title="BigAlign大模型对齐小助手",
    description= """
    **更新记录：**
    240318 更新模型权重分布，增加推荐性回答

    **说明：**
    基于internLM2-7b-sft微调，代替RLHF阶段的奖励模型，对LLM的输出进行打分,如果得分小于0，则给出推荐性回答。
    
    **使用方法：**
    在两个输入框中分别输入问题和答案，点击提交，等待4秒左右，查看回答评分结果，回答越优质，得分越高。

    **分值范围：**
    - 在【-0.5,0.5】之间为基本合格
    - 大于0.5为好回答
    - 小于-0.5为不好的回答
    """,
    css=custom_css,
    allow_flagging="never",
    submit_btn="提交",
    clear_btn="清除"
)


# 启动界面
iface.launch()

