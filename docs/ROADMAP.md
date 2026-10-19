# Implementation roadmap

| Rev | Scope | Exit criteria |
| --- | --- | --- |
| R0 | Opt-in tape personality, 8192-byte image, unsafe-command guard | Host tests, patch integration; full Pico build pending |
| R1 | Hardware INQUIRY, REQUEST SENSE and reset behavior | Golden vectors from original hardware |
| R2 | 3M MCD-40 controller commands | Per-command command/response/status tests |
| R3 | Real block addressing and QIC-100 metadata, format | Apple's tape formatter and read/verify work |
| R4 | Original Macintosh and IIgs software compatibility | Back up, restore and compare known data |
| R5 | Chassis event interface | Motor motion and indicator behavior driven by nonblocking events |

R0 is a guarded exploratory implementation, not a 40SC emulator ready for data.
