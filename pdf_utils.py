from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(file) -> str:
    """Extracts and returns text from a file-like PDF object."""
    reader = PdfReader(file)
    texts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texts.append(t)
    text = "\n".join(texts)
    # basic cleanup
    text = re.sub(r"\s+", " ", text).strip()
    return text




def chunk_text(text: str, max_tokens: int = 3000, overlap: int = 200):
    """
    Naive chunker that splits by paragraph boundaries attempting to keep under `max_tokens` words.
    Note: token vs words — this uses words as a proxy. For exact token counting, plug in a tokenizer.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap if (end - overlap) > start else end
    return chunks