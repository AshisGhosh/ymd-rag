import logging
import os

from llama_index.core.indices import VectorStoreIndex
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore


logger = logging.getLogger("uvicorn")


def get_index():
    logger.info("Connecting to index from Weaviate...")
   
    client = weaviate.Client("http://weaviate:8080")
    store = WeaviateVectorStore(
        weaviate_client=client, 
        index_name="YMDIndex"
        )
    index = VectorStoreIndex.from_vector_store(store)
    logger.info("Finished connecting to index from Weaviate.")
    return index
