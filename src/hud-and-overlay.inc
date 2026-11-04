; Four 40-byte high-bit text HUD rows followed by the first four start-overlay rows.
; The cars-left field starts as $BA (colon); its initial decrement produces 9.
; Unconsumed tail bytes are retained, including screen-hole-like padding.
; Runtime $1EB0-$1FFF; dump $5EB0-$5FFF.

hud_blank_row0:
        .assert * = $1EB0, lderror, "address drift: hud_blank_row0"
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EB0 / dump $5EB0          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EB8 / dump $5EB8          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EC0 / dump $5EC0          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EC8 / dump $5EC8          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1ED0 / dump $5ED0          
hud_blank_row1:
        .assert * = $1ED8, lderror, "address drift: hud_blank_row1"
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1ED8 / dump $5ED8          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EE0 / dump $5EE0          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EE8 / dump $5EE8          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EF0 / dump $5EF0          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1EF8 / dump $5EF8          
hud_score_row:
        .assert * = $1F00, lderror, "address drift: hud_score_row"
        .byte   $A0, $A0, $A0, $A0, $A0, $D3, $C3, $CF      ; $1F00 / dump $5F00       SCO
        .byte   $D2, $C5, $A0, $BA, $A0, $B0, $B0, $B0      ; $1F08 / dump $5F08  RE : 000
        .byte   $B0, $B0, $B0, $B0, $B0, $A0, $A0, $CC      ; $1F10 / dump $5F10  00000  L
        .byte   $C5, $C6, $D4, $A0, $BA, $A0, $BA, $A0      ; $1F18 / dump $5F18  EFT : : 
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1F20 / dump $5F20          
hud_high_row:
        .assert * = $1F28, lderror, "address drift: hud_high_row"
        .byte   $A0, $A0, $A0, $A0, $A0, $C8, $C9, $C7      ; $1F28 / dump $5F28       HIG
        .byte   $C8, $A0, $A0, $BA, $A0, $A0, $A0, $A0      ; $1F30 / dump $5F30  H  :    
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1F38 / dump $5F38          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1F40 / dump $5F40          
        .byte   $A0, $A0, $A0, $A0, $A0, $A0, $A0, $A0      ; $1F48 / dump $5F48          
start_overlay_row0:
        .assert * = $1F50, lderror, "address drift: start_overlay_row0"
        .byte   $99, $99, $89, $89, $89, $99, $F9, $F9      ; $1F50 / dump $5F50
        .byte   $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9      ; $1F58 / dump $5F58
        .byte   $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9      ; $1F60 / dump $5F60
        .byte   $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9      ; $1F68 / dump $5F68
        .byte   $F9, $F9, $99, $89, $89, $89, $99, $99      ; $1F70 / dump $5F70
start_overlay_row1:
        .assert * = $1F78, lderror, "address drift: start_overlay_row1"
        .byte   $99, $99, $88, $88, $88, $99, $FF, $FF      ; $1F78 / dump $5F78
        .byte   $FF, $FF, $0F, $F0, $F0, $FF, $F0, $00      ; $1F80 / dump $5F80
        .byte   $F0, $FF, $0F, $F0, $0F, $FF, $00, $F0      ; $1F88 / dump $5F88
        .byte   $0F, $FF, $F0, $00, $F0, $FF, $FF, $FF      ; $1F90 / dump $5F90
        .byte   $FF, $FF, $99, $88, $88, $88, $99, $99      ; $1F98 / dump $5F98
start_overlay_row2:
        .assert * = $1FA0, lderror, "address drift: start_overlay_row2"
        .byte   $99, $99, $88, $88, $88, $99, $FF, $FF      ; $1FA0 / dump $5FA0
        .byte   $FF, $FF, $0F, $F0, $FF, $FF, $FF, $00      ; $1FA8 / dump $5FA8
        .byte   $FF, $FF, $00, $F0, $00, $FF, $00, $F0      ; $1FB0 / dump $5FB0
        .byte   $0F, $FF, $FF, $00, $FF, $FF, $FF, $FF      ; $1FB8 / dump $5FB8
        .byte   $FF, $FF, $99, $88, $88, $88, $99, $99      ; $1FC0 / dump $5FC0
start_overlay_row3:
        .assert * = $1FC8, lderror, "address drift: start_overlay_row3"
        .byte   $99, $99, $98, $98, $98, $99, $9F, $9F      ; $1FC8 / dump $5FC8
        .byte   $9F, $9F, $9F, $9F, $9F, $9F, $9F, $9F      ; $1FD0 / dump $5FD0
        .byte   $9F, $9F, $9F, $9F, $9F, $9F, $9F, $9F      ; $1FD8 / dump $5FD8
        .byte   $9F, $9F, $9F, $9F, $9F, $9F, $9F, $9F      ; $1FE0 / dump $5FE0
        .byte   $9F, $9F, $99, $98, $98, $98, $99, $99      ; $1FE8 / dump $5FE8
        .byte   $00, $00, $00, $00, $00, $00, $00, $00      ; $1FF0 / dump $5FF0
        .byte   $00, $00, $00, $00, $00, $00, $00, $00      ; $1FF8 / dump $5FF8
