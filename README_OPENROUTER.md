# EduBot with OpenRouter API

## Setup Instructions

1. **Get OpenRouter API Key:**
   - Go to [OpenRouter.ai](https://openrouter.ai/)
   - Sign up and get your API key
   - Replace `your_openrouter_api_key_here` in the `.env` file with your actual API key

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Available Models

The application is configured to use `anthropic/claude-3-haiku` by default. You can change this to any model available on OpenRouter, such as:
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `openai/gpt-4`
- `openai/gpt-4-turbo`
- `meta-llama/llama-3-70b-instruct`

To change the model, edit the `model` parameter in the `get_openrouter_response()` function in both `app.py` and `chat.py`.

## Files Modified

- `requirements.txt` - Updated to use OpenAI library for OpenRouter API
- `.env` - Changed from GOOGLE_API_KEY to OPENROUTER_API_KEY
- `app.py` - Modified to use OpenRouter API instead of Google Generative AI
- `chat.py` - Modified to use OpenRouter API instead of Google Generative AI

## Features

- Educational chatbot interface
- Streaming responses
- Session state management
- Error handling
- Multiple model support via OpenRouter
