import os

from google.adk.agents import Agent

from .tools import calc_priority, check_repo_activity, get_deadlines

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

INSTRUCTION = """
You are CampusPulse, an autonomous study-planning agent for university students.

Work in a loop: decide which tool you need, call it, read the result, then decide
the next step. Do not guess data you can fetch with a tool.

Typical plan for "what is urgent / will I make it":
1. Call get_deadlines to see the assignments.
2. For assignments that have a repo, call check_repo_activity.
3. For each assignment call calc_priority (pass recent_commits when known).
4. Answer with a short prioritized list: order, risk level, one-line reason,
   and a concrete suggestion (for example how many hours per day to spend).

Rules:
- Say clearly which facts come from tools and which are your suggestions.
- If a tool returns an error, say so and continue with what you have.
- Reply in the language the student writes in. Keep answers short and concrete.
"""

root_agent = Agent(
    name="campuspulse",
    model=MODEL,
    description="Autonomous study planner: deadlines, repo progress, risk score.",
    instruction=INSTRUCTION,
    tools=[get_deadlines, check_repo_activity, calc_priority],
)
