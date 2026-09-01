#!/usr/bin/env python3

import json
import re
from pathlib import Path


VERSION_RE = re.compile(r"^PKG_VERSION\s*:?=\s*([^\s#]+)", re.MULTILINE)
RELEASE_RE = re.compile(r"^PKG_RELEASE\s*:?=\s*([^\s#]+)", re.MULTILINE)
SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    releases = config.get("releases", [])
    architectures = config.get("architectures", [])
    packages = config.get("packages", [])
    if not releases or not architectures or not packages:
        raise ValueError("releases, architectures, and packages must not be empty")

    _require_unique(releases, "series")
    _require_unique(architectures)
    _require_unique(packages, "source")
    for release in releases:
        _safe(release["series"], "release series")
        _safe(release["version"], "release version")
        if release.get("go_ref") is not None:
            _safe(release["go_ref"], "Go feed ref")
    for arch in architectures:
        _safe(arch, "architecture")
    for package in packages:
        _safe(package["source"], "package source")
        if package.get("toolchain") not in ("go", "rust"):
            raise ValueError(f"invalid toolchain for {package['source']}")
        if not package.get("outputs"):
            raise ValueError(f"no outputs configured for {package['source']}")
        _require_unique(package["outputs"])
        for output in package["outputs"]:
            _safe(output, "package output")
    return config


def package_version(repo: Path, source: str) -> tuple[str, str]:
    makefile = repo / source / "Makefile"
    if not makefile.is_file():
        raise ValueError(f"missing package Makefile: {makefile}")
    text = makefile.read_text(encoding="utf-8")
    version = VERSION_RE.search(text)
    release = RELEASE_RE.search(text)
    if not version or not release:
        raise ValueError(f"{makefile} must define PKG_VERSION and PKG_RELEASE")
    return version.group(1), release.group(1)


def load_manifest(site: Path) -> dict:
    path = site / "manifest.json"
    if not path.is_file():
        return {"schema": 1, "repositories": {}}
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema") != 1 or not isinstance(manifest.get("repositories"), dict):
        raise ValueError("unsupported published manifest schema")
    return manifest


def _safe(value: str, label: str) -> None:
    if not isinstance(value, str) or not SAFE_NAME_RE.fullmatch(value):
        raise ValueError(f"unsafe {label}: {value!r}")


def _require_unique(items: list, key: str | None = None) -> None:
    values = [item[key] for item in items] if key else items
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate values in {key or 'list'}")
