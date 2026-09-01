#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from common import load_config, load_manifest, package_version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--go-main-sha", required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    manifest = load_manifest(args.site)
    key_changed = not (args.site / "key.pem").is_file() or (
        (args.site / "key.pem").read_bytes() != (args.repo / "key.pem").read_bytes()
    )
    versions = {
        package["source"]: package_version(args.repo, package["source"])
        for package in config["packages"]
    }
    matrix = []
    expected_repositories = set()

    for release in config["releases"]:
        go_commit = args.go_main_sha if release.get("go_ref") == "main" else ""
        for arch in config["architectures"]:
            repo_key = f"{release['series']}/{arch}"
            expected_repositories.add(repo_key)
            published = manifest["repositories"].get(repo_key, {})
            published_sources = published.get("sources", {})
            stale = []
            selected_outputs = []
            for package in config["packages"]:
                source = package["source"]
                version, pkg_release = versions[source]
                old = published_sources.get(source, {})
                old_filenames = [item.get("filename", "") for item in old.get("outputs", [])]
                expected_outputs_present = all(
                    any(name.startswith(f"{output}-") and name.endswith(".apk") for name in old_filenames)
                    for output in package["outputs"]
                ) and all((args.site / repo_key / name).is_file() for name in old_filenames)
                if (
                    old.get("version") != version
                    or old.get("release") != pkg_release
                    or old.get("sdk_version") != release["version"]
                    or not expected_outputs_present
                    or key_changed
                ):
                    stale.append(source)
                    selected_outputs.extend(package["outputs"])
            if stale:
                matrix.append(
                    {
                        "series": release["series"],
                        "version": release["version"],
                        "arch": arch,
                        "go_commit": go_commit,
                        "sources": " ".join(stale),
                        "outputs": " ".join(selected_outputs),
                    }
                )

    configured_sources = {package["source"] for package in config["packages"]}
    needs_prune = set(manifest["repositories"]) != expected_repositories
    if not needs_prune:
        needs_prune = any(
            set(repository.get("sources", {})) != configured_sources
            for repository in manifest["repositories"].values()
        )
    result = {
        "matrix": {"include": matrix},
        "has_builds": bool(matrix),
        "has_changes": bool(matrix) or needs_prune or key_changed,
    }
    print(json.dumps(result, indent=2))
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"matrix={json.dumps(result['matrix'], separators=(',', ':'))}\n")
            output.write(f"has_builds={str(result['has_builds']).lower()}\n")
            output.write(f"has_changes={str(result['has_changes']).lower()}\n")


if __name__ == "__main__":
    main()
