#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path

from common import load_config, load_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    manifest = load_manifest(args.site)
    expected_repositories = {
        f"{release['series']}/{arch}"
        for release in config["releases"]
        for arch in config["architectures"]
    }
    expected_sources = {package["source"] for package in config["packages"]}
    if set(manifest["repositories"]) != expected_repositories:
        raise ValueError("manifest repository set does not match configuration")

    for repo_key, repository in manifest["repositories"].items():
        directory = args.site / repo_key
        if set(repository.get("sources", {})) != expected_sources:
            raise ValueError(f"incomplete source set in {repo_key}")
        expected_files = set()
        for source in repository["sources"].values():
            for output in source.get("outputs", []):
                filename = output["filename"]
                expected_files.add(filename)
                path = directory / filename
                if not path.is_file():
                    raise ValueError(f"missing published package: {repo_key}/{filename}")
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != output["sha256"]:
                    raise ValueError(f"published checksum mismatch: {repo_key}/{filename}")
        actual_files = {path.name for path in directory.glob("*.apk")}
        if actual_files != expected_files:
            raise ValueError(f"unexpected or missing APK files in {repo_key}")
        if expected_files and not (directory / "packages.adb").is_file():
            raise ValueError(f"missing package index in {repo_key}")


if __name__ == "__main__":
    main()

