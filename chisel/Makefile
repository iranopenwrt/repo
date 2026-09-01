# SPDX-License-Identifier: GPL-2.0-only

include $(TOPDIR)/rules.mk

PKG_NAME:=chisel
PKG_VERSION:=1.12.0
PKG_RELEASE:=1

PKG_SOURCE:=v$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://github.com/jpillora/chisel/archive/refs/tags
PKG_HASH:=5c25f054b64814f770725593db525faa1999960aecf4eb15c86529dea573c431

PKG_LICENSE:=GPL-2.0
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/chisel-$(PKG_VERSION)

PKG_BUILD_DEPENDS:=golang/host
PKG_BUILD_PARALLEL:=1
PKG_BUILD_FLAGS:=no-mips16

GO_PKG:=github.com/jpillora/chisel

GO_PKG_BUILD_PKG:=$(GO_PKG)

GO_PKG_LDFLAGS_X:=$(GO_PKG)/share.BuildVersion=$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk
include $(TOPDIR)/feeds/packages/lang/golang/golang-package.mk


define Package/chisel
  SECTION:=net
  CATEGORY:=Network
  TITLE:=chisel - Transport over Raw Packet
  URL:=https://github.com/jpillora/chisel/
  # chisel uses pcap, so it needs libpcap and CGO support
  DEPENDS:=$(GO_ARCH_DEPENDS)
endef

define Package/chisel/description
  Paqet is a bidirectional Packet-level proxy built using raw sockets in Go.
  It forwards traffic from a local client to a remote server using KCP
  for secure, reliable transport, bypassing the host TCP/IP stack.
endef

define Package/chisel/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(GO_PKG_BUILD_BIN_DIR)/chisel $(1)/usr/bin/chisel
endef

$(eval $(call BuildPackage,chisel))
