"""
GitHub API wrapper isolated inside core/github.py handling REST & GraphQL queries.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from scripts.core.cache import CacheEngine

logger = logging.getLogger("readme_engine")


@dataclass
class RepositoryInfo:
    """Dataclass holding repository details."""

    name: str
    description: str
    language: str
    stars: int
    updated_at: str
    url: str


@dataclass
class FollowerInfo:
    """Dataclass holding follower details."""

    login: str
    name: str
    avatar_url: str
    html_url: str


class GitHubClient:
    """Isolated wrapper for GitHub REST and GraphQL API calls with cache resilience."""

    REST_API_BASE = "https://api.github.com"
    GRAPHQL_API_BASE = "https://api.github.com/graphql"

    def __init__(self, username: str = "rogerio-jose-gastao", token: Optional[str] = None) -> None:
        self.username = username
        self.token = token or os.getenv("GITHUB_TOKEN", "")
        self.cache = CacheEngine()

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": "ROG1-Living-README-Engine",
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _http_get(self, endpoint: str) -> Optional[Any]:
        """Perform HTTP GET request to GitHub REST API."""
        url = f"{self.REST_API_BASE}/{endpoint.lstrip('/')}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    payload = json.loads(response.read().decode("utf-8"))
                    return payload
        except urllib.error.URLError as exc:
            logger.warning("GitHub API HTTP request failed for %s: %s", endpoint, exc)
        except Exception as exc:
            logger.error("Unexpected error fetching %s: %s", endpoint, exc)
        return None

    def _graphql_query(self, query: str, variables: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform HTTP POST GraphQL request to GitHub API."""
        if not self.token:
            logger.info("No GITHUB_TOKEN set. Skipping GraphQL request.")
            return None

        req = urllib.request.Request(
            self.GRAPHQL_API_BASE,
            data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
            headers={
                **self._get_headers(),
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            logger.warning("GraphQL request failed: %s", exc)
        return None

    def fetch_user_repositories(self, limit: int = 6) -> List[RepositoryInfo]:
        """Fetch user public repositories sorted by updated date."""
        cache_key = f"repos_{self.username}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return [RepositoryInfo(**item) for item in cached]

        data = self._http_get(f"users/{self.username}/repos?sort=updated&per_page={limit}")
        if data and isinstance(data, list):
            repos = []
            for item in data:
                repos.append(
                    RepositoryInfo(
                        name=item.get("name", ""),
                        description=item.get("description") or "No description provided.",
                        language=item.get("language") or "Markdown",
                        stars=item.get("stargazers_count", 0),
                        updated_at=item.get("updated_at", "")[:10],
                        url=item.get("html_url", ""),
                    )
                )
            self.cache.set(cache_key, [r.__dict__ for r in repos])
            return repos

        # Fallback to cached or default repositories
        stale = self.cache.get_stale_or_default(cache_key)
        if stale:
            return [RepositoryInfo(**item) for item in stale]

        return [
            RepositoryInfo(
                name="ForgeAI",
                description="AI engineering and intelligent software framework",
                language="Python",
                stars=14,
                updated_at="2026-08-05",
                url=f"https://github.com/{self.username}/ForgeAI",
            ),
            RepositoryInfo(
                name="PAC+",
                description="Intelligent systems under active development",
                language="Rust",
                stars=8,
                updated_at="2026-08-04",
                url=f"https://github.com/{self.username}/PAC-Plus",
            ),
            RepositoryInfo(
                name="Path-to-Photonic",
                description="Open research vault & photonic computing laboratory",
                language="C",
                stars=22,
                updated_at="2026-08-06",
                url=f"https://github.com/{self.username}/Path-to-Photonic",
            ),
        ]

    def fetch_followers(self, limit: int = 10) -> List[FollowerInfo]:
        """Fetch recent followers using GraphQL API with REST fallback."""
        cache_key = f"followers_{self.username}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return [FollowerInfo(**item) for item in cached]

        followers: List[FollowerInfo] = []

        # Attempt GraphQL first if token present
        if self.token:
            gql = """
            query($username: String!, $limit: Int!) {
              user(login: $username) {
                followers(first: $limit) {
                  nodes {
                    login
                    name
                    avatarUrl
                    url
                  }
                }
              }
            }
            """
            result = self._graphql_query(gql, {"username": self.username, "limit": limit})
            if result and "data" in result and result["data"].get("user"):
                nodes = result["data"]["user"]["followers"]["nodes"]
                for n in nodes:
                    followers.append(
                        FollowerInfo(
                            login=n["login"],
                            name=n.get("name") or n["login"],
                            avatar_url=n["avatarUrl"],
                            html_url=n["url"],
                        )
                    )

        # REST fallback if GraphQL yielded empty
        if not followers:
            data = self._http_get(f"users/{self.username}/followers?per_page={limit}")
            if data and isinstance(data, list):
                for item in data:
                    followers.append(
                        FollowerInfo(
                            login=item["login"],
                            name=item["login"],
                            avatar_url=item.get("avatar_url", ""),
                            html_url=item.get("html_url", ""),
                        )
                    )

        if followers:
            self.cache.set(cache_key, [f.__dict__ for f in followers])
            return followers

        stale = self.cache.get_stale_or_default(cache_key)
        if stale:
            return [FollowerInfo(**item) for item in stale]

        return [
            FollowerInfo(
                login="rogerio-jose-gastao",
                name="Rogério Gastão",
                avatar_url="https://github.com/rogerio-jose-gastao.png",
                html_url="https://github.com/rogerio-jose-gastao",
            )
        ]

    def fetch_user_stats(self) -> Dict[str, Any]:
        """Fetch general stats (repo count, language breakdown)."""
        cache_key = f"user_stats_{self.username}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        data = self._http_get(f"users/{self.username}")
        repos_count = data.get("public_repos", 24) if data else 24

        stats = {
            "public_repos": repos_count,
            "research_notes": 531,
            "projects_count": 13,
            "languages": ["Rust", "Python", "C"],
        }
        self.cache.set(cache_key, stats)
        return stats
