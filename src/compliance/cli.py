# Copyright (C) 2026 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from compliance.loader import compute_digest, load_manifest
from compliance.store import AuditStore

def _render_audits(rows: list[tuple[int, str, str, str]]) -> None:

    table = Table(title="Stored Audit Records")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Package", style="bold")
    table.add_column("License")
    table.add_column("Digest", overflow="fold")

    for row_id, pkg_name, lic_id, digest in rows:
        table.add_row(str(row_id), pkg_name, lic_id, digest)

    Console().print(table)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample OSS compliance tester")
    parser.add_argument("manifest", type=Path, nargs="?", help="Path to JSON or YAML manifest")
    parser.add_argument("--db", type=Path, default=Path("audit.db"), help="SQLite DB path")
    parser.add_argument("--list", action="store_true", help="View stored records from the database")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows shown with --list")
    args = parser.parse_args(argv)

    store = AuditStore(args.db)

    if args.list:
        rows = store.list_audits(limit=args.limit)
        if len(rows) > 0:
            _render_audits(rows)
        else:
            print ("No data found.")
        return 0

    if args.manifest is None:
        parser.error("manifest is required unless --list is specified")

    packages = load_manifest(args.manifest)
    for pkg in packages:
        name = str(pkg.get("name", "unknown"))
        lic = str(pkg.get("license", "UNKNOWN"))
        digest = compute_digest(f"{name}:{lic}")
        store.record_audit(name, lic, digest)
    print(f"Processed {len(packages)} package entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())