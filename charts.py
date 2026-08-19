import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud
from datetime import datetime
from collections import Counter



# 여러 색이 필요한 곳(카테고리 비교, 파이차트 등)에 쓸 팔레트
COLOR_PALETTE = [
    "#E9A6B2",  # 로즈
    "#9A96B5",  # 모브
    "#B8AAD6",  # 라벤더
    "#91BDB8",  # 세이지 민트
    "#E3B184",  # 피치
    "#A9C7B0",  # 세이지
    "#D8B4A0"
]
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
    st.markdown(
    """
    <style>
    div[data-testid="stProgress"] > div > div > div {
        background-color: #E9A6B2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    st.progress(achieve_rate / 100)

# 카테고리별 만족도
def show_category_satisfaction(df):
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
        color="category",
        color_discrete_sequence=COLOR_PALETTE
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
        "흥미진진": "🤩"
    }

    emotion_counts["emoji_label"] = emotion_counts["emotion_category"].map(category_to_emoji)

    fig = px.pie(
        emotion_counts, 
        names="emoji_label",   # 이모지를 라벨로 사용
        values="count",
        hole=0.4,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(
        textposition="inside",
        textinfo="label",
        textfont_size=20
    )
    fig.update_layout(height=350)

    st.plotly_chart(fig, use_container_width=True)

# 만족 포인트 유형 분석
def show_highlight_type(df):
    st.subheader("나의 만족 포인트")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    highlight_counts = df["highlight_type"].value_counts().reset_index()
    highlight_counts.columns = ["highlight_type", "count"]
    highlight_counts = highlight_counts.sort_values(by='count', ascending=False)

    fig = px.bar(
        highlight_counts, 
        x="highlight_type", 
        y="count",
        labels={"highlight_type": "만족 포인트", "count": "횟수"},
        color="highlight_type",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(height=350)
    fig.update_traces(width=0.4) # 막대 두께 조정

    st.plotly_chart(fig, use_container_width=True)

# 누적 감상 개수 추이
def show_total_count(df):
    st.subheader("누적 감상 개수")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    df['date'] = pd.to_datetime(df['date'])
    df_sorted = df.sort_values('date').reset_index(drop=True)
    df_sorted['total_count'] = range(1, len(df_sorted)+1)

    fig = px.line(
        df_sorted, x='date', y='total_count',
        labels={'date': '날짜', 'total_count': '누적 개수'}, 
        markers=True,
        color_discrete_sequence=["#91BDB8"]
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# 감정 점수 vs 별점 
def show_emotion_rating(df):
    st.subheader("별점 vs AI 감정 점수 비교")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    df['date'] = pd.to_datetime(df['date'])
    df_sorted = df.sort_values(by='date')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted['date'], y=df_sorted['rating'],
        name='내 별점', mode='lines+markers',
        line=dict(color="#E9A6B2", width=3),
        marker=dict(color="#E9A6B2")
    ))
    fig.add_trace(go.Scatter(
        x=df_sorted['date'], y=df_sorted['emotion_score'],
        name='AI 감정점수', mode='lines+markers',
         line=dict(color="#9A96B5", width=3),
        marker=dict(color="#9A96B5")
    ))
    fig.update_layout(height=350, yaxis_range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)

# 요일별 감상 패턴
def show_weekday_pattern(df):
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name()  # 요일 이름 추출
    weekday_map = {
        "Monday": "월", "Tuesday": "화", "Wednesday": "수", "Thursday": "목",
        "Friday": "금", "Saturday": "토", "Sunday": "일"
    }
    df["weekday_kr"] = df["weekday"].map(weekday_map)
    weekday_order = ["월", "화", "수", "목", "금", "토", "일"]
    
    weekday_counts = df["weekday_kr"].value_counts().reindex(weekday_order, fill_value=0).reset_index()
    weekday_counts.columns = ["weekday", "count"]

    fig = px.bar(
        weekday_counts, 
        x="weekday", 
        y="count",
        color_discrete_sequence=["#B8AAD6"]
    )
    fig.update_layout(height=300)
    return fig # 두 그래프 나란히 배치 위해 그래프 객체만 반환

# 시간대별 감상 패턴
def show_time_pattern(df):
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.hour  # 시간 추출

    def get_time_period(hour):
        if 0 <= hour < 6: return "새벽 (0-6시)"
        elif 6 <= hour < 12: return "아침 (6-12시)"
        elif 12 <= hour < 18: return "오후 (12-18시)"
        else: return "저녁 (18-24시)"

    df['time_period'] = df['hour'].apply(get_time_period)
    period_order = ["새벽 (0-6시)", "아침 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)"]

    period_counts = df['time_period'].value_counts().reindex(period_order, fill_value=0).reset_index()
    period_counts.columns = ['time_period', 'count']

    fig = px.bar(
        period_counts, 
        x="time_period", 
        y="count",
        color_discrete_sequence=["#91BDB8"]
    )
    fig.update_layout(height=300)
    return fig # 두 그래프 나란히 배치 위해 그래프 객체만 반환

def show_weekday_time_heatmap(df):
    st.subheader("요일 x 시간대 감상 패턴")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.day_name().map({
        "Monday": "월", "Tuesday": "화", "Wednesday": "수", "Thursday": "목",
        "Friday": "금", "Saturday": "토", "Sunday": "일"
    })
    df['hour'] = df['date'].dt.hour
    df['time_period'] = df['hour'].apply(lambda h: "새벽 (0-6시)" if 0 <= h < 6 else
                                         "아침 (6-12시)" if 6 <= h < 12 else
                                         "오후 (12-18시)" if 12 <= h < 18 else
                                         "저녁 (18-24시)")

    weekday_order = ["월", "화", "수", "목", "금", "토", "일"]
    period_order = ["새벽 (0-6시)", "아침 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)"]

    #pivot table 생성
    pivot = df.pivot_table(index='weekday', columns='time_period', values='title',aggfunc='size', fill_value=0)
    pivot = pivot.reindex(index=weekday_order, columns=period_order, fill_value=0)

    fig = px.imshow(
        pivot,
        labels=dict(x="시간대", y="요일", color="감상 수"),
        x=period_order,
        y=weekday_order,
        text_auto=True,
        color_continuous_scale= [
        [0, "#F6F6F6"],
        [0.5, "#F1DDE2"],
        [1, "#E9A6B2"]
    ]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# 워드클라우드
def show_wordcloud(df):
    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    all_keywords = df['keywords'].dropna().tolist()
    text = ' '.join(all_keywords).replace(',', ' ')

    if not text.strip():
        st.info("아직 키워드가 없어요")
        return

    wc = WordCloud(
        font_path = "malgun.ttf",  # 한글 폰트 경로 설정 필요
        background_color='white',
        width=600,
        height=300
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    return fig

# 가장 많이 언급된 키워드 랭킹
def show_top_keywords(df):
    if len(df) == 0:
        return None

    all_keywords = df["keywords"].dropna().tolist()
    keyword_list = []
    for k in all_keywords:
        keyword_list.extend([kw.strip() for kw in k.split(",")])

    if not keyword_list:
        return None

    top5 = Counter(keyword_list).most_common(5)
    return top5

# 인생작 top3
def show_top3_favorites(df):
    st.subheader("나의 인생작 Top3")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    top3 = df.sort_values("rating", ascending=False).head(3).reset_index(drop=True)

    medals = ["🥇", "🥈", "🥉"]
    
    cols = st.columns(3)
    for i, row in top3.iterrows():
        with cols[i]:
            st.markdown(f"<h2 style='text-align: center;'>{medals[i]}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{row['title']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{row['category']} · {'⭐' * int(row['rating'])}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #8785A2;'>{row['summary']}</p>", unsafe_allow_html=True)

# 카테고리 간 만족 포인트 비교

def show_category_radar(df):
    st.subheader("카테고리별 만족 포인트 비교")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    # 카테고리 x highlight_type 교차 집계
    cross = df.groupby(["category", "highlight_type"]).size().reset_index(name="count")

    # 가장 많이 본 카테고리 순으로 상위 2~3개
    top_categories = df["category"].value_counts().index.tolist()
    default_categories = top_categories[:3] # 상위 3개 기본값 자동 설정

    selected = st.multiselect(
        "비교할 카테고리 선택",
        options=top_categories, # 선택 가능한 전체 목록
        default=default_categories # 기본값
    )

    if not selected:
        st.info("카테고리를 하나 이상 선택해주세요")
        return

    fig = go.Figure()
    for i, cat in enumerate(selected):
        cat_data = cross[cross['category'] == cat]
        fig.add_trace(go.Scatterpolar(
            r=cat_data['count'],
            theta=cat_data['highlight_type'],
            fill='toself',
            name=cat,
            line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)])
        ))

    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# 상관관계
# 후기 글자수 - 별점
def show_length_rating(df):
    st.subheader("후기 글자수와 별점의 관계")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    df['review_length'] = df['review'].str.len()

    fig = px.scatter(
        df,
        x='review_length',
        y='rating',
        labels={'review_length': '후기 글자수',
                'rating': '별점'},
        hover_data=['title'], #마우스 올리면 제목도 보이게,-
        color_discrete_sequence=["#E3B184"]
    )
    fig.update_layout(height=350, yaxis_range=[0,5.5])
    st.plotly_chart(fig, use_container_width=True)

def show_time_satisfaction(df):
    st.subheader("시간대별 평균 만족도")

    if len(df) == 0:
        st.info("아직 기록이 없어요")
        return

    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.hour
    df['time_period'] = df['hour'].apply(lambda h: "새벽" if h < 6 
                                         else "아침" if h < 12 
                                         else "오후" if h < 18 else "저녁")
    period_order = ['새벽', '아침', '오후', '저녁']

    time_avg = df.groupby('time_period')['rating'].mean().reindex(period_order).reset_index()

    fig = px.bar(time_avg, x="time_period", y="rating", text_auto=".1f", color_discrete_sequence=["#A9C7B0"])
    fig.update_layout(height=350, yaxis_range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)