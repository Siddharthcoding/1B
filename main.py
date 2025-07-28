import json, logging, sys, os
from config import Config
from utils import setup_logging, load_input_specification
from persona_analyzer import PersonaAnalyzer

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"CWD: {os.getcwd()}")
    logger.info(f"In: {Config.INPUT_DIR.resolve()}  Out: {Config.OUTPUT_DIR.resolve()}")

    Config.setup_directories()
    pdfs = list(Config.INPUT_DIR.glob("*.pdf"))
    if len(pdfs) < Config.MIN_DOCUMENTS:
        logger.error(f"Need >= {Config.MIN_DOCUMENTS} PDFs, found {len(pdfs)}")
        sys.exit(1)

    persona, job = load_input_specification()
    try:
        result = PersonaAnalyzer().analyze_documents(pdfs, persona, job)
        logger.info(f"Result keys: {list(result.keys())}")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

    out = Config.OUTPUT_DIR / "analysis_result.json"
    try:
        logger.info(f"Saving to {out.resolve()}")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info("Saved analysis_result.json")
    except Exception as e:
        logger.error(f"Save failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
