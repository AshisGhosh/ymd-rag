# Yongmudo (UC Berkeley Martial Arts Program) - Retrieval-Augmented Generation Chatbot

[Yongmudo](http://www.yongmudo.org) is a martial art taught at UC Berkeley and is part of the UC Martial Arts Program (UCMAP). Black belt candidates as part of UCMAP submit academic martial arts papers to help deepen theirs and the the community's understanding of martial arts.

### Datasources

The collection of academic papers have been largely consolidated by Randy Vogel, the editor of the Monograph. This is a published work which compiles select papers for that edition. Currently the 10th edition is in progress.

This project takes in that semi-structured collection of documents and converts them to pdfs for processing. 

## Architecture & Tech Stack

This project was built with:
* LlamaIndex
* Weaviate
* Openrouter.ai
* Huggingface



## Retrieval-Augmented Generation (RAG) Strategies

* Hybrid search (enabled via Weaviate) showed a clear improvement on the standard RAG metrics
* Using sentence rerank (via llamaindex + huggingface ) showed a negative performance in the RAG metrics. Suspected reasons:
    * Mismatch in encoding training between the use of `BAAI/bge-small-en-v1.5` and `cross-encoder/ms-marco-MiniLM-L-2-v2`

#### Evaluation Process
* Use LlamaIndex tools to generate a question and response dataset
* Create iterations of query engines (seen in [evaluate.py](/backend/app/engine/evaluate.py)) and test against dataset using LlamaIndex framework
* Run via `docker-compose up evaluate`

#### RAG Metrics
Run | Correctness | Relevancy | Faithfulness | Semantic Similarity
--- | --- | --- | --- |--- 
Default | 3.067 | 0.967 | 0.267 | 0.916
Hybrid Search| 3.133 | 0.967 | 0.433 | 0.936
Sentence Rerank | 



### Chunk Size & Overlap
Both of the following were qualitiatively selected for a balance of processing time and data source size
* `chunk_size`: 512
* `chunk_overlap`: 20 



# Next Steps & Roadmap
* Move from chat engine to agent implement web scraper for [yongmudo.org](http://www.yongmudo.org) as a tool
* Implement [auto merging retrieval](https://docs.llamaindex.ai/en/stable/examples/retrievers/auto_merging_retriever.html) for improved performance
* Add observability via [Langfuse](http://www.langfuse.com) for prompt engineering inspection and performance tracking
* Test with other models, notably `Gemma 7B-it`. It's tuning for safety and accuracy makes it ideal for this application. At the time of writing, the `LlamaIndex` integration has an issue with it's chat template.



Built with help from the [LlamaIndex](https://www.llamaindex.ai/) tool [`create-llama`](https://github.com/run-llama/LlamaIndexTS/tree/main/packages/create-llama).