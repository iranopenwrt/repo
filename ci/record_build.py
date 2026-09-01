#!/usr/bin/env python3

import argparse
import hashlib
import json
from pathlib import Path

from common import load_config, package_version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--series", required=True)
    parser.add_argument("--sdk-version", required=True)
    parser.add_argument("--arch", required=True)
    parser.add_argument("--go-commit", default="")
    parser.add_argument("--sources", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    package_config = {item["source"]: item for item in config["packages"]}
    requested = args.sources.split()
    observed = {source: [] for source in requested}
    mapping = args.artifacts / "outputs.tsv"
    if mapping.is_file():
        for line in mapping.read_text(encoding="utf-8").splitlines():
            source, filename = line.split("\t", 1)
            if source not in observed:
                raise ValueError(f"unexpected output source: {source}")
            observed[source].append(filename)

    sources = {}
    for source in requested:
        expected = package_config[source]["outputs"]
        filenames = sorted(observed[source])
        for package_name in expected:
            if not any(name.startswith(f"{package_name}-") and name.endswith(".apk") for name in filenames):
                raise ValueError(f"{source} did not produce expected APK {package_name}")
        version, pkg_release = package_version(args.repo, source)
        outputs = []
        for filename in filenames:
            path = args.artifacts / "packages" / filename
            if not path.is_file():
                raise ValueError(f"missing recorded APK: {filename}")
            outputs.append(
                {
                    "filename": filename,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        sources[source] = {
            "version": version,
            "release": pkg_release,
            "sdk_version": args.sdk_version,
            "go_commit": args.go_commit if package_config[source]["toolchain"] == "go" else "",
            "outputs": outputs,
        }

    metadata = {
        "schema": 1,
        "series": args.series,
        "arch": args.arch,
        "sources": sources,
    }
    (args.artifacts / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

