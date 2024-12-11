import requests

def post_tts_job(text):
    apikey='Uk_A5J50.cg7j51IdE1tfQU2ou5NnwjOu'
    url = "https://arpeggi.io/api/kits/v1/tts"
    data = {
    'voiceModelId':"1594934",
    'inputTtsText': text
    }
    headers = { 'Authorization': 'Bearer Uk_A5J50.cg7j51IdE1tfQU2ou5NnwjOu'}

    response = requests.post(url, data=data, headers=headers)
    tts_job = response.json()
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
        url = f"https://arpeggi.io/api/kits/v1/voice-conversions/:{id}"
    else:
        url = "https://arpeggi.io/api/kits/v1/voice-conversions/?page=1"
    headers = {"Authorization": "Bearer Uk_A5J50.cg7j51IdE1tfQU2ou5NnwjOu"}

    response = requests.request("GET", url, headers=headers)

    print(response.text)
# res = post_tts_job('please dont heart me')
# print(res)

# fetch_job()
import dashscope
from dashscope.audio.tts_v2 import *

def get_tts(text):


    # 将your-dashscope-api-key替换成您自己的API-KEY
    dashscope.api_key = "sk-82f954923e644f6080718aa38e1bba52"
    model = "cosyvoice-v1"
    voice = "longxiaochun"


    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call(text)
    print('requestId: ', synthesizer.get_last_request_id())
    with open('output.mp3', 'wb') as f:
        f.write(audio)
    return audio


get_tts("please don't do that")