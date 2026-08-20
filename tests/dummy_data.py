import pandas as pd

dummy_data = pd.DataFrame([
    {"date": "2026-08-01", "title": "인터스텔라", "category": "영화", "rating": 5,
     "emoji": "🥹", "review": "우주 배경음악이 압도적이었다",
     "emotion_score": 5, "emotion_category": "감동",
     "keywords": "우주, 감동, 영상미", "summary": "압도적인 영상미와 감동적인 스토리",
     "highlight_type": "스토리"},
    
    {"date": "2026-08-03", "title": "무빙", "category": "드라마", "rating": 5,
     "emoji": "😍", "review": "액션신이 몰입감 넘쳤다",
     "emotion_score": 5, "emotion_category": "재밌음",
     "keywords": "액션, 몰입, 연기", "summary": "몰입감 넘치는 액션과 뛰어난 연기가 인상적",
     "highlight_type": "연기"},
    
    {"date": "2026-08-05", "title": "노이모션", "category": "책", "rating": 3,
     "emoji": "😐", "review": "생각을 많이 하게 만드는 책",
     "emotion_score": 3, "emotion_category": "그럭저럭",
     "keywords": "사색, 철학, 성찰", "summary": "깊은 고민을 불러일으키는 철학적인 책",
     "highlight_type": "주제"},
    
    {"date": "2026-08-07", "title": "The Central Tour", "category": "공연", "rating": 5,
     "emoji": "🤩", "review": "연주와 무대가 최고였다",
     "emotion_score": 5, "emotion_category": "흥미진진",
     "keywords": "연주, 무대, 분위기", "summary": "모든 요소가 완벽했던 공연",
     "highlight_type": "음악"},
    
    {"date": "2026-08-10", "title": "르네상스", "category": "전시", "rating": 4,
     "emoji": "😌", "review": "작품을 직접 보니 좋았다",
     "emotion_score": 4, "emotion_category": "힐링",
     "keywords": "명작, 감상, 여운", "summary": "직접 감상하는 즐거움이 컸던 전시",
     "highlight_type": "주제"},
])

dummy_data.to_csv("dummy_content_data.csv", index=False, encoding="utf-8-sig")
print("더미 데이터 생성 완료")