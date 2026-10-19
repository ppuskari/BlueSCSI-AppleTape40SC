#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
root="$(pwd)"
out="$root/work/BlueSCSI-v2"
if [ -e "$out" ]; then
    echo "Refusing existing destination: $out" >&2
    exit 1
fi
mkdir -p "$root/work"
git clone --recurse-submodules https://github.com/BlueSCSI/BlueSCSI-v2.git "$out"
git -C "$out" checkout 5e64e3b4a09088c67a2a6728385600ea67ddbe0d
git -C "$out" switch -c feature/apple-tape40sc-r0
python3 "$root/tools/apply_overlay.py" --check "$out"
python3 "$root/tools/apply_overlay.py" "$out"
bash "$root/tests/run_host_tests.sh"
echo "Prepared $out. Build there with the upstream BUILDING.md toolchain."
