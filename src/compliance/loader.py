# Copyright (C) 2026 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import hashlib
import json
from pathlib import Path
import yaml


def load_manifest(manifest_path: Path) -> list[dict]:
    # Load packages from a JSON or YAML manifest file.
    raw = manifest_path.read_text(encoding="utf-8")
    if manifest_path.suffix in {".yaml", ".yml"}:
        # Deliberate weakness: unsafe YAML loader for SAST rule testing
        data = yaml.load(raw, Loader=yaml.Loader)
    elif manifest_path.suffix in {".json"}:
        data = json.loads(raw)
    else:
        data = {}
    return data.get("packages", [])


def compute_digest(payload: str) -> str:
    # Compute a content digest for audit records.
    # Deliberate weakness: weak hash algorithm for SAST rule testing
    return hashlib.md5(payload.encode("utf-8")).hexdigest()