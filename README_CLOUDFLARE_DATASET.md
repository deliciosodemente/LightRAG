# LightRAG Cloudflare Worker Dataset Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![LightRAG](https://img.shields.io/badge/LightRAG-Latest-green.svg)](https://github.com/HKUDS/LightRAG)
[![Cloudflare](https://img.shields.io/badge/Cloudflare-Workers-orange.svg)](https://workers.cloudflare.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Datasets-yellow.svg)](https://huggingface.co/datasets)

A comprehensive integration that combines LightRAG's knowledge graph capabilities with Cloudflare Workers for AI inference and Hugging Face datasets for data ingestion.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🚀 **Seamless Integration**: Combine LightRAG, Cloudflare Workers, and Hugging Face datasets
- 🤖 **AI-Powered**: Use Cloudflare's AI models for LLM and embeddings
- 📊 **Dataset Support**: Load and process Hugging Face datasets automatically
- 🔒 **Secure**: Proper authentication and credential management
- ⚡ **High Performance**: Async processing with batch operations
- 🛠️ **Developer Friendly**: Comprehensive logging and error handling
- 📈 **Scalable**: Handle large datasets with efficient processing
- 🧪 **Well Tested**: Comprehensive test suite with mocking

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16+ (for Wrangler CLI)
- **Git**: For version control

### Accounts & API Keys
- **Cloudflare Account**: With Workers and AI Gateway access
- **Hugging Face Account**: (Optional) For private datasets
- **GitHub Account**: For code contributions

### Dependencies
```bash
# Core dependencies
pip install lightrag datasets requests numpy python-dotenv

# Development dependencies
pip install pytest mock tenacity

# Cloudflare CLI
npm install -g wrangler
```

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd lightrag-cloudflare-dataset
   pip install -e .
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the demo**:
   ```bash
   python examples/lightrag_hf_cloudflare_dataset_demo.py
   ```

4. **Test the integration**:
   ```bash
   python test_connectivity.py
   ```

## 📦 Installation

### Option 1: From Source
```bash
git clone https://github.com/your-org/lightrag-cloudflare-dataset.git
cd lightrag-cloudflare-dataset
pip install -e .
```

### Option 2: Docker
```bash
docker build -t lightrag-cloudflare .
docker run -p 8000:8000 lightrag-cloudflare
```

### Option 3: Docker Compose
```bash
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Cloudflare Configuration
CLOUDFLARE_API_KEY=your_cloudflare_api_key_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here

# Hugging Face Configuration (optional)
HF_TOKEN=your_huggingface_token_here

# LightRAG Configuration
WORKING_DIR=./data
LOG_DIR=./logs
VERBOSE_DEBUG=false

# AI Model Configuration
LLM_MODEL=@cf/meta/llama-3.2-3b-instruct
EMBEDDING_MODEL=@cf/baai/bge-m3
EMBEDDING_DIM=1024
```

### Cloudflare Setup

1. **Authenticate with Cloudflare**:
   ```bash
   npx wrangler auth login
   ```

2. **Create AI Gateway**:
   ```bash
   npx wrangler ai gateway create lightrag-gateway
   ```

3. **Get your account information**:
   ```bash
   npx wrangler whoami
   ```

## 💡 Usage

### Basic Usage

```python
from examples.lightrag_hf_cloudflare_dataset_demo import main
import asyncio

# Run the complete integration
asyncio.run(main())
```

### Custom Dataset Integration

```python
from datasets import load_dataset
from lightrag import LightRAG
from examples.lightrag_hf_cloudflare_dataset_demo import (
    CloudflareWorker,
    process_dataset_entries
)

# Load your dataset
dataset = load_dataset("your-dataset-name")
texts = process_dataset_entries(dataset)

# Initialize with Cloudflare
cloudflare_worker = CloudflareWorker(
    cloudflare_api_key="your-key",
    account_id="your-account",
    llm_model_name="@cf/meta/llama-3.2-3b-instruct",
    embedding_model_name="@cf/baai/bge-m3"
)

# Create LightRAG instance
rag = LightRAG(
    working_dir="./data",
    llm_model_func=cloudflare_worker.query,
    embedding_func=cloudflare_worker.embedding_chunk
)

# Insert data
await rag.ainsert(texts)

# Query
result = await rag.aquery("What is this dataset about?")
print(result)
```

### Advanced Configuration

```python
# Custom processing pipeline
async def custom_processing_pipeline(dataset_name, config):
    # Load dataset
    dataset = load_dataset(dataset_name)

    # Custom preprocessing
    processed_texts = []
    for entry in dataset['train']:
        # Your custom logic here
        text = preprocess_entry(entry)
        if text:
            processed_texts.append(text)

    # Initialize RAG with custom config
    rag = await initialize_rag_with_config(config)

    # Batch insert with progress tracking
    batch_size = 100
    for i in range(0, len(processed_texts), batch_size):
        batch = processed_texts[i:i + batch_size]
        await rag.ainsert(batch)
        print(f"Processed {i + len(batch)}/{len(processed_texts)} entries")

    return rag
```

## 📚 API Reference

### CloudflareWorker Class

```python
class CloudflareWorker:
    def __init__(self, cloudflare_api_key, api_base_url, llm_model_name, embedding_model_name)
    async def query(self, prompt, system_prompt="", **kwargs) -> str
    async def embedding_chunk(self, texts: list[str]) -> np.ndarray
```

### Dataset Processing Functions

```python
def load_hf_dataset_with_auth(dataset_name: str, token: str = None) -> Dataset
def process_dataset_entries(dataset) -> list[str]
```

### LightRAG Integration

```python
async def initialize_rag() -> LightRAG
async def process_and_insert_dataset(rag: LightRAG, dataset) -> None
```

## 🧪 Testing

### Run All Tests
```bash
# Run the connectivity test
python test_connectivity.py

# Run with verbose output
python test_connectivity.py --verbose

# Run specific test categories
python test_connectivity.py --test imports
python test_connectivity.py --test cloudflare
python test_connectivity.py --test dataset
```

### Test Coverage

The test suite covers:
- ✅ **Import Validation**: Ensures all dependencies are available
- ✅ **Cloudflare Worker**: Tests class structure and methods
- ✅ **Dataset Processing**: Validates data transformation functions
- ✅ **Configuration**: Tests environment variable handling
- ✅ **Error Handling**: Verifies robust error management
- ✅ **Connectivity**: Mocks network calls for safe testing

### Writing Custom Tests

```python
import pytest
from unittest.mock import Mock, patch
from examples.lightrag_hf_cloudflare_dataset_demo import CloudflareWorker

def test_custom_cloudflare_integration():
    # Mock the requests module
    with patch('examples.lightrag_hf_cloudflare_dataset_demo.requests') as mock_requests:
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"result": {"response": "Test response"}}
        mock_requests.post.return_value = mock_response

        # Test your integration
        worker = CloudflareWorker("test_key", "test_url", "test_llm", "test_emb")
        result = await worker.query("Test prompt")

        assert result == "Test response"
        mock_requests.post.assert_called_once()
```

## 🚢 Deployment

### Local Development
```bash
# Start development server
python examples/lightrag_hf_cloudflare_dataset_demo.py

# With custom configuration
WORKING_DIR=./dev_data LOG_DIR=./dev_logs python examples/lightrag_hf_cloudflare_dataset_demo.py
```

### Production Deployment
```bash
# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Using the deployment script
./deploy.sh deploy .env.production

# Check deployment status
docker-compose logs -f lightrag
```

### Cloudflare Worker Deployment
```bash
# Deploy to Cloudflare Workers
npx wrangler deploy

# Check deployment
npx wrangler tail
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Install missing dependencies
pip install lightrag datasets requests numpy python-dotenv

# Check Python version
python --version  # Should be 3.8+
```

#### 2. Cloudflare Authentication
```bash
# Re-authenticate
npx wrangler auth login

# Check account
npx wrangler whoami

# Verify API key
curl -H "Authorization: Bearer YOUR_KEY" https://api.cloudflare.com/client/v4/user
```

#### 3. Dataset Loading Issues
```python
# Test dataset access
from datasets import load_dataset
try:
    ds = load_dataset("deli333777/data")
    print("Dataset accessible")
except Exception as e:
    print(f"Dataset error: {e}")
```

#### 4. Memory Issues
```python
# Process in smaller batches
BATCH_SIZE = 50  # Reduce from default 100

# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")
```

### Debug Mode
```bash
# Enable verbose logging
export VERBOSE_DEBUG=true

# Run with debug output
python examples/lightrag_hf_cloudflare_dataset_demo.py 2>&1 | tee debug.log
```

### Performance Optimization
```python
# Adjust concurrency settings
MAX_PARALLEL_INSERT = 2  # Reduce for lower memory usage
EMBEDDING_BATCH_SIZE = 10  # Smaller batches for embeddings

# Use connection pooling
import aiohttp
connector = aiohttp.TCPConnector(limit=10)  # Limit concurrent connections
```

## 🤝 Contributing

### Development Setup
```bash
# Fork the repository
git clone https://github.com/your-org/lightrag-cloudflare-dataset.git
cd lightrag-cloudflare-dataset

# Create feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -e ".[dev]"
```

### Code Standards
```bash
# Run linting
black examples/ test_*.py
flake8 examples/ test_*.py

# Run tests
pytest tests/ -v --cov=examples

# Type checking
mypy examples/ --ignore-missing-imports
```

### Pull Request Process
1. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
2. **Make Changes**: Implement your feature with tests
3. **Run Tests**: Ensure all tests pass
4. **Update Documentation**: Add usage examples if needed
5. **Commit Changes**: Use conventional commit messages
6. **Push Branch**: `git push origin feature/amazing-feature`
7. **Create PR**: Open a pull request with detailed description

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LightRAG](https://github.com/HKUDS/LightRAG) - The core RAG framework
- [Cloudflare Workers](https://workers.cloudflare.com/) - AI inference platform
- [Hugging Face](https://huggingface.co/) - Dataset hosting platform
- [OpenAI](https://openai.com/) - AI model inspiration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/lightrag-cloudflare-dataset/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/lightrag-cloudflare-dataset/discussions)
- **Documentation**: [Wiki](https://github.com/your-org/lightrag-cloudflare-dataset/wiki)

---

**Happy coding! 🚀**

For more information, visit the [LightRAG Cloudflare Dataset Integration Guide](LIGHTRAG_CLOUDFLARE_DATASET_INTEGRATION_GUIDE.md).