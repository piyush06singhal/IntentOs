# Gemini API Rate Limits & Solutions

## 🚨 Current Issue: Quota Exceeded

Your API key has exceeded the free tier quota:
- **Limit**: 20 requests per day
- **Model**: gemini-2.5-flash
- **Reset**: Every 24 hours

## ✅ Solutions Implemented

### 1. Model Fallback Chain
The system now tries models in this order:
1. `gemini-2.0-flash-lite` (lightest, lowest quota)
2. `gemini-2.5-flash-lite` (light version)
3. `gemini-2.0-flash` (standard)
4. `gemini-2.5-flash` (latest, highest quota)

### 2. Automatic Retry
- Retries up to 2 times with 2-second delays
- Switches to lighter models if quota exceeded

### 3. Better Error Messages
- Clear quota exceeded messages
- Tells users when to try again

## 🔧 How to Fix Quota Issues

### Option 1: Wait 24 Hours
The quota resets every 24 hours. Just wait and try again tomorrow.

### Option 2: Get a New API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Update `.env.local`:
   ```
   GEMINI_API_KEY=your_new_key_here
   ```
4. Restart the server

### Option 3: Upgrade to Paid Plan
1. Go to https://ai.google.dev/pricing
2. Upgrade to paid tier for higher limits:
   - **Free**: 20 requests/day
   - **Paid**: 1,500 requests/day (and more)

### Option 4: Use Multiple API Keys (Rotation)
Create multiple free API keys and rotate between them:

```javascript
// In .env.local
GEMINI_API_KEY_1=key1
GEMINI_API_KEY_2=key2
GEMINI_API_KEY_3=key3
```

Then implement key rotation in the code.

## 📊 Current Quota Status

To check your current usage:
- Visit: https://ai.dev/usage?tab=rate-limit
- Login with your Google account
- View usage for each model

## 🎯 Best Practices

1. **Use Lighter Models**: Start with `gemini-2.0-flash-lite` for testing
2. **Cache Results**: Store responses to avoid repeated calls
3. **Batch Requests**: Combine multiple questions into one request
4. **Monitor Usage**: Check usage regularly at https://ai.dev/usage

## 🔄 Model Comparison

| Model | Speed | Quality | Quota Usage |
|-------|-------|---------|-------------|
| gemini-2.0-flash-lite | ⚡⚡⚡ | ⭐⭐⭐ | 💰 (Low) |
| gemini-2.5-flash-lite | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 (Low) |
| gemini-2.0-flash | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 (Medium) |
| gemini-2.5-flash | ⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 (High) |

## 🚀 For Production

For production deployment:
1. **Upgrade to paid plan** (recommended)
2. **Implement caching** (Redis/Memcached)
3. **Add rate limiting** on your end
4. **Monitor usage** with alerts
5. **Use CDN** for static content

---

**Current Status**: System will automatically try lighter models when quota is exceeded.
