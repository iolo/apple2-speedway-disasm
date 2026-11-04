; Traffic sprite data: three four-row variants, then three six-row variants.
; Rows end in $FF. Variant offsets are selected by curvature thresholds.
; Preserve the unused tail and row terminators exactly.
; Runtime $0AD0-$0BFF; dump $4AD0-$4BFF.

traffic_medium_sprites:
        .assert * = $0AD0, lderror, "address drift: traffic_medium_sprites"
        .byte   $66, $66, $66, $66, $66, $66, $66, $FF      ; $0AD0 / dump $4AD0
        .byte   $00, $00, $66, $88, $66, $00, $00, $FF      ; $0AD8 / dump $4AD8
        .byte   $00, $00, $11, $EE, $11, $00, $00, $FF      ; $0AE0 / dump $4AE0
        .byte   $00, $00, $AA, $AA, $AA, $00, $00, $FF      ; $0AE8 / dump $4AE8
traffic_medium_variant1:
        .assert * = $0AF0, lderror, "address drift: traffic_medium_variant1"
        .byte   $66, $66, $66, $66, $66, $AA, $AA, $FF      ; $0AF0 / dump $4AF0
        .byte   $00, $00, $11, $00, $00, $66, $AA, $FF      ; $0AF8 / dump $4AF8
        .byte   $00, $00, $EE, $00, $00, $66, $00, $FF      ; $0B00 / dump $4B00
        .byte   $00, $00, $AA, $00, $00, $66, $00, $FF      ; $0B08 / dump $4B08
traffic_medium_variant2:
        .assert * = $0B10, lderror, "address drift: traffic_medium_variant2"
        .byte   $AA, $AA, $66, $66, $66, $66, $66, $FF      ; $0B10 / dump $4B10
        .byte   $AA, $66, $00, $00, $11, $00, $00, $FF      ; $0B18 / dump $4B18
        .byte   $00, $66, $00, $00, $EE, $00, $00, $FF      ; $0B20 / dump $4B20
        .byte   $00, $66, $00, $00, $AA, $00, $00, $FF      ; $0B28 / dump $4B28
traffic_large_sprites:
        .assert * = $0B30, lderror, "address drift: traffic_large_sprites"
        .byte   $66, $66, $66, $66, $66, $66, $66, $66      ; $0B30 / dump $4B30
        .byte   $66, $66, $FF, $AA, $AA, $66, $AA, $AA      ; $0B38 / dump $4B38
        .byte   $AA, $AA, $66, $AA, $AA, $FF, $00, $00      ; $0B40 / dump $4B40
        .byte   $00, $66, $88, $88, $66, $00, $00, $00      ; $0B48 / dump $4B48
        .byte   $FF, $00, $00, $00, $88, $EE, $EE, $88      ; $0B50 / dump $4B50
        .byte   $00, $00, $00, $FF, $00, $00, $00, $11      ; $0B58 / dump $4B58
        .byte   $88, $88, $11, $00, $00, $00, $FF, $00      ; $0B60 / dump $4B60
        .byte   $00, $00, $AA, $AA, $AA, $AA, $00, $00      ; $0B68 / dump $4B68
        .byte   $00, $FF                                    ; $0B70 / dump $4B70
traffic_large_variant1:
        .assert * = $0B72, lderror, "address drift: traffic_large_variant1"
        .byte   $AA, $66, $66, $66, $66, $66, $66, $66      ; $0B72 / dump $4B72
        .byte   $AA, $AA, $FF, $AA, $AA, $66, $66, $AA      ; $0B7A / dump $4B7A
        .byte   $AA, $66, $AA, $AA, $AA, $FF, $00, $00      ; $0B82 / dump $4B82
        .byte   $00, $66, $88, $00, $00, $66, $AA, $AA      ; $0B8A / dump $4B8A
        .byte   $FF, $00, $00, $88, $EE, $EE, $00, $00      ; $0B92 / dump $4B92
        .byte   $00, $66, $AA, $FF, $00, $00, $11, $88      ; $0B9A / dump $4B9A
        .byte   $88, $00, $00, $00, $66, $00, $FF, $00      ; $0BA2 / dump $4BA2
        .byte   $00, $00, $AA, $AA, $00, $00, $00, $66      ; $0BAA / dump $4BAA
        .byte   $00, $FF                                    ; $0BB2 / dump $4BB2
traffic_large_variant2:
        .assert * = $0BB4, lderror, "address drift: traffic_large_variant2"
        .byte   $AA, $AA, $66, $66, $66, $66, $66, $66      ; $0BB4 / dump $4BB4
        .byte   $66, $AA, $FF, $AA, $AA, $AA, $66, $AA      ; $0BBC / dump $4BBC
        .byte   $AA, $66, $66, $AA, $AA, $FF, $AA, $AA      ; $0BC4 / dump $4BC4
        .byte   $66, $00, $00, $88, $66, $00, $00, $00      ; $0BCC / dump $4BCC
        .byte   $FF, $AA, $66, $00, $00, $00, $EE, $EE      ; $0BD4 / dump $4BD4
        .byte   $88, $00, $00, $FF, $00, $66, $00, $00      ; $0BDC / dump $4BDC
        .byte   $00, $88, $88, $11, $00, $00, $FF, $00      ; $0BE4 / dump $4BE4
        .byte   $66, $00, $00, $00, $AA, $AA, $00, $00      ; $0BEC / dump $4BEC
        .byte   $00, $FF, $00, $00, $00, $00, $00, $00      ; $0BF4 / dump $4BF4
        .byte   $00, $00, $00, $00                          ; $0BFC / dump $4BFC
