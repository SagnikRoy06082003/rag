
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(texts):
    embeddings = model.encode(texts)

    # 🔥 normalize vectors
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms