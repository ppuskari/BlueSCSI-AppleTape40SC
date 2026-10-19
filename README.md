# BlueSCSI Apple Tape Backup 40SC

Experimental **Apple Tape Backup 40SC / 3M MCD-40** compatibility personality for BlueSCSI V2.

**R0 status: initial integration scaffold. Not yet a functional or authentic Apple 40SC. Do not use this revision for valuable backups.**

This project is a **source overlay**, not a fork of the full BlueSCSI tree. It clones pinned upstream firmware and integrates our code; the original source remains obtainable and its history is preserved.

## Tested foundation

- Upstream: https://github.com/BlueSCSI/BlueSCSI-v2
- Base commit: 5e64e3b4a09088c67a2a6728385600ea67ddbe0d (Oct 3, 2026).
- Native g++ C++17 protocol and dispatcher tests cover all 256 opcodes.
- Full Pico/Pico 2 firmware compile and hardware SCSI interoperability still **unverified**.

## Quick start (Linux, macOS, or WSL)

~~~sh
git clone https://github.com/ppuskari/BlueSCSI-AppleTape40SC.git
cd BlueSCSI-AppleTape40SC
bash tests/run_host_tests.sh
bash tools/bootstrap.sh
cd work/BlueSCSI-v2
~~~

The bootstrap script checks out the pinned BlueSCSI upstream into work/BlueSCSI-v2, then applies the source overlay. A network connection is required. It will not overwrite an existing checkout.

Build with the current upstream toolchain (see its BUILDING.md), using Bash 4+ and the proper Pico target:

~~~sh
nix develop -c ./build.sh Pico        # RP2040
nix develop -c ./build.sh Pico_2      # RP2350
~~~

For non-Nix systems follow upstream BUILDING.md to set PICO_SDK_PATH, PICO_EXTRAS_PATH and the ARM toolchain. A successfully compiled UF2 alone does **not** prove 40SC command compatibility.

## SD test setup

Create a new non-QIC, experimental image (4848 x 8192 bytes = 39,714,816 bytes):

~~~sh
python3 utils/apple40sc_create_image.py TP1_8192.img
~~~

Copy examples/bluescsi.ini to the SD root as bluescsi.ini, along with the raw image:

~~~ini
[SCSI1]
Type = tape
BlockSize = 8192
AppleTape40SC = 1
~~~

Only SCSI ID 1 is enabled by this example. R0 validates 8192-byte blocks and a single raw image. The capacity is based on one historical observation, not yet a universal 40SC specification.

**Protocol limitations:** 3M-specific opcodes and known generic collisions deliberately return CHECK CONDITION rather than fabricated success. READ(6) and WRITE(6) provisionally take the generic BlueSCSI tape path; the 3M block-addressed format has not been implemented. INQUIRY strings remain generic/configurable until real hardware identification bytes are captured.

## Layout

- src/AppleTape40SC* — native personality with explicit opcode guard and geometry constants
- tools/apply_overlay.py — guarded source edits against exact pinned upstream
- tools/bootstrap.sh — upstream clone, checkout and overlay application
- tests/ — C++17 host protocol and dispatcher tests
- docs/PROTOCOL_CAPTURE.md — safe characterization of the original MCD-40
- docs/ROADMAP.md — milestones through physical mechanism animation
- examples/bluescsi.ini — experimental configuration

## Next steps

1. Build Pico/Pico 2 firmware, fix any integration problems.
2. Read INQUIRY and sense data from at least two of the four original MCD-40 controllers using safe SCSI discovery commands.
3. Add measured controller-specific commands, QIC-100 metadata, real block-addressable behavior and tests.
4. Validate backup/restore with original Macintosh and GS/OS software.
5. Emit nonblocking events to a secondary MCU for LEDs, forward/reverse motor motion and dummy tape reels.

## License

New source code GPL-3.0-or-later, matching the upstream firmware. Preserve all upstream licenses and copyright notices when compiling and redistributing firmware. See LICENSE.
