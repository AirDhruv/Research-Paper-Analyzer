from ai_client import AIClient
from embeddings_utils import InMemoryVectorStore

MAX_EMBED_CHARS = 600   # safe chunk size for embedding API

def split_for_embedding(text, max_chars=MAX_EMBED_CHARS):
    """Split text into small embedding-safe chunks."""
    chunks = []
    text = text.strip()
    while len(text) > max_chars:
        split_pos = text.rfind(" ", 0, max_chars)
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos:].strip()
    if text:
        chunks.append(text)
    return chunks


class RAGHelper:
    def __init__(self, client: AIClient, embed_model=None):
        self.client = client
        self.store = InMemoryVectorStore()
        self.embed_model = embed_model or client.embed_model

    def build_index(self, large_chunks):
        """
        large_chunks = chunks from PDF (maybe large)
        We split them into small embed-safe pieces before calling embed API.
        """
        all_embed_texts = []
        all_metas = []

        # 1. Break large chunks into small embed-safe parts
        for chunk_id, large_chunk in enumerate(large_chunks):
            small_parts = split_for_embedding(large_chunk)

            for part in small_parts:
                all_embed_texts.append(part)
                all_metas.append({
                    "chunk_id": chunk_id,
                    "text": part
                })

        # 2. Embed in small batches (avoid the 10KB request limit)
        vectors = []
        BATCH = 3  # VERY small batches since payload is sensitive
        for i in range(0, len(all_embed_texts), BATCH):
            batch_texts = all_embed_texts[i:i+BATCH]
            vecs = self.client.embed_text(batch_texts)
            if isinstance(vecs[0], float):
                # Sometimes single vector case
                vecs = [vecs]
            vectors.extend(vecs)

        # 3. Load into memory store
        self.store.add(vectors, all_metas)

    def retrieve(self, question, top_k=4):
        qvec = self.client.embed_text(question)
        results = self.store.search(qvec, top_k=top_k)

        contexts = []
        for r in results:
            contexts.append((r["score"], r["metadata"]["text"], r["metadata"]["chunk_id"]))
        return contexts
