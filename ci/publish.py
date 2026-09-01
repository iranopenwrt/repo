#!/usr/bin/env python3

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from common import load_config, load_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--index-list", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    manifest = load_manifest(args.site)
    repositories = manifest["repositories"]
    valid_repositories = {
        f"{release['series']}/{arch}"
        for release in config["releases"]
        for arch in config["architectures"]
    }
    valid_sources = {package["source"] for package in config["packages"]}
    affected = set()

    for repo_key in list(repositories):
        if repo_key not in valid_repositories:
            shutil.rmtree(args.site / repo_key, ignore_errors=True)
            del repositories[repo_key]
            continue
        sources = repositories[repo_key].setdefault("sources", {})
        for source in list(sources):
            if source not in valid_sources:
                remove_outputs(args.site / repo_key, sources[source])
                del sources[source]
                affected.add(repo_key)

    if args.artifacts.is_dir():
        for metadata_path in args.artifacts.rglob("metadata.json"):
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("schema") != 1:
                raise ValueError(f"unsupported build metadata: {metadata_path}")
            repo_key = f"{metadata['series']}/{metadata['arch']}"
            if repo_key not in valid_repositories:
                raise ValueError(f"build produced unconfigured repository: {repo_key}")
            destination = args.site / repo_key
            destination.mkdir(parents=True, exist_ok=True)
            repository = repositories.setdefault(repo_key, {"sources": {}})
            for source, data in metadata["sources"].items():
                old = repository["sources"].get(source)
                if old:
                    remove_outputs(destination, old)
                for output in data["outputs"]:
                    source_file = metadata_path.parent / "packages" / output["filename"]
                    digest = hashlib.sha256(source_file.read_bytes()).hexdigest()
                    if digest != output["sha256"]:
                        raise ValueError(f"checksum mismatch: {source_file}")
                    shutil.copy2(source_file, destination / output["filename"])
                repository["sources"][source] = data
            affected.add(repo_key)

    for repo_key in valid_repositories:
        repositories.setdefault(repo_key, {"sources": {}})
    shutil.copy2(args.repo / "key.pem", args.site / "key.pem")
    (args.site / ".nojekyll").touch()
    manifest["generated_at"] = datetime.now(timezone.utc).isoformat()
    (args.site / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    args.index_list.write_text("".join(f"{item}\n" for item in sorted(affected)), encoding="utf-8")


def remove_outputs(directory: Path, source: dict) -> None:
    for output in source.get("outputs", []):
        filename = output.get("filename", "")
        if filename and Path(filename).name == filename:
            (directory / filename).unlink(missing_ok=True)


if __name__ == "__main__":
    main()

