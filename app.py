import streamlit as st
import pandas as pd
from datetime import datetime
import os
from prompt import analyze_review
from records import show_all_records
from dashboard import show_dashboard

tab1, tab2, tab3 = st.tabs(['메인','기록 보기','대시보드'])

CSV_FILE = "content_data.csv"

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "id", "date", "title", "category", "rating", "emoji", "review",
        "emotion_score", "emotion_category", "keywords", "summary", "highlight_type"
    ])
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

with tab1:
    st.markdown(
        """
        <div style="text-align: center; padding-bottom: 40px;">
            <div style="font-size: 42px; font-weight: bold;">
                contentlog
            </div>
            <div style="font-size: 15px; color: #777;">
                오늘 본 콘텐츠를 기록해보세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    CATEGORY_OPTIONS = ["영화", "드라마", "책", "공연", "전시","기타"]
    EMOJI_OPTIONS = ["😍(재밌음)", "🥹(감동)", "😢(슬픔)", "😑(지루함)", "😌(힐링)", "😐(그럭저럭)", "🤩(몰입/흥미진진)"]

    user_id = st.text_input("아이디")
    title = st.text_input("콘텐츠 제목")
    category = st.selectbox("카테고리", CATEGORY_OPTIONS)
    rating = st.feedback("stars")
    if rating is not None:
        rating = rating + 1  # 0~4로 나오는 걸 1~5로 변환
    else:
        rating = 0  # 아직 안 눌렀을 때
    emoji = st.radio("오늘의 감정", EMOJI_OPTIONS, horizontal=True)
    review = st.text_area("후기를 남겨주세요")

    def save_entry(user_id, title, category, rating, emoji, review, ai_result):
        df = pd.read_csv(CSV_FILE)
        keywords_str = ", ".join(ai_result["keywords"]) if ai_result["keywords"] else ""

        new_row = {
            "id": user_id,
            "date": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
            "title": title,
            "category": category,
            "rating": rating,
            "emoji": emoji,
            "review": review,
            "emotion_score": ai_result["emotion_score"],       
            "emotion_category": ai_result["emotion_category"],
            "keywords": keywords_str,
            "summary": ai_result["summary"],
            "highlight_type": ai_result["highlight_type"]
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])

    with col3:
        submit = st.button("제출")


    if submit:
        if user_id and title and review:
            with st.spinner("AI가 후기를 분석하고 있어요..."):
                ai_result = analyze_review(title, category, rating, emoji, review)
            
            if ai_result["emotion_score"] == "":
                st.error("분석에 실패했어요, 다시 시도해주세요")
            else:
                save_entry(user_id, title, category, rating, emoji, review, ai_result)
                st.success("저장되었습니다! ✅")
                
                star_display = "⭐" * rating
                today_str = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
                keywords_display = ", ".join(ai_result["keywords"]) 

                st.markdown(
                    f"""
                    <div style="display: flex; align-items: baseline; gap: 8px;">
                        <span style="font-size: 24px; font-weight: 700;">{title}</span>
                        <span style="font-size: 20px;">{emoji}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**아이디**: {user_id}")
                    st.markdown(f"**카테고리**: {category}")

                with col2:
                    st.markdown(f"**작성일**: {today_str}")
                    st.markdown(f"**별점**: {star_display} ({rating}/5)")

                st.markdown(f"""
                > {review}
                
                ---
                """)
                st.markdown("### AI 분석")
                st.markdown(f"""
                - **감정 점수**: {ai_result['emotion_score']}/5
                - **감정 카테고리**: {ai_result['emotion_category']}
                - **만족 포인트**: {ai_result['highlight_type']}
                - **키워드**: {keywords_display}
                - **요약**: {ai_result['summary']}
                """)
        else:
            st.warning("아이디와 제목과 후기는 꼭 입력해주세요!")

with tab2:
    df = pd.read_csv(CSV_FILE)
    if user_id:
        show_all_records(df, user_id)
    else:
        st.info("먼저 '메인' 탭에서 아이디를 입력해주세요!")    

with tab3:
    df = pd.read_csv(CSV_FILE)
    if user_id:
        show_dashboard(df, user_id)
    else:
        st.info("먼저 '메인' 탭에서 아이디를 입력해주세요!")