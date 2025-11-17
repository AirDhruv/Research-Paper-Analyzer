SUMMARY_PROMPT_TEMPLATE = """
You are an expert research analyst. Your task is to generate a clear, structured,
human-readable summary from a section of an academic research paper.

Formatting Rules:
- DO NOT use JSON.
- DO NOT use any braces like {{ }} except the one used for inserting text.
- DO NOT output arrays, objects, or code blocks.
- Write only clean text with headings and paragraphs.

Required Output Sections:
1. Overview
2. Problem Statement
3. Methodology
4. Key Findings
5. Conclusion

TEXT TO SUMMARIZE:
---------------------
{paper_text}

Now produce the structured summary.
"""
