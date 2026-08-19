import streamlit as st
import pandas as pd
from charts import (
    show_total_count, show_basic_stats, show_category_satisfaction, 
    show_emotion_pie, show_emotion_rating, show_highlight_type, 
    show_weekday_pattern, show_time_pattern, show_weekday_time_heatmap, 
    show_wordcloud, show_top_keywords, show_top3_favorites,
    show_category_radar, show_length_rating, show_time_satisfaction)

def show_dashboard(df, user_id):
    my_df = df[df['id'] == user_id]  # 전체 대시보드 안에서 내 것만 필터링
    st.title("나의 콘텐츠 감상 기록 대시보드")



    show_basic_stats(my_df)
    show_category_satisfaction(my_df)
    show_emotion_pie(my_df)
    show_highlight_type(my_df)
    show_total_count(my_df)
    show_emotion_rating(my_df)

    # 요일별/시간대별 나란히 배치
    st.subheader("요일별/시간대별 감상 기록")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(show_weekday_pattern(my_df), use_container_width=True)
    with col2:
        st.plotly_chart(show_time_pattern(my_df), use_container_width=True)

    show_weekday_time_heatmap(my_df)

    font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 한글 폰트 경로
    st.subheader("키워드 분석")
    col1, col2 = st.columns(2)
    with col1:
        wc_fig = show_wordcloud(my_df)
        if wc_fig:
            st.pyplot(wc_fig)
        else:
            st.info("아직 키워드가 없어요")
    with col2:
        st.markdown("**가장 많이 언급된 키워드**")
        top5 = show_top_keywords(my_df)
        if top5:
            for i, (keyword, count) in enumerate(top5, start=1):
                st.write(f"{i}. {keyword} ({count}회)")
        else:
            st.info("아직 키워드가 없어요")

    show_top3_favorites(my_df)
    show_category_radar(my_df)

    st.subheader("상관관계 분석")
    col1, col2 = st.columns(2)
    with col1:
        show_length_rating(my_df)
    with col2:
        show_time_satisfaction(my_df)
