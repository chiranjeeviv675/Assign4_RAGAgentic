This project implements a **Self-Critique Agentic RAG (Retrieval Augmented Generation) Pipeline** using:
- **Azure OpenAI API** (GPT-4 or GPT-35-turbo)
- **LangGraph** (Stateful Agentic Workflows)
- **ChromaDB** (for Vector Knowledge Base)
- **Self-Critique Refinement Loop**

## Prerequisites

- Python 3.10+
- Azure OpenAI subscription (API keys)
- Local environment (tested on Ubuntu VM)

---

## Setup Secrets

Create your `config_secrets.py` file:

```python
# config_secrets.py

AZURE_OPENAI_API_KEY = "<your-azure-openai-api-key>"
AZURE_OPENAI_API_VERSION = "<your-azure-openai-api-version>"
AZURE_OPENAI_ENDPOINT = "<your-azure-openai-endpoint>"


python3 -m venv venv
source venv/bin/activate


pip install -r requirements.txt




