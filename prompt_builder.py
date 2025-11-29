# prompt_builder.py

def build_prompt(question: str, retrieved: list):
    bullets = []

    for r in retrieved:
        snippet = r["text"].replace("\n", " ")
        snippet = snippet[:300] + ("..." if len(snippet) > 300 else "")
        bullets.append(
            f"[#{r['rank']}] | {r['doc']} | s={r['score']:.3f} | {snippet}"
        )

    context = "\n".join(bullets)

    return (
        "You are given retrieved context bullets. Answer ONLY using this context. "
        "If the answer is not present, say you do not know.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context}\n\n"
        "Answer succinctly in 3–6 sentences and cite chunk ids like [#1], [#3]."
    )
