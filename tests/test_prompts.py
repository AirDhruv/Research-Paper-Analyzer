from prompts import SUMMARY_PROMPT_TEMPLATE

def test_prompt_formatting():
    s = SUMMARY_PROMPT_TEMPLATE.format(paper_text="Hello world")
    assert "Paper chunk" in s or "paper chunk" in s.lower()