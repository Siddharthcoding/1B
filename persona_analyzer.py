import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from document_loader import DocumentLoader
from embeddings_manager import EmbeddingsManager
from llm_manager import LLMManager
from retriever import DocumentRetriever
from config import Config

logger = logging.getLogger(__name__)

class PersonaAnalyzer:
    def analyze_documents(self, pdf_paths: List[Path], persona: str, job: str) -> Dict[str, Any]:
        start = datetime.now()
        logger.info(f"Analyzing {len(pdf_paths)} documents")

        loader = DocumentLoader(chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP)
        docs = loader.load_multiple_pdfs(pdf_paths)
        chunks = loader.split_documents(docs)

        emb_mgr = EmbeddingsManager(Config.EMBEDDING_MODEL)
        emb_mgr.create_vector_db(chunks)

        retr = DocumentRetriever(LLMManager(Config.HF_LLM_MODEL), emb_mgr)
        retr.setup_retriever()

        query = f"Role={persona}; Task={job}"
        sections = retr.retrieve_relevant_sections(query, top_k=Config.RETRIEVAL_TOP_K)

        trimmed = sections[:3]
        context = "\n\n".join(
            f"Section {s['importance_rank']} (page {s['page']}): {s['content'][:200].replace(chr(10), ' ')}..."
            for s in trimmed
        )
        prompt = (
            f"You are an expert assistant.\n\n{context}\n\n"
            f"Persona: {persona}\nJob: {job}\n\n"
            f"Provide a concise structured analysis."
        )

        llm_callable = retr.llm_mgr.get_llm()
        logger.info("Invoking HF Transformers LLM")
        analysis = llm_callable(prompt)
        logger.info("LLM analysis completed")

        output = {
            "metadata": {
                "input_documents": [p.name for p in pdf_paths],
                "persona": persona,
                "job_to_be_done": job,
                "timestamp": start.isoformat()
            },
            "extracted_sections": sections,
            "llm_analysis": analysis,
            "sub_section_analysis": []
        }
        logger.info("Analysis complete")
        return output
