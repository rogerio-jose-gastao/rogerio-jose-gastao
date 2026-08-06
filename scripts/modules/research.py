"""
Research Module: Renders latest Obsidian vault notes and research progress.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import Dict, Any, List
from scripts.core.markdown import render_progress_bar
from scripts.core.utils import load_toml_config


def render() -> str:
    """
    Render Research section in Markdown format.

    Returns:
        Markdown string showing latest research notes and progress bars.
    """
    config = load_toml_config("config/roadmap.toml")
    research_cfg = config.get("research", {})

    notes: List[str] = research_cfg.get(
        "notes",
        [
            "Quantum Error Correction",
            "Integrated Photonics",
            "Reinforcement Learning",
        ],
    )

    categories: List[Dict[str, Any]] = research_cfg.get(
        "categories",
        [
            {"name": "AI + CS", "progress": 10, "total": 14},
            {"name": "Photonic CS", "progress": 6, "total": 12},
            {"name": "BTM", "progress": 4, "total": 12},
            {"name": "Robotics", "progress": 8, "total": 12},
        ],
    )

    lines: List[str] = ["### Latest Notes\n"]
    for note in notes:
        lines.append(f"• {note}")

    lines.append("\n### Research Progress\n")
    lines.append("| Category | Progress |")
    lines.append("|---|---|")
    for cat in categories:
        name = cat.get("name", "")
        prog = cat.get("progress", 0)
        total = cat.get("total", 10)
        bar = render_progress_bar(prog, total)
        lines.append(f"| **{name}** | `{bar}` |")

    return "\n".join(lines)
