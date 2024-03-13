import os
import time
import asyncio
from collections import defaultdict
import pandas as pd
import numpy as np
import pickle

import nest_asyncio
nest_asyncio.apply()

from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset
from llama_index.core.node_parser import get_root_nodes

from llama_index.core.evaluation import (
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    RelevancyEvaluator,
    FaithfulnessEvaluator,
    PairwiseComparisonEvaluator,
)

from llama_index.core.evaluation.eval_utils import (
    get_responses,
    get_results_df,
)
from llama_index.core.evaluation import BatchEvalRunner
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
)

from app.settings import init_settings
from app.engine import get_index

EVAL_DIR = "data/eval_data"

def cache_object(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_cached_object(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return None

async def check_for_dataset():
    try:
        dataset = QueryResponseDataset.from_json(f"{EVAL_DIR}/mistral_eval_qr_dataset.json")
        print("Dataset already exists")
    except FileNotFoundError:
        print("Generating new dataset")
        print("This may take about 3 minutes")
        dataset = await generate_eval_dataset()
    finally:
        return dataset

def get_nodes():
    if load_cached_object(f"{EVAL_DIR}/mistral_nodes.pkl") is not None:
        return load_cached_object(f"{EVAL_DIR}/mistral_nodes.pkl")
    else:
        index = get_index()
        nodes = index.storage_context.vector_store.query(VectorStoreQuery(similarity_top_k=20))
        nodes = nodes.nodes
        cache_object(nodes, f"{EVAL_DIR}/mistral_nodes.pkl")
        return nodes

def get_pred_responses(eval_qs, query_engine):
    if load_cached_object(f"{EVAL_DIR}/mistral_pred_responses.pkl") is not None:
        print("Loading cached responses")
        return load_cached_object(f"{EVAL_DIR}/mistral_pred_responses.pkl")
    else:
        print("Generating new responses")
        print("This may take about 5 minutes")
        pred_responses = get_responses(eval_qs, query_engine, show_progress=True)
        cache_object(pred_responses, f"{EVAL_DIR}/mistral_pred_responses.pkl")
        return pred_responses

async def generate_eval_dataset():
    index = get_index()
    print("Index loaded")
    # nodes = index.docstore.docs.values()
    nodes = get_nodes()
    print(f"Nodes loaded, {len(nodes)} nodes found.")
    # root_nodes = get_root_nodes(nodes)
    # print(f"Root nodes parsed, {len(root_nodes)} root nodes found.")

    dataset_generator = DatasetGenerator(
        nodes,
        show_progress=True,
        num_questions_per_chunk=3,
    )
    print("Dataset generator created")
    print("Generating dataset")
    start_time = time.time()
    eval_dataset = await dataset_generator.agenerate_dataset_from_nodes(num=60)
    print(f"Dataset generated in {time.time() - start_time} seconds")
    eval_dataset.save_json(f"{EVAL_DIR}/mistral_eval_qr_dataset.json")
    print(f"Dataset saved to {EVAL_DIR}/mistral_eval_qr_dataset.json")


async def evaluate(eval_dataset):
    print(f"Evaluating dataset with {len(eval_dataset.questions)} questions")
    evaluator_c = CorrectnessEvaluator()
    evaluator_s = SemanticSimilarityEvaluator()
    evaluator_r = RelevancyEvaluator()
    evaluator_f = FaithfulnessEvaluator()

    eval_qs = eval_dataset.questions
    qr_pairs = eval_dataset.qr_pairs
    ref_response_strs = [r for (_, r) in qr_pairs]

    index = get_index()
    query_engine = index.as_query_engine()

    print("Getting responses")
    start_time = time.time()
    pred_responses = get_pred_responses(eval_qs, query_engine)
    print(f"Responses generated in {time.time() - start_time} seconds")
    # base_pred_responses = get_responses(
    #     eval_qs, base_query_engine, show_progress=True
    # )

    pred_response_strs = [str(p) for p in pred_responses]
    # base_pred_response_strs = [str(p) for p in base_pred_responses]
    evaluator_dict = {
    "correctness": evaluator_c,
    "faithfulness": evaluator_f,
    "relevancy": evaluator_r,
    "semantic_similarity": evaluator_s,
    }
    batch_runner = BatchEvalRunner(evaluator_dict, workers=2, show_progress=True)
    print("Evaluating responses")
    print("This may take about 15 minutes")
    start_time = time.time()
    eval_results = await batch_runner.aevaluate_responses(
        eval_qs, responses=pred_responses, reference=ref_response_strs
    )
    print(f"Responses evaluated in {time.time() - start_time} seconds")
    results_df = get_results_df(
        [eval_results],
        ["Default Query Engine"],
        ["correctness", "relevancy", "faithfulness", "semantic_similarity"],
    )
    # base_eval_results = await batch_runner.aevaluate_responses(
    #     eval_qs, responses=base_pred_responses, reference=ref_response_strs
    # )
    # results_df = get_results_df(
    #     [eval_results, base_eval_results],
    #     ["Auto Merging Retriever", "Base Retriever"],
    #     ["correctness", "relevancy", "faithfulness", "semantic_similarity"],
    # )

    print(results_df)
    cache_object(results_df, f"{EVAL_DIR}/mistral_eval_results.pkl")
    results_df.to_csv(f"{EVAL_DIR}/mistral_eval_results.csv")


if __name__ == "__main__":
    init_settings()
    print("Starting evaluation")
    dataset = asyncio.run(check_for_dataset())
    asyncio.run(evaluate(dataset))
    