# embeddings_manager.py

import logging
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from typing import List
from config import Config

logger = logging.getLogger(__name__)

class LocalEmbeddings:
    def __init__(self, model_name):
        cache_dir = os.path.abspath("./hf_cache")
        resolved_model_dir = os.path.join(cache_dir, model_name)
        snapshots_dir = os.path.join(resolved_model_dir, "snapshots")
        if os.path.isdir(snapshots_dir):
            all_subs = [os.path.join(snapshots_dir, d) for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))]
            if all_subs:
                resolved_model_dir = all_subs[0]
        if not os.path.exists(resolved_model_dir):
            raise FileNotFoundError(
                f"Could not find the embedding model folder '{resolved_model_dir}'. "
                "Please pre-download/copy the files here."
            )
        self.model = SentenceTransformer(
            resolved_model_dir,
            local_files_only=True
        )

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

class EmbeddingsManager:
    def __init__(self, model_name):
        self.embedder = LocalEmbeddings(model_name)
        dim = self.embedder.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.metadatas = []

    def create_vector_db(self, documents):
        self.texts = [d.page_content for d in documents]
        self.metadatas = [d.metadata for d in documents]
        emb = self.embedder.embed(self.texts)
        self.index.add(emb.astype('float32'))
        logger.info(f"FAISS index built with {len(self.texts)} embeddings")

    def get_retriever(self, k=5):
        def retrieve(query: str):
            q_emb = self.embedder.embed([query]).astype('float32')
            _, idxs = self.index.search(q_emb, k)
            results = []
            for i in idxs[0]:
                results.append({"content": self.texts[i], **self.metadatas[i]})
            return results
        return retrieve
