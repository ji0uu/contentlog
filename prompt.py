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

def analyze_review(title, category, rating, emoji, review):
    user_input = f"""
제목: {title}
카테고리: {category}
별점: {rating}/5
이모지: {emoji_meaning.get(emoji, "알 수 없음")}
후기: {review}
"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=system_prompt + "\n" + user_input,
        config={"response_mime_type": "application/json"}
    )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"emotion_score": "", "emotion_category": "", "keywords": "", "summary": "", "highlight_type": ""}