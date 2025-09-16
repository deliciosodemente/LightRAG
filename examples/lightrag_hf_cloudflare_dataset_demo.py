import asyncio
import os
import inspect
import logging
import logging.config
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc, logger, set_verbose_debug
from lightrag.kg.shared_storage import initialize_pipeline_status

import requests
import numpy as np
from datasets import load_dataset
from dotenv import load_dotenv

"""LightRAG demo with Hugging Face dataset integration and Cloudflare Worker AI models"""

# Load environment variables
load_dotenv(dotenv_path=".env", override=False)

"""    ----========= IMPORTANT: CHANGE THESE VALUES! =========----    """
cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY", "YOUR_API_KEY")
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "YOUR_ACCOUNT_ID")

# Automatically constructed API base URL
api_base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"

# Choose AI models
EMBEDDING_MODEL = "@cf/baai/bge-m3"
LLM_MODEL = "@cf/meta/llama-3.2-3b-instruct"

# Working directory for LightRAG data
WORKING_DIR = "./hf_cloudflare_demo"

# Hugging Face dataset configuration
HF_DATASET_NAME = "deli333777/data"
HF_TOKEN = os.getenv("HF_TOKEN")  # Optional: for private datasets


class CloudflareWorker:
    """Cloudflare Worker integration for AI models"""

    def __init__(
        self,
        cloudflare_api_key: str,
        api_base_url: str,
        llm_model_name: str,
        embedding_model_name: str,
        max_tokens: int = 4080,
        max_response_tokens: int = 4080,
    ):
        self.cloudflare_api_key = cloudflare_api_key
        self.api_base_url = api_base_url
        self.llm_model_name = llm_model_name
        self.embedding_model_name = embedding_model_name
        self.max_tokens = max_tokens
        self.max_response_tokens = max_response_tokens

    async def _send_request(self, model_name: str, input_: dict, debug_log: str):
        headers = {"Authorization": f"Bearer {self.cloudflare_api_key}"}

        logger.debug(f"Cloudflare request: {debug_log}")

        try:
            response_raw = requests.post(
                f"{self.api_base_url}{model_name}", headers=headers, json=input_
            ).json()

            logger.debug(f"Cloudflare response: {str(response_raw)}")
            result = response_raw.get("result", {})

            if "data" in result:  # Embedding case
                return np.array(result["data"])

            if "response" in result:  # LLM response
                return result["response"]

            raise ValueError("Unexpected Cloudflare response format")

        except Exception as e:
            logger.error(f"Cloudflare API error: {e}")
            return None

    async def query(self, prompt, system_prompt: str = "", **kwargs) -> str:
        # Remove caching kwargs that might interfere
        kwargs.pop("hashing_kv", None)

        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        input_ = {
            "messages": message,
            "max_tokens": self.max_tokens,
            "response_token_limit": self.max_response_tokens,
        }

        return await self._send_request(
            self.llm_model_name,
            input_,
            debug_log=f"LLM Query - Model: {self.llm_model_name}, Prompt: {prompt[:100]}...",
        )

    async def embedding_chunk(self, texts: list[str]) -> np.ndarray:
        logger.debug(f"Embedding texts: {len(texts)} chunks")

        input_ = {
            "text": texts,
            "max_tokens": self.max_tokens,
            "response_token_limit": self.max_response_tokens,
        }

        return await self._send_request(
            self.embedding_model_name,
            input_,
            debug_log=f"Embedding - Model: {self.embedding_model_name}, Texts: {len(texts)}",
        )


def configure_logging():
    """Configure logging for the application"""

    # Reset any existing handlers to ensure clean configuration
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "lightrag"]:
        logger_instance = logging.getLogger(logger_name)
        logger_instance.handlers = []
        logger_instance.filters = []

    # Get log directory path from environment variable or use current directory
    log_dir = os.getenv("LOG_DIR", os.getcwd())
    log_file_path = os.path.abspath(
        os.path.join(log_dir, "lightrag_hf_cloudflare_demo.log")
    )

    print(f"\nLightRAG Hugging Face + Cloudflare demo log file: {log_file_path}\n")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Get log file max size and backup count from environment variables
    log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 10485760))  # Default 10MB
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))  # Default 5 backups

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "formatter": "detailed",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "lightrag": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    # Set the logger level to INFO
    logger.setLevel(logging.INFO)
    # Enable verbose debug if needed
    set_verbose_debug(os.getenv("VERBOSE_DEBUG", "false").lower() == "true")


def load_hf_dataset_with_auth(dataset_name: str, token: str = None):
    """Load Hugging Face dataset with authentication handling"""
    try:
        logger.info(f"Loading Hugging Face dataset: {dataset_name}")

        # Set token if provided
        if token:
            os.environ["HF_TOKEN"] = token
            logger.info("Using Hugging Face authentication token")

        ds = load_dataset(dataset_name)
        logger.info(f"Dataset loaded successfully. Available splits: {list(ds.keys())}")
        return ds
    except Exception as e:
        logger.error(f"Failed to load dataset {dataset_name}: {e}")
        raise


