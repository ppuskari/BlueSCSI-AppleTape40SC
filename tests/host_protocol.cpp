// SPDX-License-Identifier: GPL-3.0-or-later
#include "AppleTape40SC_protocol.h"
#include <cassert>
#include <cstdio>
int main()
{
    static_assert(AppleTape40SC::kBlockSize == 8192);
    static_assert(AppleTape40SC::kReferenceBlocks == 4848);
    static_assert(AppleTape40SC::kReferenceBytes == 39714816ULL);
    for (int op = 0; op != 256; ++op)
    {
        const bool expected = op==0x04 || op==0x05 || op==0x06 ||
            op==0x0E || op==0x10 || op==0x11 || op==0x13 ||
            op==0x14 || op==0x19 || op==0x2B || op==0x34;
        assert(AppleTape40SC::isUnverifiedOpcode((uint8_t)op) == expected);
    }
    std::puts("PASS: AppleTape40SC protocol guard (256 opcodes)");
}
