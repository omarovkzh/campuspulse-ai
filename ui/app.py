"""Streamlit client: chat + live view of the agent's steps (thought -> tool -> result).

REMOTE mode: set AGENT_ENGINE_ID (resource name from deploy.py).
LOCAL mode:  no AGENT_ENGINE_ID, the agent runs in-process (good fallback for the demo).
"""
import os
import sys

import streamlit as st
import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
ENGINE_ID = os.getenv("AGENT_ENGINE_ID", "")
USER_ID = "student-1"

st.set_page_config(page_title="CampusPulse AI", page_icon="🎓")
st.title("🎓 CampusPulse AI")
st.caption("Autonomous study planner · Gemini + tools · Vertex AI Agent Engine")


@st.cache_resource
def get_agent():
    vertexai.init(project=PROJECT, location=LOCATION)
    if ENGINE_ID:
        return agent_engines.get(ENGINE_ID), "remote"
    from campuspulse.agent import root_agent
    app = agent_engines.AdkApp(agent=root_agent)
    app.set_up()
    return app, "local"


agent, mode = get_agent()
st.sidebar.write(f"Mode: **{mode}**")

if "session_id" not in st.session_state:
    s = agent.create_session(user_id=USER_ID)
    st.session_state.session_id = s["id"] if isinstance(s, dict) else s.id
    st.session_state.history = []

for role, text in st.session_state.history:
    st.chat_message(role).write(text)

prompt = st.chat_input("e.g. What is urgent this week and will I make it?")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.history.append(("user", prompt))
    answer = ""
    with st.chat_message("assistant"):
        steps = st.status("Agent is working...", expanded=True)
        box = st.empty()
        for event in agent.stream_query(
            user_id=USER_ID, session_id=st.session_state.session_id, message=prompt
        ):
            parts = (event.get("content") or {}).get("parts", [])
            for p in parts:
                if "function_call" in p:
                    fc = p["function_call"]
                    steps.write(f"🔧 **Tool call:** `{fc['name']}`")
                    steps.json(fc.get("args", {}))
                elif "function_response" in p:
                    fr = p["function_response"]
                    steps.write(f"📥 **Result of** `{fr['name']}`")
                    steps.json(fr.get("response", {}))
                elif p.get("text"):
                    answer += p["text"]
                    box.write(answer)
        steps.update(label="Done", state="complete", expanded=False)
    st.session_state.history.append(("assistant", answer))
