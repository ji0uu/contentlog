import streamlit as st
import pandas as pd

def show_all_records(df, user_id):
    st.subheader("나의 전체 기록")
    my_df = df[df['id'] == user_id].sort_values(by='date', ascending=False)

    if my_df.empty:
        st.info("아직 기록이 없어요")
        return

    for _, row in my_df.iterrows():
        with st.expander(f"**{row['title']}** | ({row['category']}) | {row['emoji']} | {row['date']}"):
            col1, col2 = st.columns(2)
            with col1:
                star_display = "⭐" * int(row['rating'])
                st.write(f"**별점** | {star_display}({row['rating']}/5)")
            with col2:
                st.write(f"**감정** | {row['emotion_category']}")

            st.write(f"**후기** | {row['review']}")

            keywords_list = row['keywords'].split(", ")
            hashtags = ' '.join([f"#{keyword}" for keyword in keywords_list])

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**만족 포인트** | {row['highlight_type']}")
            with col2:
                st.write(f"**키워드** | {hashtags}")
            st.write(f"**한줄 요약** | {row['summary']}")
