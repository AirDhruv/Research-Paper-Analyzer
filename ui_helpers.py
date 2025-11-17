import streamlit as st
from io import BytesIO

def render_summary(summary_text: str):
    st.header("AI-generated Summary")
    st.text_area("Summary", value=summary_text, height=400)


def download_button(text: str, filename: str = "summary.txt"):
    b = text.encode("utf-8")
    st.download_button("Download summary", data=b, file_name=filename, mime="text/plain")