#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

chown -f root:root /opt/piss/chrome-sandbox || true
chmod -f 4755 /opt/piss/chrome-sandbox || true
ln -s /opt/piss/resources/app.asar.unpacked/daemon/piss /usr/bin/piss || true
ln -s /opt/piss/piss-blockchain /usr/bin/piss-blockchain || true
