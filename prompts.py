SUMMARY_PROMPT_TEMPLATE = """
You are an expert research assistant. Read the following chunk of an academic paper and produce a concise, structured summary containing the following sections:


1. Title (if available) — otherwise write "Unknown Title"
2. Domain/Area
3. Problem statement (1-2 sentences)
4. Approach/Methods (bulleted list)
5. Key results / findings (bulleted list)
6. Strengths and weaknesses (short)
7. Important citations mentioned (short list)
8. 3 suggested keywords


Paper chunk:\n{paper_text}


Respond in JSON format using keys: title, domain, problem, methods, results, strengths_weaknesses, citations, keywords
"""