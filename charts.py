import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 기본 통계형
def show_basic_stats(df):
    st.subheader("이번 달 요약")
    df['date'] = pd.to_datetime(df['date'])
    this_month = datetime.now().month
    this_year = datetime.now().year
    this_month_df = df[(df['date'].dt.month == this_month) & (df['date'].dt.year == this_year)]

    # 총 감상 수, 평균 별점, 가장 많이 본 카테고리 계산
    total_count = len(this_month_df)
    avg_rating = this_month_df['rating'].mean() if total_count > 0 else 0
    most_watched_category = this_month_df['category'].mode()[0] if total_count > 0 else '-'

    # 목표 달성률 계산
    goal = 10 # 고정값
    achieve_rate = min(total_count / goal, 1) * 100


    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("**이번 달 감상한 콘텐츠 수**", f"{total_count}개")
    with col2:
        st.metric("**이번 달 평균 별점**", f"{avg_rating:.1f}점")
    with col3:
        st.metric("**이번 달 가장 많이 본 카테고리**", most_watched_category)

    st.markdown(f"**이번 달 목표 달성률:** {achieve_rate:.0f}%, ({total_count}/{goal})")
    st.progress(achieve_rate / 100)

# 카테고리별 만족도
def show_category_satisfacation(df):
    st.subheader("카테고리별 만족도")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    category_avg_rating = df.groupby('category')['rating'].mean().reset_index()
    category_avg_rating = category_avg_rating.sort_values(by='rating', ascending=False)

    fig = px.bar(
        category_avg_rating, 
        x="category", 
        y="rating",
        labels={"category": "카테고리", "rating": "평균 별점"},
    )
    fig.update_layout(
        yaxis_range=[0, 5],# 별점이 1~5점이니 y축 고정
        height=350
    )
    fig.update_traces(width=0.4) # 막대 두께 조정

    st.plotly_chart(fig, use_container_width=True)

# 감정 분포
def show_emotion_pie(df):
    st.subheader("감정 분포")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    emotion_counts = df["emotion_category"].value_counts().reset_index()
    emotion_counts.columns = ["emotion_category", "count"]

    # 감정 텍스트 → 이모지로 매핑 (emoji_meaning의 반대 방향)
    category_to_emoji = {
        "재밌음": "😍",
        "감동": "🥹",
        "힐링": "😌",
        "슬픔": "😢",
        "지루함": "😑",
        "그럭저럭": "😐",
        "몰입/흥미진진": "🤩"
    }

    emotion_counts["emoji_label"] = emotion_counts["emotion_category"].map(category_to_emoji)

    fig = px.pie(
        emotion_counts, 
        names="emoji_label",   # 이모지를 라벨로 사용
        values="count",
        hole=0.4
    )
    fig.update_traces(
        textposition="inside",
        textinfo="label",
        textfont_size=20
    )
    fig.update_layout(height=350)

    st.plotly_chart(fig, use_container_width=True)