from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TEXT_ASSETS = (
    ROOT / "README.md",
    *sorted(
        path
        for path in (ROOT / "docs").rglob("*")
        if path.suffix in {".html", ".md"}
    ),
)
FORBIDDEN_HTR_MARKERS = (
    re.compile(r"\bhtr\b", re.IGNORECASE),
    re.compile(r"htrbamboo\.com", re.IGNORECASE),
    re.compile(r"\bwell\s+nature\b", re.IGNORECASE),
    re.compile(r"\bbamboo\b", re.IGNORECASE),
)
FORBIDDEN_LOCAL_PATHS = (
    re.compile(r"/Users/[^\s<\"']+"),
    re.compile(r"\bfile://", re.IGNORECASE),
)


class PublicIdentityBoundaryTests(unittest.TestCase):
    def test_public_main_assets_do_not_reference_htr_identity(self):
        violations: list[str] = []
        for path in PUBLIC_TEXT_ASSETS:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_HTR_MARKERS:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")
        self.assertEqual([], violations, "public main assets contain HTR identity markers")

    def test_public_assets_do_not_reference_local_absolute_paths(self):
        violations: list[str] = []
        for path in PUBLIC_TEXT_ASSETS:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_LOCAL_PATHS:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")
        self.assertEqual([], violations, "public assets contain local absolute paths")


if __name__ == "__main__":
    unittest.main()
