import streamlit as st
import pandas as pd
from charts import show_basic_stats, show_category_satisfaction, show_emotion_pie, show_emotion_trend, show_highlight_type, show_weekday_pattern, show_time_pattern, show_weekday_time_heatmap

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