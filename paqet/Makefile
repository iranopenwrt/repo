# SPDX-License-Identifier: GPL-2.0-only

include $(TOPDIR)/rules.mk

PKG_NAME:=paqet
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

PKG_SOURCE:=v$(PKG_VERSION)-alpha.21.tar.gz
PKG_SOURCE_URL:=https://github.com/hanselime/paqet/archive/refs/tags
PKG_HASH:=b4842eba72f117742efc21b22d2694daf936f98faf71cfc30ea95da11dc8e352

PKG_LICENSE:=GPL-2.0
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/paqet-$(PKG_VERSION)-alpha.21

PKG_BUILD_DEPENDS:=golang/host
PKG_BUILD_PARALLEL:=1
PKG_BUILD_FLAGS:=no-mips16

GO_PKG:=paqet

CGO_ENABLED:=1

BUILD_TIME:=$(shell date -u -d "@$(SOURCE_DATE_EPOCH)" "+%Y-%m-%d_%H:%M:%S-UTC")

GO_PKG_LDFLAGS_X:= \
	paqet/cmd/version.GitTag="v$(PKG_VERSION)-alpha.21" \
	paqet/cmd/version.BuildTime=$(BUILD_TIME)


include $(INCLUDE_DIR)/package.mk
include $(TOPDIR)/feeds/packages/lang/golang/golang-package.mk


define Package/paqet
  SECTION:=net
  CATEGORY:=Network
  TITLE:=paqet - Transport over Raw Packet
  URL:=https://github.com/hanselime/paqet
  # paqet uses pcap, so it needs libpcap and CGO support
  DEPENDS:=$(GO_ARCH_DEPENDS) +libpcap
endef

define Package/paqet/description
  Paqet is a bidirectional Packet-level proxy built using raw sockets in Go.
  It forwards traffic from a local client to a remote server using KCP
  for secure, reliable transport, bypassing the host TCP/IP stack.
endef

define Package/paqet/install
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/paqet.init $(1)/etc/init.d/paqet

	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_CONF) ./files/paqet.config $(1)/etc/config/paqet

	$(INSTALL_DIR) $(1)/etc/paqet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/example/client.yaml.example $(1)/etc/paqet/
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/example/server.yaml.example $(1)/etc/paqet/
	$(INSTALL_CONF) ./files/paqet-server.nft $(1)/etc/paqet/


	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(GO_PKG_BUILD_BIN_DIR)/cmd $(1)/usr/bin/paqet
endef

$(eval $(call BuildPackage,paqet))
