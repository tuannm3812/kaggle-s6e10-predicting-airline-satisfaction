#!/usr/bin/env python3
"""Archive the log of a Kaggle kernel's LATEST run.

Run this after every kernel run. It has to be done at the time: Kaggle
offers no way to fetch a past run's log. `kernels output
<owner>/<kernel>/<version>` accepts the version suffix its own help
advertises and silently returns the latest run; `ApiGetKernelRequest`
carries a `version_number` field that the server also ignores (both
verified 2026-09-07 — see assets/kernel_logs/README.md). S6E9 lost the logs for kernel versions 1–8 that way. This helper
exists so S6E10 does not repeat it.

Usage:
    python3 scripts/archive_kernel_log.py 1 eda
    python3 scripts/archive_kernel_log.py 1 eda --kernel eda
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARCHIVE = REPO / "assets" / "kernel_logs"
JSON_STAMP = re.compile(r'"notebook_version"\s*:\s*"(v\d+)"')
TEXT_STAMP = re.compile(r"NOTEBOOK_VERSION\s+(v\d+)")


def log_text(raw: str) -> str:
    """Join a Kaggle kernel log's streamed text.

    Args:
        raw: File contents. A JSON list of stream entries, or plain text.

    Returns:
        The concatenated log text the version stamps are printed into.
    """
    try:
        entries = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(entries, list):
        return "\n".join(str(entry.get("data", "")) for entry in entries)
    return raw


def notebook_versions(text: str) -> list[str]:
    """Return notebook-version stamps in the order they appear.

    Args:
        text: Combined stdout/stderr of one kernel run.

    Returns:
        Stamps such as `v1`, from either `"notebook_version": "v1"` or
        a printed `NOTEBOOK_VERSION v1` line.
    """
    return JSON_STAMP.findall(text) + TEXT_STAMP.findall(text)


def require_notebook_version(text: str, version: int) -> str:
    """Refuse to archive a log that does not report this kernel version.

    Args:
        text: Combined log text.
        version: Kernel version the caller claims this run produced.

    Returns:
        The matching stamp, for example `v2`.

    Raises:
        SystemExit: If the log has no stamp, or any stamp other than
            `v{version}`.
    """
    expected = f"v{int(version)}"
    found = sorted(set(notebook_versions(text)))
    if found != [expected]:
        seen = ", ".join(found) if found else "none"
        raise SystemExit(
            f"refusing to archive: log stamps {seen}, expected {expected}"
        )
    return expected


def self_check() -> None:
    """Prove the v1 log is recognized and a wrong version is refused."""
    raw = (ARCHIVE / "kernel_v01_eda.log").read_text()
    text = log_text(raw)
    require_notebook_version(text, 1)
    try:
        require_notebook_version(text, 2)
    except SystemExit as exc:
        if "expected v2" not in str(exc):
            raise
    else:
        raise SystemExit("v1 log was accepted as v2")
    require_notebook_version('{"notebook_version": "v3"}\n', 3)
    print("archive guard ok: v1 log matches v1 and rejects v2")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="kernel version this run produced")
    parser.add_argument("label", help="what it recorded, e.g. E11_new_features")
    parser.add_argument("--kernel", default="eda",
                        help="kernel directory under notebooks/kernels/")
    parser.add_argument("--self-check", action="store_true",
                        help="check the v1 log locally and exit")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return

    meta = REPO / "notebooks" / "kernels" / args.kernel / "kernel-metadata.json"
    if not meta.exists():
        sys.exit(f"no kernel metadata at {meta}")
    kernel_id = json.loads(meta.read_text())["id"]

    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["kaggle", "kernels", "output", kernel_id, "-p", td],
                       check=True, capture_output=True)
        logs = list(Path(td).glob("*.log"))
        if not logs:
            sys.exit(f"no log in the output of {kernel_id}")
        text = log_text(logs[0].read_text())
        stamp = require_notebook_version(text, int(args.version))

        ARCHIVE.mkdir(parents=True, exist_ok=True)
        dest = ARCHIVE / f"kernel_v{int(args.version):02d}_{args.label}.log"
        if dest.exists():
            sys.exit(f"{dest.name} already archived — refusing to overwrite")
        shutil.copy2(logs[0], dest)

    print(f"archived {dest.relative_to(REPO)} ({dest.stat().st_size // 1024} KB)")
    print(f"  the log reports notebook version {stamp}")
    print("  add a row to assets/kernel_logs/README.md")


if __name__ == "__main__":
    main()
