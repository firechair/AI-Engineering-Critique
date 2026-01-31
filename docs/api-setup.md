# API Setup Guide

This project uses the Anthropic API to generate responses.

## Getting an API Key
1. Go to [console.anthropic.com](https://console.anthropic.com/).
2. Sign up or log in.
3. Generate a new API Key.

## Configuration
You can provide the API key in two ways:

### 1. Environment Variable (Recommended)
Create a `.env` file in the `ai-engineering-critique/` root directory:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```
Or export it in your shell:
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 2. In the App
You can enter the key directly in the sidebar of the Streamlit app. This is temporary and not saved to disk.
