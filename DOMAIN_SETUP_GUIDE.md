# 🌐 Domain Setup: radhikatmosphere.com + Cloudflare AI Gateway

## 📋 Current Status
- ✅ **Cloudflare authenticated** with account ID: `d63a3181701030f91121871e55a0a46c`
- ✅ **Domain to configure**: `radhikatmosphere.com`
- ⏳ **AI Gateway creation** needed
- ⏳ **Domain verification** needed

## 🚀 Complete Setup Process

### Step 1: Add Domain to Cloudflare (if not already added)

1. **Go to Cloudflare Dashboard:**
   - Visit: https://dash.cloudflare.com/

2. **Add Site:**
   - Click "Add Site" or "Add a Domain"
   - Enter: `radhikatmosphere.com`
   - Click "Add Site"

3. **Update Nameservers:**
   - Cloudflare will provide 2 nameservers
   - Update these at your domain registrar
   - Wait for DNS propagation (can take 24-48 hours)

### Step 2: Create AI Gateway

1. **Navigate to AI Gateway:**
   - In Cloudflare Dashboard, click "AI" in sidebar
   - Click "AI Gateway"
   - Click "Create Gateway"

2. **Configure Gateway:**
   - **Name**: `radhikatmosphere-gateway`
   - **Description**: `AI Gateway for radhikatmosphere.com LightRAG deployment`
   - Click "Create"

3. **Copy Gateway ID:**
   - After creation, copy the Gateway ID
   - It will look like: `abc123def456...`

### Step 3: Create API Token

1. **Go to API Tokens:**
   - Visit: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"

2. **Configure Token:**
   - **Name**: `radhikatmosphere-ai-token`
   - **Permissions**: Add `AI Gateway - AI Gateway - Edit`
   - **Resources**: Select your account
   - Click "Create Token"

3. **Copy Token:**
   - Copy the generated API token immediately
   - Keep it secure!

### Step 4: Configure Domain Routing (Optional)

If you want to route AI requests through your domain:

1. **Go to DNS Settings:**
   - In Cloudflare Dashboard, select your domain
   - Go to "DNS" → "Records"

2. **Add CNAME Record:**
   - **Type**: CNAME
   - **Name**: `ai` (or `api.ai`)
   - **Target**: `gateway.ai.cloudflare.com`
   - **Proxy Status**: Proxied
   - Click "Save"

## 🔧 Environment Configuration

Once you have the Gateway ID and API Token, I'll update your `.env.production`:

```bash
# Your Cloudflare credentials
CLOUDFLARE_ACCOUNT_ID=d63a3181701030f91121871e55a0a46c
CLOUDFLARE_GATEWAY_ID=YOUR_GATEWAY_ID_HERE
CLOUDFLARE_API_KEY=YOUR_API_TOKEN_HERE

# Domain configuration (optional)
DOMAIN=radhikatmosphere.com
AI_SUBDOMAIN=ai.radhikatmosphere.com
```

## 🧪 Testing the Setup

### Test AI Gateway Directly:
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "https://gateway.ai.cloudflare.com/v1/d63a3181701030f91121871e55a0a46c/YOUR_GATEWAY_ID/openai/models"
```

### Test Through Domain (if configured):
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "https://ai.radhikatmosphere.com/v1/d63a3181701030f91121871e55a0a46c/YOUR_GATEWAY_ID/openai/models"
```

## 📊 What You'll Get

### AI Gateway Features:
- ✅ **Rate Limiting**: Control request frequency
- ✅ **Caching**: Reduce costs with response caching
- ✅ **Analytics**: Monitor usage and performance
- ✅ **Fallbacks**: Automatic provider switching
- ✅ **Cost Tracking**: Monitor spending

### Domain Integration:
- ✅ **Custom URL**: `ai.radhikatmosphere.com`
- ✅ **SSL/TLS**: Automatic certificate provisioning
- ✅ **DDoS Protection**: Cloudflare's edge protection
- ✅ **Global CDN**: Fast response times worldwide

## 🎯 Next Steps

**Please provide:**
1. **Gateway ID** from the AI Gateway you created
2. **API Token** from the token you generated
3. **Confirmation** if domain is added to Cloudflare

Then I'll:
1. Update `.env.production` with your credentials
2. Configure domain routing if desired
3. Deploy the production environment
4. Test the complete integration

## 📞 Support

If you encounter any issues:
- Check domain nameserver updates (can take 24-48 hours)
- Verify API token permissions
- Ensure gateway is active in Cloudflare dashboard

**Estimated setup time:** 10-15 minutes