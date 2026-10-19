// SPDX-License-Identifier: GPL-3.0-or-later
// Experimental 3M MCD-40 compatibility personality. Not authentic yet.
#include "AppleTape40SC.h"
#include "AppleTape40SC_protocol.h"
#include "BlueSCSI_log.h"
extern "C" {
#include <scsi.h>
}

int scsiAppleTape40SCCommand()
{
    const uint8_t opcode = scsiDev.cdb[0];
    if (AppleTape40SC::isUnverifiedOpcode(opcode))
    {
        dbgmsg("AppleTape40SC R0: unverified 3M opcode ", (int)opcode);
        scsiDev.status = CHECK_CONDITION;
        scsiDev.target->sense.code = ILLEGAL_REQUEST;
        scsiDev.target->sense.asc = INVALID_FIELD_IN_CDB;
        scsiDev.phase = STATUS;
        return 1;
    }
    if (opcode == 0x08 || opcode == 0x0A)
    {
        // Provisional generic READ/WRITE path. Not proven to match MCD-40.
        dbgmsg("AppleTape40SC R0: generic transfer ", (int)opcode);
    }
    return 0;
}