def process_dataset_entries(dataset):
    """Process dataset entries into text format for LightRAG insertion"""
    texts_to_insert = []

    # Handle different dataset formats
    if 'train' in dataset:
        data_split = dataset['train']
    else:
        data_split = dataset[list(dataset.keys())[0]]

    logger.info(f"Processing {len(data_split)} dataset entries")

    for i, entry in enumerate(data_split):
        try:
            # Extract text content (adjust based on actual dataset structure)
            if 'text' in entry:
                text_content = entry['text']
            elif 'content' in entry:
                text_content = entry['content']
            elif isinstance(entry, dict):
                # Convert dict to formatted text
                text_content = "\n".join([f"{k}: {v}" for k, v in entry.items() if v])
            else:
                # Fallback: convert entry to string
                text_content = str(entry)

            if text_content.strip():  # Only add non-empty content
                texts_to_insert.append(text_content)

            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(data_split)} entries")

        except Exception as e:
            logger.warning(f"Error processing entry {i}: {e}")
            continue

    logger.info(f"Successfully processed {len(texts_to_insert)} valid text entries")
    return texts_to_insert


if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    """Initialize LightRAG with Cloudflare Worker integration"""
    cloudflare_worker = CloudflareWorker(
        cloudflare_api_key=cloudflare_api_key,
        api_base_url=api_base_url,
        embedding_model_name=EMBEDDING_MODEL,
        llm_model_name=LLM_MODEL,
    )

    rag = LightRAG(
        working_dir=WORKING_DIR,
        max_parallel_insert=2,
        llm_model_func=cloudflare_worker.query,
        llm_model_name=os.getenv("LLM_MODEL", LLM_MODEL),
        summary_max_tokens=4080,
        embedding_func=EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1024")),
            max_token_size=int(os.getenv("MAX_EMBED_TOKENS", "2048")),
            func=lambda texts: cloudflare_worker.embedding_chunk(texts),
        ),
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def print_stream(stream):
    """Print streaming response"""
    async for chunk in stream:
        print(chunk, end="", flush=True)


async def main():
    """Main execution function"""
    try:
        # Validate required environment variables
        if cloudflare_api_key == "YOUR_API_KEY":
            raise ValueError("Please set CLOUDFLARE_API_KEY environment variable")
        if account_id == "YOUR_ACCOUNT_ID":
            raise ValueError("Please set CLOUDFLARE_ACCOUNT_ID environment variable")

        # Clear old data files
        files_to_delete = [
            "graph_chunk_entity_relation.graphml",
            "kv_store_doc_status.json",
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "vdb_chunks.json",
            "vdb_entities.json",
            "vdb_relationships.json",
        ]

        for file in files_to_delete:
            file_path = os.path.join(WORKING_DIR, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted old file: {file_path}")

        # Initialize RAG instance
        logger.info("Initializing LightRAG with Cloudflare Worker integration...")
        rag = await initialize_rag()

        # Test embedding function
        test_text = ["This is a test string for embedding."]
        embedding = await rag.embedding_func(test_text)
        embedding_dim = embedding.shape[1]
        print("\n=======================")
        print("Test embedding function")
        print("=======================")
        print(f"Test text: {test_text}")
        print(f"Detected embedding dimension: {embedding_dim}\n")

        # Load and process Hugging Face dataset
        logger.info("Loading and processing Hugging Face dataset...")
        dataset = load_hf_dataset_with_auth(HF_DATASET_NAME, HF_TOKEN)
        texts_to_insert = process_dataset_entries(dataset)

        # Insert dataset into LightRAG
        if texts_to_insert:
            logger.info(f"Inserting {len(texts_to_insert)} text entries into LightRAG...")
            await rag.ainsert(texts_to_insert)
            logger.info("Dataset insertion completed successfully!")
        else:
            logger.warning("No valid text entries found to insert")
            return

        # Test queries
        test_queries = [
            "What is the main content of this dataset?",
            "Summarize the key themes or topics found in the data",
            "What are the most important entities mentioned?"
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"Test Query {i}: {query}")
            print('='*60)

            try:
                resp = await rag.aquery(
                    query,
                    param=QueryParam(mode="hybrid", stream=True),
                )
                if inspect.isasyncgen(resp):
                    await print_stream(resp)
                else:
                    print(resp)
            except Exception as e:
                logger.error(f"Error during query {i}: {e}")

        # Interactive mode (uncomment to enable)
        """
        print("\n" + "=" * 60)
        print("🤖 AI ASSISTANT READY!")
        print("Ask questions about the loaded dataset")
        print("Type 'quit' to exit")
        print("=" * 60)

        while True:
            question = input("\n🔥 Your question: ")

            if question.lower() in ['quit', 'exit', 'bye']:
                break

            print("\nThinking...")
            response = await rag.aquery(question, param=QueryParam(mode="hybrid"))
            print(f"\nAnswer: {response}")
        """

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        if 'rag' in locals():
            await rag.finalize_storages()


if __name__ == "__main__":
    # Configure logging before running the main function
    configure_logging()
    asyncio.run(main())
    print("\n✅ Demo completed successfully!")