# LightRAG Docker Deployment Guide

This guide provides comprehensive instructions for deploying LightRAG using Docker with containerization, secure environment variable management, and Cloudflare AI Gateway integration.

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (or Docker Engine)
- Docker Compose
- Git
- At least 4GB RAM recommended

### Basic Deployment

1. **Clone and navigate to the repository:**
   ```bash
   git clone https://github.com/HKUDS/LightRAG.git
   cd LightRAG
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.production .env
   # Edit .env with your API keys and configuration
   ```

3. **Deploy using the deployment script:**
   ```bash
   ./deploy.sh deploy
   ```

4. **Access the application:**
   - Web UI: http://localhost:9621
   - API Docs: http://localhost:9621/docs
   - Health Check: http://localhost:9621/health

## 📋 Detailed Configuration

### Environment Variables Setup

#### Required Variables

Edit `.env.production` and configure these essential variables:

```bash
# API Keys (replace with your actual keys)
LLM_BINDING_API_KEY=your-openai-api-key
EMBEDDING_BINDING_API_KEY=your-openai-embedding-key
LIGHTRAG_API_KEY=your-secure-api-key

# Database (if using PostgreSQL)
POSTGRES_PASSWORD=your-secure-postgres-password
```

#### Cloudflare AI Gateway Configuration

To enable Cloudflare AI Gateway for enhanced security and performance:

1. **Create a Cloudflare AI Gateway:**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - Navigate to AI > AI Gateway
   - Create a new gateway
   - Note your Account ID and Gateway ID

2. **Configure environment variables:**
   ```bash
   USE_CLOUDFLARE_GATEWAY=true
   CLOUDFLARE_ACCOUNT_ID=your-account-id
   CLOUDFLARE_GATEWAY_ID=your-gateway-id
   CLOUDFLARE_API_KEY=your-cloudflare-api-key
   ```

3. **The system will automatically configure:**
   - LLM requests to route through Cloudflare Gateway
   - Embedding requests to use Cloudflare Gateway
   - Rate limiting and caching via Cloudflare

### Storage Options

#### Option 1: Default (File-based)
No additional configuration needed. Data persists in `./data/` directory.

#### Option 2: PostgreSQL (Production Recommended)
```bash
# Enable PostgreSQL storage
LIGHTRAG_KV_STORAGE=PGKVStorage
LIGHTRAG_VECTOR_STORAGE=PGVectorStorage
LIGHTRAG_GRAPH_STORAGE=PGGraphStorage
LIGHTRAG_DOC_STATUS_STORAGE=PGDocStatusStorage

# PostgreSQL connection
POSTGRES_HOST=postgres
POSTGRES_USER=lightrag
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DATABASE=lightrag
```

#### Option 3: Redis + PostgreSQL
```bash
# Use Redis for caching, PostgreSQL for persistence
LIGHTRAG_KV_STORAGE=RedisKVStorage
LIGHTRAG_DOC_STATUS_STORAGE=RedisDocStatusStorage
LIGHTRAG_VECTOR_STORAGE=PGVectorStorage
LIGHTRAG_GRAPH_STORAGE=PGGraphStorage
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │  Cloudflare AI  │
│   (Optional)    │    │     Gateway     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └─────────┬────────────┘
                    │
          ┌─────────▼────────────┐
          │   LightRAG Server    │
          │   (FastAPI + WebUI)  │
          └─────────┬────────────┘
                    │
          ┌─────────▼────────────┐
          │     Databases        │
          │ PostgreSQL + Redis   │
          └──────────────────────┘
```

### Services

- **LightRAG Server**: Main application with API and WebUI
- **PostgreSQL**: Primary database for production
- **Redis**: Caching and session storage
- **Nginx**: Reverse proxy for production deployments

## 🚀 Deployment Options

### Development Deployment

```bash
# Quick development setup
./deploy.sh deploy .env.local
```

### Production Deployment

```bash
# Full production deployment with Nginx
./deploy.sh deploy .env.production production
```

### Custom Deployment

```bash
# Deploy with custom environment file
./deploy.sh deploy path/to/your/.env
```

## 🔒 Security Best Practices

### Environment Variables

1. **Never commit secrets to version control**
2. **Use strong, unique passwords**
3. **Rotate API keys regularly**
4. **Use environment-specific configurations**

### Network Security

