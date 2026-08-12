import streamlit as st
import pandas as pd

def show_all_records(df, user_id):
    st.subheader("나의 전체 기록")
    my_df = df[df['user_id'] == user_id].sort_values(by='date', ascending=False)

    if my_df.empty:
        st.info("아직 기록이 없어요")
        return

    for _, row in my_df.iterrows():
        with st.expander(f"{row['title']} {row['emoji']} {row['date']}"):
            st.write(f"별점 | {row['rating']}/5")
            st.write(f"후기 | {row['review']}")
            st.write(f"한줄 요약 | {row['summary']}")


