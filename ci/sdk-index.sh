#!/usr/bin/env bash

set -euo pipefail

cd /builder
[ -d scripts ] || ./setup.sh
install -m 0600 /signing/private-key.pem private-key.pem
apk_bin="staging_dir/host/bin/apk"
[ -x "$apk_bin" ] || { echo "SDK apk tool is missing" >&2; exit 1; }

while IFS= read -r repository; do
  [ -n "$repository" ] || continue
  directory="/site/$repository"
  mapfile -t packages < <(find "$directory" -maxdepth 1 -type f -name '*.apk' -print | sort)
  if [ "${#packages[@]}" -eq 0 ]; then
    rm -f "$directory/packages.adb"
    continue
  fi
  temporary="$directory/packages.adb.new"
  "$apk_bin" mkndx \
    --root /builder \
    --keys-dir /builder \
    --allow-untrusted \
    --sign /builder/private-key.pem \
    --output "$temporary" \
    "${packages[@]}"
  mv "$temporary" "$directory/packages.adb"
done < /site/indexes.txt
rm -f /site/indexes.txt private-key.pem

