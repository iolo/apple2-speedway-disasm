"""One-time source recovery. Normal builds use only src/, tools/, and Makefile."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
b=(R/'crowded speed way.bin').read_bytes()
flow=json.loads((R/'speedway-debug/disassembly/flow.json').read_text())
dec={int(a):d for a,d in flow['decoded'].items()}
# Candidate retained instructions: no caller from the game's entry was found.
dec.update({0x9ab:dict(name='lda',mode='Ab',raw=[0xad,0,0xc0],value=0xc000),0x9ae:dict(name='cmp',mode='Im',raw=[0xc9,0xa0],value=0xa0),0x9b0:dict(name='bne',mode='Lb',raw=[0xd0,0xee],value=0xee,target=0x9a0),0x9b2:dict(name='rts',mode='Ip',raw=[0x60],value=0),0x295f:dict(name='jmp',mode='Ab',raw=[0x4c,0xa8,0xfc],value=0xfca8)})
routines={
0x0800:('multiply_shift_add','Shift/add helper. $50/$51 is the 16-bit addend; $54 supplies bits.\nX+1 iterations build $52/$53. Clobbers A, X, flags and $52-$54; preserves Y.'),
0x0820:('build_road_positions','Build perspective/curve lookup pages $4000-$53FF for curve indices 1..63.\nEach page represents one of 20 depth rows. Uses the multiply helper and $02-$05.'),
0x0880:('build_road_widths','Write depth-dependent road widths at offset zero of pages $4000-$5300.\nWidths are 4*depth+2; the renderer uses this table to fill the road.'),
0x08a0:('build_traffic_paths','Build seven 15-entry lane/displacement tables at $4050, $4150, ... $4650.\nThe traffic update routines select one table through their path pointer.'),
0x08f0:('random_byte','Read ROM through ($06),Y and XOR with the evolving $4E/$4F pair.\nReturns A; advances $08 and the ROM page on wrap. Not a uniform-RNG claim.'),
0x0906:('reset_random_cursor','Set the ROM stream cursor to $E000 and index zero; preserves A with PHA/PLA.\nThe XOR seed bytes $4E/$4F are deliberately not initialized here.'),
0x0920:('clear_road_buffer','Fill twenty 256-byte row buffers at $6000-$73FF with $CC.\nEach byte initially holds background color 12 in both lores nibbles.'),
0x0970:('frame_click','Two short speaker toggles separated by ROM WAIT calls.\nUsed for frame pacing and in the crash animation; clobbers A, Y.'),
0x0980:('draw_road','For each depth: read width at table offset 0, position at curve_index,\nthen fill that span in the corresponding $60xx-$73xx buffer with $AA.'),
0x09ab:('retained_keyboard_fragment','UNREFERENCED instruction fragment. Reads the keyboard and compares SPACE.\nIts literal BNE targets $09A0 inside draw_road, not this polling instruction.\nNo caller was found. Preserve these bytes and the unusual branch unchanged.'),
0x09c0:('random_lane','Return random_byte AND 7, mapping the result 7 to 3.\nThe result chooses one of seven lane tables; no statistical guarantee.'),
0x09d0:('random_two_bits','Return random_byte AND 3; zero permits traffic/sign spawning.'),
0x09e0:('update_car_one','Spawn/update/draw traffic car 1 using state $60-$68.\nDepth chooses small solid marks or four-/six-row perspective sprites.\n$FF terminates each medium/large sprite row; it is not drawn.'),
0x0c00:('update_left_sign','Spawn/update a left-side white sign in the row buffers using $70-$75.\nThe sign grows from a point to a 4/6/8-row block as depth increases.'),
0x0c90:('update_right_sign','Right-side counterpart of update_left_sign; state lives at $80-$85.'),
0x0d20:('update_car_two','Spawn/update/draw traffic car 2 using state $90-$98.\nShares the medium/large traffic sprite tables with update_car_one.'),
0x0e10:('draw_traffic_in_depth_order','Compare the two depth bytes, then update/draw the farther car first.\nTail JMP lets the second update return directly to the caller.'),
0x0e30:('blit_road_window','Copy a 40-byte viewport from twenty row buffers to lores page 1.\nPair the low nibble from one row with the high nibble from the next.\nY starts at view_offset+$94; screen rows use Apple II interleaved addresses.'),
0x0ef0:('blit_scenery','Copy 40 columns from ten 256-byte scenery strips at $1000-$19FF.\nscenery_offset is the wrapping source index; destination is lores page 1.'),
0x0f40:('advance_road_segment','Count down segment_steps. Alternate a straight section and a nonzero\nsigned turn from random_byte. Durations come from $0C/$0D.'),
0x0f60:('steer_on_straight','Read paddle 0 with ROM PREAD. After four right shifts, values 3 or 4\nare neutral (raw paddle 48..79). Other values move curve_index within bounds.'),
0x0f90:('steer_on_curve','Read paddle 0 and alter the signed view_offset during a turn.\nExtreme readings can move it twice. This uses signed-byte tests, not a clamp.'),
0x0fd0:('increment_score','Increment eight high-bit Apple II decimal characters at SCORE_TEXT.\nCarry from the least-significant character toward the left; no BCD mode.'),
0x1a00:('advance_curve_and_steer','Apply the current segment turn to road curvature, scenery, and viewport.\nThen tail-call the appropriate paddle steering routine.'),
0x1a60:('draw_player_car','Select one of three 10-column poses from the sign of view_offset.\nDraw six rows into $6E00-$7300 at $7C+view_offset; zero pixels are transparent.'),
0x1b80:('draw_cockpit_details','Update small screen details at $055F-$0568 / $05DF-$05E8 according\nto the sign of view_offset. Exact visual meaning is not fully identified.'),
0x1c00:('decrement_score','Subtract one from the same high-bit decimal score text.\nCalled while braking so the later increment_score does not increase score.'),
0x1c20:('update_brake','Read PB0 bit 7. Released brake recovers reserve up to a signed-byte limit.\nHeld brake slows active cars once per divider, spends reserve, and sounds.\nWhen reserve reaches zero, brake_failed stays set until a new game.'),
0x1c70:('check_player_collision','Inspect the player footprint in rows $7200/$7300 before drawing the car.\nOnly $AA road and $CC background are allowed. On contact JMP handle_crash;\nthat handler discards this routine\'s JSR return address.'),
0x1d30:('draw_crash_frame_a','Copy a 16-column, four-byte-row crash picture directly to lores page 1.'),
0x1d50:('draw_crash_frame_b','Second crash picture, using the adjacent 64-byte sprite block.'),
0x1d70:('handle_crash','NONLOCAL entry reached by JMP from check_player_collision.\nPLA/PLA discard that routine\'s return address, then flash two crash frames.\nAfter a delay, continue at lose_car_and_restart; this handler does not RTS.'),
0x1dc0:('lose_car_and_restart','Decrement the high-bit text character at CARS_LEFT_TEXT.\nStart-up template contains a colon ($BA), so the first decrement displays 9.\nAfter 0, $AF compares below $B0 and reaches game_over (ten cars in total).'),
0x1dd4:('game_loop','One gameplay update: clear buffers, advance road/steering, draw road,\napply brake, update traffic/signs, test collision, draw car, blit scenery/road,\nupdate cockpit, pace/sound, increment score, repeat.'),
0x1e10:('game_over','Compare the eight score digits with the displayed high score, propagating\nborrow from right to left. Save the score in $A0-$A7; update $11-$18 if larger.\nCopy the page at $2000 to the display, then jump to the result presentation.'),
0x1e50:('show_title_and_wait','Copy the 1 KB title page at $2400 to screen $0400-$07FF.\nBusy-wait for paddle button 0, then return to the game initializer.'),
0x1e80:('initialize_hud','Copy four 40-character HUD rows and the eight-digit high score to page 1.\nThis resets the score and the cars-left colon sentinel from the templates.'),
0x2880:('draw_start_overlay','Copy seven 40-byte lores rows from split overlay data to the start view.\nThe source is split across $1F50-$1FEF and $2800-$2877.'),
0x28b0:('prepare_start_view','Render the road, player, scenery, cockpit, overlay, then initialize HUD.\nThe final JMP to initialize_hud returns to the original caller.'),
0x28d0:('animate_start_lights','Draw a small signal on lores page 1, change its lamps in sequence,\nand play countdown/start tones using the speaker and ROM WAIT.'),
0x2930:('countdown_tone','Toggle speaker 96 times with a fixed ROM WAIT argument, then pause.'),
0x2950:('start_tone','Toggle speaker 256 times (Y wraps from zero) with a shorter delay.'),
0x295f:('retained_wait_jump','UNREFERENCED JMP WAIT fragment following start_tone; preserve literally.'),
0x2970:('game_entry','Entry after BASIC declares GR and the $0300 loader relocates the payload.\nBuild perspective/path tables, reset the ROM cursor, initialize high score.\nThere is no return to BASIC: its source has already been overwritten.'),
0x2985:('new_game','Show title and wait for PB0. Reset game state, prepare the start view,\nrun the signal sequence, then enter lose_car_and_restart.'),
0x29b0:('game_over_sound','Seven groups of delayed speaker toggles. Clobbers A, X, Y.'),
0x29d0:('present_game_over','Initialize HUD, restore the just-finished score from $A0-$A7, play sound,\npause, and jump to new_game without clearing the saved high score.'),
}
zp={0x00:('curve_index','road curve/table index'),0x01:('view_offset','signed horizontal viewport/player offset'),0x02:('work_ptr_lo','shared pointer / byte scratch'),0x03:('work_ptr_hi','shared pointer high / row count'),0x04:('draw_ptr_lo','shared destination pointer low'),0x05:('draw_ptr_hi','shared destination pointer high / sign'),0x06:('random_ptr_lo','ROM stream pointer low'),0x07:('random_ptr_hi','ROM stream pointer high'),0x08:('random_index','ROM stream offset'),0x09:('scenery_offset','wrapping scenery-strip index'),0x0a:('segment_steps','remaining straight/curve updates'),0x0b:('segment_turn','zero=straight; sign chooses turn'),0x0c:('straight_steps','straight-section duration'),0x0d:('curve_steps','turn-section duration'),0x0e:('brake_divider','car-slowdown divider'),0x0f:('brake_reserve','remaining brake reserve, recovered when released'),0x10:('brake_failed','nonzero after reserve reaches zero'),0x11:('high_score','eight high-bit decimal characters ($11-$18)'),0x4e:('random_xor_lo','evolving XOR seed low'),0x4f:('random_xor_hi','evolving XOR seed high'),0x50:('multiply_factor_lo','shift/add addend low'),0x51:('multiply_factor_hi','shift/add addend high'),0x52:('multiply_result_lo','shift/add result low'),0x53:('multiply_result_hi','shift/add result high'),0x54:('multiply_bits','shifted source bits')}
for base,prefix in [(0x60,'car_one'),(0x90,'car_two')]:
 for ofs,suffix,note in [(0,'active','active flag'),(1,'path_lo','lane-table pointer low'),(2,'path_hi','lane-table pointer high'),(3,'depth','distance/depth counter'),(4,'speed','alternating update flag'),(5,'draw_lo','row-buffer pointer low'),(6,'draw_hi','row-buffer pointer high'),(7,'lookup_lo','perspective lookup pointer low'),(8,'lookup_hi','perspective lookup pointer high')]:zp[base+ofs]=(prefix+'_'+suffix,note)
for base,prefix in [(0x70,'left_sign'),(0x80,'right_sign')]:
 for ofs,suffix,note in [(0,'active','active flag'),(1,'depth','depth counter'),(2,'draw_lo','row-buffer pointer low'),(3,'draw_hi','row-buffer pointer high'),(4,'lookup_lo','perspective pointer low'),(5,'lookup_hi','perspective pointer high')]:zp[base+ofs]=(prefix+'_'+suffix,note)
zp[0xa0]=('last_score','eight saved score characters ($A0-$A7)')
hw={0xc000:'KEYBOARD',0xc030:'SPEAKER',0xc061:'PADDLE_BUTTON0',0xfb1e:'ROM_PREAD',0xfca8:'ROM_WAIT',0x75d:'SCORE_TEXT',0x76e:'CARS_LEFT_TEXT',0x7dd:'HIGH_SCORE_TEXT'}
anchors={0x0400:'initial_orchard_page',0x0ad0:'traffic_medium_sprites',0x0af0:'traffic_medium_variant1',0x0b10:'traffic_medium_variant2',0x0b30:'traffic_large_sprites',0x0b72:'traffic_large_variant1',0x0bb4:'traffic_large_variant2',0x1ac0:'player_sprite_row0',0x1ade:'player_sprite_row1',0x1afc:'player_sprite_row2',0x1b1a:'player_sprite_row3',0x1b38:'player_sprite_row4',0x1b56:'player_sprite_row5',0x1cb0:'crash_a_row0',0x1cc0:'crash_a_row1',0x1cd0:'crash_a_row2',0x1ce0:'crash_a_row3',0x1cf0:'crash_b_row0',0x1d00:'crash_b_row1',0x1d10:'crash_b_row2',0x1d20:'crash_b_row3',0x1eb0:'hud_blank_row0',0x1ed8:'hud_blank_row1',0x1f00:'hud_score_row',0x1f28:'hud_high_row',0x2000:'game_over_page',0x2400:'title_page'}
for i in range(10):anchors[0x1000+i*256]=f'scenery_strip_{i}'
for i,a in enumerate([0x1f50,0x1f78,0x1fa0,0x1fc8,0x2800,0x2828,0x2850]):anchors[a]=f'start_overlay_row{i}'
labels={a:name for a,(name,comment) in routines.items()};labels.update(anchors)
for d in dec.values():
 if d['mode']=='Lb':labels.setdefault(d['target'],f'L{d["target"]:04X}')
 elif d['name'] in ['jsr','jmp'] and d['value']<0xc000:labels.setdefault(d['value'],f'L{d["value"]:04X}')
# Every run starts with an explicit boundary, even where control simply falls through.
owned=set()
for a,d in dec.items():owned.update(range(a,a+len(d['raw'])))
for a in dec:
 if a-1 not in owned:labels.setdefault(a,f'L{a:04X}')
sections=[(0x0400,0x0800,'initial-screen.inc','Initial 1 KB lores orchard page. The loader copies this straight to page 1.\nIt is visible during the loader delay, then overwritten by the game.'),(0x0ad0,0x0c00,'traffic-sprites.inc','Traffic sprite data: three four-row variants, then three six-row variants.\nRows end in $FF. Variant offsets are selected by curvature thresholds.\nPreserve the unused tail and row terminators exactly.'),(0x1000,0x1a00,'scenery.inc','Ten 256-byte scenery strips, consumed by blit_scenery with a wrapping Y index.\nThese are horizontal raster strips, not an Apple II screen-memory page.'),(0x1ac0,0x1b80,'player-sprites.inc','Six player-car rows. Each contains three consecutive 10-column poses.\nZero means transparent to draw_player_car. Tail bytes are preserved.'),(0x1cb0,0x1d30,'crash-sprites.inc','Two crash pictures: four rows of 16 lores bytes per picture.'),(0x1eb0,0x2000,'hud-and-overlay.inc','Four 40-byte high-bit text HUD rows followed by the first four start-overlay rows.\nThe cars-left field starts as $BA (colon); its initial decrement produces 9.\nUnconsumed tail bytes are retained, including screen-hole-like padding.'),(0x2000,0x2800,'screen-pages.inc','Two 1 KB Apple II page-layout images, including all screen holes.\n$2000 is copied on game over; $2400 is copied by show_title_and_wait.'),(0x2800,0x2880,'start-overlay.inc','Last three 40-byte rows of the start overlay. Eight trailing bytes retained.')]
inline={0x0993:'Repair: A4 (LDY curve_index), replacing the literal dump\'s 44.',0x0a0a:'Historical CMP, unlike car 2\'s ORA #$40: leaves A unchanged.',0x0a0c:'Thus this high pointer byte receives depth itself. Preserved literally.',0x0a0c:'Stores depth as lookup high byte; suspicious but preserved literally.',0x0f54:'Repair: JSR $08F0, replacing the literal dump\'s JSR $0BF0.',0x0f66:'Four shifts quantize raw paddle input into 16-value bands.',0x0fd0:'The main loop always increments; braking first subtracts one.',0x1c63:'Cancel the main loop\'s later increment while braking.',0x1c66:'Latch brake failure for the rest of this game.',0x1d70:'Discard the low return-address byte from the collision check\'s JSR.',0x1d71:'Discard the high return-address byte; continue without returning.',0x1dc6:'High-bit digit zero is $B0; $AF means the final car was used.',0x1e34:'Pointer high: source game_over_page ($2000).',0x1e50:'Pointer high: source title_page ($2400).',0x297e:'Initialize all eight high-score characters to high-bit ASCII zero.',0x2992:'Start with centered curvature index $20.',0x29ea:'Restart without reinitializing high_score.'}

def data_lines(start,end):
 out=[];a=start
 while a<end:
  if a in labels:out += [f'{labels[a]}:',f'        .assert * = ${a:04X}, lderror, "address drift: {labels[a]}"']
  n=min(8,end-a)
  for z in range(a+1,a+n):
   if z in labels:n=z-a;break
  vals=b[a-0x400:a-0x400+n]
  line='        .byte   '+', '.join(f'${v:02X}' for v in vals)
  note=f'${a:04X} / dump ${a+0x4000:04X}'
  if start>=0x1eb0 and end<=0x2000 and a<0x1f50:
   note+='  '+''.join(chr(v&127) if 32<=v&127<127 else '.' for v in vals)
  out.append(line.ljust(60)+'; '+note);a+=n
 return out

mem=['; Named Apple II hardware, ROM entries, and game zero-page variables.', '; Addresses are runtime addresses after relocation; the payload is stored at +$4000.', '; Zero page is owned by the game; it does not preserve Applesoft state.', '']
for a,(name,comment) in sorted(zp.items()):mem.append(f'{name:26} = ${a:02X}       ; {comment}')
mem+=['','; Display text fields, shared with the HUD templates.']
for a,name in sorted(hw.items()):mem.append(f'{name:26} = ${a:04X}')
mem+=['','; ROM_PREAD: X=paddle number, returns timed paddle value in Y.', '; ROM_WAIT: delay controlled by A (zero wraps for a long delay); A/flags clobbered.', '; SPEAKER toggles on access; PADDLE_BUTTON0 is pressed when bit 7 is set.', '']
(R/'src/memory.inc').write_text('\n'.join(mem))
for start,end,file,comment in sections:
 lines=['; '+s for s in comment.splitlines()]+[f'; Runtime ${start:04X}-${end-1:04X}; dump ${start+0x4000:04X}-${end-1+0x4000:04X}.','']+data_lines(start,end)
 (R/'src'/file).write_text('\n'.join(lines)+'\n')
sectionmap={a:(z,f,c) for a,z,f,c in sections}
lines=['; Crowded Speedway, Dec. 1984: ca65 reconstruction of the REPAIRED dump.', '; Source dump addresses $4400-$69FF become runtime $0400-$29FF.', '; All instruction/address annotations below use runtime addresses.', '; Default source must reproduce the working 9728-byte payload exactly.', '; Live code was traced recursively from game_entry ($2970). Two unreferenced', '; instruction fragments are identified explicitly. All other bytes are retained', '; as data, graphics, or padding; opaque pixels are not treated as opcodes.', '; No INCBIN or reference binary is required to assemble this source.', '', '        .setcpu "6502"', '        .include "memory.inc"', '        .segment "PAYLOAD"', '        .export game_entry, game_loop, handle_crash, game_over, new_game', 'payload_start:', '']
a=0x400
while a<0x2a00:
 if a in sectionmap:
  end,file,_=sectionmap[a];lines+=['',f'        .include "{file}"',''];a=end;continue
 if a in dec:
  d=dec[a];name=d['name'];mode=d['mode'];v=d['value']
  if a in routines:
   label,comment=routines[a];lines+=['','; '+'-'*76]+['; '+s for s in comment.splitlines()]
  if a in labels:lines += [labels[a]+':',f'        .assert * = ${a:04X}, lderror, "address drift: {labels[a]}"']
  def symbol(v):return hw.get(v) or (zp.get(v) or (None,))[0] or labels.get(v) or f'${v:04X}'
  if mode=='Im':operand=f'#${v:02X}'
  elif mode=='A':operand='a'
  elif mode=='Ip':operand=''
  elif mode=='Lb':operand=labels[d['target']]
  elif mode in ['Z','Zx','Zy','Ix','Iy']:
   operand=zp.get(v,(f'${v:02X}',))[0]
   operand={'Z':operand,'Zx':operand+',x','Zy':operand+',y','Ix':'('+operand+',x)','Iy':'('+operand+'),y'}[mode]
  else:
   operand=symbol(v)
   if v<256:operand='a:'+operand
   if mode in ['Ax','Ay']:operand+=','+mode[-1].lower()
   if mode=='In':operand='('+operand+')'
  text=f'        {name:7} {operand}'.rstrip()
  note=f'${a:04X}  '+bytes(d['raw']).hex(' ').upper()
  if a in inline:note+='  '+inline[a]
  lines.append(text.ljust(53)+'; '+note)
  a+=len(d['raw'])
 else:
  end=a+1
  while end<0x2a00 and end not in dec and end not in sectionmap:end+=1
  lines+=['',f'; Retained bytes ${a:04X}-${end-1:04X}: alignment/padding; no reachable instructions.']+data_lines(a,end)
  a=end
lines+=['','payload_end:', '        .assert payload_start = $0400, lderror, "payload origin changed"','        .assert payload_end = $2A00, lderror, "payload extent changed"','        .assert payload_end-payload_start = $2600, error, "payload size changed"','']
(R/'src/speedway.s').write_text('\n'.join(lines))
summary={'origin':1024,'end_exclusive':10752,'staging_origin':17408,'entry':10608,'reachable_instructions':1281,'reachable_instruction_bytes':2673,'retained_instruction_fragments':{'$09AB-$09B2':8,'$295F-$2961':3},'data_and_padding_bytes':len(b)-2673-11,'routines':[{'address':f'${a:04X}','name':n,'comment':c}for a,(n,c)in routines.items()]}
(R/'src/coverage.json').write_text(json.dumps(summary,indent=2)+'\n')
print('wrote source and',len(sections),'data includes')
