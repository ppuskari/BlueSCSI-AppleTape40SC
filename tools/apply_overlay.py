#!/usr/bin/env python3
"""Apply R0 to a clean checkout of a pinned BlueSCSI-v2 revision."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PIN = "5e64e3b4a09088c67a2a6728385600ea67ddbe0d"
REPLACE = {
    "CMakeLists.txt": [
        ("    src/BlueSCSI_tape.cpp\n",
         "    src/BlueSCSI_tape.cpp\n    src/AppleTape40SC.cpp\n"),
    ],
    "src/BlueSCSI_disk.h": [
        ("    bool     tape_load_next_file;\n",
         "    bool     tape_load_next_file;\n    bool     appleTape40SC; // opt-in MCD-40 mode\n"),
    ],
    "src/BlueSCSI_disk.cpp": [
        ('#include "BlueSCSI_disk.h"\n',
         '#include "BlueSCSI_disk.h"\n#include "AppleTape40SC_protocol.h"\n'),
        ("    img.cdrom_track_end_lba = 0;\n    scsiDiskSetImageConfig(target_idx);\n",
         "    img.cdrom_track_end_lba = 0;\n    img.appleTape40SC = false;\n    scsiDiskSetImageConfig(target_idx);\n"),
        ("            img.tape_load_next_file = true;\n        }\n        else if (type == S2S_CFG_ZIP100)\n",
         "            img.tape_load_next_file = true;\n"
         "            char section[12];\n"
         '            snprintf(section, sizeof(section), "SCSI%d", target_idx);\n'
         '            if (ini_getbool(section, "AppleTape40SC", false, CONFIGFILE))\n'
         "            {\n"
         "                if (blocksize != AppleTape40SC::kBlockSize ||\n"
         "                    img.file.isFolder() ||\n"
         "                    (img.file.size() % AppleTape40SC::kBlockSize))\n"
         "                {\n"
         '                    logmsg("AppleTape40SC needs one 8192-byte/block image");\n'
         "                    img.file.close();\n"
         "                    return false;\n"
         "                }\n"
         "                img.appleTape40SC = true;\n"
         '                logmsg("AppleTape40SC R0 enabled on ID ", target_idx);\n'
         "            }\n"
         "        }\n        else if (type == S2S_CFG_ZIP100)\n"),
    ],
    "src/BlueSCSI_tape.cpp": [
        ('#include "BlueSCSI_config.h"\n',
         '#include "BlueSCSI_config.h"\n#include "AppleTape40SC.h"\n'),
        ("    uint8_t command = scsiDev.cdb[0];\n    if (command == 0x08)\n",
         "    uint8_t command = scsiDev.cdb[0];\n"
         "    if (img.appleTape40SC && scsiAppleTape40SCCommand())\n"
         "        return 1;\n"
         "    if (command == 0x08)\n"),
    ],
}
NEW = {
    "src/AppleTape40SC_protocol.h": "src/AppleTape40SC_protocol.h",
    "src/AppleTape40SC.h": "src/AppleTape40SC.h",
    "src/AppleTape40SC.cpp": "src/AppleTape40SC.cpp",
    "tests/host_protocol.cpp": "tests/host_protocol.cpp",
    "tests/host_dispatch.cpp": "tests/host_dispatch.cpp",
    "tests/stubs/scsi.h": "tests/stubs/scsi.h",
    "tests/stubs/BlueSCSI_log.h": "tests/stubs/BlueSCSI_log.h",
    "tests/run_host_tests.sh": "tests/run_host_tests.sh",
    "docs/AppleTape40SC_PROTOCOL_CAPTURE.md": "docs/PROTOCOL_CAPTURE.md",
    "docs/AppleTape40SC_ROADMAP.md": "docs/ROADMAP.md",
}

def git(work, *args):
    return subprocess.check_output(["git", "-C", str(work), *args], text=True).strip()

def run(work, check):
    if not (work / ".git").exists():
        raise ValueError("Target must be an existing Git checkout")
    if git(work, "rev-parse", "HEAD") != PIN:
        raise ValueError("Expected BlueSCSI upstream commit " + PIN)
    if git(work, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Checkout has tracked changes, refusing to overwrite")
    edits = {}
    for name, replacements in REPLACE.items():
        old_text = (work / name).read_text(encoding="utf-8")
        new_text = old_text
        for old, new in replacements:
            if new_text.count(old) != 1:
                raise ValueError("Missing/duplicate source anchor in " + name)
            new_text = new_text.replace(old, new, 1)
        edits[name] = new_text
    for name, original in NEW.items():
        if (work / name).exists():
            raise ValueError("Refusing existing file " + name)
        if not (ROOT / original).is_file():
            raise ValueError("Missing overlay file " + original)
    if check:
        print("PASS: pinned revision, clean checkout, anchors and destinations")
        return
    for name, source in edits.items():
        (work / name).write_text(source, encoding="utf-8")
    for name, original in NEW.items():
        dest = work / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / original, dest)
    print("PASS: R0 overlay integrated. Use upstream BUILDING.md to compile.")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("destination", type=Path)
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    try:
        run(a.destination.resolve(), a.check)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(1)
