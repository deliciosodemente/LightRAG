# 🚀 Quick Cloudflare AI Gateway Setup for Production

Since the automated script requires interactive input, let's set up Cloudflare manually:

## Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

## Step 2: Authenticate with Cloudflare

```bash
npx wrangler auth login
```

Follow the browser login process.

## Step 3: Create AI Gateway

```bash
# Create a new gateway
npx wrangler ai gateway create lightrag-prod-gateway

# List gateways to get the ID
npx wrangler ai gateway list
```

## Step 4: Create API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Choose "Create Custom Token"
4. Name: `lightrag-prod-token`
5. Permissions: `AI Gateway - AI Gateway - Edit`
6. Resources: Your account
7. Create and copy the token

## Step 5: Get Your Account ID

```bash
npx wrangler whoami
```

## Step 6: Update .env.production

Replace these lines in `.env.production`:

```bash
# Replace with your actual values:
CLOUDFLARE_ACCOUNT_ID=YOUR_ACCOUNT_ID_HERE
CLOUDFLARE_GATEWAY_ID=YOUR_GATEWAY_ID_HERE
CLOUDFLARE_API_KEY=YOUR_API_TOKEN_HERE

# Also update these:
LIGHTRAG_API_KEY=your-secure-production-api-key-here
POSTGRES_PASSWORD=your-secure-postgres-password
```

## Step 7: Deploy

```bash
deploy.bat deploy .env.production production
```

## Alternative: Skip Cloudflare for now

If you want to deploy immediately without Cloudflare:

1. Edit `.env.production` and set:
   ```bash
   USE_CLOUDFLARE_GATEWAY=false
   LLM_BINDING_API_KEY=your-openai-api-key
   EMBEDDING_BINDING_API_KEY=your-openai-embedding-key
   ```

2. Deploy:
   ```bash
   deploy.bat deploy .env.production
   ```

Which option would you like to use?