import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import base64
from tqdm import tqdm

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 함수 정의: 이미지 파일을 base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

text_prompt="""
Compare the provided screenshots, which are variations of the same page for A/B test on UI, and identify major differences between them. The purple-colored sections are guides to help you focus on varying elements.
Based on these differences, analyze which version is likely to be more user-friendly and preferred by users, considering usability, design aesthetics, and functionality.
(Inner contents like specific products in shopping website or different example pictures can be different, focus on the overall design and layout)

Answer format should be as follows:
Difference)
1. <difference 1>
2. <difference 2>
...
User-friendly Choice) Screenshot <number>
Reason) <reasoning>

Answer:
Difference)
""".strip()

results = []

for folder in tqdm(os.listdir('data/goodui')):
    base64_image = encode_image(f'data/goodui/{folder}/concat.png')
        
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [
                {
                    "type": "text", 
                    "text": text_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content
    answer_num = answer.split('User-friendly Choice)')[1].split('\n')[0].strip('*()Screenshot ')

    results.append({'folder': folder, 'answer': answer, 'answer_num': answer_num})
    
    with open('gpt_results.json', 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)