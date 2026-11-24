import json
def S(t,k,n,opt=False):
    d={"time":t,"k":k,"note":n}
    if opt: d['opt']=True
    return d
P=json.load(open('paris.json')); ks=[p['k'] for p in P]
add=[
{"k":"p-daw","n":"디즈니 어드벤처 월드","en":"Disney Adventure World","c":"sight","a":"발 데 유럽","lat":48.8677,"lng":2.7797,"t":"두 번째 파크 · 라따뚜이 어드벤처 · 월드 오브 프로즌","tip":"2026년 월트 디즈니 스튜디오에서 이름이 바뀐 파크. 라따뚜이(파리 원조)와 2026 신규 월드 오브 프로즌. 타워 오브 테러·코스터류는 이번 일정에서 패스"},
{"k":"p-remy","n":"비스트로 셰 레미","en":"Bistrot Chez Remy Disneyland Paris","c":"food","m":"점심","a":"발 데 유럽","lat":48.8669,"lng":2.7808,"t":"라따뚜이 테마 레스토랑 · 12/6 점심","tip":"쥐 크기로 작아진 듯한 거대한 소품 사이에서 식사. 테이블 서비스라 공식 앱·사이트에서 사전 예약 추천"},
{"k":"p-dvillage","n":"디즈니 빌리지","en":"Disney Village","c":"food","m":"저녁","a":"발 데 유럽","lat":48.8703,"lng":2.7861,"t":"파크 입구 앞 식당·상점 거리 · 12/6 저녁","tip":"버거·스테이크·테마 레스토랑이 모여 있음. 일요일 저녁은 붐비니 예약 또는 이른 방문"}]
for x in add:
    if x['k'] not in ks: P.append(x)
for p in P:
    if p['k']=='p-disney':
        p['n']='디즈니랜드 파리 (디즈니랜드 파크)'
        p['tip']='12/6 상세 일정은 카드의 "디즈니 상세 일정" 버튼에서. 1일 2파크(결제 완료). 성 지하 용의 동굴·앨리스의 미로·노틸러스호 등 파리 전용 어트랙션 위주, 낙하·무서운 기구는 패스'
