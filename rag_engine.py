from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import requests

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load knowledge base documents
def load_kb(folder="data/kb"):
    texts, files = [], []
    for fname in os.listdir(folder):
        with open(os.path.join(folder, fname), "r", encoding="utf-8") as f:
            content = f.read()
            texts.append(content)
            files.append(fname)
    return texts, files

# Load and embed KB
texts, files = load_kb()
embeddings = model.encode(texts)
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))

# RAG answer generator
def get_rag_answer(query):
    query_emb = model.encode([query])
    D, I = index.search(np.array(query_emb), k=2)
    retrieved = [texts[i] for i in I[0]]
    # Optional: also retrieve source filenames
    # sources = [files[i] for i in I[0]]

    context = "\n".join(retrieved)

    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "You are a helpful banking assistant."},
            {"role": "user", "content": f"""Context:
{context}

Question:
{query}"""}
        ]
    }

    try:
        res = requests.post("http://localhost:11434/api/chat", json=payload)
        return res.json()["message"]["content"]
        # return f"{res.json()['message']['content']}\n\nSources: {', '.join(sources)}"  # Optional
    except Exception as e:
        return "❌ Failed to connect to Ollama. Make sure it's running with `ollama run mistral`."
