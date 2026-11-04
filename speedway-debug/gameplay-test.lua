local m=manager.machine
local s=m.devices[':maincpu'].spaces.program
local x=m.ioport.ports[':gameio:joy:joystick_1_x'].fields['P1 Joystick X']
local button=m.ioport.ports[':gameio:joy:joystick_buttons'].fields['P1 Button 1']
local frames,crashes=0,0
local samples={}
local function sample(event)
 local score=''
 for i=0,7 do score=score..string.char(s:read_u8(0x75d+i)&0x7f) end
 samples[#samples+1]={event=event,frame=frames,curve=s:read_u8(0),window=s:read_u8(1),brake=s:read_u8(0xe),brakeNG=s:read_u8(0x10),lives=s:read_u8(0x76e)&0x7f,score=score}
end
player=a2_automation.new{result_path=os.getenv('A2_MAME_SESSION')..'/gameplay-result.json',progress_timeout=60}
player:phase('joystick gameplay',{
 [0x1dd4]=function(self)
  frames=frames+1
  if frames==1 then sample('initial'); x:set_value(0) end
  if frames==12 then sample('left');x:set_value(255) end
  if frames==24 then sample('right');x:set_value(128);button:set_value(1);sample('brake start') end
  if frames==45 then sample('braking');button:clear_value() end
  if frames%100==0 then sample('driving') end
  if frames==500 then x:clear_value();button:clear_value();self:finish(true,'500 gameplay loops',{samples=samples,crashes=crashes}) end
 end,
 [0x1d70]=function(self)crashes=crashes+1 end,
 [0x1e10]=function(self) sample('game over');x:clear_value();button:clear_value();self:finish(true,'native game over',{samples=samples,crashes=crashes}) end,
 [0xff59]=function(self) sample('unexpected monitor');x:clear_value();button:clear_value();self:finish(false,'entered monitor',{samples=samples,crashes=crashes}) end,
},function()return s:read_u8(0x1dd4)==0x20 and s:read_u8(0x1dd5)==0x20 and s:read_u8(0x993)==0xa4 end)
return {installed=true}
