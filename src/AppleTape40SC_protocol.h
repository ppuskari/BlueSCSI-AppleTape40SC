// SPDX-License-Identifier: GPL-3.0-or-later
// Candidate 3M MCD-40 opcodes require verification against actual hardware.
#pragma once
#include <stdint.h>
namespace AppleTape40SC {
constexpr uint32_t kBlockSize = 8192;
constexpr uint32_t kReferenceBlocks = 4848;
constexpr uint64_t kReferenceBytes = static_cast<uint64_t>(kBlockSize) * kReferenceBlocks;
constexpr bool isUnverifiedOpcode(uint8_t opcode)
{
    switch (opcode)
    {
        case 0x04: // FORMAT UNIT
        case 0x05: // Generic READ BLOCK LIMITS collision
        case 0x06:
        case 0x0E:
        case 0x10: // Generic WRITE FILEMARKS collision
        case 0x11: // Generic SPACE collision
        case 0x13: // Generic VERIFY collision
        case 0x14:
        case 0x19: // Generic ERASE is currently a stub
        case 0x2B: // Generic LOCATE unverified
        case 0x34: // Generic READ POSITION unverified
            return true;
        default: return false;
    }
}
} // namespace AppleTape40SC
