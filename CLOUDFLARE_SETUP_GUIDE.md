# 🚀 Cloudflare AI Gateway Setup Guide for LightRAG

This guide will help you configure Cloudflare AI Gateway for your LightRAG deployment using the automated setup script.

## 📋 Prerequisites

1. **Node.js and npm** installed on your system
2. **Cloudflare account** with AI Gateway access
3. **Wrangler CLI** (will be installed automatically)

## ⚡ Quick Setup (Automated)

### Step 1: Run the Setup Script

```bash
# For local development
./setup-cloudflare.sh

# For production environment
./setup-cloudflare.sh .env.production

# With custom gateway name
./setup-cloudflare.sh .env.local my-custom-gateway
```

### Step 2: Follow the Interactive Setup

The script will:
1. ✅ Check prerequisites
2. ✅ Install Wrangler CLI if needed
3. ✅ Authenticate with Cloudflare
4. ✅ Create AI Gateway
5. ✅ Generate API token (manual step)
6. ✅ Update your environment file
7. ✅ Test the configuration

## 🔧 Manual Setup (Alternative)

If you prefer to set up manually or the automated script fails:

### Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

### Step 2: Authenticate with Cloudflare

```bash
npx wrangler auth login
```

### Step 3: Create AI Gateway

```bash
# Create a new AI Gateway
npx wrangler ai gateway create lightrag-gateway

# List your gateways to get the ID
npx wrangler ai gateway list
```

### Step 4: Create API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. Click **"Create Token"**
3. Choose **"Create Custom Token"**
4. Configure the token:
   - **Name**: `lightrag-gateway-token`
   - **Permissions**: `AI Gateway - AI Gateway - Edit`
   - **Resources**: Your account
5. Click **"Create"** and copy the token

### Step 5: Get Your Account ID

```bash
# Get your account information
npx wrangler whoami
```

### Step 6: Update Environment Variables

Edit your `.env.local` or `.env.production` file:

```bash
# Enable Cloudflare Gateway
USE_CLOUDFLARE_GATEWAY=true

# Your Cloudflare credentials
CLOUDFLARE_ACCOUNT_ID=your-account-id-here
CLOUDFLARE_GATEWAY_ID=your-gateway-id-here
CLOUDFLARE_API_KEY=your-api-token-here

# LLM Configuration (will use gateway automatically)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_BINDING_API_KEY=${CLOUDFLARE_API_KEY}

# Embedding Configuration (will use gateway automatically)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_BINDING_API_KEY=${CLOUDFLARE_API_KEY}
```

## 🧪 Testing Your Setup

### Test Gateway Connection

```bash
# Test the gateway endpoint
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "https://gateway.ai.cloudflare.com/v1/YOUR_ACCOUNT_ID/YOUR_GATEWAY_ID/openai/models"
```

### Deploy and Test LightRAG

```bash
# Deploy with your configuration
./deploy.sh deploy .env.local

# Check if LightRAG is using the gateway
docker-compose logs lightrag | grep "Cloudflare AI Gateway"
```

## 📊 Monitoring Your Gateway

### View Gateway Analytics

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **AI > AI Gateway**
3. Select your gateway
4. View **Analytics** tab for:
   - Request volume
   - Response times
   - Error rates
   - Cost savings

### Check Logs

```bash
# View gateway logs
npx wrangler tail

# View LightRAG logs
docker-compose logs -f lightrag
```

## ⚙️ Advanced Configuration

### Gateway Settings

You can configure additional gateway settings through the Cloudflare Dashboard:

1. **Rate Limiting**: Set request limits per minute/hour
2. **Caching**: Configure cache TTL and policies
3. **Fallbacks**: Set fallback providers
4. **Cost Limits**: Set spending limits

### Multiple Gateways

Create separate gateways for different environments:

```bash
# Development gateway
npx wrangler ai gateway create lightrag-dev

# Production gateway
npx wrangler ai gateway create lightrag-prod
```

### Custom Gateway Configuration

```bash
# Update gateway settings
npx wrangler ai gateway update lightrag-gateway \
  --rate-limit=100 \
  --cache-ttl=3600
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Failed
```bash
# Re-authenticate
npx wrangler auth login
```

#### 2. Gateway Creation Failed
```bash
# Check account permissions
npx wrangler whoami

# Verify AI Gateway is enabled for your account
```

#### 3. API Token Issues
- Ensure token has correct permissions
- Check token hasn't expired
- Verify token is for the correct account

#### 4. Environment Variables Not Working
```bash
# Check variable substitution
docker-compose exec lightrag env | grep CLOUDFLARE

# Restart services after env changes
docker-compose restart
```

#### 5. Gateway Not Being Used
```bash
# Check logs for gateway configuration
docker-compose logs lightrag | grep -i gateway

# Verify LLM_BINDING_HOST is set correctly
docker-compose exec lightrag env | grep LLM_BINDING_HOST
```

### Debug Commands

```bash
# Check gateway status
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://gateway.ai.cloudflare.com/v1/YOUR_ACCOUNT/YOUR_GATEWAY/openai/models"

# Test direct OpenAI (bypass gateway)
curl -H "Authorization: Bearer YOUR_OPENAI_KEY" \
     "https://api.openai.com/v1/models"

# Check Docker network
docker-compose ps
docker network ls
```

## 📚 Additional Resources

- [Cloudflare AI Gateway Documentation](https://developers.cloudflare.com/ai-gateway/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/)
- [LightRAG Documentation](./DOCKER_DEPLOYMENT_README.md)

## 🎯 Next Steps

1. ✅ Configure Cloudflare AI Gateway
2. ✅ Update environment variables
3. ✅ Deploy LightRAG with Docker
4. ✅ Test the integration
5. 🔄 Monitor performance and costs
6. 🔄 Optimize gateway settings as needed

---

**Note**: The automated setup script handles most of these steps for you. If you encounter issues, the manual setup provides more control over the configuration process.