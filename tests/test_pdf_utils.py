from pdf_utils import chunk_text


def test_chunking_small():
    text = "".join(["word "] * 100)
    chunks = chunk_text(text, max_tokens=50, overlap=10)
    assert len(chunks) >= 2


def test_chunking_no_overlap_issue():
    text = "".join(["w "] * 30)
    chunks = chunk_text(text, max_tokens=100, overlap=200)
    assert len(chunks) == 1