"""Read-only Interactive HTML Sitemap & UI/UX Spec extractor."""

from .extractor import (
    AUTO_EXTRACT_ALL_MAX_SCREENS,
    SitemapExtractResult,
    extract_sitemap,
    inspect_sitemap,
    is_interactive_sitemap_html,
)

__all__ = [
    "AUTO_EXTRACT_ALL_MAX_SCREENS",
    "SitemapExtractResult",
    "extract_sitemap",
    "inspect_sitemap",
    "is_interactive_sitemap_html",
]