1. **Enable SSL/TLS in production:**
   ```bash
   SSL=true
   SSL_CERTFILE=/path/to/cert.pem
   SSL_KEYFILE=/path/to/key.pem
   ```

2. **Configure firewall rules**
3. **Use internal networking for database connections**

### API Security

1. **Enable API key authentication:**
   ```bash
   LIGHTRAG_API_KEY=your-secure-api-key
   ```

2. **Configure JWT authentication for WebUI:**
   ```bash
   AUTH_ACCOUNTS=admin:secure-password
   TOKEN_SECRET=your-jwt-secret
   ```

## 📊 Monitoring and Maintenance

### Health Checks

The application includes built-in health checks:
- Container health: `docker-compose ps`
- Application health: `curl http://localhost:9621/health`
- Database connectivity: Check logs for connection errors

### Logs

```bash
# View all logs
./deploy.sh logs

# View specific service logs
./deploy.sh logs lightrag

# View with follow
docker-compose logs -f lightrag
```

### Backup and Recovery

#### Database Backup
```bash
# PostgreSQL backup
docker exec lightrag_postgres pg_dump -U lightrag lightrag > backup.sql

# Restore
docker exec -i lightrag_postgres psql -U lightrag lightrag < backup.sql
```

#### Data Directory Backup
```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Updates

```bash
# Update and rebuild
git pull
docker-compose build --no-cache
docker-compose up -d
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :9621

# Change port in .env
PORT=9622
```

#### 2. Database Connection Failed
```bash
# Check database logs
docker-compose logs postgres

# Verify connection
docker exec lightrag_postgres psql -U lightrag -d lightrag -c "SELECT 1;"
```

#### 3. API Key Issues
```bash
# Test API key
curl -H "X-API-Key: your-api-key" http://localhost:9621/health
```

#### 4. Cloudflare Gateway Issues
```bash
# Check gateway configuration
curl -H "Authorization: Bearer your-cloudflare-key" \
     https://gateway.ai.cloudflare.com/v1/your-account-id/your-gateway-id/openai/models
```

### Performance Tuning

#### Memory Optimization
```bash
# Adjust worker count based on available RAM
WORKERS=2  # For 8GB RAM
WORKERS=4  # For 16GB+ RAM
```

#### Concurrency Settings
```bash
# Adjust based on LLM provider limits
MAX_ASYNC=4          # Concurrent LLM requests
MAX_PARALLEL_INSERT=2 # Parallel document processing
```

## 🔧 Advanced Configuration

### Custom Nginx Configuration

Edit `nginx.conf` for custom proxy settings, SSL configuration, or additional security headers.

### Database Optimization

#### PostgreSQL Tuning
```bash
# Connection pooling
POSTGRES_MAX_CONNECTIONS=20

# Vector index optimization
POSTGRES_HNSW_M=16
POSTGRES_HNSW_EF=200
```

#### Redis Configuration
```bash
# Redis performance tuning
REDIS_MAX_CONNECTIONS=100
REDIS_SOCKET_TIMEOUT=30
```

### Scaling

#### Horizontal Scaling
```bash
# Run multiple instances
docker-compose up -d --scale lightrag=3
```

#### Load Balancing
Use Nginx upstream configuration for load balancing across multiple instances.

## 📚 API Usage Examples

### Python Client
```python
import requests

headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:9621/query",
    headers=headers,
    json={"query": "What is LightRAG?"}
)

print(response.json())
```

### cURL
```bash
curl -X POST "http://localhost:9621/query" \
     -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is LightRAG?"}'
```

### JavaScript
```javascript
fetch('http://localhost:9621/query', {
    method: 'POST',
    headers: {
        'X-API-Key': 'your-api-key',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: 'What is LightRAG?' })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎯 Next Steps

1. **Configure your LLM provider** (OpenAI, Anthropic, etc.)
2. **Set up Cloudflare AI Gateway** for production
3. **Configure persistent storage** (PostgreSQL recommended)
4. **Enable SSL/TLS** for secure connections
5. **Set up monitoring** and alerting
6. **Configure backup strategies**

## 📞 Support

- **Documentation**: [LightRAG Docs](https://github.com/HKUDS/LightRAG)
- **Issues**: [GitHub Issues](https://github.com/HKUDS/LightRAG/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HKUDS/LightRAG/discussions)

---

**Note**: This deployment provides a production-ready setup with security, scalability, and monitoring capabilities. Always test thoroughly in a staging environment before deploying to production.