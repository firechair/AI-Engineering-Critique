# API Setup Guide

This project uses the OpenRouter API to access free AI models.

## Getting an API Key

1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to **API Keys** in your account settings
4. Click **Create Key**
5. Copy your new key (starts with `sk-or-v1-...`)

## Configuration

You can provide the API key in two ways:

### 1. Environment Variable (Recommended)

Create a `.env` file in the `ai-engineering-critique/` root directory:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Or export it in your shell:

```bash
export OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 2. In the App

Enter the key directly in the sidebar when you launch the Streamlit app. This isn't saved — you'll need to enter it each session.

## Free Models Only

The app automatically filters to show only free models from OpenRouter. You won't incur any charges while using the platform.

Free models include options from:
- **Google** (Gemma)
- **Meta** (Llama)
- **Mistral**
- **DeepSeek**
- And others

The available models change over time as providers update their offerings.

## Troubleshooting

**"Invalid API key" error**
- Check you copied the full key (including the `sk-or-v1-` prefix)
- Make sure there are no extra spaces
- Try generating a new key if the problem persists

**"Rate limit exceeded" error**
- Free models have usage limits
- Wait 30-60 seconds and try again
- Try a different free model

**No models appearing in dropdown**
- Check your internet connection
- Verify your API key is entered correctly
- OpenRouter might be temporarily down — check their status page

**Slow responses**
- Some free models are slower than others
- Try a different model
- Reduce the max tokens setting

## Data Privacy

OpenRouter routes your requests to various AI providers. Review their privacy policy at [openrouter.ai/privacy](https://openrouter.ai/privacy) if you're working with sensitive data.
