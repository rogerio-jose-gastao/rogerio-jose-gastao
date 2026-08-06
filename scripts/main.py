"""
Main Orchestration Script for ROG1 Living README Engine.

Orchestrates independent modules:
Dashboard -> Research -> Projects -> Followers -> Renderer
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project directory is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.renderer import ReadmeRenderer
from scripts.core.utils import setup_logging, load_toml_config, logger
from scripts.modules import dashboard, research, projects, followers, learning, engineering


def main() -> None:
    """Execute the living README rendering pipeline."""
    setup_logging(verbose=False)

    print("Initializing...\n")

    print("Loading configuration...")
    try:
        config = load_toml_config("config/roadmap.toml")
        print("✓\n")
    except Exception as exc:
        logger.error("Failed to load configuration: %s", exc)
        print("❌ Error loading config\n")
        sys.exit(1)

    rendered_sections: dict[str, str] = {}

    # Update Dashboard
    print("Updating Dashboard...")
    try:
        rendered_sections["dashboard"] = dashboard.render()
        print("✓\n")
    except Exception as exc:
        logger.error("Error updating Dashboard: %s", exc)
        print("❌ Failed\n")

    # Update Research
    print("Updating Research...")
    try:
        rendered_sections["research"] = research.render()
        print("✓\n")
    except Exception as exc:
        logger.error("Error updating Research: %s", exc)
        print("❌ Failed\n")

    # Update Engineering
    try:
        rendered_sections["engineering"] = engineering.render()
    except Exception as exc:
        logger.error("Error updating Engineering: %s", exc)

    # Update Projects
    print("Updating Projects...")
    try:
        rendered_sections["projects"] = projects.render()
        print("✓\n")
    except Exception as exc:
        logger.error("Error updating Projects: %s", exc)
        print("❌ Failed\n")

    # Update Learning
    try:
        rendered_sections["learning"] = learning.render()
    except Exception as exc:
        logger.error("Error updating Learning: %s", exc)

    # Update Followers
    print("Updating Followers...")
    try:
        rendered_sections["followers"] = followers.render()
        print("✓\n")
    except Exception as exc:
        logger.error("Error updating Followers: %s", exc)
        print("❌ Failed\n")

    # Rendering README
    print("Rendering README...")
    try:
        renderer = ReadmeRenderer("README.md")
        success = renderer.render_sections(rendered_sections)
        print("✓\n")
    except Exception as exc:
        logger.error("Error rendering README: %s", exc)
        print("❌ Failed\n")
        sys.exit(1)

    print("Finished successfully.\n")
    print("README updated.")


if __name__ == "__main__":
    main()
