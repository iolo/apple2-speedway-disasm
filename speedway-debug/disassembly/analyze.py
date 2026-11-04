from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
meta=json.loads(Path('/home/iolo/.codex/skills/a2skills/a2-cc65/references/6502-opcodes.json').read_text())
lengths={'Im':2,'Z':2,'Zx':2,'Zy':2,'Ab':3,'Ax':3,'Ay':3,'Ix':2,'Iy':2,'In':3,'Lb':2,'A':1,'Ip':1}
ops={int(h,16):(item['name'].lower(),mode,lengths[mode]) for item in meta['opcodes'] for mode,h in item['hex'].items()}
b=(ROOT/'crowded speed way.bin').read_bytes(); mem=lambda a:b[a-0x400]
todo=[0x2970];decoded={};refs={};calls=set(); external=set(); branches=set()
while todo:
 pc=todo.pop()
 if pc>=0xc000:external.add(pc);continue
 assert 0x800<=pc<0x2a00,hex(pc)
 if pc in decoded:continue
 op=mem(pc);name,mode,n=ops[op];assert name!='brk',hex(pc)
 raw=b[pc-0x400:pc-0x400+n]; val=int.from_bytes(raw[1:],'little')
 decoded[pc]={'name':name,'mode':mode,'raw':list(raw),'value':val}
 if name in ['jsr','jmp']:
  assert mode!='In';refs.setdefault(val,[]).append(pc);todo.append(val)
  if name=='jsr':calls.add(val)
  if name=='jmp':continue
 if mode=='Lb':
  val=pc+2+(val if val<128 else val-256);decoded[pc]['target']=val;branches.add(val);refs.setdefault(val,[]).append(pc);todo.append(val)
 if name not in ['rts','rti']:todo.append(pc+n)
owned={}
for pc,d in decoded.items():
 for a in range(pc,pc+len(d['raw'])):assert a not in owned,(hex(pc),hex(a));owned[a]=pc
out=[]
for pc in sorted(decoded):
 d=decoded[pc];name=d['name'];mode=d['mode'];v=d['value']; raw=d['raw'];fmt={'Im':'#${:02X}','Z':'${:02X}','Zx':'${:02X},x','Zy':'${:02X},y','Ab':'${:04X}','Ax':'${:04X},x','Ay':'${:04X},y','Ix':'(${:02X},x)','Iy':'(${:02X}),y','In':'(${:04X})','Lb':'${:04X}','A':'a','Ip':''}[mode]
 if pc in calls or pc in [0x2970] or pc-1 not in owned:out.append('\n; ----- '+hex(pc)+' -----')
 operand=fmt.format(d.get('target',v))
 out.append(f'{pc:04X}  {bytes(raw).hex(" ").upper():8}  {name:3} {operand}')
(ROOT/'speedway-debug/disassembly/code.txt').write_text('\n'.join(out)+'\n')
(ROOT/'speedway-debug/disassembly/flow.json').write_text(json.dumps({'decoded':decoded,'calls':sorted(calls),'external':sorted(external),'refs':refs},indent=2)+'\n')
print('instructions',len(decoded),'code bytes',len(owned),'retained bytes',len(b)-len(owned))
print('call targets:',', '.join(f'{a:04X}' for a in sorted(calls)))
