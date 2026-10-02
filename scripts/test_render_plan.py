#!/usr/bin/env python3
"""Regression checks for notebook render selection.

Run with Python 3.11 or newer. ``render_pdf`` uses 3.10 type syntax.

    python3.11 scripts/test_render_plan.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_pdf  # noqa: E402


def notebooks() -> list[Path]:
    """Two notebook paths. The files do not need to exist."""
    return [Path("notebooks/01_eda.ipynb"), Path("notebooks/02_modeling.ipynb")]


class RenderPlanTest(unittest.TestCase):
    """Cover the selection bugs that previously dropped or clobbered PDFs."""

    def test_named_source_only_renders_one_notebook_without_evidence(self) -> None:
        planned = render_pdf.plan_notebook_renders(
            notebooks(), "02_modeling", wants_evidence=False
        )
        self.assertEqual(
            [(path.name, attach) for path, attach in planned],
            [("02_modeling.ipynb", False)],
        )

    def test_named_evidence_attaches_only_to_that_notebook(self) -> None:
        planned = render_pdf.plan_notebook_renders(
            notebooks(), "01_eda.ipynb", wants_evidence=True
        )
        self.assertEqual(
            [(path.stem, attach) for path, attach in planned],
            [("01_eda", True)],
        )

    def test_unknown_name_exits(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            render_pdf.plan_notebook_renders(
                notebooks(), "does-not-exist", wants_evidence=False
            )
        self.assertIn("does-not-exist", str(caught.exception))

    def test_evidence_without_a_name_refuses_multiple_notebooks(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            render_pdf.plan_notebook_renders(
                notebooks(), None, wants_evidence=True
            )
        self.assertIn("--notebook", str(caught.exception))

    def test_one_notebook_receives_unnamed_evidence(self) -> None:
        only = [Path("notebooks/02_modeling.ipynb")]
        planned = render_pdf.plan_notebook_renders(only, None, wants_evidence=True)
        self.assertEqual(
            [(path.stem, attach) for path, attach in planned],
            [("02_modeling", True)],
        )


if __name__ == "__main__":
    unittest.main()
