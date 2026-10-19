// SPDX-License-Identifier: GPL-3.0-or-later
#include "AppleTape40SC.h"
#include "AppleTape40SC_protocol.h"
extern "C" {
#include <scsi.h>
}
#include <cassert>
#include <cstdio>
MockScsiDev scsiDev{};
int main()
{
    MockTarget target{};
    scsiDev.target = &target;
    for (int op = 0; op != 256; ++op)
    {
        scsiDev.cdb[0] = op;
        scsiDev.status = 999;
        scsiDev.phase = 888;
        target.sense = {0,0};
        const int handled = scsiAppleTape40SCCommand();
        if (AppleTape40SC::isUnverifiedOpcode((uint8_t)op))
        {
            assert(handled == 1);
            assert(scsiDev.status == CHECK_CONDITION);
            assert(scsiDev.phase == STATUS);
            assert(target.sense.code == ILLEGAL_REQUEST);
            assert(target.sense.asc == INVALID_FIELD_IN_CDB);
        }
        else
        {
            assert(handled == 0);
            assert(scsiDev.status == 999 && scsiDev.phase == 888);
        }
    }
    std::puts("PASS: AppleTape40SC dispatcher (256 opcodes)");
}
