# SPDX-License-Identifier: GPL-2.0-only

include $(TOPDIR)/rules.mk

PKG_NAME:=aether
PKG_VERSION:=1.7.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/CluvexStudio/Aether/tar.gz/v$(PKG_VERSION)?
PKG_HASH:=1b8d1fd2e463951ffcb4d093b32b438e464258db681b3577555c0e7b03eb1e67

PKG_LICENSE:=AGPL-3.0-only
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/Aether-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=rust/host
PKG_BUILD_PARALLEL:=1

MAKE_PATH:=aether

include $(INCLUDE_DIR)/package.mk
include ../../lang/rust/rust-package.mk

# boring-sys generates bindings with host clang. Point clang at the OpenWrt
# target headers so it does not parse the build host's libc headers as if they
# belonged to the target. OpenWrt uses modern musl with 64-bit time_t on 32-bit
# targets, so libc's Rust definitions must use the matching ABI as well.
CARGO_PKG_VARS += \
	BINDGEN_EXTRA_CLANG_ARGS="--target=$(RUSTC_TARGET_ARCH) --sysroot=$(TOOLCHAIN_DIR)" \
	RUST_LIBC_UNSTABLE_MUSL_V1_2_3=1

define Package/aether
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Censorship circumvention client
  URL:=https://github.com/CluvexStudio/Aether
  DEPENDS:=$(RUST_ARCH_DEPENDS)
endef

define Package/aether/description
  Aether discovers reachable routes, establishes an encrypted tunnel and
  exposes a local SOCKS5 proxy.
endef

define Package/aether/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/bin/aether $(1)/usr/bin/aether
endef

$(eval $(call BuildPackage,aether))
