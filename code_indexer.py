''' in .env
OPENAI_API_KEY="YOUR_OPENAI_KEY"
ACTIVELOOP_TOKEN="YOUR_ACTIVELOOP_TOKEN"
DATASET_PATH="hub://YOUR_ORG/repository_vector_store"


need to install llama-index, python-dotenv, llama-index-vector-stores-deeplake, deeplake
'''

import os
import textwrap
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import CodeSplitter
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline

# Load environment variables
load_dotenv()

# Fetch and set API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
active_loop_token = os.getenv("ACTIVELOOP_TOKEN")
dataset_path = os.getenv("DATASET_PATH")

# Configuration
directory_path = "/Users/aaols/PycharmProjects/leetcode_org"  # Replace with your directory


max_chars = 2000
chunk_lines = 10
chunk_overlap = 2


def main():
    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OpenAI API key not found in environment variables")

    # Check for Activeloop Token
    active_loop_token = os.getenv("ACTIVELOOP_TOKEN")
    if not active_loop_token:
        raise EnvironmentError("Activeloop token not found in environment variables")

    reader = SimpleDirectoryReader(input_dir=directory_path)

    # create the pipeline with transformations
    pipeline = IngestionPipeline(
        transformations=[
            CodeSplitter(
                language="python",
                max_chars=max_chars,
                chunk_lines=chunk_lines,
                chunk_lines_overlap=chunk_overlap),
            TitleExtractor(),
            OpenAIEmbedding(),
        ]
    )

    # run the pipeline
    nodes = pipeline.run(documents=reader.load_data())

    vector_store = DeepLakeVectorStore(
            dataset_path=dataset_path,
            overwrite=True,
            runtime={"tensor_db": True},
        )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
    query_engine = index.as_query_engine()

    # Include a simple question to test.
    intro_question = "What is dfs?"
    print(f"Test question: {intro_question}")
    print("=" * 50)
    answer = query_engine.query(intro_question)

    print(f"Answer: {textwrap.fill(str(answer), 100)} \n")
    while True:
        user_question = input("Please enter your question (or type 'exit' to quit): ")
        if user_question.lower() == "exit":
            print("Exiting, thanks for chatting!")
            break

        print(f"Your question: {user_question}")
        print("=" * 50)

        answer = query_engine.query(user_question)
        print(f"Answer: {textwrap.fill(str(answer), 100)} \n")


if __name__ == "__main__":
    main()
