import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

system_prompt = """
너는 콘텐츠 감상 후기를 분석하는 프로그램이야.
아래 정보를 바탕으로 반드시 JSON 형식으로만 답해.

출력 형식:
{
  "emotion_score": "1~5 사이 정수 (유저가 입력한 별점을 우선적으로 참고하고, 후기 텍스트로 세부 조정)",
  "emotion_category": "재밌음/감동/힐링/슬픔/지루함/그럭저럭/흥미진진 중 하나 (유저가 선택한 이모지를 우선적으로 참고하고, 후기 텍스트로 세부 조정)",
  "highlight_type": "주제/스토리/연출/연기/음악/분위기 중 해당되는 것",
  "keywords": ["키워드1", "키워드2"] (정확히 2~3개, 각 키워드는 최대한 한 단어로),
  "summary": "한 문장 요약"
}
"""

emoji_meaning = {
    "😍" : "재밌음", 
    "🥹" : "감동",
    "😌" : "힐링",
    "😢" : "슬픔",
    "😑" : "지루함",
    "😐" : "그럭저럭",
    "🤩" : "몰입/흥미진진"
}

categories = ["영화", "드라마", "책", "공연", "전시", "기타"]

# 테스트 케이스 
test_cases = [
    {"title": "프로젝트 헤일메리", "category": "영화", "rating": 5, "emoji": "🥹", "review": "우주 장면들이 너무 압도적이었고, 스토리가 정말 감동적이었다."},
    {"title": "르네상스", "category": "전시", "rating": 4, "emoji": "🤩", "review": "인터넷으로만 보던 작품들을 실제로 볼 수 있어 좋았지만, 동선이 살짝 아쉬웠음"},
    {"title": "The Central Tour", "category": "공연", "rating": 5, "emoji": "😍", "review": "연주, 조명, 무대, 노래, 분위기 모두 최고"},
    {"title": "노이모션", "category": "책", "rating": 3, "emoji": "😐", "review": "많은 생각이 들게 하는 책"},
    {"title": "스물다섯 스물하나", "category": "드라마", "rating": 2, "emoji": "😌", "review": "내용이 전반적으로 따뜻했지만 엔딩이 아쉽다"}
]

for case in test_cases:
    user_input = f"""
제목: {case['title']}
카테고리: {case['category']}
별점: {case['rating']}/5
이모지: {emoji_meaning.get(case['emoji'], "알 수 없음")}
후기: {case['review']}
""" # 나중에 기본 선택되는 이모지 정해도 좋을 듯

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=system_prompt + "\n" + user_input,
        config={"response_mime_type": "application/json"}
    )

    try:
        result = json.loads(response.text)
        print(f"[{case['title']}]")
        print(result)
        print("-" * 40)
    except json.JSONDecodeError:
        print(f"[{case['title']}] 파싱 실패:", response.text)

