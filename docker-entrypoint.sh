#!/bin/bash
set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting LightRAG Docker container..."

# Create necessary directories if they don't exist
mkdir -p /app/data/rag_storage
mkdir -p /app/data/inputs
mkdir -p /app/logs
mkdir -p /app/temp/tiktoken

# Set proper permissions (skip if chown fails - common on Windows mounts)
if chown -R lightrag:lightrag /app/data 2>/dev/null; then
    log "Data directory permissions set successfully"
else
    log "Warning: Could not set data directory permissions (normal on Windows mounts)"
fi

if chown -R lightrag:lightrag /app/logs 2>/dev/null; then
    log "Logs directory permissions set successfully"
else
    log "Warning: Could not set logs directory permissions (normal on Windows mounts)"
fi

if chown -R lightrag:lightrag /app/temp 2>/dev/null; then
    log "Temp directory permissions set successfully"
else
    log "Warning: Could not set temp directory permissions (normal on Windows mounts)"
fi

# Configure Cloudflare AI Gateway if enabled
if [ "${USE_CLOUDFLARE_GATEWAY}" = "true" ]; then
    log "Configuring Cloudflare AI Gateway..."

    if [ -z "${CLOUDFLARE_ACCOUNT_ID}" ] || [ -z "${CLOUDFLARE_GATEWAY_ID}" ]; then
        log "ERROR: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_GATEWAY_ID must be set when USE_CLOUDFLARE_GATEWAY=true"
        exit 1
    fi

    # Set LLM binding host to Cloudflare Gateway
    export LLM_BINDING_HOST="https://gateway.ai.cloudflare.com/v1/${CLOUDFLARE_ACCOUNT_ID}/${CLOUDFLARE_GATEWAY_ID}/openai"

    # Set embedding host to Cloudflare Gateway if using OpenAI embeddings
    if [ "${EMBEDDING_BINDING}" = "openai" ]; then
        export EMBEDDING_BINDING_HOST="https://gateway.ai.cloudflare.com/v1/${CLOUDFLARE_ACCOUNT_ID}/${CLOUDFLARE_GATEWAY_ID}/openai"
    fi

    # Use Cloudflare API key if provided
    if [ -n "${CLOUDFLARE_API_KEY}" ]; then
        export LLM_BINDING_API_KEY="${CLOUDFLARE_API_KEY}"
        if [ "${EMBEDDING_BINDING}" = "openai" ]; then
            export EMBEDDING_BINDING_API_KEY="${CLOUDFLARE_API_KEY}"
        fi
    fi

    log "Cloudflare AI Gateway configured successfully"
    log "LLM Gateway URL: ${LLM_BINDING_HOST}"
else
    log "Using direct API connections (Cloudflare Gateway disabled)"
fi

# Wait for database services if using external databases
if [ "${LIGHTRAG_KV_STORAGE}" = "PGKVStorage" ]; then
    log "Waiting for PostgreSQL to be ready..."
    while ! nc -z postgres 5432; do
        sleep 1
    done
    log "PostgreSQL is ready"
fi

if [ "${LIGHTRAG_KV_STORAGE}" = "RedisKVStorage" ]; then
    log "Waiting for Redis to be ready..."
    while ! nc -z redis 6379; do
        sleep 1
    done
    log "Redis is ready"
fi

# Run database migrations/initialization if needed
# (Add any initialization scripts here)

log "Starting LightRAG server..."
exec "$@"