"""
Declarative Markdown formatting utilities for building clean Markdown elements.
"""

from __future__ import annotations

from typing import List, Dict, Any


def render_progress_bar(current: int, total: int, width: int = 14) -> str:
    """
    Generate clean unicode progress bar.
    Example: ██████████░░░░
    """
    if total <= 0:
        filled = width
    else:
        ratio = min(max(current / total, 0.0), 1.0)
        filled = int(round(ratio * width))

    empty = width - filled
    return "█" * filled + "░" * empty


def render_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Generate clean Markdown table.
    """
    if not headers:
        return ""

    header_row = "| " + " | ".join(headers) + " |"
    divider_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_rows = ["| " + " | ".join(row) + " |" for row in rows]

    return "\n".join([header_row, divider_row] + data_rows)


def render_badge(label: str, text: str, color: str = "blue", logo: str = "") -> str:
    """Generate Markdown shields.io badge image link."""
    logo_part = f"&logo={logo}" if logo else ""
    badge_url = f"https://img.shields.io/badge/{label}-{text}-{color}?style=flat-square{logo_part}"
    return f"![{label}: {text}]({badge_url})"


def render_key_value_list(items: Dict[str, Any]) -> str:
    """Format key-value dictionary into bulleted Markdown list."""
    lines = []
    for k, v in items.items():
        if isinstance(v, list):
            v_str = ", ".join(v)
        else:
            v_str = str(v)
        lines.append(f"- **{k}**: {v_str}")
    return "\n".join(lines)


def render_grid_cards(items: List[Dict[str, str]], columns: int = 2) -> str:
    """Format cards into Markdown table grid."""
    if not items:
        return ""
    rows = []
    for i in range(0, len(items), columns):
        chunk = items[i : i + columns]
        row_cells = []
        for c in chunk:
            cell_content = f"**{c.get('title', '')}**<br>{c.get('description', '')}"
            row_cells.append(cell_content)
        while len(row_cells) < columns:
            row_cells.append("")
        rows.append(row_cells)
    
    headers = [f"System {i+1}" for i in range(columns)]
    return render_table(headers, rows)
