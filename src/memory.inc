; Named Apple II hardware, ROM entries, and game zero-page variables.
; Addresses are runtime addresses after relocation; the payload is stored at +$4000.
; Zero page is owned by the game; it does not preserve Applesoft state.

curve_index                = $00       ; road curve/table index
view_offset                = $01       ; signed horizontal viewport/player offset
work_ptr_lo                = $02       ; shared pointer / byte scratch
work_ptr_hi                = $03       ; shared pointer high / row count
draw_ptr_lo                = $04       ; shared destination pointer low
draw_ptr_hi                = $05       ; shared destination pointer high / sign
random_ptr_lo              = $06       ; ROM stream pointer low
random_ptr_hi              = $07       ; ROM stream pointer high
random_index               = $08       ; ROM stream offset
scenery_offset             = $09       ; wrapping scenery-strip index
segment_steps              = $0A       ; remaining straight/curve updates
segment_turn               = $0B       ; zero=straight; sign chooses turn
straight_steps             = $0C       ; straight-section duration
curve_steps                = $0D       ; turn-section duration
brake_divider              = $0E       ; car-slowdown divider
brake_reserve              = $0F       ; remaining brake reserve, recovered when released
brake_failed               = $10       ; nonzero after reserve reaches zero
high_score                 = $11       ; eight high-bit decimal characters ($11-$18)
random_xor_lo              = $4E       ; evolving XOR seed low
random_xor_hi              = $4F       ; evolving XOR seed high
multiply_factor_lo         = $50       ; shift/add addend low
multiply_factor_hi         = $51       ; shift/add addend high
multiply_result_lo         = $52       ; shift/add result low
multiply_result_hi         = $53       ; shift/add result high
multiply_bits              = $54       ; shifted source bits
car_one_active             = $60       ; active flag
car_one_path_lo            = $61       ; lane-table pointer low
car_one_path_hi            = $62       ; lane-table pointer high
car_one_depth              = $63       ; distance/depth counter
car_one_speed              = $64       ; alternating update flag
car_one_draw_lo            = $65       ; row-buffer pointer low
car_one_draw_hi            = $66       ; row-buffer pointer high
car_one_lookup_lo          = $67       ; perspective lookup pointer low
car_one_lookup_hi          = $68       ; perspective lookup pointer high
left_sign_active           = $70       ; active flag
left_sign_depth            = $71       ; depth counter
left_sign_draw_lo          = $72       ; row-buffer pointer low
left_sign_draw_hi          = $73       ; row-buffer pointer high
left_sign_lookup_lo        = $74       ; perspective pointer low
left_sign_lookup_hi        = $75       ; perspective pointer high
right_sign_active          = $80       ; active flag
right_sign_depth           = $81       ; depth counter
right_sign_draw_lo         = $82       ; row-buffer pointer low
right_sign_draw_hi         = $83       ; row-buffer pointer high
right_sign_lookup_lo       = $84       ; perspective pointer low
right_sign_lookup_hi       = $85       ; perspective pointer high
car_two_active             = $90       ; active flag
car_two_path_lo            = $91       ; lane-table pointer low
car_two_path_hi            = $92       ; lane-table pointer high
car_two_depth              = $93       ; distance/depth counter
car_two_speed              = $94       ; alternating update flag
car_two_draw_lo            = $95       ; row-buffer pointer low
car_two_draw_hi            = $96       ; row-buffer pointer high
car_two_lookup_lo          = $97       ; perspective lookup pointer low
car_two_lookup_hi          = $98       ; perspective lookup pointer high
last_score                 = $A0       ; eight saved score characters ($A0-$A7)

; Display text fields, shared with the HUD templates.
SCORE_TEXT                 = $075D
CARS_LEFT_TEXT             = $076E
HIGH_SCORE_TEXT            = $07DD
KEYBOARD                   = $C000
SPEAKER                    = $C030
PADDLE_BUTTON0             = $C061
ROM_PREAD                  = $FB1E
ROM_WAIT                   = $FCA8

; ROM_PREAD: X=paddle number, returns timed paddle value in Y.
; ROM_WAIT: delay controlled by A (zero wraps for a long delay); A/flags clobbered.
; SPEAKER toggles on access; PADDLE_BUTTON0 is pressed when bit 7 is set.
