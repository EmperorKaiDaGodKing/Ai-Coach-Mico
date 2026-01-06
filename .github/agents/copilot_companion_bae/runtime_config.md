# runtime_config.md

## Hosted API Integration: Option A

This setup uses cloud-hosted models via API (OpenAI or Anthropic) to run Myko.

### 🔑 Environment Variables
Create a `.env` file based on `.env.example` and add your API keys:

- `OPENAI_API_KEY`: Your OpenAI secret key
- `OPENAI_MODEL`: e.g., `gpt-4`, `gpt-4-1106-preview`
- `ANTHROPIC_API_KEY`: (Optional) Your Claude API key
- `ANTHROPIC_MODEL`: e.g., `claude-4.5`

### 🧠 Model Selection
Myko will default to the model defined in `companion_config.yaml` under `model_preferences.preferred_models`.

### 🚀 Usage
You’ll use a script (e.g., `run_companion.py`) to:
1. Load your prompt and config
2. Send input to the selected API
3. Return and optionally log the response

### 🔒 Security
- Never commit `.env` to GitHub
- Use GitHub Secrets for CI/CD or GitHub Actions
