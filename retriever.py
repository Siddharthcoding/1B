import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self, llm_mgr, emb_mgr):
        self.llm_mgr = llm_mgr
        self.emb_mgr = emb_mgr
        self.retrieve_fn = None

    def setup_retriever(self):
        self.retrieve_fn = self.emb_mgr.get_retriever()
        logger.info("Retriever ready")

    def retrieve_relevant_sections(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.retrieve_fn:
            self.setup_retriever()
        secs = self.retrieve_fn(query)
        for i, sec in enumerate(secs, start=1):
            sec["importance_rank"] = i
        logger.info(f"Retrieved {len(secs)} sections")
        return secs
