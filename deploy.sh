#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to validate environment variables
validate_env() {
    local env_file="$1"

    if [ ! -f "$env_file" ]; then
        print_error "Environment file $env_file not found!"
        return 1
    fi

    # Check for required variables
    local required_vars=("LLM_BINDING_API_KEY" "EMBEDDING_BINDING_API_KEY")

    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" "$env_file" || grep -q "^${var}=your-" "$env_file"; then
            print_error "Required variable $var is not set or has default placeholder value in $env_file"
            return 1
        fi
    done

    # Check Cloudflare configuration if enabled
    if grep -q "^USE_CLOUDFLARE_GATEWAY=true" "$env_file"; then
        local cf_vars=("CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_GATEWAY_ID" "CLOUDFLARE_API_KEY")
        for var in "${cf_vars[@]}"; do
            if ! grep -q "^${var}=" "$env_file" || grep -q "^${var}=your-" "$env_file"; then
                print_error "Cloudflare variable $var is not set or has default placeholder value in $env_file"
                return 1
            fi
        done
    fi

    print_success "Environment validation passed"
    return 0
}

# Function to setup environment
setup_environment() {
    print_info "Setting up deployment environment..."

    # Create necessary directories
    mkdir -p data/rag_storage
    mkdir -p data/inputs
    mkdir -p logs
    mkdir -p ssl

    # Set proper permissions
    chmod 755 data logs ssl

    print_success "Environment setup completed"
}

# Function to build and deploy
deploy() {
    local env_file="${1:-.env.production}"
    local profile="${2:-}"

    print_info "Starting deployment with environment file: $env_file"

    # Validate environment
    if ! validate_env "$env_file"; then
        print_error "Environment validation failed. Please check your configuration."
        exit 1
    fi

    # Setup environment
    setup_environment

    # Copy environment file
    cp "$env_file" .env

    # Build and start services
    print_info "Building and starting Docker services..."

    if [ -n "$profile" ]; then
        docker-compose --profile "$profile" up -d --build
    else
        docker-compose up -d --build
    fi

    # Wait for services to be healthy
    print_info "Waiting for services to be healthy..."
    sleep 30

    # Check service health
    if docker-compose ps | grep -q "Up"; then
        print_success "Deployment completed successfully!"
        print_info "LightRAG is now running at http://localhost:9621"
        print_info "Web UI: http://localhost:9621"
        print_info "API Docs: http://localhost:9621/docs"

        if [ "$profile" = "production" ]; then
            print_info "Production deployment with Nginx at http://localhost"
        fi
    else
        print_error "Deployment failed. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    local service="${1:-}"
    if [ -n "$service" ]; then
        docker-compose logs -f "$service"
    else
        docker-compose logs -f
    fi
}

# Function to stop services
stop_services() {
    print_info "Stopping all services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to cleanup
cleanup() {
    print_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Cleaning up deployment..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        rm -rf data logs
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Function to show usage
usage() {
    cat << EOF
LightRAG Docker Deployment Script

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    deploy [env_file] [profile]    Deploy LightRAG (default: .env.production)
    logs [service]                 Show logs for all services or specific service
    stop                           Stop all services
    cleanup                        Remove all containers, volumes, and data
    setup                          Setup deployment environment
    validate [env_file]            Validate environment configuration

EXAMPLES:
    $0 deploy                      # Deploy with default production config
    $0 deploy .env.local           # Deploy with custom environment file
    $0 deploy .env.production production  # Deploy with production profile
    $0 logs                        # Show all logs
    $0 logs lightrag               # Show LightRAG logs only
    $0 stop                        # Stop all services
    $0 validate .env.production    # Validate production config

ENVIRONMENT FILES:
    .env.production                Production configuration with Cloudflare Gateway
    .env.local                     Local development configuration

PROFILES:
    production                     Includes Nginx reverse proxy
    (default)                      Basic deployment without Nginx

EOF
}

# Main script logic
case "${1:-}" in
    deploy)
        deploy "${2:-.env.production}" "${3:-}"
        ;;
    logs)
        show_logs "${2:-}"
        ;;
    stop)
        stop_services
        ;;
    cleanup)
        cleanup
        ;;
    setup)
        setup_environment
        ;;
    validate)
        validate_env "${2:-.env.production}"
        ;;
    *)
        usage
        ;;
esac