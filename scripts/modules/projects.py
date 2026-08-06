"""
Projects Module: Renders GitHub repositories table queried from GitHub API.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import List
from scripts.core.github import GitHubClient
from scripts.core.markdown import render_table
from scripts.core.utils import load_toml_config


def render() -> str:
    """
    Render Projects section in Markdown format.

    Returns:
        Markdown string containing table of repositories with stars, language, updated date.
    """
    config = load_toml_config("config/roadmap.toml")
    profile_cfg = config.get("profile", {})
    username = profile_cfg.get("username", "rogerio-jose-gastao")

    client = GitHubClient(username=username)
    repos = client.fetch_user_repositories(limit=6)

    headers = ["Repository", "Language", "Updated", "Stars", "Description"]
    rows: List[List[str]] = []

    for repo in repos:
        repo_link = f"[{repo.name}]({repo.url})"
        stars_str = f"⭐ {repo.stars}"
        rows.append([repo_link, repo.language, repo.updated_at, stars_str, repo.description])

    return render_table(headers, rows)
