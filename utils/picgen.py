from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis

model = "flux-schnell"
prompt = "Eagle flying freely in the blue sky and white clouds"
prompt_cn = "一只飞翔在蓝天白云的鹰"
import openai
import os
openai.api_key=os.getenv('OPENAI_API_KEY')

def sample_block_call_ali(input_prompt):
    print('Now generating images----')
    rsp = ImageSynthesis.call(model=model,
                              prompt=input_prompt,
                              size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
            return requests.get(result.url).content
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

def sample_block_call(input_prompt):
    print('正在生成图片----')
    try:
        # 调用 OpenAI 的 DALL-E 模型生成图片
        response = openai.images.generate(
            model="dall-e-3",
            quality="standard",
            prompt=input_prompt,
            n=1,
            size="1024x1024"
        )
        # print(response.text)
        # 获取生成的图片 URL
        image_url = response.data[0].url
        print(image_url)
        
        # 下载图片并保存到当前目录
        file_name = PurePosixPath(unquote(urlparse(image_url).path)).parts[-1]
        with open(f'./{file_name}', 'wb+') as f:
            f.write(requests.get(image_url).content)
        
        print(f'图片已保存为: {file_name}')
        return requests.get(image_url).content
    
    except Exception as e:
        print(f'Failed, error: {e}')


if __name__=='__main__':
    sample_block_call(prompt)