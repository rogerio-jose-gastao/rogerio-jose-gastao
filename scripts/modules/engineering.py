"""
Engineering Module: Renders core engineering systems table.
Exposes single public function: render() -> str.
"""

from __future__ import annotations

from typing import List, Dict, Any
from scripts.core.markdown import render_table
from scripts.core.utils import load_toml_config


def render() -> str:
    """
    Render Engineering section in Markdown format.

    Returns:
        Markdown string showing current engineering systems and descriptions.
    """
    config = load_toml_config("config/roadmap.toml")
    eng_cfg = config.get("engineering", {})
    systems: List[Dict[str, str]] = eng_cfg.get("systems", [])

    if not systems:
        systems = [
            {"name": "ForgeAI", "description": "AI engineering and intelligent software"},
            {"name": "PAC+", "description": "High-performance intelligent system under active development"},
            {"name": "Cliro", "description": "Automated developer and robotics tooling CLI"},
            {"name": "AdMais", "description": "Creative technologies powered by AI"},
            {"name": "Path to Photonic", "description": "Open research vault & photonic computing laboratory"},
            {"name": "Sentinel.ai", "description": "Autonomous monitoring and decision system"},
        ]

    headers = ["System", "Description"]
    rows = [[s.get("name", ""), s.get("description", "")] for s in systems]

    return render_table(headers, rows)
