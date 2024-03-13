import os
# from llama_index.llms.openai import OpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.llms.huggingface import HuggingFace
# from llama_index.llms.ollama import Ollama
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings

from dotenv import load_dotenv

load_dotenv()


def init_settings():
    # llm_model = os.getenv("MODEL", "gpt-3.5-turbo")
    # embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")


    # Settings.llm = OpenAI(model=llm_model)
    # Settings.embed_model = OpenAIEmbedding(model=embedding_model)
    # Settings.llm = HuggingFace(model_name="EleutherAI/gpt-neo-2.7B")
    # ollama_llm = Ollama(model="gemma:2b", request_timeout=30.0)
    # ollama_llm.base_url="http://ollama:11434"
    # Settings.llm = ollama_llm
    # Settings.llm = Ollama(model="gemma:2b", request_timeout=30.0)
    Settings.llm = OpenRouter(model="mistralai/mistral-7b-instruct:free", max_retries=60, request_timeout=30.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.chunk_size = 512
    Settings.chunk_overlap = 20
