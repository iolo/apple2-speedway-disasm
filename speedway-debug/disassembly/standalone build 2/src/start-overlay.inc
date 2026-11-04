; Last three 40-byte rows of the start overlay. Eight trailing bytes retained.
; Runtime $2800-$287F; dump $6800-$687F.

start_overlay_row4:
        .assert * = $2800, lderror, "address drift: start_overlay_row4"
        .byte   $CC, $FC, $0C, $0F, $F0, $F0, $F0, $0F      ; $2800 / dump $6800
        .byte   $0F, $F0, $F0, $F0, $0F, $0F, $0F, $F0      ; $2808 / dump $6808
        .byte   $F0, $F0, $0F, $0F, $0F, $0F, $F0, $F0      ; $2810 / dump $6810
        .byte   $F0, $0F, $0F, $0F, $F0, $F0, $F0, $0F      ; $2818 / dump $6818
        .byte   $0F, $F0, $F0, $F0, $0F, $0C, $FC, $CC      ; $2820 / dump $6820
start_overlay_row5:
        .assert * = $2828, lderror, "address drift: start_overlay_row5"
        .byte   $F0, $F0, $0F, $0F, $00, $F0, $F0, $FF      ; $2828 / dump $6828
        .byte   $0F, $00, $00, $F0, $FF, $FF, $0F, $00      ; $2830 / dump $6830
        .byte   $00, $00, $FF, $FF, $FF, $FF, $00, $00      ; $2838 / dump $6838
        .byte   $00, $0F, $FF, $FF, $F0, $00, $00, $0F      ; $2840 / dump $6840
        .byte   $FF, $F0, $F0, $00, $0F, $0F, $F0, $F0      ; $2848 / dump $6848
start_overlay_row6:
        .assert * = $2850, lderror, "address drift: start_overlay_row6"
        .byte   $00, $F0, $FF, $FF, $0F, $00, $00, $F0      ; $2850 / dump $6850
        .byte   $FF, $FF, $0F, $00, $00, $00, $FF, $FF      ; $2858 / dump $6858
        .byte   $FF, $FF, $00, $00, $00, $00, $FF, $FF      ; $2860 / dump $6860
        .byte   $FF, $FF, $00, $00, $00, $0F, $FF, $FF      ; $2868 / dump $6868
        .byte   $F0, $00, $00, $0F, $FF, $FF, $F0, $00      ; $2870 / dump $6870
        .byte   $00, $00, $00, $00, $00, $00, $00, $00      ; $2878 / dump $6878
