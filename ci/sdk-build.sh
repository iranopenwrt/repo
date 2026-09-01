#!/usr/bin/env bash

set -euo pipefail

: "${ARCH:?ARCH is required}"
: "${OUTPUT_PACKAGES:?OUTPUT_PACKAGES is required}"
: "${SOURCES:?SOURCES is required}"
: "${SDK_VERSION:?SDK_VERSION is required}"

cd /builder
[ -d scripts ] || ./setup.sh

sed \
  -e 's,https://git.openwrt.org/feed/,https://github.com/openwrt/,' \
  -e 's,https://git.openwrt.org/openwrt/,https://github.com/openwrt/,' \
  -e 's,https://git.openwrt.org/project/,https://github.com/openwrt/,' \
  feeds.conf.default > feeds.conf
echo 'src-link iranopenwrt /feed' >> feeds.conf
./scripts/feeds update -a

if [ -d /go-override/lang/golang ]; then
  rm -rf feeds/packages/lang/golang
  cp -a /go-override/lang/golang feeds/packages/lang/golang
  ./scripts/feeds update -i packages
  go_version="$(sed -n 's/^[[:space:]]*GO_DEFAULT_VERSION:=[[:space:]]*//p' \
    feeds/packages/lang/golang/golang-values.mk)"
  test -n "$go_version"
  ./scripts/feeds install -p packages -f \
    golang "golang${go_version}" golang-bootstrap
fi

for source in $SOURCES; do
  ./scripts/feeds install -p iranopenwrt -f "$source"
done

for package in $OUTPUT_PACKAGES; do
  echo "CONFIG_PACKAGE_${package}=m" >> .config
done
echo 'CONFIG_SIGNED_PACKAGES=y' >> .config
make defconfig
install -m 0600 /signing/private-key.pem private-key.pem

package_dir="bin/packages/${ARCH}/iranopenwrt"
mkdir -p "$package_dir" /artifacts/packages
: > /artifacts/outputs.tsv

for source in $SOURCES; do
  before="$(mktemp)"
  after="$(mktemp)"
  find "$package_dir" -maxdepth 1 -type f -name '*.apk' -printf '%f\n' | sort > "$before"
  make -j"$(nproc)" V=s "package/${source}/compile"
  find "$package_dir" -maxdepth 1 -type f -name '*.apk' -printf '%f\n' | sort > "$after"
  comm -13 "$before" "$after" | while IFS= read -r filename; do
    [ -n "$filename" ] || continue
    printf '%s\t%s\n' "$source" "$filename" >> /artifacts/outputs.tsv
    cp -a "$package_dir/$filename" /artifacts/packages/
  done
  rm -f "$before" "$after"
done
