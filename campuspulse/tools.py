"""Tools for the CampusPulse agent.

Plain Python functions with type hints and docstrings: ADK turns them into
Gemini function declarations automatically. The same functions are exposed
over MCP in mcp_server/server.py.
"""
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

DATA_FILE = Path(__file__).parent / "data" / "deadlines.json"


def get_deadlines(course: str = "") -> dict:
    """Returns the student's assignment deadlines, sorted by due date.

    Args:
        course: Optional course name filter (substring, case-insensitive).
            Empty string returns all courses.

    Returns:
        dict with status, today's date and a list of assignments
        (id, course, title, due, days_left, hours_needed, repo).
    """
    items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    today = date.today()
    out = []
    for it in items:
        if course and course.lower() not in it["course"].lower():
            continue
        due = datetime.strptime(it["due"], "%Y-%m-%d").date()
        out.append({**it, "days_left": (due - today).days})
    out.sort(key=lambda x: x["due"])
    return {"status": "success", "today": today.isoformat(), "assignments": out}


def calc_priority(
    deadline: str,
    hours_needed: float,
    hours_per_day: float = 3.0,
    recent_commits: int = -1,
) -> dict:
    """Calculates the Deadline Risk Score for one assignment.

    Args:
        deadline: Due date in YYYY-MM-DD format.
        hours_needed: Estimated remaining work in hours.
        hours_per_day: How many hours per day the student can spend (default 3).
        recent_commits: Commits in the last 7 days from check_repo_activity;
            -1 if unknown or the assignment has no repository.

    Returns:
        dict with risk_level (low/medium/high), risk_score (0-100),
        days_left, available_hours and a short reason.
    """
    try:
        due = datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        return {"status": "error", "message": "deadline must be YYYY-MM-DD"}

    days_left = (due - date.today()).days
    if days_left < 0:
        return {"status": "success", "risk_level": "high", "risk_score": 100,
                "days_left": days_left, "available_hours": 0,
                "reason": "The deadline has already passed."}

    available = max(days_left, 0) * hours_per_day
    ratio = hours_needed / available if available > 0 else 9.9
    score = min(100, int(ratio * 100))
    reason = (f"Needs {hours_needed}h, about {available:.0f}h available "
              f"in {days_left} day(s) at {hours_per_day}h/day.")

    if recent_commits == 0 and ratio >= 0.4:
        score = min(100, score + 20)
        reason += " No commits in the last 7 days."

    level = "high" if score >= 80 else "medium" if score >= 50 else "low"
    return {"status": "success", "risk_level": level, "risk_score": score,
            "days_left": days_left, "available_hours": round(available, 1),
            "reason": reason}


def check_repo_activity(repo: str, days: int = 7) -> dict:
    """Checks recent commit activity in a GitHub repository.

    Args:
        repo: Repository in "owner/name" format.
        days: Look-back window in days (default 7).

    Returns:
        dict with commit_count, last_commit_date and recent commit messages.
    """
    if not repo or "/" not in repo:
        return {"status": "error", "message": "repo must be 'owner/name'"}

    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.get(
            f"https://api.github.com/repos/{repo}/commits",
            params={"since": since, "per_page": 30},
            headers=headers,
            timeout=10,
        )
    except requests.RequestException as e:
        return {"status": "error", "message": f"GitHub request failed: {e}"}
    if r.status_code != 200:
        return {"status": "error", "message": f"GitHub returned {r.status_code}"}

    commits = r.json()
    return {
        "status": "success",
        "repo": repo,
        "window_days": days,
        "commit_count": len(commits),
        "last_commit_date": commits[0]["commit"]["author"]["date"] if commits else None,
        "recent_messages": [c["commit"]["message"].split("\n")[0] for c in commits[:5]],
    }
