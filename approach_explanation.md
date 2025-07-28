
# Team CODDIIII 1B project walkthrough

## Approach

The 1B project is designed as a fully offline document analysis pipeline that ingests large collections of PDF files and generates detailed, persona-driven insights using local large language models (LLMs) and vector-based similarity search. 

**Core Components and Workflow**

1. **Document Loading & Splitting:**  
PDF documents are loaded page-by-page using PyMuPDF. Each page’s text is extracted and then chunked into overlapping sections using LangChain’s RecursiveCharacterTextSplitter. This maintains contextual continuity across chunks and improves relevance during retrieval.

2. **Embeddings Generation & Vector Indexing:**  
Text chunks are converted into vector embeddings using a locally cached sentence-transformers model (default: all-MiniLM-L6-v2). These embeddings are indexed with FAISS, a highly efficient similarity search library that enables quick retrieval of relevant text sections based on query embeddings.

3. **Retrieval Based on Persona & Job:**  
A query is constructed combining the user’s persona and job description. The FAISS index is searched to retrieve the top relevant document chunks matching the query, ensuring the context provided to the LLM is focused and informative.

4. **Local LLM Analysis with Hugging Face Models:**  
Instead of relying on cloud APIs, the pipeline uses a local Hugging Face Transformer model (default: distilgpt2) for textual analysis. Models and tokenizers are pre-downloaded and cached to enable offline operation. The prompt includes top retrieved chunks along with persona and job info, and the LLM generates a structured, detailed analysis.

**Offline & Reproducibility Focus**

- Model files for both embeddings and LLM are cached locally in a project folder (hf_cache) to guarantee offline usage after the initial setup.
- A helper script (models_online.py) automates downloading these models and organizing cache folders for seamless offline reference.
- The pipeline avoids any internet dependency at runtime by enforcing local_files_only=True in Hugging Face and sentence-transformers loaders.

**Extensibility & Deployment**

- The modular architecture supports swapping or upgrading embedding or LLM models.
- The entire environment can be containerized with Docker, encapsulating all dependencies including native libraries, so end users can run the system without local build tools or Python setup.

In summary, 1B empowers privacy-conscious, scalable document analysis with modern NLP tooling optimized for fully offline, reliable operation in diverse deployment scenarios.




## Docker Run Steps

- First create two folders named as input & output 

- In the input folder the user need to put all the pdfs that the user wants to analyze

- In that same input folder the user also needs to create a JSON file named as input_spec.json where user will specify persona & job to be done in following format:

```json
{
    "persona": "Student",
    "job_to_be_done": "What is a protocol"
}

```

- The user can access the output from the output folder where a new JSON file will be generated.

Finally run the below command to run the docker:

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output chiranjeet12/adobe_round1b:latest
```

**User first need network to  download the image locally then can use the below without network command**

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output  -network none chiranjeet12/adobe_round1b:latest
```
