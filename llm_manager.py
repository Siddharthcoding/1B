import logging
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
from config import Config

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self, model_name_or_path=None):
        model_name_or_path = model_name_or_path or Config.HF_LLM_MODEL
        cache_dir = os.path.abspath("./hf_cache")
        resolved_model_dir = os.path.join(cache_dir, model_name_or_path)

        # If the directory contains a 'snapshots' folder, use the first subfolder inside it
        snapshots_dir = os.path.join(resolved_model_dir, "snapshots")
        if os.path.isdir(snapshots_dir):
            all_subs = [os.path.join(snapshots_dir, d) for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))]
            if all_subs:
                resolved_model_dir = all_subs[0]  # use the first one

        if not os.path.exists(resolved_model_dir):
            raise FileNotFoundError(
                f"Could not find the model folder '{resolved_model_dir}'. "
                "Please pre-download it (see README) or copy the model files here."
            )

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                resolved_model_dir, local_files_only=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                resolved_model_dir, local_files_only=True,
                torch_dtype="auto", low_cpu_mem_usage=True
            )
        except Exception as e:
            raise RuntimeError(
                f"Could not load local model/tokenizer from {resolved_model_dir}: "
                f"{e}\nSee README for offline instructions."
            ) from e

        self.pipeline = TextGenerationPipeline(
            model=self.model, tokenizer=self.tokenizer, device=-1
        )
        logger.info(f"Loaded HF model locally: {resolved_model_dir}")

    def create_multi_query_retriever(self, base_retriever):
        return base_retriever

    def get_llm(self):
        def run(prompt):
            out = self.pipeline(
                prompt, max_new_tokens=256, do_sample=False, pad_token_id=self.tokenizer.eos_token_id
            )
            return out[0]["generated_text"]
        return run
