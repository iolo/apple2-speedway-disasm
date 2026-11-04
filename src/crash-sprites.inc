; Two crash pictures: four rows of 16 lores bytes per picture.
; Runtime $1CB0-$1D2F; dump $5CB0-$5D2F.

crash_a_row0:
        .assert * = $1CB0, lderror, "address drift: crash_a_row0"
        .byte   $AA, $DA, $AA, $AA, $AD, $DA, $AA, $DD      ; $1CB0 / dump $5CB0
        .byte   $9A, $DD, $AA, $DA, $AD, $AA, $DA, $AA      ; $1CB8 / dump $5CB8
crash_a_row1:
        .assert * = $1CC0, lderror, "address drift: crash_a_row1"
        .byte   $AA, $AA, $AD, $AD, $DA, $AD, $9A, $AD      ; $1CC0 / dump $5CC0
        .byte   $AA, $9D, $AA, $9D, $AA, $AD, $AA, $AA      ; $1CC8 / dump $5CC8
crash_a_row2:
        .assert * = $1CD0, lderror, "address drift: crash_a_row2"
        .byte   $AA, $AD, $AD, $DA, $DA, $A9, $3A, $33      ; $1CD0 / dump $5CD0
        .byte   $33, $3A, $A9, $DA, $DA, $AD, $AD, $AA      ; $1CD8 / dump $5CD8
crash_a_row3:
        .assert * = $1CE0, lderror, "address drift: crash_a_row3"
        .byte   $AD, $AD, $DA, $D9, $9A, $9A, $33, $11      ; $1CE0 / dump $5CE0
        .byte   $11, $33, $9A, $9A, $D9, $DA, $AD, $AD      ; $1CE8 / dump $5CE8
crash_b_row0:
        .assert * = $1CF0, lderror, "address drift: crash_b_row0"
        .byte   $AA, $AD, $DA, $AA, $9A, $AA, $DD, $AA      ; $1CF0 / dump $5CF0
        .byte   $DD, $AA, $AA, $A9, $DA, $AD, $AA, $AA      ; $1CF8 / dump $5CF8
crash_b_row1:
        .assert * = $1D00, lderror, "address drift: crash_b_row1"
        .byte   $AA, $AD, $9A, $AD, $DA, $9A, $AD, $A9      ; $1D00 / dump $5D00
        .byte   $DD, $A9, $DA, $AD, $DA, $AD, $AD, $AA      ; $1D08 / dump $5D08
crash_b_row2:
        .assert * = $1D10, lderror, "address drift: crash_b_row2"
        .byte   $AD, $AD, $9D, $DA, $DA, $A9, $19, $11      ; $1D10 / dump $5D10
        .byte   $11, $1A, $A9, $DA, $DA, $AD, $9D, $AD      ; $1D18 / dump $5D18
crash_b_row3:
        .assert * = $1D20, lderror, "address drift: crash_b_row3"
        .byte   $DA, $DA, $DA, $A9, $A9, $A9, $11, $33      ; $1D20 / dump $5D20
        .byte   $33, $11, $A9, $A9, $A9, $DA, $DA, $DA      ; $1D28 / dump $5D28
