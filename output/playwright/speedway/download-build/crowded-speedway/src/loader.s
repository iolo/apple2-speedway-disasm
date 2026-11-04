; The 44-byte relocation stub formerly stored in Applesoft line 190 DATA.
; Applesoft declares GR before CALL $0300. ROM MOVE copies the inclusive
; staging range $4400-$69FF to runtime $0400-$29FF. This destroys BASIC.
; The initial orchard page remains visible during the delay, then game_entry
; builds its tables and presents the title. There is no return to Applesoft.

        .setcpu "6502"
        .segment "LOADER"
        .export relocate_and_start

MOVE_SOURCE     = $3C             ; monitor A1L/A1H
MOVE_END        = $3E             ; monitor A2L/A2H (inclusive)
MOVE_DEST       = $42             ; monitor A4L/A4H
ROM_MOVE        = $FE2C
ROM_WAIT        = $FCA8
GAME_ENTRY      = $2970           ; asserted by src/speedway.s

relocate_and_start:
        lda     #<$4400
        sta     MOVE_SOURCE
        lda     #>$4400
        sta     MOVE_SOURCE+1
        lda     #<$69FF           ; corrected inclusive end, not $6A00
        sta     MOVE_END
        lda     #>$69FF
        sta     MOVE_END+1
        lda     #<$0400
        sta     MOVE_DEST
        lda     #>$0400
        sta     MOVE_DEST+1
        ldy     #$00
        jsr     ROM_MOVE
        ldy     #$0A
delay:
        lda     #$FF
        jsr     ROM_WAIT
        dey
        cpy     #$00              ; retain the original two-byte comparison
        bne     delay
        jmp     GAME_ENTRY
loader_end:
        .assert relocate_and_start = $0300, lderror, "loader origin changed"
        .assert loader_end-relocate_and_start = 44, error, "loader size changed"
