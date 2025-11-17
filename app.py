import streamlit as st
import os
from dotenv import load_dotenv
from ai_client import AIClient
from pdf_utils import extract_text_from_pdf, chunk_text
from prompts import SUMMARY_PROMPT_TEMPLATE

# Load .env
load_dotenv()

# Initialize AI client
client = AIClient()

# Streamlit page config
st.set_page_config(
    page_title="Research Paper Analyzer",
    layout="wide",
    page_icon="📄"
)

# Custom CSS for nicer UI
st.markdown("""
<style>
.summary-box {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    color: #000;
    font-size: 16px;
    line-height: 1.6;
}
.header-title {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: -10px;
}
.sub-header {
    font-size: 18px;
    color: #555;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# --- HEADER ---
st.markdown("<div class='header-title'>📄 Research Paper Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Upload any research paper PDF and generate a structured AI-powered summary.</div>", unsafe_allow_html=True)

st.write("---")

# --- LAYOUT ---
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("Upload PDF")
    uploaded_file = st.file_uploader("Upload your file here", type=["pdf"])

    max_tokens = int(os.getenv("MAX_CHUNK_TOKENS", 3000))
    overlap = int(os.getenv("CHUNK_OVERLAP", 200))


with right_col:
    st.subheader("Summary Output")

    if uploaded_file:
        with st.spinner("📄 Extracting text from PDF..."):
            raw_text = extract_text_from_pdf(uploaded_file)

        if not raw_text or not raw_text.strip():
            st.error("No extractable text found. This PDF may be scanned or contain unrecognized text.")
        else:
            chunks = chunk_text(raw_text, max_tokens=max_tokens, overlap=overlap)
            st.success(f"Extracted text successfully! Split into {len(chunks)} chunk(s).")

            with st.expander("🔍 View Extracted Text Chunks"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk[:1200] + " ...")

            if st.button("Generate Summary", type="primary"):
                summaries = []
                progress = st.progress(0)

                for i, chunk in enumerate(chunks):
                    prompt = SUMMARY_PROMPT_TEMPLATE.format(paper_text=chunk)
                    resp = client.summarize(prompt)
                    summaries.append(resp.strip())
                    progress.progress((i+1) / len(chunks))

                # Merge summaries
                merged_prompt = SUMMARY_PROMPT_TEMPLATE.format(
                    paper_text="\n\n".join(summaries)
                )
                final_summary = client.summarize(merged_prompt)

                # Display in styled container
                st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                st.markdown(final_summary)
                st.markdown("</div>", unsafe_allow_html=True)

                # Download button
                st.download_button(
                    label="⬇ Download Summary",
                    data=final_summary,
                    file_name="research_summary.txt",
                    mime="text/plain"
                )
    else:
        st.info("Upload a research PDF to begin.")