json.dump(P,open('paris.json','w'),ensure_ascii=False,indent=0)
M=json.load(open('sources/menus-paris.json'))
M['p-remy']=["라따뚜이 (프로방스식 채소 요리)","스테이크·감자 메인 코스","디저트 코스"]
M['p-dvillage']=["버거","스테이크","테마 레스토랑 세트"]
json.dump(M,open('sources/menus-paris.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('paris-itinerary.json'))
for D in it:
    if D['d']=='12/6':
        D['title']='디즈니랜드 파리 · 라발레 빌리지'
        D['stops']=[
         S('08:30','p-moxy','RER A 한 정거장(마른라발레-셰시) 또는 도보 20분'),
         S('09:00','p-disney','오픈런: 피터팬 → 성·용의 동굴 → 앨리스의 미로 → 보트·스몰 월드 → 노틸러스호 (상세 일정 버튼 참고)'),
         S('13:00','p-remy','점심 · 라따뚜이 테마 레스토랑 (사전 예약)'),
         S('14:15','p-daw','라따뚜이 어드벤처 → 월드 오브 프로즌 아렌델 마을'),
         S('16:45','p-disney','메인 스트리트 크리스마스 조명·퍼레이드 (시간은 앱 확인)'),
         S('17:45','p-vallee','라발레 빌리지 아울렛 (시트 일정) · 숙소 바로 옆'),
         S('19:45','p-dvillage','저녁 · 디즈니 빌리지 식당가'),
         S('21:00','p-disney','성 야간 쇼 (폐장 시간 맞춰, 앱 확인)',True),
         S('22:00','p-moxy','숙소 복귀')]
json.dump(it,open('paris-itinerary.json','w'),ensure_ascii=False,indent=1)
R=json.load(open('reservations.json'))
if not any(r['k']=='p-remy' for r in R):
    i=[j for j,r in enumerate(R) if r['k']=='p-disney'][0]
    R.insert(i+1,{"city":"paris","d":"12/6","time":"13:00","k":"p-remy","what":"비스트로 셰 레미 점심","st":"rec","note":"디즈니 공식 앱·사이트에서 테이블 예약"})
json.dump(R,open('reservations.json','w'),ensure_ascii=False,indent=0)

# ---- UI: modal ----
t=open('template.html',encoding='utf-8').read()
if 'id="modal"' not in t:
    t=t.replace('<div class="app">','<div class="modal" id="modal" hidden role="dialog" aria-modal="true" aria-labelledby="mTitle"><div class="mbox" id="mbox"></div></div>\n<div class="app">',1)
    t=t.replace('.ob{','''.modal{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:100;display:flex;align-items:center;justify-content:center;padding:max(12px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) max(12px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px))}
.mbox{background:var(--surface);color:var(--fg);border-radius:14px;max-width:760px;width:100%;max-height:100%;overflow-y:auto;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.mhead{position:sticky;top:0;background:var(--surface);padding:16px 18px 10px;border-bottom:1px solid var(--line);display:grid;gap:4px;z-index:2}
.mhead h2{margin:0;font-family:var(--font-display);font-size:20px;padding-right:40px}
.mhead p{margin:0;color:var(--muted);font-size:12.5px}
.mclose{position:absolute;top:10px;right:10px;width:40px;height:40px;border:0;border-radius:8px;background:var(--bg);color:var(--fg);font-size:22px;cursor:pointer}
.mtabs{display:flex;gap:6px;overflow-x:auto;padding-top:6px}
.mtabs button{flex:none;border:1px solid var(--line);background:transparent;color:var(--fg);border-radius:999px;padding:7px 12px;font:inherit;font-size:12.5px;cursor:pointer;min-height:36px}
.mtabs button[aria-selected="true"]{background:var(--fg);color:var(--surface)}
.msec{padding:12px 18px 18px;display:grid;gap:8px}
.mfacts{margin:0;padding-left:18px;display:grid;gap:4px;font-size:13px;line-height:1.55;color:var(--muted)}
.tl{display:grid;grid-template-columns:48px 1fr;gap:2px 12px;padding:9px 0;border-bottom:1px solid var(--line)}
.tl .t{font-weight:700;font-variant-numeric:tabular-nums}
.tl .w{font-weight:700}.tl .pk{font-size:11px;color:var(--muted);font-weight:600;margin-left:6px}
.tl .n{grid-column:2;color:var(--muted);font-size:12.5px;line-height:1.5}
.tl .w.opt{opacity:.75}
.rd{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;padding:8px 0;border-bottom:1px solid var(--line);align-items:start}
.rd .v{font-size:11px;font-weight:700;border-radius:4px;padding:2px 7px;color:#fff;margin-top:2px}
.rd .v.추천{background:var(--xmas)}.rd .v.선택{background:var(--sight)}.rd .v.패스{background:var(--muted)}
.rd .nm2{font-weight:700}.rd .pr{font-size:10.5px;font-weight:700;color:var(--food);border:1px solid currentColor;border-radius:4px;padding:0 4px;margin-left:6px}
.rd .why{grid-column:2;color:var(--muted);font-size:12.5px}
.rd .pkn{font-size:11px;color:var(--muted);margin-left:6px}
.mgrp{font-weight:700;font-size:12.5px;color:var(--muted);padding-top:8px}
.fd{border:1px solid var(--line);border-radius:8px;padding:10px 12px;display:grid;gap:3px;font-size:13px}
.fd b{font-size:14px}.fd span{color:var(--muted);font-size:12px}
.dbtn{border:0;border-radius:8px;background:var(--fg);color:var(--surface);font:inherit;font-weight:700;font-size:13px;padding:9px 12px;cursor:pointer;justify-self:start}
@media (max-width:760px){.modal{padding:0;align-items:stretch}.mbox{border-radius:0;max-height:100dvh}}
.ob{''',1)
open('template.html','w',encoding='utf-8').write(t)

s=open('script.js',encoding='utf-8').read()
if 'openDisney' not in s:
    s=s.replace("// controls\nconst RES = __RES__;","""// controls
const RES = __RES__;
const DISNEY = __DISNEY__;
const modal=document.getElementById('modal'), mbox=document.getElementById('mbox');
function closeModal(){ modal.hidden=true; }
modal.addEventListener('click',e=>{ if(e.target===modal) closeModal(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&!modal.hidden) closeModal(); });
function openDisney(tab){
  const D=DISNEY; tab=tab||'time';
  const tabs=[['time','시간표'],['rides','어트랙션'],['food','식사'],['tips','팁']];
  let body='';
  if(tab==='time') body=`<ul class="mfacts">${D.facts.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`+D.timeline.map(x=>`<div class="tl"><span class="t">${esc(x.t)}</span><span class="w${/\\(선택\\)/.test(x.what)?' opt':''}">${esc(x.what)}<span class="pk">${esc(x.park)}</span></span><span class="n">${esc(x.note)}</span></div>`).join('');
  if(tab==='rides'){ const grp=v=>D.rides.filter(r=>r.v===v); body=['추천','선택','패스'].map(v=>`<div class="mgrp">${v==='패스'?'패스 (낙하·코스터·공포)':v} · ${grp(v).length}</div>`+grp(v).map(r=>`<div class="rd"><span class="v ${r.v}">${r.v}</span><span class="nm2">${esc(r.n)}${r.paris?'<span class="pr">파리 전용</span>':''}<span class="pkn">${esc(r.park)}</span></span><span class="why">${esc(r.why)}</span></div>`).join('')).join(''); }
  if(tab==='food') body=D.food.map(f=>`<div class="fd"><b>${esc(f.n)}</b><span>${esc(f.when)} · ${esc(f.where)}</span><div>${esc(f.what)}</div><span>${esc(f.tip)}</span></div>`).join('');
  if(tab==='tips') body=`<ul class="mfacts" style="color:var(--fg)">${D.tips.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`;
  mbox.innerHTML=`<div class="mhead"><h2 id="mTitle">${esc(D.title)}</h2><p>${esc(D.sub)}</p><button class="mclose" aria-label="닫기">×</button>
    <div class="mtabs" role="tablist">${tabs.map(([k,l])=>`<button role="tab" data-t="${k}" aria-selected="${k===tab}">${l}</button>`).join('')}</div></div>
    <div class="msec">${body}<p class="src" style="margin:8px 0 0">파크 운영·퍼레이드·쇼 시간은 공식 앱에서 당일 확인하세요. 어트랙션 정보는 일반적으로 알려진 내용 기준이에요.</p></div>`;
  mbox.querySelector('.mclose').onclick=closeModal;
  mbox.querySelectorAll('.mtabs button').forEach(b=>b.onclick=()=>{openDisney(b.dataset.t); mbox.scrollTop=0;});
  modal.hidden=false;
}
window.openDisney=openDisney;""",1)
    # button in day header when the day includes Disney
    s=s.replace("h.innerHTML=`<h3>${D.d} (${D.w}) ${esc(D.title)}</h3>","h.innerHTML=`<h3>${D.d} (${D.w}) ${esc(D.title)}</h3>${D.stops.some(x=>x.k==='p-disney')?'<button class=\"dbtn\" onclick=\"openDisney()\">디즈니 상세 일정 보기</button>':''}",1)
    # button in card
    s=s.replace("<p>${esc(p.t)}</p>","<p>${esc(p.t)}</p>${(p.k==='p-disney'||p.k==='p-daw'||p.k==='p-remy')?'<button class=\"dbtn\" onclick=\"openDisney()\">디즈니 상세 일정 보기</button>':''}",1)
open('script.js','w',encoding='utf-8').write(s)
print('script', s.count('openDisney'))

b=open('build.py',encoding='utf-8').read()
if '__DISNEY__' not in b:
    b=b.replace(".replace('__RES__',open('reservations.json',encoding='utf-8').read())",".replace('__RES__',open('reservations.json',encoding='utf-8').read()).replace('__DISNEY__',open('disney.json',encoding='utf-8').read())")
open('build.py','w',encoding='utf-8').write(b)
print('build', b.count('__DISNEY__'))
