import faiss
import numpy as np
import pandas as pd
from embedder import embed

documents = []
index = None


def load_csv_dataset(path):
    import pandas as pd

    df = pd.read_csv(path)

    texts = []

    for _, row in df.iterrows():
        # 🔥 Combine ALL columns automatically
        text = " ".join([str(v) for v in row.values])
        texts.append(text)

    return texts


def build_index(texts):
    global index, documents
    import numpy as np
    import faiss

    documents = texts

    # 🔥 embed ALL at once
    vectors = embed(texts)

    dimension = vectors.shape[1]

    # 🔥 cosine similarity index
    index = faiss.IndexFlatIP(dimension)

    index.add(np.array(vectors))


def search(query, k=3):
    import numpy as np

    query_vec = embed([query])

    distances, indices = index.search(np.array(query_vec), k)

    results = []

    for i, dist in zip(indices[0], distances[0]):

        doc = documents[i]

        # 🔥 Convert distance → similarity score
        score = 1 - dist/2
        score = max(0, min(score, 1))   # value between 0–1

        results.append({
            "text": doc,
            "score": round(float(score), 3)
        })

    return results