"""
Standalone script to fetch updated user dashboard metrics from GitHub API and update
the <!--START_SECTION:dashboard--> section in README.md.
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
from scripts.modules import dashboard


def main() -> None:
    """Fetch updated user metrics and update README.md dashboard section."""
    setup_logging(verbose=False)
    print("Fetching live dashboard metrics from GitHub API...")

    try:
        markdown_content = dashboard.render()
        renderer = ReadmeRenderer("README.md")
        updated = renderer.render_sections({"dashboard": markdown_content})
        
        if updated:
            print("✓ Dashboard section successfully updated in README.md.")
        else:
            print("✓ Dashboard section is already up to date.")
    except Exception as exc:
        logger.error("Failed to update dashboard section: %s", exc)
        print(f"❌ Error updating dashboard: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
