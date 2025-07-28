import os
from pathlib import Path

class Config:
    EMBEDDING_MODEL   = "sentence-transformers_all-MiniLM-L6-v2"
    HF_LLM_MODEL      = "distilgpt2"   # change to "tiiuae/falcon-1b-instruct" or any local huggingface model if desired
    MIN_DOCUMENTS     = 2
    MAX_DOCUMENTS     = 10
    CHUNK_SIZE        = 7500
    CHUNK_OVERLAP     = 100
    INPUT_DIR         = Path("input")
    OUTPUT_DIR        = Path("output")
    RETRIEVAL_TOP_K   = 5

    @classmethod
    def setup_directories(cls):
        cls.INPUT_DIR.mkdir(exist_ok=True, parents=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
