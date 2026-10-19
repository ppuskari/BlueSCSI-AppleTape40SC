# Non-destructive 3M MCD-40 protocol capture

Four real Apple Tape Backup 40SC mechanisms are available, with deteriorated
rubber drive wheels. One has unspooled a cartridge after missed EOT detection.
**Do not run another full format or tape motion test until BOT/EOT detection
and transport reliability have been checked.**

With a compatible SCSI initiator, preferably without media or motion, inventory
the SCSI ID, controller PCB, ROM labels and original mechanism. Capture raw
CDBs, status, transfer direction/lengths and returned data in hex.

Start with:

- TEST UNIT READY: 00 00 00 00 00 00
- INQUIRY (request 36 bytes): 12 00 00 00 24 00
- REQUEST SENSE (up to 18 bytes): 03 00 00 00 12 00
  only when a real, non-destructively obtained CHECK CONDITION warrants it.

Only send MODE SENSE or 3M-native commands after confirming CDB layout from
the original engineering manual or reliable host software traces.

Capture vectors from at least two different drive controllers before hardcoding
the vendor/product/revision strings and command semantics. Document whether
each observed CHECK CONDITION is media-related or a controller response.
