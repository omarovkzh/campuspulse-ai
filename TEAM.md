# Roles and checklist (4 people, 1 day)

## 1. Cloud/DevOps
- [ ] GCP project, billing/credits, `scripts/setup_gcp.sh`
- [ ] IAM: Vertex AI User, Storage Admin for the deploying account
- [ ] `python deploy.py` works, AGENT_ENGINE_ID saved in .env (do this FIRST)
- [ ] Screenshots of the deployed engine in the console (for slides)

## 2. Agent/AI
- [ ] Run `adk web`, check the model name works in the project
- [ ] Tune INSTRUCTION in campuspulse/agent.py
- [ ] Test both demo scenarios, fix tool selection issues

## 3. MCP/Backend
- [ ] Replace deadlines.json with real student data
- [ ] Real repos in deadlines.json, GITHUB_TOKEN in .env
- [ ] `python mcp_server/server.py` runs; optional Cloud Run deploy
- [ ] Document each tool in README

## 4. UI + presentation
- [ ] `streamlit run ui/app.py` works in local and remote mode
- [ ] Check that tool calls/results show up in the steps panel
- [ ] Slides (PDF): problem, architecture, reasoning loop, MCP/tools, GCP deploy, demo, next steps
- [ ] Record backup demo video

## Everyone, last 2 hours
- [ ] Push to GitHub, README is correct
- [ ] Submit repo link + PDF with a time buffer
