#!/usr/bin/env bash

set -euo pipefail

# Bindgen must load libclang from the same Debian runtime as the SDK. Host
# libraries cannot be mounted safely because their symlinks and glibc ABI may
# differ from the OpenWrt buildworker image.
if ! find -L /usr/lib/llvm-* -maxdepth 2 -type f \
  \( -name 'libclang.so' -o -name 'libclang.so.*' \) -print -quit 2>/dev/null | grep -q .; then
  apt-get update
  apt-get install --no-install-recommends --yes libclang-dev
  rm -rf /var/lib/apt/lists/*
fi

library="$(find -L /usr/lib/llvm-* -maxdepth 2 -type f \
  \( -name 'libclang.so' -o -name 'libclang.so.*' \) -print -quit)"
export LIBCLANG_PATH="$(dirname "$library")"

exec runuser -u buildbot --preserve-environment -- bash /feed/ci/sdk-build.sh
