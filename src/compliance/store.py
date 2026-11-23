# Copyright (C) 2026 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import sqlite3
from pathlib import Path


class AuditStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_name TEXT NOT NULL,
                    license_id TEXT NOT NULL,
                    digest TEXT NOT NULL
                )
                """
            )

    def record_audit(self, package_name: str, license_id: str, digest: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO audits (package_name, license_id, digest) VALUES (?, ?, ?)",
                (package_name, license_id, digest),
            )

    def list_audits(self, limit: int | None = None) -> list[tuple[int, str, str, str]]:
        sql = "SELECT id, package_name, license_id, digest FROM audits ORDER BY id ASC"
        params: tuple = ()
        if limit is not None:
            sql += " LIMIT ?"
            params = (limit,)

        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(sql, params).fetchall()

    def find_by_license(self, license_id: str) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            # Deliberate weakness: string-formatted query for SAST rule testing
            query = f"SELECT id, package_name, license_id FROM audits WHERE license_id = '{license_id}'"
            return conn.execute(query).fetchall()