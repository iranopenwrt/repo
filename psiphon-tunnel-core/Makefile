# SPDX-License-Identifier: GPL-2.0-only

include $(TOPDIR)/rules.mk

PKG_NAME:=psiphon-tunnel-core
PKG_VERSION:=2.0.40
PKG_RELEASE:=1

PKG_SOURCE:=v$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://github.com/Psiphon-Labs/psiphon-tunnel-core/archive/refs/tags
PKG_HASH:=62f0247a357f538796ff3962c97e79ea170b0ba3e833c9459fe6dff6c9e2ad5c

PKG_LICENSE:=GPL-3.0
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/psiphon-tunnel-core-$(PKG_VERSION)

PKG_BUILD_DEPENDS:=golang/host
PKG_BUILD_PARALLEL:=1
PKG_BUILD_FLAGS:=no-mips16

GO_PKG:=github.com/Psiphon-Labs/psiphon-tunnel-core

GO_PKG_BUILD_PKG:=\
	$(if $(CONFIG_PACKAGE_psiphon),$(GO_PKG)/ConsoleClient) \
	$(if $(CONFIG_PACKAGE_psiphond),$(GO_PKG)/Server)

GO_PKG_LDFLAGS_X:= \
	$(GO_PKG)/psiphon/common/buildinfo.buildDate=$(SOURCE_DATE_EPOCH) \
	$(GO_PKG)/psiphon/common/buildinfo.buildRepo=$(GO_PKG) \
	$(GO_PKG)/psiphon/common/buildinfo.buildRev=$(PKG_VERSION) \
	$(GO_PKG)/psiphon/common/buildinfo.goVersion=$(shell $(STAGING_DIR_HOSTPKG)/bin/go version | cut -d ' ' -f3)

include $(INCLUDE_DIR)/package.mk
include $(TOPDIR)/feeds/packages/lang/golang/golang-package.mk

define Package/psiphon
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Web Servers/Proxies
  TITLE:=Psiphon tunnel core Console Client
  URL:=https://github.com/Psiphon-Labs/psiphon-tunnel-core
  DEPENDS:=$(GO_ARCH_DEPENDS)
endef

define Package/psiphon/description
  Psiphon is a circumvention system that uses a combination of secure communication
  and obfuscation technologies. This package provides the CLI client program (psiphon).
endef

define Package/psiphond
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Web Servers/Proxies
  TITLE:=Psiphon tunnel core Server (Daemon)
  URL:=https://github.com/Psiphon-Labs/psiphon-tunnel-core
  DEPENDS:=$(GO_ARCH_DEPENDS)
endef

define Package/psiphond/description
  Psiphon is a circumvention system that uses a combination of secure communication
  and obfuscation technologies. This package provides the Server program (psiphond).
endef

define Package/psiphon/install
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./files/psiphon.conf $(1)/etc/config/psiphon

	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_CONF) ./files/psiphon.config $(1)/etc/psiphon.config

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/psiphon.init $(1)/etc/init.d/psiphon

	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(GO_PKG_BUILD_BIN_DIR)/ConsoleClient $(1)/usr/bin/psiphon
endef

define Package/psiphond/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(GO_PKG_BUILD_BIN_DIR)/Server $(1)/usr/bin/psiphond
endef

$(eval $(call BuildPackage,psiphon))
$(eval $(call BuildPackage,psiphond))
