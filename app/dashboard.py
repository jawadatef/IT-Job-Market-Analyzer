from pathlib import Path
import sys

import pandas as pd
import streamlit as st
from dotenv import dotenv_values

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.job_qa import answer_job_question
st.set_page_config(page_title="IT Job Market Analyzer", layout="wide")


@st.cache_data
def load_jobs():
    return pd.read_pickle(project_root / "data" / "processed" / "it_jobs.pkl")


jobs = load_jobs()
titles = sorted(jobs["title"].dropna().unique())

st.title("IT Job Market Analyzer")
st.header("Market overview")
st.caption("LinkedIn IT job postings · 2023–2024")

category_counts = (
    jobs.groupby("category")["job_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("Job postings")
)

left, middle, right = st.columns(3)
left.metric("Job postings", f"{jobs['job_id'].nunique():,}")
middle.metric("IT fields", len(category_counts))
right.metric("Largest field", category_counts.idxmax())

st.subheader("Job postings by field")
import altair as alt

chart_data = category_counts.reset_index()

chart = alt.Chart(chart_data).mark_bar().encode(
    y=alt.Y(
        "category:N",
        sort="-x",
        title=None,
        axis=alt.Axis(labelLimit=220),
    ),
    x=alt.X(
        "Job postings:Q",
        title="Number of job postings",
        scale=alt.Scale(zero=True),
    ),
    tooltip=["category:N", "Job postings:Q"],
)

st.altair_chart(chart, use_container_width=True)

st.divider()
st.header("اسأل عن وظيفة")

with st.form("job_question"):
    selected_title = st.selectbox("اختار المسمّى الوظيفي", titles)
    question = st.text_input(
        "شو حاب تعرف عن الوظيفة؟",
        placeholder="مثال: شو المهارات المطلوبة؟ وهل الإعلانات بتذكر Docker؟",
    )
    submitted = st.form_submit_button("اعرض الجواب")


def find_jobs_by_title(_question):
    matches = jobs.loc[jobs["title"] == selected_title]
    return matches.dropna(subset=["description"]).drop_duplicates("description").head(3)


if submitted:
    if question.strip():
        api_key = dotenv_values(project_root / ".env").get("GEMINI_API_KEY")
        with st.spinner("جاري قراءة الإعلانات..."):
            answer, sources = answer_job_question(
                question.strip(), find_jobs_by_title, api_key
            )

        st.markdown(answer)
        if not sources.empty:
            st.subheader("الإعلانات المستخدمة")
            st.dataframe(sources[["job_id", "title"]], hide_index=True)
    else:
        st.info("اكتب سؤالك أول.")