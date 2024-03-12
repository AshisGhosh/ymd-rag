from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

DATA_DIR = "data"  # directory containing the documents


def get_documents():
    parser = LlamaParse(result_type="markdown", verbose=True, language="en")

    reader = SimpleDirectoryReader(DATA_DIR, file_extractor={".pdf": parser}, recursive=True, exclude=["*/weaviate_data/*"])
    pdfs = reader.load_data()

    docs_reader = SimpleDirectoryReader(DATA_DIR, required_exts=[".docx"], recursive=True, exclude=["*/weaviate_data/*"])
    docs = docs_reader.load_data()

    return pdfs + docs