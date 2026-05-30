import os

_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        try:
            from sentence_transformers.cross_encoder import CrossEncoder
            model = os.getenv("CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
            print(f"Loading cross-encoder: {model}")
            _reranker = CrossEncoder(model)
        except Exception as e:
            print(f"Reranker load failed: {e}. Reranking disabled.")
            _reranker = False  # sentinel so we don't retry
    return _reranker if _reranker else None


def rerank(query: str, candidates: list[dict]) -> list[dict]:
    reranker = get_reranker()
    if not reranker or not candidates:
        return candidates

    texts = [c.get("semantic_string") or c.get("title", "") for c in candidates]
    pairs = [[query, t] for t in texts]

    try:
        scores = reranker.predict(pairs)
        for i, c in enumerate(candidates):
            c["rerank_score"] = float(scores[i])
        return sorted(candidates, key=lambda x: x.get("rerank_score", 0), reverse=True)
    except Exception as e:
        print(f"Reranking failed: {e}")
        return candidates
