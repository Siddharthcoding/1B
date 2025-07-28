# models_online.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import shutil, os

def download_hf_model(model_name, target_dir):
    # Temporary download into HuggingFace default cache
    tmp = f"./hf_cache_tmp/{model_name.replace('/', '_')}"
    os.makedirs(tmp, exist_ok=True)
    AutoTokenizer.from_pretrained(model_name, cache_dir=tmp, local_files_only=False)
    AutoModelForCausalLM.from_pretrained(model_name, cache_dir=tmp, local_files_only=False)
    # Move into your desired folder
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.move(tmp, target_dir)

def download_sentence_transformer(model_name, target_dir):
    tmp = f"./hf_cache_tmp/{model_name}"
    os.makedirs(tmp, exist_ok=True)
    SentenceTransformer(model_name, cache_folder=tmp)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.move(tmp, target_dir)

if __name__=="__main__":
    os.makedirs("hf_cache", exist_ok=True)
    download_hf_model("distilgpt2",          "hf_cache/distilgpt2")
    download_sentence_transformer(
        "all-MiniLM-L6-v2",
        "hf_cache/sentence-transformers_all-MiniLM-L6-v2"
    )
