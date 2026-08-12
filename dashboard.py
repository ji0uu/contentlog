import streamlit as st
import pandas as pd
from charts import show_basic_stats, show_category_satisfacation, show_emotion_pie

st.title("나의 콘텐츠 감상 기록 대시보드")

# 더미 데이터 불러오기
df = pd.read_csv("dummy_content_data.csv")

show_basic_stats(df)
show_category_satisfacation(df)
show_emotion_pie(df)