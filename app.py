# app.py
import streamlit as st
from dotenv import load_dotenv
import os
from ai_client import AIClient
from pdf_utils import extract_text_from_pdf, chunk_text
from prompts import BRIEF_SUMMARY_PROMPT, DETAILED_SUMMARY_PROMPT, EXAM_SUMMARY_PROMPT, RAG_ANSWER_PROMPT

# Load environment
load_dotenv()

st.set_page_config(page_title="Research Paper Assistant", layout="wide", page_icon="🧠")

# Sidebar controls (RAG/embeddings removed)
with st.sidebar:
    st.title("Controls")
    gen_model = st.selectbox(
        "Generation model",
        options=[
            "models/gemini-flash-latest",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro"
        ],
        index=0,
    )
    summary_mode = st.radio("Summarization mode", ("Brief", "Detailed", "Exam-Oriented"))
    chunk_size = st.number_input(
        "Chunk token proxy (words)", min_value=300, max_value=10000, value=int(os.getenv("MAX_CHUNK_TOKENS", 3000))
    )
    overlap = st.number_input("Chunk overlap (words)", min_value=0, max_value=2000, value=int(os.getenv("CHUNK_OVERLAP", 200)))
    st.markdown("---")
    st.info("Chat uses a fast keyword-based retrieval over document chunks (no embeddings).")

# Apply selected model to environment for AI client
os.environ["GEN_MODEL"] = gen_model
client = AIClient()

# Page layout
st.title("Research Paper Assistant")
st.write("Upload a research PDF, generate summaries, or ask questions about the document.")

left, right = st.columns([1, 2])

# Shared state variables
document_chunks = []  # will hold chunks for retrieval/summarization
raw_text = ""

with left:
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting text..."):
            raw_text = extract_text_from_pdf(uploaded_file)
        if not raw_text or not raw_text.strip():
            st.error("No extractable text found. This PDF may be scanned or need OCR.")
            raw_text = ""
            document_chunks = []
        else:
            st.success("Text extracted.")
            document_chunks = chunk_text(raw_text, max_tokens=int(chunk_size), overlap=int(overlap))
            st.write(f"Document split into {len(document_chunks)} chunk(s).")

            if st.checkbox("Show chunk previews"):
                for i, c in enumerate(document_chunks):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(c[:600] + ("..." if len(c) > 600 else ""))

with right:
    st.subheader("Summarize / Chat")

    # Summarization
    if uploaded_file and raw_text:
        if st.button("Generate Summary"):
            st.info("Generating summary. This may take time depending on model and document size.")
            # choose prompt template
            if summary_mode == "Brief":
                prompt_template = BRIEF_SUMMARY_PROMPT
            elif summary_mode == "Detailed":
                prompt_template = DETAILED_SUMMARY_PROMPT
            else:
                prompt_template = EXAM_SUMMARY_PROMPT

            # Summarize each chunk, then optionally merge
            partial_summaries = []
            prog = st.progress(0)
            for i, chunk in enumerate(document_chunks):
                p = prompt_template.format(paper_text=chunk)
                try:
                    s = client.generate_text(p)
                except Exception as e:
                    st.error(f"Generation error on chunk {i+1}: {e}")
                    s = ""
                partial_summaries.append(s.strip())
                prog.progress((i + 1) / max(1, len(document_chunks)))

            # Merge partial summaries into a final structured summary pass
            merged_input = "\n\n".join([p for p in partial_summaries if p])
            final_prompt = DETAILED_SUMMARY_PROMPT.format(paper_text=merged_input)
            try:
                final_summary = client.generate_text(final_prompt)
            except Exception as e:
                st.error(f"Final merge generation error: {e}")
                final_summary = "\n\n".join(partial_summaries)

            st.markdown("### Final Summary")
            st.markdown("<div style='background:#f8f9fa;padding:18px;border-radius:10px;'>", unsafe_allow_html=True)
            st.markdown(final_summary, unsafe_allow_html=False)
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button("⬇ Download Summary", data=final_summary, file_name="research_summary.txt", mime="text/plain")

        # Chat / QA (keyword-based retrieval)
        st.markdown("---")
        st.markdown("### Ask questions about the PDF")
        question = st.text_input("Enter question and press Ask", key="qa_input")
        if st.button("Ask"):
            if not question or not question.strip():
                st.warning("Please type a question first.")
            else:
                # Keyword-based retrieval: score chunks by keyword overlap
                kw = [w.strip() for w in question.lower().split() if len(w) > 2]
                matches = []
                for i, c in enumerate(document_chunks):
                    text_lower = c.lower()
                    score = sum(1 for w in kw if w in text_lower)
                    if score > 0:
                        matches.append((score, i, c))
                # sort by score
                matches = sorted(matches, key=lambda x: x[0], reverse=True)[:5]

                if not matches:
                    st.info("No relevant passages found in the document. Try a different question or rephrase.")
                else:
                    # Build contexts for prompt
                    contexts_text = ""
                    for score, idx, text in matches:
                        contexts_text += f"CONTEXT #{idx} (score {score}):\n{text}\n\n"

                    rag_prompt = RAG_ANSWER_PROMPT.format(contexts=contexts_text, question=question)
                    try:
                        answer = client.generate_text(rag_prompt)
                    except Exception as e:
                        st.error(f"Generation error while answering: {e}")
                        answer = "Error generating answer."

                    st.markdown("**Answer:**")
                    st.markdown(answer)

                    with st.expander("Contexts used"):
                        st.text(contexts_text)

    else:
        st.info("Upload a PDF to enable summarization and question-answering.")
