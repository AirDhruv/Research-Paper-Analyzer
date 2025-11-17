import os
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import extract_text_from_pdf, chunk_text
from ai_client import AIClient
from ui_helpers import render_summary, download_button
from prompts import SUMMARY_PROMPT_TEMPLATE


load_dotenv()

print("Loaded API KEY:", os.getenv("GOOGLE_API_KEY"))


API_KEY = os.getenv("GOOGLE_API_KEY")
client = AIClient()


st.set_page_config(page_title="Research Paper Analyzer", layout="wide")
st.title("Research Paper Analyzer")
st.write("Upload a PDF and get a concise, structured summary using an LLM.")


uploaded_file = st.file_uploader("Upload research paper (PDF)", type=["pdf"])


if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        raw_text = extract_text_from_pdf(uploaded_file)


    if not raw_text.strip():
        st.error("No extractable text found in PDF. Try a different file or scanned PDF (OCR not supported in this version).")
    else:
        max_tokens = int(os.getenv("MAX_CHUNK_TOKENS", 3000))
        overlap = int(os.getenv("CHUNK_OVERLAP", 200))
        chunks = chunk_text(raw_text, max_tokens=max_tokens, overlap=overlap)
        st.info(f"Extracted text and split into {len(chunks)} chunk(s) for summarization")
        
        if st.button("Generate Summary"):
            summaries = []
            progress = st.progress(0)
            for i, c in enumerate(chunks):
                prompt = SUMMARY_PROMPT_TEMPLATE.format(paper_text=c)
                resp = client.summarize(prompt)
                summaries.append(resp.strip())
                progress.progress((i + 1) / len(chunks))


            # Merge chunk summaries into final summary
            merged_prompt = SUMMARY_PROMPT_TEMPLATE.format(paper_text="\n\n".join(summaries))
            final_summary = client.summarize(merged_prompt)


            render_summary(final_summary)
            download_button(final_summary, "research_summary.txt")