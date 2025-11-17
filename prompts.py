BRIEF_SUMMARY_PROMPT = """
You are an expert research analyst. Produce a short (3-4 sentences) plain-English summary of the text below.
Do NOT output JSON or code fences. Keep it concise and high-level.

Text:
{paper_text}
"""

DETAILED_SUMMARY_PROMPT = """
You are an expert research analyst. Produce a detailed, non-JSON, human-readable summary of the text below using the sections:
Overview, Problem Statement, Methodology, Key Findings, Conclusion.
Write in clear paragraphs under each heading. Avoid code fences or JSON.

Text:
{paper_text}
"""

EXAM_SUMMARY_PROMPT = """
You are an academic tutor. From the text below, produce concise exam-style notes: short bullets (no JSON), key facts, definitions, and 5 short Q&A pairs (question and one-line answer). Do NOT return JSON or code fences.

Text:
{paper_text}
"""

RAG_ANSWER_PROMPT = """
You are an expert research assistant. Use the context passages provided (each labeled CONTEXT #n) and the user's question to produce a direct, well-explained answer.

Context:
{contexts}

User question:
{question}

Guidelines:
- Answer using only the provided contexts. If the answer is not present, say: "I could not find the answer in the document."
- Provide citations like (Context #2) inline if referencing a context.
- Keep the tone neutral and academic.
"""
