from pathlib import Path
import re,json
ops={int(op,16):(name,int(n)) for name,op,n in re.findall(r'PCODE\("(\w+)", ADDR_MODE\.\w+, 0x([0-9A-Fa-f]+), (\d)\)',Path('/home/iolo/workspace/retro/apple2ts/src/common/opcodes.ts').read_text())}
b=Path('tmp/crowded speed way.bin').read_bytes();todo=[0x2970];seen={};errors=[];rom=set()
while todo:
 pc=todo.pop()
 if pc>=0xc000:rom.add(pc);continue
 if pc in seen:continue
 if not 0x800<=pc<0x2a00:errors.append((hex(pc),'outside code'));continue
 op=b[pc-0x400]; name,n=ops.get(op,('???',1));seen[pc]=(name,n)
 if name in ['BRK','???']:errors.append((hex(pc),name));continue
 if op in [0x60,0x40]:continue
 target=int.from_bytes(b[pc-0x400+1:pc-0x400+3],'little')
 if op in [0x20,0x4c]:
  todo.append(target)
  if op==0x4c:continue
 elif op==0x6c: errors.append((hex(pc),'indirect jump'));continue
 elif op in [0x10,0x30,0x50,0x70,0x90,0xb0,0xd0,0xf0]:
  rel=b[pc-0x400+1];todo.append(pc+2+(rel if rel<128 else rel-256))
 todo.append(pc+n)
print('reachable instructions',len(seen),'errors',errors,'ROM targets',[hex(x) for x in sorted(rom)])
Path('tmp/flow-check.json').write_text(json.dumps({'instructions':len(seen),'errors':errors,'ROM':[hex(x) for x in sorted(rom)]},indent=2)+'\n')
