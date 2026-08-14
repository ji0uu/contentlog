import streamlit as st
import pandas as pd
from charts import (
    show_basic_stats, show_category_satisfaction, 
    show_emotion_pie, show_emotion_trend, show_highlight_type, 
    show_weekday_pattern, show_time_pattern, show_weekday_time_heatmap, 
    show_wordcloud, show_top_keywords)

st.title("나의 콘텐츠 감상 기록 대시보드")

# 더미 데이터 불러오기
df = pd.read_csv("dummy_content_data.csv")

show_basic_stats(df)
show_category_satisfaction(df)
show_emotion_pie(df)
show_highlight_type(df)
show_emotion_trend(df)

# 요일별/시간대별 나란히 배치
st.subheader("요일별/시간대별 감상 기록")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(show_weekday_pattern(df), use_container_width=True)
with col2:
    st.plotly_chart(show_time_pattern(df), use_container_width=True)

show_weekday_time_heatmap(df)

font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 한글 폰트 경로
st.subheader("키워드 분석")
col1, col2 = st.columns(2)
with col1:
    wc_fig = show_wordcloud(df)
    if wc_fig:
        st.pyplot(wc_fig)
    else:
        st.info("아직 키워드가 없어요")
with col2:
    st.markdown("**가장 많이 언급된 키워드**")
    top5 = show_top_keywords(df)
    if top5:
        for i, (keyword, count) in enumerate(top5, start=1):
            st.write(f"{i}. {keyword} ({count}회)")
    else:
        st.info("아직 키워드가 없어요")