# 실습 : image to text
from ollama import chat

IMAGE_PATH = "imgs/img01.jpg"
MODEL_NAME = "qwen3.5:9b"

response = chat(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": """
이 이미지를 한국어로 설명해줘.

다음 형식으로 답변해줘.
1. 전체 장면
2. 주요 객체
3. 배경
4. 이미지에서 추론 가능한 상황
""",
            "images": [IMAGE_PATH],
        }
    ],
    think=False,
    stream=False,       #streaming으로 받으려면 True로 설정 스트리밍이란 한번에 대답이 뽝 나오는게 아니라 쭈르륵 나오게 하는거.
)

print(response.message.content)