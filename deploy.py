"""Deploys the agent to Vertex AI Agent Engine (Reasoning Engine).

Usage:  python deploy.py
Needs:  GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, STAGING_BUCKET in .env
"""
import os

import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines

load_dotenv()

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
BUCKET = os.environ["STAGING_BUCKET"]  # e.g. gs://my-project-staging

vertexai.init(project=PROJECT, location=LOCATION, staging_bucket=BUCKET)

from campuspulse.agent import root_agent  # noqa: E402

app = agent_engines.AdkApp(agent=root_agent, enable_tracing=True)

remote = agent_engines.create(
    agent_engine=app,
    display_name="campuspulse-agent",
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "requests",
    ],
    extra_packages=["./campuspulse"],
    env_vars={"MODEL": os.getenv("MODEL", "gemini-2.5-flash")},
)

print("DEPLOYED:", remote.resource_name)
print("Put this into .env as AGENT_ENGINE_ID=", remote.resource_name)
