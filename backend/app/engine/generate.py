from dotenv import load_dotenv

load_dotenv()

import os
import logging
from llama_index.core.storage import StorageContext
from llama_index.core.indices import VectorStoreIndex
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore
# from llama_index.vector_stores.pinecone import PineconeVectorStore
from app.settings import init_settings
from app.engine.loader import get_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def generate_datasource():
    logger.info("Creating new index")
    # load the documents and create the index
    documents = get_documents()
    client = weaviate.Client("http://weaviate:8080")
    store = WeaviateVectorStore(
        weaviate_client=client, 
        index_name="YMDIndex"
        )
    # store = PineconeVectorStore(
    #     api_key=os.environ["PINECONE_API_KEY"],
    #     index_name=os.environ["PINECONE_INDEX_NAME"],
    #     environment=os.environ["PINECONE_ENVIRONMENT"],
    # )
    storage_context = StorageContext.from_defaults(vector_store=store)
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,  # this will show you a progress bar as the embeddings are created
    )
    logger.info(
        f"Successfully created embeddings and save to your Weaviate index YMDIndex"
    )


if __name__ == "__main__":
    init_settings()
    generate_datasource()
