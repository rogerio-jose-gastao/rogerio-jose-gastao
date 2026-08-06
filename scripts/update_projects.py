"""
Standalone script to fetch all public repositories from GitHub API and update
the <!--START_SECTION:projects--> section in README.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.renderer import ReadmeRenderer
from scripts.core.utils import setup_logging, logger
from scripts.modules import projects


def main() -> None:
    """Fetch all repositories and update README.md projects section."""
    setup_logging(verbose=False)
    print("Searching all actual repositories from GitHub API...")

    try:
        markdown_content = projects.render(limit=100)
        renderer = ReadmeRenderer("README.md")
        updated = renderer.render_sections({"projects": markdown_content})
        
        if updated:
            print("✓ Projects section successfully updated in README.md.")
        else:
            print("✓ Projects section is already up to date.")
    except Exception as exc:
        logger.error("Failed to update projects section: %s", exc)
        print(f"❌ Error updating projects: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
