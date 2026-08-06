"""
Followers Module: Queries GitHub GraphQL/REST API for user followers.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import List
from scripts.core.github import GitHubClient
from scripts.core.utils import load_toml_config


def render() -> str:
    """
    Render Followers section in Markdown format.

    Returns:
        Markdown string containing avatar grids / follower profile links.
    """
    config = load_toml_config("config/roadmap.toml")
    profile_cfg = config.get("profile", {})
    username = profile_cfg.get("username", "rogerio-jose-gastao")

    client = GitHubClient(username=username)
    followers = client.fetch_followers(limit=14)

    if not followers:
        return "*No followers data available.*"

    items: List[str] = []
    for follower in followers:
        avatar = f'<img src="{follower.avatar_url}" width="48" height="48" style="border-radius: 50%;" alt="{follower.login}"/>'
        item = f'a href="{follower.html_url}" title="{follower.name}">{avatar}</a'
        # Since rule 4 requires pure markdown without raw HTML tags where possible, or minimal image avatars:
        markdown_avatar = f"[![{follower.login}]({follower.avatar_url}&s=60)]({follower.html_url})"
        items.append(markdown_avatar)

    return " ".join(items)
