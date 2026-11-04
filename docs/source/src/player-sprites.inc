; Six player-car rows. Each contains three consecutive 10-column poses.
; Zero means transparent to draw_player_car. Tail bytes are preserved.
; Runtime $1AC0-$1B7F; dump $5AC0-$5B7F.

player_sprite_row0:
        .assert * = $1AC0, lderror, "address drift: player_sprite_row0"
        .byte   $99, $99, $99, $99, $99, $99, $99, $99      ; $1AC0 / dump $5AC0
        .byte   $99, $99, $00, $99, $99, $99, $99, $99      ; $1AC8 / dump $5AC8
        .byte   $99, $99, $00, $00, $00, $00, $99, $99      ; $1AD0 / dump $5AD0
        .byte   $99, $99, $99, $99, $99, $00                ; $1AD8 / dump $5AD8
player_sprite_row1:
        .assert * = $1ADE, lderror, "address drift: player_sprite_row1"
        .byte   $00, $00, $99, $00, $00, $00, $00, $99      ; $1ADE / dump $5ADE
        .byte   $00, $00, $00, $00, $99, $99, $00, $00      ; $1AE6 / dump $5AE6
        .byte   $99, $00, $00, $00, $00, $00, $00, $99      ; $1AEE / dump $5AEE
        .byte   $00, $00, $99, $99, $00, $00                ; $1AF6 / dump $5AF6
player_sprite_row2:
        .assert * = $1AFC, lderror, "address drift: player_sprite_row2"
        .byte   $AA, $AA, $AA, $99, $88, $88, $99, $AA      ; $1AFC / dump $5AFC
        .byte   $AA, $AA, $AA, $AA, $AA, $99, $88, $AA      ; $1B04 / dump $5B04
        .byte   $AA, $99, $00, $00, $00, $00, $99, $AA      ; $1B0C / dump $5B0C
        .byte   $AA, $88, $99, $AA, $AA, $AA                ; $1B14 / dump $5B14
player_sprite_row3:
        .assert * = $1B1A, lderror, "address drift: player_sprite_row3"
        .byte   $AA, $AA, $AA, $88, $66, $66, $88, $AA      ; $1B1A / dump $5B1A
        .byte   $AA, $AA, $AA, $AA, $88, $66, $66, $AA      ; $1B22 / dump $5B22
        .byte   $AA, $AA, $99, $00, $00, $99, $AA, $AA      ; $1B2A / dump $5B2A
        .byte   $AA, $66, $66, $88, $AA, $AA                ; $1B32 / dump $5B32
player_sprite_row4:
        .assert * = $1B38, lderror, "address drift: player_sprite_row4"
        .byte   $AA, $AA, $AA, $22, $88, $88, $22, $AA      ; $1B38 / dump $5B38
        .byte   $AA, $AA, $AA, $AA, $22, $88, $88, $AA      ; $1B40 / dump $5B40
        .byte   $AA, $AA, $99, $AA, $AA, $99, $AA, $AA      ; $1B48 / dump $5B48
        .byte   $AA, $88, $88, $22, $AA, $AA                ; $1B50 / dump $5B50
player_sprite_row5:
        .assert * = $1B56, lderror, "address drift: player_sprite_row5"
        .byte   $AA, $AA, $AA, $00, $00, $00, $00, $AA      ; $1B56 / dump $5B56
        .byte   $AA, $AA, $AA, $AA, $AA, $00, $00, $AA      ; $1B5E / dump $5B5E
        .byte   $AA, $AA, $99, $AA, $AA, $99, $AA, $AA      ; $1B66 / dump $5B66
        .byte   $AA, $00, $00, $AA, $AA, $AA, $00, $00      ; $1B6E / dump $5B6E
        .byte   $00, $00, $00, $00, $00, $00, $00, $00      ; $1B76 / dump $5B76
        .byte   $00, $00                                    ; $1B7E / dump $5B7E
