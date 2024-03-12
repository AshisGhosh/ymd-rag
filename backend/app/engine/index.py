import logging
import os

from llama_index.core.indices import VectorStoreIndex
# from llama_index.vector_stores.pinecone import PineconeVectorStore
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore


logger = logging.getLogger("uvicorn")


def get_index():
    logger.info("Connecting to index from Weaviate...")
    # store = PineconeVectorStore(
    #     api_key=os.environ["PINECONE_API_KEY"],
    #     index_name=os.environ["PINECONE_INDEX_NAME"],
    #     environment=os.environ["PINECONE_ENVIRONMENT"],
    # )
    client = weaviate.Client("http://weaviate:8080")
    store = WeaviateVectorStore(
        weaviate_client=client, 
        index_name="YMDIndex"
        )
    index = VectorStoreIndex.from_vector_store(store)
    logger.info("Finished connecting to index from Weaviate.")
    return index
