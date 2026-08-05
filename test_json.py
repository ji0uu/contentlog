import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

'''
# 1차 안정화
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="다음 문장의 감정을 분석해서 JSON으로만 답해. 형식: {\"emotion\": \"긍정/부정/중립\"}. 문장: 오늘 공연 진짜 좋았어",
    config={"response_mime_type": "application/json"}
)

try:
    result = json.loads(response.text)
    print(result)
except json.JSONDecodeError:
    print("파싱 실패:", response.text)
'''
# 2차 안정화 : 긍정/중립/부정 
test_sentences = [
    "오늘 공연 진짜 좋았어",
    "그냥 그랬어요",
    "완전 별로였음, 다시는 안 볼래"
]

for sentence in test_sentences:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"다음 문장의 감정을 분석해서 JSON으로만 답해. 형식: {{\"emotion\": \"긍정/부정/중립\"}}. 문장: {sentence}",
        config={"response_mime_type": "application/json"}
    )
    try:
        result = json.loads(response.text)
        print(sentence, "→", result)
    except json.JSONDecodeError:
        print(sentence, "→ 파싱 실패:", response.text)