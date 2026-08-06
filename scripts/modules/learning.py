"""
Learning Module: Renders roadmap topics from config/roadmap.toml.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import List, Dict, Any
from scripts.core.utils import load_toml_config


def render() -> str:
    """
    Render Learning section in Markdown format.

    Returns:
        Markdown string containing learning roadmap topics.
    """
    config = load_toml_config("config/roadmap.toml")
    learning_cfg = config.get("learning", {})
    categories: List[Dict[str, Any]] = learning_cfg.get("categories", [])

    if not categories:
        topics = [
            "Rust", "Leptos", "Tokio", "CUDA",
            "Photonic Simulation", "ROS2", "Control Theory", "Business Strategy"
        ]
        return "\n".join([f"- **{t}**" for t in topics])

    lines: List[str] = []
    for cat in categories:
        name = cat.get("name", "Category")
        topics = cat.get("topics", [])
        topics_str = " • ".join([f"`{t}`" for t in topics])
        lines.append(f"- **{name}**: {topics_str}")

    return "\n".join(lines)
