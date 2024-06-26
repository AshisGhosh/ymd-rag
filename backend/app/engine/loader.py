from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

import logging
logger = logging.getLogger("uvicorn")

DATA_DIR = "data/processed_data"  # directory containing the documents


def get_documents():
    parser = LlamaParse(result_type="markdown", verbose=True, language="en")

    # reader = SimpleDirectoryReader(DATA_DIR, file_extractor={".pdf": parser}, recursive=True, exclude=["*/weaviate_data/*"])
    reader = SimpleDirectoryReader(DATA_DIR, recursive=True)
    pdfs = reader.load_data(show_progress=True)


    # docs_reader = SimpleDirectoryReader(DATA_DIR, required_exts=[".docx"], recursive=True, exclude=["*/weaviate_data/*"])
    # docs = docs_reader.load_data(show_progress=True)
    logging.info(f"Loaded {len(pdfs)} documents")
    return pdfs