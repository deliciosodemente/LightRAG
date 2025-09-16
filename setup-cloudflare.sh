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

# Function to get Cloudflare account info
get_cloudflare_info() {
    print_info "Getting Cloudflare account information..."

    # Check if wrangler is authenticated
    if ! npx wrangler auth status >/dev/null 2>&1; then
        print_warning "Wrangler is not authenticated. Please run:"
        echo "npx wrangler auth login"
        exit 1
    fi

    # Get account ID
    print_info "Fetching your Cloudflare account ID..."
    ACCOUNT_ID=$(npx wrangler whoami | grep "Account ID" | awk '{print $3}')

    if [ -z "$ACCOUNT_ID" ]; then
        print_error "Could not retrieve Account ID. Please check your wrangler authentication."
        exit 1
    fi

    print_success "Account ID: $ACCOUNT_ID"
    echo "$ACCOUNT_ID"
}

# Function to create AI Gateway
create_ai_gateway() {
    local account_id="$1"
    local gateway_name="$2"

    print_info "Creating AI Gateway: $gateway_name"

    # Create the gateway using wrangler
    if npx wrangler ai gateway create "$gateway_name" >/dev/null 2>&1; then
        print_success "AI Gateway '$gateway_name' created successfully"

        # Get gateway details
        GATEWAY_ID=$(npx wrangler ai gateway list | grep "$gateway_name" | awk '{print $1}')

        if [ -z "$GATEWAY_ID" ]; then
            print_error "Could not retrieve Gateway ID"
            exit 1
        fi

        print_success "Gateway ID: $GATEWAY_ID"
        echo "$GATEWAY_ID"
    else
        print_error "Failed to create AI Gateway"
        exit 1
    fi
}

# Function to create API token
create_api_token() {
    local account_id="$1"
    local token_name="$2"

    print_info "Creating API token for AI Gateway access..."

    # Note: This requires manual creation through the dashboard
    print_warning "API Token creation requires manual setup through Cloudflare Dashboard:"
    echo ""
    echo "1. Go to https://dash.cloudflare.com/profile/api-tokens"
    echo "2. Click 'Create Token'"
    echo "3. Choose 'Create Custom Token'"
    echo "4. Set token name: '$token_name'"
    echo "5. Add permission: 'AI Gateway - AI Gateway - Edit'"
    echo "6. Add your account to the resources"
    echo "7. Create and copy the token"
    echo ""
    read -p "Enter your API token: " API_TOKEN

    if [ -z "$API_TOKEN" ]; then
        print_error "API token is required"
        exit 1
    fi

    echo "$API_TOKEN"
}

# Function to update environment file
update_env_file() {
    local env_file="$1"
    local account_id="$2"
    local gateway_id="$3"
    local api_token="$4"

    print_info "Updating environment file: $env_file"

    # Create backup
    if [ -f "$env_file" ]; then
        cp "$env_file" "${env_file}.backup"
        print_info "Backup created: ${env_file}.backup"
    fi

    # Update the environment variables
    sed -i.bak \
        -e "s/CLOUDFLARE_ACCOUNT_ID=.*/CLOUDFLARE_ACCOUNT_ID=$account_id/" \
        -e "s/CLOUDFLARE_GATEWAY_ID=.*/CLOUDFLARE_GATEWAY_ID=$gateway_id/" \
        -e "s/CLOUDFLARE_API_KEY=.*/CLOUDFLARE_API_KEY=$api_token/" \
        "$env_file"

    print_success "Environment file updated successfully"
}

# Function to test gateway configuration
test_gateway_config() {
    local account_id="$1"
    local gateway_id="$2"
    local api_token="$3"

    print_info "Testing AI Gateway configuration..."

    # Test the gateway endpoint
    local test_url="https://gateway.ai.cloudflare.com/v1/$account_id/$gateway_id/openai/models"

    if curl -s -H "Authorization: Bearer $api_token" "$test_url" >/dev/null 2>&1; then
        print_success "AI Gateway configuration is working!"
    else
        print_warning "Could not verify gateway configuration. Please check your settings."
    fi
}

# Main setup function
setup_cloudflare_gateway() {
    local env_file="${1:-.env.local}"
    local gateway_name="${2:-lightrag-gateway}"

    print_info "Setting up Cloudflare AI Gateway for LightRAG"
    echo ""

    # Check prerequisites
    if ! command_exists node || ! command_exists npm; then
        print_error "Node.js and npm are required. Please install them first."
        exit 1
    fi

    if ! command_exists npx; then
        print_error "npx is required. Please install Node.js properly."
        exit 1
    fi

    # Check if wrangler is installed
    if ! command_exists wrangler; then
        print_info "Installing Wrangler CLI..."
        npm install -g wrangler
    fi

    # Authenticate with Cloudflare
    print_info "Please authenticate with Cloudflare..."
    npx wrangler auth login

    # Get account information
    ACCOUNT_ID=$(get_cloudflare_info)

    # Create AI Gateway
    GATEWAY_ID=$(create_ai_gateway "$ACCOUNT_ID" "$gateway_name")

    # Create API token
    API_TOKEN=$(create_api_token "$ACCOUNT_ID" "$gateway_name-token")

    # Update environment file
    update_env_file "$env_file" "$ACCOUNT_ID" "$GATEWAY_ID" "$API_TOKEN"

    # Test configuration
    test_gateway_config "$ACCOUNT_ID" "$GATEWAY_ID" "$API_TOKEN"

    print_success "Cloudflare AI Gateway setup completed!"
    echo ""
    print_info "Configuration Summary:"
    echo "  Account ID: $ACCOUNT_ID"
    echo "  Gateway ID: $GATEWAY_ID"
    echo "  Gateway Name: $gateway_name"
    echo "  Environment File: $env_file"
    echo ""
    print_info "Next steps:"
    echo "1. Review and update your OpenAI API keys in $env_file"
    echo "2. Run: ./deploy.sh deploy $env_file"
    echo "3. Access LightRAG at http://localhost:9621"
}

# Function to show usage
usage() {
    cat << EOF
Cloudflare AI Gateway Setup Script for LightRAG

USAGE:
    $0 [ENV_FILE] [GATEWAY_NAME]

ARGUMENTS:
    ENV_FILE        Environment file to update (default: .env.local)
    GATEWAY_NAME    Name for the AI Gateway (default: lightrag-gateway)

EXAMPLES:
    $0                          # Setup with defaults
    $0 .env.production          # Setup for production
    $0 .env.local my-gateway    # Custom gateway name

PREREQUISITES:
    - Node.js and npm installed
    - Cloudflare account
    - Wrangler CLI (will be installed if missing)

EOF
}

# Main script logic
case "${1:-}" in
    -h|--help)
        usage
        ;;
    *)
        setup_cloudflare_gateway "${1:-.env.local}" "${2:-lightrag-gateway}"
        ;;
esac