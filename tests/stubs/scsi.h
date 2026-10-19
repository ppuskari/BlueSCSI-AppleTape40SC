// Host-only BlueSCSI SCSI API subset; not intended for embedded firmware.
#pragma once
#include <stdint.h>
#define CHECK_CONDITION 0x02
#define ILLEGAL_REQUEST 0x05
#define INVALID_FIELD_IN_CDB 0x2400
#define STATUS 3
struct MockSense { int code; int asc; };
struct MockTarget { MockSense sense; };
struct MockScsiDev { uint8_t cdb[16]; int status; int phase; MockTarget* target; };
extern MockScsiDev scsiDev;
