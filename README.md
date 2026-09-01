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
