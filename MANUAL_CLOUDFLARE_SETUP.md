# 🔧 Manual Cloudflare AI Gateway Setup

Since the automated authentication isn't working in this environment, let's set up Cloudflare manually:

## Step 1: Create AI Gateway

1. **Go to Cloudflare Dashboard:**
   - Visit: https://dash.cloudflare.com/
   - Log in to your account

2. **Navigate to AI Gateway:**
   - Click on "AI" in the sidebar
   - Click on "AI Gateway"
   - Click "Create Gateway"

3. **Create Gateway:**
   - Name: `lightrag-production`
   - Click "Create"

4. **Copy Gateway ID:**
   - After creation, copy the Gateway ID from the list
   - It will look like: `abc123def456...`

## Step 2: Create API Token

1. **Go to API Tokens:**
   - Visit: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"

2. **Create Custom Token:**
   - Name: `lightrag-production-token`
   - Permissions: Add `AI Gateway - AI Gateway - Edit`
   - Resources: Select your account
   - Click "Create Token"

3. **Copy Token:**
   - Copy the generated token immediately
   - Keep it secure!

## Step 3: Get Account ID

1. **Go to Account Settings:**
   - In Cloudflare Dashboard, click on your account name
   - The Account ID is shown in the URL or account details
   - It looks like: `1234567890abcdef...`

## Step 4: Update Environment File

Edit `.env.production` and replace these values:

```bash
# Replace with your actual values:
CLOUDFLARE_ACCOUNT_ID=YOUR_ACCOUNT_ID_HERE
CLOUDFLARE_GATEWAY_ID=YOUR_GATEWAY_ID_HERE
CLOUDFLARE_API_KEY=YOUR_API_TOKEN_HERE

# Also set these:
LIGHTRAG_API_KEY=your-secure-production-api-key-here
POSTGRES_PASSWORD=your-secure-postgres-password
```

## Step 5: Deploy

```bash
deploy.bat deploy .env.production production
```

## 📋 Your Values to Collect:

- **Account ID**: _______________
- **Gateway ID**: _______________
- **API Token**: _______________
- **API Key**: _______________
- **DB Password**: _______________

Once you have these values, let me know and I'll help you update the environment file and deploy!