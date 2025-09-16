# 🚀 LightRAG Cloudflare Worker Dataset Integration Guide

This comprehensive guide covers committing code changes, updating Cloudflare Worker integration, and incorporating Hugging Face dataset functionality into LightRAG.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Committing Code Changes](#committing-code-changes)
4. [Cloudflare Worker Integration](#cloudflare-worker-integration)
5. [Dataset Integration](#dataset-integration)
6. [Testing and Deployment](#testing-and-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## 🔧 Prerequisites

### Required Software
- **Python 3.8+** with pip
- **Node.js 16+** and npm
- **Git** for version control
- **Wrangler CLI** for Cloudflare Workers

### Required Accounts
- **GitHub account** for code contributions
- **Cloudflare account** with Workers and AI Gateway access
- **Hugging Face account** (optional, for private datasets)

### Environment Setup
```bash
# Install Python dependencies
pip install lightrag datasets requests numpy python-dotenv

# Install Wrangler CLI globally
npm install -g wrangler

# Authenticate with Cloudflare
npx wrangler auth login

# Authenticate with Hugging Face (for private datasets)
huggingface-cli login
```

## 🏗️ Project Setup

### 1. Clone and Setup LightRAG
```bash
# Clone the repository
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Environment Configuration
Create `.env` file with your credentials:
```bash
# Cloudflare Configuration
CLOUDFLARE_API_KEY=your_cloudflare_api_key
CLOUDFLARE_ACCOUNT_ID=your_account_id

# Hugging Face Configuration (optional)
HF_TOKEN=your_huggingface_token

# Logging Configuration
LOG_DIR=./logs
VERBOSE_DEBUG=false
```

## 📝 Committing Code Changes

### 1. Development Workflow
```bash
# Create a feature branch
git checkout -b feature/hf-cloudflare-integration

# Make your changes
# ... edit files ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: integrate Hugging Face datasets with Cloudflare Workers

- Add Cloudflare Worker class for AI model inference
- Implement Hugging Face dataset loading with authentication
- Create comprehensive example script combining both features
- Add proper error handling and logging
- Update documentation with integration guide

Closes #123"
```

### 2. Code Quality Checks
```bash
# Run linting
pip install flake8 black
black examples/lightrag_hf_cloudflare_dataset_demo.py
flake8 examples/lightrag_hf_cloudflare_dataset_demo.py

# Run tests
python -m pytest tests/ -v

# Check for security issues
pip install bandit
bandit -r examples/lightrag_hf_cloudflare_dataset_demo.py
```

### 3. Pull Request Process
```bash
# Push your branch
git push origin feature/hf-cloudflare-integration

# Create pull request on GitHub
# 1. Go to https://github.com/HKUDS/LightRAG/pulls
# 2. Click "New Pull Request"
# 3. Select your feature branch
# 4. Fill in PR description with:
#    - What changes were made
#    - Why they were needed
#    - How to test the changes
#    - Screenshots/videos if applicable
```

### 4. Commit Message Guidelines
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

## ☁️ Cloudflare Worker Integration

### 1. Cloudflare AI Gateway Setup
```bash
# Run the automated setup script
./setup-cloudflare.sh

# Or set up manually
npx wrangler ai gateway create lightrag-gateway
```

### 2. Update Environment Variables
```bash
# Add to your .env file
USE_CLOUDFLARE_GATEWAY=true
CLOUDFLARE_GATEWAY_ID=your_gateway_id
LLM_BINDING=cloudflare
EMBEDDING_BINDING=cloudflare
```

### 3. Cloudflare Worker Class Implementation
The `CloudflareWorker` class handles AI model inference:

```python
class CloudflareWorker:
    def __init__(self, api_key, account_id, llm_model, embedding_model):
        self.api_base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.api_key = api_key
        self.llm_model = llm_model
        self.embedding_model = embedding_model

    async def query(self, prompt, system_prompt="", **kwargs):
        # Implementation for LLM queries

    async def embedding_chunk(self, texts):
        # Implementation for text embeddings
```

### 4. Integration with LightRAG
```python
# Initialize Cloudflare Worker
cloudflare_worker = CloudflareWorker(
    cloudflare_api_key=os.getenv("CLOUDFLARE_API_KEY"),
    account_id=os.getenv("CLOUDFLARE_ACCOUNT_ID"),
    llm_model_name="@cf/meta/llama-3.2-3b-instruct",
    embedding_model_name="@cf/baai/bge-m3"
)

# Create LightRAG instance
rag = LightRAG(
    working_dir="./data",
    llm_model_func=cloudflare_worker.query,
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,
        func=lambda texts: cloudflare_worker.embedding_chunk(texts)
    )
)
```

## 📊 Dataset Integration

### 1. Hugging Face Dataset Loading
```python
from datasets import load_dataset

def load_hf_dataset_with_auth(dataset_name, token=None):
    """Load dataset with authentication"""
    if token:
        os.environ["HF_TOKEN"] = token

    dataset = load_dataset(dataset_name)
    return dataset
```

### 2. Data Processing
```python
def process_dataset_entries(dataset):
    """Convert dataset entries to text format"""
    texts = []

    # Handle different dataset structures
    data_split = dataset['train'] if 'train' in dataset else dataset[list(dataset.keys())[0]]

    for entry in data_split:
        if 'text' in entry:
            text_content = entry['text']
        elif 'content' in entry:
            text_content = entry['content']
        else:
            text_content = str(entry)

        if text_content.strip():
            texts.append(text_content)

    return texts
```

### 3. Insert into LightRAG
```python
# Process and insert dataset
dataset = load_hf_dataset_with_auth("deli333777/data")
texts_to_insert = process_dataset_entries(dataset)

# Insert into knowledge graph
await rag.ainsert(texts_to_insert)
```

## 🧪 Testing and Deployment

### 1. Local Testing
```bash
# Run the integrated demo
python examples/lightrag_hf_cloudflare_dataset_demo.py

# Test specific functionality
python -c "
import asyncio
from examples.lightrag_hf_cloudflare_dataset_demo import load_hf_dataset_with_auth, process_dataset_entries

async def test():
    dataset = load_hf_dataset_with_auth('deli333777/data')
    texts = process_dataset_entries(dataset)
    print(f'Loaded {len(texts)} text entries')

asyncio.run(test())
"
```

### 2. Integration Testing
```python
# Test Cloudflare Worker connection
async def test_cloudflare_connection():
    worker = CloudflareWorker(api_key, account_id, llm_model, embedding_model)

    # Test embedding
    test_texts = ["Hello world"]
    embeddings = await worker.embedding_chunk(test_texts)
    assert embeddings is not None

    # Test LLM query
    response = await worker.query("What is AI?")
    assert response is not None

    print("✅ Cloudflare Worker tests passed")

# Test dataset insertion
async def test_dataset_insertion():
    rag = await initialize_rag()

    # Insert test data
    test_texts = ["This is a test document about artificial intelligence."]
    await rag.ainsert(test_texts)

    # Query the data
    result = await rag.aquery("What is this document about?")
    assert "artificial intelligence" in result.lower()

    print("✅ Dataset insertion tests passed")
```

### 3. Deployment
```bash
# Deploy with Docker
./deploy.sh deploy .env.production

# Or deploy manually
docker-compose up -d

# Check deployment status
docker-compose logs lightrag
```

### 4. Monitoring
```bash
# Monitor Cloudflare usage
npx wrangler tail

# Check LightRAG logs
docker-compose logs -f lightrag

# View gateway analytics
# Go to Cloudflare Dashboard > AI > AI Gateway
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Cloudflare Authentication
```bash
# Re-authenticate
npx wrangler auth login

# Check account info
npx wrangler whoami
```

#### 2. Dataset Loading Errors
```python
# Check dataset access
from datasets import load_dataset
try:
    ds = load_dataset("deli333777/data")
    print("Dataset loaded successfully")
except Exception as e:
    print(f"Error: {e}")
    # May need authentication for private datasets
```

#### 3. API Rate Limits
```python
# Implement retry logic
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def robust_query(worker, prompt):
    return await worker.query(prompt)
```

#### 4. Memory Issues with Large Datasets
```python
# Process datasets in batches
def process_in_batches(dataset, batch_size=100):
    for i in range(0, len(dataset), batch_size):
        batch = dataset[i:i + batch_size]
        yield process_dataset_entries(batch)
```

## 📚 Best Practices

### 1. Code Organization
```
examples/
├── lightrag_hf_cloudflare_dataset_demo.py  # Main integration script
├── lightrag_cloudflare_demo.py            # Cloudflare-only demo
└── lightrag_openai_demo.py                # OpenAI demo

lightrag/
├── llm/
│   ├── cloudflare.py                      # Cloudflare LLM implementation
│   └── openai.py                         # OpenAI LLM implementation
└── kg/
    └── cloudflare_impl.py                 # Cloudflare-specific storage
```

### 2. Error Handling
```python
import logging
logger = logging.getLogger(__name__)

async def safe_operation():
    try:
        # Your operation here
        result = await risky_function()
        return result
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        # Implement fallback or recovery
        return fallback_result
```

### 3. Configuration Management
```python
# Use environment variables with defaults
class Config:
    CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    WORKING_DIR = os.getenv("WORKING_DIR", "./data")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

### 4. Performance Optimization
```python
# Use async processing for multiple requests
async def process_multiple_queries(queries):
    tasks = [rag.aquery(query) for query in queries]
    results = await asyncio.gather(*tasks)
    return results

# Cache embeddings for repeated texts
from functools import lru_cache

@lru_cache(maxsize=1000)
async def cached_embedding(text):
    return await embedding_func([text])
```

### 5. Security Considerations
```python
# Never commit secrets
# .env files should be in .gitignore

# Use secret management
import os
api_key = os.getenv("CLOUDFLARE_API_KEY")
if not api_key:
    raise ValueError("CLOUDFLARE_API_KEY not set")

# Validate inputs
def sanitize_text(text):
    # Remove potentially harmful content
    return text.strip()[:10000]  # Limit length
```

## 🎯 Next Steps

1. ✅ Set up development environment
2. ✅ Implement Cloudflare Worker integration
3. ✅ Add Hugging Face dataset support
4. ✅ Create comprehensive example script
5. 🔄 Test with real datasets
6. 🔄 Optimize performance
7. 🔄 Add monitoring and alerting
8. 🔄 Create deployment pipeline

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/HKUDS/LightRAG/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HKUDS/LightRAG/discussions)
- **Documentation**: [LightRAG Docs](https://lightrag.readthedocs.io/)

---

**Note**: This guide assumes you're working with the latest version of LightRAG. Always check the official documentation for the most up-to-date information.