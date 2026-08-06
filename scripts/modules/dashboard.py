"""
Dashboard Module: Generates repository & laboratory status metrics.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import Dict, Any
from scripts.core.github import GitHubClient
from scripts.core.markdown import render_table
from scripts.core.utils import get_current_date_str, load_toml_config


LANGUAGE_ICONS: dict[str, str] = {
    "Rust": '<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/rust/rust-original.svg" width="16" height="16" alt="Rust" /> Rust',
    "Python": '<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="16" height="16" alt="Python" /> Python',
    "C": '<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/c/c-original.svg" width="16" height="16" alt="C" /> C',
    "TypeScript": '<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/typescript/typescript-original.svg" width="16" height="16" alt="TypeScript" /> TypeScript',
    "Mojo": '<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mojo/mojo-original.svg" width="16" height="16" alt="Mojo" /> Mojo',
}


def render() -> str:
    """
    Render Dashboard section in Markdown format.

    Returns:
        Markdown string containing dashboard table & operational metadata.
    """
    config = load_toml_config("config/roadmap.toml")
    profile_cfg = config.get("profile", {})

    client = GitHubClient(username=profile_cfg.get("username", "rogerio-jose-gastao"))
    stats = client.fetch_user_stats()

    status = profile_cfg.get("status", "🟢 Online")
    focus_list = profile_cfg.get("focus", ["Artificial Intelligence", "Robotics", "Photonic Quantum Computing"])
    current_focus = "<br>".join(focus_list)
    lang_list = profile_cfg.get("languages") or stats.get("languages", ["Rust", "Python", "C", "TypeScript", "Mojo"])
    
    formatted_languages = [LANGUAGE_ICONS.get(lang, f"💻 {lang}") for lang in lang_list]
    languages = "<br>".join(formatted_languages)
    last_update = get_current_date_str()

    headers = ["Metric", "Value"]
    rows = [
        ["Status", status],
        ["Repositories", str(stats.get("public_repos", 7))],
        ["Research Notes", str(stats.get("research_notes", 531))],
        ["Projects", str(stats.get("projects_count", 13))],
        ["Languages", languages],
        ["Current Focus", current_focus],
        ["Last Update", last_update],
    ]

    return render_table(headers, rows)

