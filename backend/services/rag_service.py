from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KNOWLEDGE_PATH = Path("backend/rag/knowledge.txt")


def load_knowledge():
    text = KNOWLEDGE_PATH.read_text(encoding="utf-8")

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    return chunks


chunks = load_knowledge()

vectorizer = TfidfVectorizer(stop_words="english")
vectors = vectorizer.fit_transform(chunks)


def retrieve(query, top_k=3):

    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector,
        vectors
    )[0]

    top_indices = scores.argsort()[-top_k:][::-1]

    results = []

    for index in top_indices:
        results.append({
            "text": chunks[index],
            "score": round(float(scores[index]), 4)
        })

    return results