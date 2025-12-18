# 🚀 Running IntentOS with Ollama (No Rate Limits!)

## Why Ollama?

- ✅ **Completely FREE** - No API costs
- ✅ **No Rate Limits** - Use as much as you want
- ✅ **Privacy** - Runs locally on your machine
- ✅ **Fast** - No network latency
- ✅ **Offline** - Works without internet

## Quick Setup

### 1. Install Ollama

**Windows/Mac/Linux:**
```bash
# Visit https://ollama.com/download
# Or use curl:
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull a Model

```bash
# Recommended: Llama 3.2 (3B - fast and good)
ollama pull llama3.2

# Or use a larger model for better quality:
ollama pull llama3.1:8b
```

### 3. Start Ollama

```bash
ollama serve
```

### 4. Update .env

```env
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 5. Run IntentOS

```bash
streamlit run app.py
```

## Available Models

| Model | Size | Speed | Quality | RAM Needed |
|-------|------|-------|---------|------------|
| llama3.2 | 3B | ⚡⚡⚡ | ⭐⭐⭐ | 4GB |
| llama3.1:8b | 8B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| mistral | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| phi3 | 3.8B | ⚡⚡⚡ | ⭐⭐⭐ | 4GB |

## Troubleshooting

### Ollama not running?
```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama
ollama serve
```

### Model not found?
```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.2
```

### Slow responses?
- Use a smaller model (llama3.2 or phi3)
- Reduce MAX_TOKENS in .env
- Close other applications

## For Streamlit Cloud

Unfortunately, Ollama requires a local installation and can't run on Streamlit Cloud's free tier. For cloud deployment, you'll need to:

1. **Use Gemini** (has rate limits but free)
2. **Use OpenAI** (costs money but reliable)
3. **Deploy on your own server** with Ollama installed

## Comparison

| Provider | Cost | Rate Limits | Setup | Best For |
|----------|------|-------------|-------|----------|
| Ollama | FREE | None | Medium | Local development |
| Gemini | FREE | 20-1500/day | Easy | Light usage |
| OpenAI | $$ | High | Easy | Production |
