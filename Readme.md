# Transcript Summarization Agent with Vertex AI Agent Engine

This project demonstrates how to build, test, deploy, and manage an agent using the **Google Agent Development Kit (ADK)** and **Vertex AI Agent Engine**.

## 🧠 Agent Description
A simple AI agent that summarizes chat transcripts using Gemini models via Vertex AI.

---

## 📁 Project Structure
```
transcript_summarization_agent/
├── .env                                # Environment config
├── requirements.txt                    # Python dependencies
├── __init__.py                         # Package init
├── agent.py                            # ADK agent definition
├── deploy_to_agent_engine.py          # Deployment script
├── test_agent_app_locally.py          # Local test using AdkApp
├── query_app_on_agent_engine.py       # Query deployed agent
└── agent_engine_utils.py              # List/Delete agents
```

---

## ⚙️ Setup Instructions

### 1. Clone Repo and Set Up Environment
```bash
git clone <your-repo-url>
cd transcript_summarization_agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Update `.env` with your values:
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>
GOOGLE_CLOUD_LOCATION=us-central1
MODEL=gemini-2.0-flash-exp
APP_NAME="Transcript Summarizer"
```

### 3. Authenticate to GCP (Optional Locally)
```bash
gcloud auth application-default login
gcloud config set project <your-gcp-project-id>
```

---

## 🧪 Test Agent Locally
```bash
python3 test_agent_app_locally.py
```

---

## 🚀 Deploy Agent to Vertex AI Agent Engine
```bash
python3 deploy_to_agent_engine.py
```

---

## 🔍 Query Deployed Agent
```bash
python3 query_app_on_agent_engine.py
```

---

## 🧹 List or Delete Deployed Agents

### List
```bash
python3 agent_engine_utils.py list
```

### Delete
```bash
python3 agent_engine_utils.py delete <RESOURCE_NAME>
```

---

## ✅ GitHub Actions CI/CD Support
This repo can be integrated with GitHub Actions for:
- Deploying the agent
- Listing agents
- Deleting agents

See `.github/workflows/adk-agent-engine.yml` for workflow configuration.

---

## 📚 Resources
- [Vertex AI Agent Engine Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [Google ADK on PyPI](https://pypi.org/project/google-adk/)
- [Qwiklabs: Deploy ADK Agents to Agent Engine](https://www.cloudskillsboost.google/)
