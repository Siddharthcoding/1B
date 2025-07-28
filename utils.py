import logging, json, os
from pathlib import Path
from typing import Tuple

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("persona_analyzer.log", mode="a")
        ]
    )

def load_input_specification() -> Tuple[str, str]:
    persona = os.getenv("PERSONA")
    job     = os.getenv("JOB_TO_BE_DONE")
    if persona and job:
        return persona, job
    spec = Path("input") / "input_spec.json"
    if spec.exists():
        data = json.loads(spec.read_text(encoding="utf-8"))
        return data.get("persona", ""), data.get("job_to_be_done", "")
    return (
        "PhD Researcher in Computational Biology",
        "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    )
