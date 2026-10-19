#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -Wall -Wextra -Werror -Isrc tests/host_protocol.cpp -o "$tmp/host_protocol"
"$tmp/host_protocol"
g++ -std=c++17 -Wall -Wextra -Werror -Itests/stubs -Isrc tests/host_dispatch.cpp src/AppleTape40SC.cpp -o "$tmp/host_dispatch"
"$tmp/host_dispatch"
