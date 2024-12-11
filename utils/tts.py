from dotenv import load_dotenv
import os

load_dotenv()

import requests
import subprocess
import json
import time
def post_tts_job(text):
    kits_key=os.getenv('KITS_API_KEY')
    command = [
    "curl",
    "-X", "POST",
    "https://arpeggi.io/api/kits/v1/tts",
    "-H", f"Authorization: Bearer {kits_key}",
    "-F", "voiceModelId=1594934",
    "-F", f"inputTtsText={text}"
]    
    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    tts_job = json.loads(result.stdout)
    # url = "https://arpeggi.io/api/kits/v1/tts"

    # # 定义请求头
    # headers = {
    #     "Authorization": "Bearer FL9y918x.AxY1ckB8COMWUub7ScEB90t6",
    # }

    # # 定义请求体
    # data = {
    #     "Authorization": "Bearer FL9y918x.AxY1ckB8COMWUub7ScEB90t6",
    #     "voiceModelId": "1594934",
    #     "inputTtsText": f"{text}"
    # }

    # # 发送 POST 请求
    # response = requests.post(url, headers=headers, data=data)

    # 检查响应状态码
    # if response.status_code == 200:
    #     print("请求成功！")
    #     # 处理响应内容（例如保存音频文件）
    #     with open("output.wav", "wb") as f:
    #         f.write(response.content)
    #     print("音频文件已保存为 output.wav")
    # else:
    #     print(f"请求失败，状态码：{response.status_code}")
    #     print(f"错误信息：{response.text}")
    # tts_job = response.json()
    return tts_job
    
# {
#     "id": 1,
#     "createdAt": "2023-09-19 20:13:50.428000 +00:00",
#     "type": "tts",
#     "voiceModelId": 2,
#     "status": "running",
#     "jobStartTime": "2023-09-19 20:15:50.428000 +00:00",
#     "jobEndTime": null
# }

def fetch_job(id=None):
    if id:
        url = f"https://arpeggi.io/api/kits/v1/voice-conversions/{id}"
    else:
        url = "https://arpeggi.io/api/kits/v1/voice-conversions/?page=1"
    headers = {"Authorization": "Bearer Uk_A5J50.cg7j51IdE1tfQU2ou5NnwjOu"}

    response = requests.request("GET", url, headers=headers)
    tts_job = response.json()
    print(tts_job)
    print(response.text)

    return tts_job

import dashscope
from dashscope.audio.tts_v2 import *

def get_tts(text,filename,use_ali=False):
    if use_ali:
        # my API KEY HERE
        DASHSCOPE_API_KEY= os.getenv('DASHSCOPE_API_KEY')
        dashscope.api_key = DASHSCOPE_API_KEY

        model = "cosyvoice-v1"
        voice = "longxiaochun"


        synthesizer = SpeechSynthesizer(model=model, voice=voice)
        audio = synthesizer.call(text)
        print('requestId: ', synthesizer.get_last_request_id())
        with open(f'{filename}.mp3', 'wb') as f:
            f.write(audio)
        return audio
    else:
        res = post_tts_job(text=text)
        try:
            job_id = res['id']
            job_res = fetch_job(job_id)
            while job_res['status']!='success':
                time.sleep(1)
                job_res = fetch_job(job_id)
            fileurl = job_res['outputFileUrl']
            audio = requests.get(fileurl).content
            with open(f'{filename}.wav', 'wb') as f:
                f.write(audio)
            with open(f'{filename}.wav', 'rb') as f:
                audiobytes = f.read()
            return audiobytes
        except Exception as e:
            print(e)


# get_tts("please don't do that",'23213214')
# fetch_job('34957862')
