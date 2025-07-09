# Anthropic API Proxy for Azure OpenAI, Gemini & OpenAI Models 🔄

**Use Anthropic clients (like Claude Code) with Azure OpenAI, Gemini, or OpenAI backends.** 🤝

A proxy server that lets you use Anthropic clients with Azure OpenAI, Gemini, or OpenAI models via LiteLLM. 🌉

![Anthropic API Proxy](pic.png)

## Quick Start ⚡

### Prerequisites

- At least one of the following API keys: 🔑
  - OpenAI API key
  - Google AI Studio (Gemini) API key
  - Azure OpenAI API key and endpoint
- [uv](https://github.com/astral-sh/uv) installed

### Setup 🛠️

1. **Clone this repository**:
   ```bash
   git clone https://github.com/elgertam/claude-code-proxy.git
   cd claude-code-proxy
   ```

2. **Install uv** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your API keys and model configurations:

   **For OpenAI (default)**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PREFERRED_PROVIDER=openai
   BIG_MODEL=gpt-4.1
   SMALL_MODEL=gpt-4.1-mini
   ```

   **For Google/Gemini**:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PREFERRED_PROVIDER=google
   BIG_MODEL=gemini-2.5-pro-preview-03-25
   SMALL_MODEL=gemini-2.0-flash
   ```

   **For Azure OpenAI**:
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   AZURE_OPENAI_API_VERSION=2024-10-21
   PREFERRED_PROVIDER=azure
   BIG_MODEL=your-gpt-4o-deployment-name
   SMALL_MODEL=your-gpt-4o-mini-deployment-name
   ```

4. **Run the server**:
   ```bash
   uv run uvicorn server:app --host 0.0.0.0 --port 8082 --reload
   ```

### Using with Claude Code 🎮

1. **Install Claude Code** (if you haven't already):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Connect to your proxy**:
   ```bash
   ANTHROPIC_BASE_URL=http://localhost:8082 claude
   ```

3. **That's it!** Your Claude Code client will now use the configured backend models through the proxy. 🎯

## Supported Providers 🌐

### OpenAI
- Standard OpenAI API with your API key
- Supports all current OpenAI models (GPT-4, GPT-4o, GPT-4o-mini, etc.)
- Automatic model prefix handling

### Google Gemini
- Google AI Studio API
- Supports Gemini 2.5 Pro and Gemini 2.0 Flash models
- Automatic model prefix handling

### Azure OpenAI ✨ NEW!
- Azure OpenAI Service with your deployed models
- Supports all Azure OpenAI deployments
- Configurable endpoint and API version
- Uses your custom deployment names

## Model Mapping 🗺️

The proxy automatically maps Claude models to your configured backend:

| Claude Model | OpenAI (default) | Google | Azure |
|--------------|------------------|---------|--------|
| haiku        | gpt-4.1-mini     | gemini-2.0-flash | Your SMALL_MODEL deployment |
| sonnet       | gpt-4.1          | gemini-2.5-pro-preview-03-25 | Your BIG_MODEL deployment |

### Azure OpenAI Configuration

For Azure OpenAI, you need to:

1. **Deploy models** in Azure Portal:
   - Go to your Azure OpenAI resource
   - Deploy GPT-4o and GPT-4o-mini (or your preferred models)
   - Note the deployment names (NOT the model names)

2. **Configure environment variables**:
   ```env
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   AZURE_OPENAI_API_VERSION=2024-10-21
   PREFERRED_PROVIDER=azure
   BIG_MODEL=your-gpt-4o-deployment-name
   SMALL_MODEL=your-gpt-4o-mini-deployment-name
   ```

3. **Important**: Use your **deployment names**, not the model names. For example:
   - ✅ `BIG_MODEL=my-gpt-4o-deployment`
   - ❌ `BIG_MODEL=gpt-4o`

### Supported Models by Provider

#### OpenAI Models
- o3-mini
- o1, o1-mini, o1-pro
- gpt-4.5-preview
- gpt-4o, gpt-4o-mini
- gpt-4o-audio-preview, gpt-4o-mini-audio-preview
- chatgpt-4o-latest
- gpt-4.1, gpt-4.1-mini

#### Gemini Models
- gemini-2.5-pro-preview-03-25
- gemini-2.0-flash

#### Azure OpenAI Models
- Any model you've deployed in your Azure OpenAI resource
- Common deployments: GPT-4o, GPT-4o-mini, GPT-4, GPT-3.5-turbo

## Configuration Examples 📋

### Multi-Provider Fallback
```env
# Primary provider
PREFERRED_PROVIDER=azure
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
BIG_MODEL=gpt-4o-deployment
SMALL_MODEL=gpt-4o-mini-deployment

# Fallback providers
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### Cost Optimization with Azure
```env
# Use Azure OpenAI for cheaper pricing
PREFERRED_PROVIDER=azure
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
BIG_MODEL=gpt-4o-deployment
SMALL_MODEL=gpt-35-turbo-deployment  # Cheaper option
```

## API Endpoints 📡

### Messages
- **POST** `/v1/messages` - Create a message (streaming and non-streaming)
- **POST** `/v1/messages/count_tokens` - Count tokens in a message

### Health Check
- **GET** `/` - Root endpoint with server information
- **GET** `/health` - Health check endpoint

## How It Works 🧩

This proxy works by:

1. **Receiving requests** in Anthropic's API format 📥
2. **Mapping models** based on your preferred provider configuration 🔄
3. **Translating** the requests to the target provider format via LiteLLM 🔄
4. **Sending** the translated request to your configured provider 📤
5. **Converting** the response back to Anthropic format 🔄
6. **Returning** the formatted response to the client ✅

The proxy handles both streaming and non-streaming responses, maintaining compatibility with all Claude clients. 🌊

## Azure OpenAI Setup Guide 🌟

### Step 1: Create Azure OpenAI Resource

1. Go to the [Azure Portal](https://portal.azure.com)
2. Create a new Azure OpenAI resource
3. Note your endpoint URL (e.g., `https://your-resource.openai.azure.com`)
4. Get your API key from the "Keys and Endpoint" section

### Step 2: Deploy Models

1. Go to your Azure OpenAI resource
2. Click "Model deployments" → "Create new deployment"
3. Deploy the models you want to use:
   - **GPT-4o** (for BIG_MODEL)
   - **GPT-4o-mini** (for SMALL_MODEL)
4. Note the deployment names (these are what you'll use in your config)

### Step 3: Configure the Proxy

Create a `.env` file with your Azure configuration:

```env
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-10-21
PREFERRED_PROVIDER=azure
BIG_MODEL=my-gpt-4o-deployment
SMALL_MODEL=my-gpt-4o-mini-deployment
```

### Step 4: Test the Configuration

Start the proxy and test with a simple request:

```bash
# Start the proxy
uv run uvicorn server:app --host 0.0.0.0 --port 8082

# Test with Claude Code
ANTHROPIC_BASE_URL=http://localhost:8082 claude "Hello, world!"
```

## Environment Variables Reference 📋

### Required (choose one set)

#### OpenAI
```env
OPENAI_API_KEY=sk-...
```

#### Gemini
```env
GEMINI_API_KEY=your_gemini_key
```

#### Azure OpenAI
```env
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-10-21
```

### Optional Configuration

```env
# Provider preference (openai, google, azure)
PREFERRED_PROVIDER=openai

# Model mapping
BIG_MODEL=gpt-4.1
SMALL_MODEL=gpt-4.1-mini

# Server configuration
HOST=0.0.0.0
PORT=8082
```

## Troubleshooting 🔧

### Common Issues

#### Azure OpenAI
- **"Model not found"**: Check your deployment names in Azure Portal
- **"Invalid API key"**: Verify your API key in the Azure Portal
- **"Endpoint not found"**: Ensure your endpoint URL is correct

#### General
- **"Connection refused"**: Make sure the proxy server is running
- **"API key not provided"**: Check your environment variables are set correctly

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. 🎁

## License 📄

This project is licensed under the MIT License.

## About

This proxy enables you to use Anthropic's Claude Code CLI with alternative LLM providers including Azure OpenAI, providing cost optimization and provider flexibility while maintaining the same development experience.

## Support

For issues and support, please check the [GitHub repository](https://github.com/elgertam/claude-code-proxy) or create an issue.