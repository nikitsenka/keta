# LLM Configuration Guide

KETA supports multiple LLM providers for flexibility across different deployment environments.

## Supported Providers

1. **Local (Ollama)** - For development and cost-effective local deployment
2. **Azure Mistral** - For production deployments on Azure
3. **OpenAI** - Optional fallback provider

## Configuration

LLM provider is configured via environment variables in the `.env` file.

### Provider Selection

Set the `LLM_PROVIDER` variable:

```bash
# Options: local, azure, openai
LLM_PROVIDER=local
```

## Local Development with Ollama

### Pull Ollama model (if using docker compose)

```bash
  docker exec keta-ollama ollama pull mistral
```


### Setup

1. **Install Ollama** (if not using Docker):
   ```bash
   # macOS
   brew install ollama

   # Or download from https://ollama.com
   ```

2. **Pull Mistral Model**:
   ```bash
   # Recommended for M4 Pro (48GB RAM)
   ollama pull mistral-nemo

   # Or smaller model
   ollama pull mistral
   ```

3. **Configure Environment**:
   ```bash
   LLM_PROVIDER=local
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=mistral-nemo  # or 'mistral'
   MODEL_TEMPERATURE=0.0
   ```
4. ** Call the Ollama API to verify**:
   ```bash
   curl -X POST http://localhost:11434/v1/chat/completions \
   -H "Content-Type: application/json" \
   -d '{
     "model": "mistral",
     "messages": [{"role": "user", "content": "Hello, Ollama!"}]
   }'
   ```

### Using Docker Compose

The project includes an Ollama service in `docker-compose.yml`:

```bash
# Start all services including Ollama
docker-compose up -d

# Pull Mistral model into the container
docker exec keta-ollama ollama pull mistral-nemo
```

The Ollama service will:
- Run on port 11434
- Store models in `keta_ollama_data` volume
- Be accessible to the API service at `http://ollama:11434`

### Model Options

| Model | Size | RAM Required | Best For |
|-------|------|--------------|----------|
| mistral | 7B | 4-8GB | Quick testing, limited resources |
| mistral-nemo | 12B | 8-16GB | Better quality, recommended for M4 Pro |
| mixtral | 8x7B | 32GB+ | Highest quality, requires significant RAM |

## Azure Mistral (Production)

### Setup

1. **Deploy Mistral on Azure**:
   - Follow [Azure Mistral deployment guide](https://docs.mistral.ai/deployment/cloud/azure)
   - Choose between Serverless (MaaS) or Real-time endpoints

2. **Get Endpoint and API Key**:
   - Endpoint format: `https://your-endpoint.region.inference.ai.azure.com`
   - Copy API key from Azure portal

3. **Configure Environment**:
   ```bash
   LLM_PROVIDER=azure
   AZURE_MISTRAL_ENDPOINT=https://your-endpoint.francecentral.inference.ai.azure.com
   AZURE_MISTRAL_API_KEY=your_azure_api_key_here
   MISTRAL_MODEL=mistral-large-latest
   MODEL_TEMPERATURE=0.0
   MODEL_MAX_RETRIES=5
   MODEL_TIMEOUT=120
   ```

### Available Models on Azure

- **mistral-large-latest** (recommended for production)
- mistral-medium-latest
- mistral-small-latest
- mistral-nemo
- ministral-3b

## OpenAI (Optional Fallback)

### Setup

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```
