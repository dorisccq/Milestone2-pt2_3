import os
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
from PyPDF import PdfReader  # choose needed databse

# 加载模型
tokenizer = AutoTokenizer.from_pretrained('sentence-transformer-model')
model = AutoModel.from_pretrained('sentence-transformer-model')

def embed_text(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        embeddings = model(**inputs)
    return embeddings.detach().numpy()

def create_index(documents_dir, index_path):
    # read files
    texts = []
    for file in os.listdir(documents_dir):
        if file.endswith('.pdf'):
            reader = PdfReader(os.path.join(documents_dir, file))
            for page in reader.pages:
                texts.append(page.extract_text())
        # Deal with formats

    embeddings = np.array([embed_text(text) for text in texts])

    # FAISS index
    index = faiss.IndexIDMap(faiss.IndexFlatL2(embeddings.shape[1]))
    index.add_with_ids(embeddings, np.arange(len(embeddings)))
    faiss.write_index(index, index_path)

def search_knowledge(query, index_path, top_k=5):
    query_embedding = embed_text(query)
    index = faiss.read_index(index_path)
    distances, indices = index.search(query_embedding, top_k)
    return indices.flatten().tolist()