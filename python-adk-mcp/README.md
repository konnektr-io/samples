# Konnektr Graph Agent (Google ADK)

This agent demonstrates how to give **Google Gemini** structured memory using the **Konnektr MCP Server**.

## Prerequisites

1.  **Google Cloud Project** with Vertex AI API enabled.
2.  **Konnektr Graph** instance (or local Docker container).
3.  Python 3.10+

## Setup

```bash
# 1. Install Google ADK and dependencies
pip install google-adk

# 2. Set your credentials
export GOOGLE_API_KEY="your-gemini-key"
export KONNEKTR_API_KEY="your-graph-key"

# 3. Run the agent
python graph_agent.py
```
