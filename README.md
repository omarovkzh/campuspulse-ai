# CampusPulse AI

Autonomous study-planning agent: reads deadlines, checks GitHub progress,
computes a Deadline Risk Score, and builds a prioritized plan.
Built on Gemini (Vertex AI), Google ADK, FastMCP; deployed to Vertex AI Agent Engine.

## Architecture
Streamlit UI -> Vertex AI Agent Engine (ADK agent + Gemini) -> tools:
`get_deadlines`, `check_repo_activity` (GitHub API), `calc_priority`.
The same tools are exposed as an MCP server (`mcp_server/server.py`, FastMCP).

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in project, bucket
PROJECT_ID=<id> bash scripts/setup_gcp.sh
```

## Run locally
```bash
adk web                      # ADK dev UI (run from repo root)
streamlit run ui/app.py      # our UI, local mode
python mcp_server/server.py  # MCP server on :8080
```

## Deploy to Agent Engine
```bash
python deploy.py             # prints the resource name
# put it in .env as AGENT_ENGINE_ID, then:
streamlit run ui/app.py      # now in remote mode
```

## Demo scenarios
1. "What is urgent this week and will I make it?"
2. "Will I finish the Database Systems lab? Check my repo."
