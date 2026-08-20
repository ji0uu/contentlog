from prompt import analyze_review

# 테스트 케이스 
test_cases = [
    {"title": "프로젝트 헤일메리", "category": "영화", "rating": 5, "emoji": "🥹", "review": "우주 장면들이 너무 압도적이었고, 스토리가 정말 감동적이었다."},
    {"title": "르네상스", "category": "전시", "rating": 4, "emoji": "🤩", "review": "인터넷으로만 보던 작품들을 실제로 볼 수 있어 좋았지만, 동선이 살짝 아쉬웠음"},
    {"title": "The Central Tour", "category": "공연", "rating": 5, "emoji": "😍", "review": "연주, 조명, 무대, 노래, 분위기 모두 최고"},
    {"title": "노이모션", "category": "책", "rating": 3, "emoji": "😐", "review": "많은 생각이 들게 하는 책"},
    {"title": "스물다섯 스물하나", "category": "드라마", "rating": 2, "emoji": "😌", "review": "내용이 전반적으로 따뜻했지만 엔딩이 아쉽다"}
]

for case in test_cases:
    result = analyze_review(case["title"], case["category"], case["rating"], case["emoji"], case["review"])
    print(f"[{case['title']}]")
    print(result)

