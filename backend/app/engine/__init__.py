from app.engine.index import get_index
from llama_index.core.retrievers import AutoMergingRetriever



def get_chat_engine():
    # index = get_index()
    # base_retriever = index.as_retriever(similarity_top_k=6)
    # retriever = AutoMergingRetriever(base_retriever, index.storage_context, verbose=True)
    return get_index().as_chat_engine(
        similarity_top_k=3, 
        chat_mode="condense_plus_context",
        # system_prompt=(
        # "You are a helpful assistant that can answer questions about Yongmudo, a martial art that is also known as YMD. "
        # "You have access to a number of documents and can provide specific and detailed answers to questions. "
        # ),
        # retriever=retriever,
    )
