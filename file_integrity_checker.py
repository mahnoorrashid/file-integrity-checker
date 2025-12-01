#!/usr/bin/env python3
"""
File Integrity Checker

- Creates a baseline of file hashes in a directory
- Later, compares current hashes to the baseline to spot changes

Author: Mahnoor Rashid
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict

BASELINE_FILE = "baseline.json"


def hash_file(path: Path) -> str:
    """
    Calculate SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def build_baseline(target_dir: Path) -> Dict[str, str]:
    """
    Walk through target_dir and build a mapping:
    { "relative/path/to/file": "sha256hash" }
    """
    baseline = {}

    for root, _, files in os.walk(target_dir):
        for name in files:
            file_path = Path(root) / name
            # store relative path so it works even if you move the folder
            rel_path = str(file_path.relative_to(target_dir))
            baseline[rel_path] = hash_file(file_path)

    return baseline


def save_baseline(baseline: Dict[str, str], target_dir: Path) -> None:
    """
    Save the baseline hashes + base directory to a JSON file.
    """
    data = {
        "base_dir": str(target_dir.resolve()),
        "files": baseline,
    }
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Baseline saved to {BASELINE_FILE}")


def load_baseline() -> Dict:
    """
    Load baseline JSON from disk.
    """
    if not Path(BASELINE_FILE).exists():
        print(f"[!] No {BASELINE_FILE} found. Create a baseline first.")
        return {}

    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def check_integrity() -> None:
    """
    Compare current file hashes with the saved baseline.
    """
    baseline_data = load_baseline()
    if not baseline_data:
        return

    base_dir = Path(baseline_data["base_dir"])
    old_files = baseline_data["files"]

    print(f"[+] Loaded baseline for: {base_dir}")
    print("[*] Scanning current files...\n")

    current_files: Dict[str, str] = {}

    # Rebuild current hashes
    for root, _, files in os.walk(base_dir):
        for name in files:
            file_path = Path(root) / name
            rel_path = str(file_path.relative_to(base_dir))
            current_files[rel_path] = hash_file(file_path)

    modified = []
    new_files = []
    missing = []

    # Check for modified or missing files
    for rel_path, old_hash in old_files.items():
        if rel_path not in current_files:
            missing.append(rel_path)
        elif current_files[rel_path] != old_hash:
            modified.append(rel_path)

    # Check for new files
    for rel_path in current_files:
        if rel_path not in old_files:
            new_files.append(rel_path)

    print("===== INTEGRITY REPORT =====")
    if modified:
        print("\nModified files:")
        for p in modified:
            print(f"  - {p}")
    else:
        print("\nModified files: None")

    if new_files:
        print("\nNew files since baseline:")
        for p in new_files:
            print(f"  - {p}")
    else:
        print("\nNew files: None")

    if missing:
        print("\nMissing files since baseline:")
        for p in missing:
            print(f"  - {p}")
    else:
        print("\nMissing files: None")

    print("\n[+] Check complete.")


def main():
    print("🔐 Simple File Integrity Checker")
    print("1) Create / update baseline")
    print("2) Check integrity against baseline")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        target = input(
            "Enter directory to monitor (e.g. . for current folder): "
        ).strip() or "."
        target_dir = Path(target)

        if not target_dir.exists() or not target_dir.is_dir():
            print("[!] That directory does not exist.")
            return

        print(f"[*] Building baseline for: {target_dir.resolve()}")
        baseline = build_baseline(target_dir)
        save_baseline(baseline, target_dir)

    elif choice == "2":
        check_integrity()
    else:
        print("[!] Invalid choice. Please run again and choose 1 or 2.")


if __name__ == "__main__":
    main()
