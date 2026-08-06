"""
Markdown rendering isolated inside core/renderer.py.
Scans README.md and updates contents between section markers.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict

from scripts.core.utils import get_project_root

logger = logging.getLogger("readme_engine")


class ReadmeRenderer:
    """Modifies README.md by replacing content between START_SECTION and END_SECTION markers."""

    START_MARKER_PATTERN = r"<!--START_SECTION:{section}-->"
    END_MARKER_PATTERN = r"<!--END_SECTION:{section}-->"

    def __init__(self, readme_path: str | Path = "README.md") -> None:
        path = Path(readme_path)
        if not path.is_absolute():
            path = get_project_root() / path
        self.readme_path = path

    def read_readme(self) -> str:
        """Read original README content from disk."""
        if not self.readme_path.exists():
            logger.error("README file not found at %s", self.readme_path)
            raise FileNotFoundError(f"README file not found at {self.readme_path}")
        with open(self.readme_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_readme(self, content: str) -> None:
        """Write updated README content back to disk."""
        with open(self.readme_path, "w", encoding="utf-8") as f:
            f.write(content)

    def render_sections(self, sections: Dict[str, str]) -> bool:
        """
        Replace sections in README.md matching markers <!--START_SECTION:key-->...<!--END_SECTION:key-->.

        Args:
            sections: Dictionary mapping section keys (e.g. 'dashboard') to markdown content strings.

        Returns:
            bool indicating if updates were rendered successfully.
        """
        readme_content = self.read_readme()
        updated_content = readme_content

        for section_name, new_markdown in sections.items():
            start_tag = f"<!--START_SECTION:{section_name}-->"
            end_tag = f"<!--END_SECTION:{section_name}-->"

            pattern = re.compile(
                rf"({re.escape(start_tag)})(.*?)({re.escape(end_tag)})",
                flags=re.DOTALL,
            )

            if not pattern.search(updated_content):
                logger.warning(
                    "Section markers for '%s' (%s ... %s) not found in README.md",
                    section_name,
                    start_tag,
                    end_tag,
                )
                continue

            replacement = f"{start_tag}\n{new_markdown.strip()}\n{end_tag}"
            updated_content = pattern.sub(replacement, updated_content)

        if updated_content != readme_content:
            self.write_readme(updated_content)
            logger.info("Successfully updated README.md sections: %s", list(sections.keys()))
            return True
        else:
            logger.info("No changes required in README.md.")
            return False
