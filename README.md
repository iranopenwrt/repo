# IranOpenWrt repository

## Usage

### Add repository signing key

Download :

```sh
wget -O /etc/apk/keys/iranopenwrt-feed.pem https://iranopenwrt.github.io/repo/key.pem
```

Offline :

```sh
cat << "EOF" > /etc/apk/keys/iranopenwrt-feed.pem
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAESQusoT81KfR4u5/XYsYDuQt4QiNk
9tO2fi3CVwjXUCPLvtdF5KkHgMSlFwjY2b1/K07NKJoyWre/tCUSItmJ+w==
-----END PUBLIC KEY-----
EOF
```

### Add IranOpenWrt repository

```sh
. /etc/openwrt_release

release="${DISTRIB_RELEASE%.*}"
arch="$DISTRIB_ARCH"

echo "https://iranopenwrt.github.io/repo/${release}/${arch}/packages.adb" >> /etc/apk/repositories.d/customfeeds.list
```

### Update package index

```sh
apk update
```

### Install packages from IranOpenWrt repository

```sh
apk add aether paqet chisel
```

## Repository CI

Packages are built and published to GitHub Pages by
`.github/workflows/publish.yml` on pushes to `main`. The workflow builds only a
package whose `PKG_VERSION` or `PKG_RELEASE` changed, or whose configured
OpenWrt release/architecture has not been published yet. Package source changes
without a version or release bump are intentionally not rebuilt.

The release, architecture, and package lists are maintained in
`.github/repository.json`. The initial build targets OpenWrt 25.12.5 for:

- `arm_cortex-a7_neon-vfpv4`
- `aarch64_cortex-a53`
- `aarch64_cortex-a72`
- `aarch64_cortex-a76`
- `arm_cortex-a9_vfpv3-d16`
- `x86_64`

Each architecture is compiled in one SDK workspace. This builds the Go host
toolchain once for all selected Go packages on that architecture and similarly
avoids duplicate Rust host builds.

### Required repository setup

1. Add an Actions repository secret named `APK_PRIVATE_KEY` containing the PEM
   private key corresponding to `key.pem`.
2. In **Settings → Pages**, select **GitHub Actions** as the Pages source. The
   standard workflow token cannot enable Pages on a repository where it has not
   already been enabled.

The generated `gh-pages` branch is replaced with a single snapshot commit after
each successful deployment, so APK binaries do not accumulate in Git history.
