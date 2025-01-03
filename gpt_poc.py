import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

img1 = 'test_data/leak017_imp.png'
img2 = 'test_data/leak022_rej.png'

# 함수 정의: 이미지 파일을 base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 이미지 인코딩
base64_image1 = encode_image(img1)
base64_image2 = encode_image(img2)

prompt = """
You are an expert analyzing user behavior using websites.
You are given two screenshots of variants for same website. Analyze the images and their differences. Then, choose the variant that users would have preferred more.
""".strip()
prompt = """
Explain the differences between the two images and choose the variant that users would have preferred more.
""".strip()
prompt = """
Explain the differences between two images.
""".strip()
        
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an expert analyzing user behavior using websites."},
        {"role": "user", "content": [
            {
                "type": "text", 
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image1}"}
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image2}"}
            }
        ]}
    ],
    temperature=0
)
print('Prompt:')
print(prompt)
print('Answer:')
print(response.choices[0].message.content)