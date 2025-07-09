# Anthropic API Proxy for Gemini & OpenAI Models

## Overview

This repository contains a proxy server that allows Anthropic clients (like Claude Code) to work with Gemini or OpenAI models via LiteLLM. The proxy translates Anthropic API requests to the appropriate backend provider while maintaining compatibility with Anthropic's API format.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **2025-01-09**: Added comprehensive Azure OpenAI integration
  - Enhanced ModelMapper with Azure provider support
  - Added Azure API key, endpoint, and version configuration
  - Updated model mapping logic to handle Azure deployments
  - Added Azure support to both /v1/messages and /v1/messages/count_tokens endpoints
  - Updated environment configuration and documentation
  - Created comprehensive README with Azure setup guide

## System Architecture

### Core Architecture
- **Proxy Server**: FastAPI-based HTTP server that acts as a translation layer
- **Backend Integration**: Uses LiteLLM to interface with multiple AI providers (OpenAI, Gemini, Anthropic)
- **Model Mapping**: Intelligent routing system that maps Anthropic model names to equivalent models from other providers
- **Streaming Support**: Handles both streaming and non-streaming responses

### Technology Stack
- **Framework**: FastAPI for the HTTP server
- **HTTP Client**: httpx for making backend requests
- **AI Integration**: LiteLLM for unified AI provider interface
- **Configuration**: Environment variables via python-dotenv
- **Validation**: Pydantic for request/response validation
- **Runtime**: Python with uvicorn ASGI server

## Key Components

### 1. Proxy Server (`server.py`)
- Main FastAPI application
- Handles `/v1/messages` endpoint to mimic Anthropic's API
- Implements request validation and response formatting
- Manages streaming and non-streaming responses
- Includes logging and error handling

### 2. Model Mapping System
- Maps Anthropic model names (`haiku`, `sonnet`) to provider-specific models
- Configurable via environment variables
- Supports fallback mechanisms when preferred providers are unavailable
- Handles model prefixing for different providers (`openai/`, `gemini/`)

### 3. Provider Configuration
- **OpenAI**: Primary backend option with GPT-4 models
- **Gemini**: Google's AI models via AI Studio API
- **Anthropic**: Optional direct routing for actual Claude models
- **Preferred Provider**: Configurable primary provider selection

### 4. Testing Suite (`tests.py`)
- Comprehensive test coverage for both streaming and non-streaming
- Tool use testing capabilities
- Multi-turn conversation testing
- Comparison testing between real Anthropic API and proxy

## Data Flow

1. **Request Reception**: Client sends Anthropic-formatted request to proxy
2. **Model Resolution**: Proxy maps requested model to actual backend model
3. **Provider Selection**: Determines which backend provider to use
4. **Request Translation**: Converts Anthropic format to provider-specific format via LiteLLM
5. **Backend Communication**: Makes request to selected provider
6. **Response Processing**: Translates backend response back to Anthropic format
7. **Response Delivery**: Returns formatted response to client

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for the proxy server
- **LiteLLM**: Unified interface for multiple AI providers
- **httpx**: HTTP client for backend requests
- **uvicorn**: ASGI server for running the application
- **pydantic**: Data validation and serialization
- **python-dotenv**: Environment variable management

### AI Provider APIs
- **OpenAI API**: Requires `OPENAI_API_KEY`
- **Google AI Studio (Gemini)**: Requires `GEMINI_API_KEY`
- **Anthropic API**: Optional, requires `ANTHROPIC_API_KEY`

## Deployment Strategy

### Development Setup
- Uses `uv` for dependency management
- Environment configuration via `.env` files
- Local development server on configurable port (default: 8082)

### Configuration Management
- **Environment Variables**: All API keys and model configurations
- **Model Mapping**: Configurable via `PREFERRED_PROVIDER`, `BIG_MODEL`, `SMALL_MODEL`
- **Fallback Strategy**: Automatic fallback to OpenAI if preferred provider fails

### Production Considerations
- FastAPI application suitable for containerization
- Uvicorn ASGI server for production deployment
- Configurable logging levels for monitoring
- Error handling and request validation for reliability

### Security Features
- API key validation for incoming requests
- Secure handling of multiple provider API keys
- Request/response logging control for sensitive data