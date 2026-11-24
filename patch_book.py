import re
t=open('template.html',encoding='utf-8').read()
if 'tab-book' not in t:
    t=t.replace('<button id="tab-all" role="tab" aria-selected="false">장소 <span id="total"></span>곳</button>',
                '<button id="tab-all" role="tab" aria-selected="false">장소 <span id="total"></span>곳</button>\n        <button id="tab-book" role="tab" aria-selected="false">예약 <span id="bookN"></span></button>')
    t=t.replace('.ob{','''.bk{display:grid;grid-template-columns:26px 1fr;gap:4px 10px;padding:11px 16px;border-bottom:1px solid var(--line);align-items:start;cursor:pointer}
.bk:hover{background:var(--bg)}
.bk input{width:20px;height:20px;margin-top:2px;accent-color:var(--fg)}
.bk .bt{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-weight:700}
.bk .bt .tm{font-variant-numeric:tabular-nums;color:var(--muted);font-weight:600;font-size:12.5px}
.bk .bw{grid-column:2;font-size:13px}
.bk .bn{grid-column:2;font-size:12px;color:var(--muted);line-height:1.45}
.bk .bl{grid-column:2;font-size:12.5px;display:flex;gap:10px;flex-wrap:wrap}
.bk .bl a{color:var(--sight)}
.bk.done .bt,.bk.done .bw{text-decoration:line-through;opacity:.55}
.st{font-size:10.5px;font-weight:700;border-radius:4px;padding:1px 6px;color:#fff}
.st.must{background:var(--food)}.st.rec{background:var(--sight)}.st.check{background:var(--hotel)}.st.done{background:var(--xmas)}.st.none{background:var(--muted)}
.bsum{padding:12px 16px;border-bottom:1px solid var(--line);display:grid;gap:8px;font-size:12.5px;color:var(--muted)}
.bsum .row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.bday{position:sticky;top:0;background:var(--surface);padding:10px 16px 6px;font-weight:700;font-size:12.5px;border-bottom:1px solid var(--line);z-index:1}
.ob{''',1)
open('template.html','w',encoding='utf-8').write(t)

s=open('script.js',encoding='utf-8').read()
if 'buildBook' not in s:
    s=s.replace("// controls","""// controls
const RES = __RES__;
const ST={must:'예약 필수',rec:'예약 추천',check:'확인 필요',done:'완료',none:'예약 불가'};
const resKey=r=>'res:'+r.city+':'+r.d+':'+r.k+':'+r.what;
const isDone=r=>{ if(r.st==='done') return true; try{return localStorage.getItem(resKey(r))==='1';}catch(e){return false;} };
function curCityKey(){ return Object.keys(CITIES).find(k=>CITIES[k]===C); }
window.bookKeys=()=>{ const ck=curCityKey(); return new Set(RES.filter(r=>r.city===ck||(ck==='prague'&&r.city==='prague')).map(r=>r.k)); };
const dnum=d=>{const [m,dd]=d.split('/').map(Number); return m*100+dd;};
const tnum=t=>/^\\d/.test(t)?parseInt(t.replace(':',''),10):9999;
function buildBook(){
  listEl.innerHTML='';
  const act=RES.filter(r=>r.st!=='none');
  const cnt=k=>act.filter(r=>r.st===k&&!isDone(r)).length;
  const done=act.filter(isDone).length;
  const sm=document.createElement('div'); sm.className='bsum';
  sm.innerHTML=`<div class="row"><span class="st must">예약 필수</span> ${cnt('must')} <span class="st rec">예약 추천</span> ${cnt('rec')} <span class="st check">확인 필요</span> ${cnt('check')} <span class="st done">완료</span> ${done}</div>
    <div>다섯 도시 예약 항목을 날짜순으로 모았어요. 예약을 마치면 체크하세요 (이 브라우저에만 저장). 줄을 누르면 지도에서 위치를 보여줘요.</div>`;
  listEl.appendChild(sm);
  const sorted=RES.map((r,i)=>({...r,i})).sort((a,b)=>dnum(a.d)-dnum(b.d)||tnum(a.time)-tnum(b.time));
  let last='';
  sorted.forEach(r=>{
    const city=CITIES[r.city]; const p=city.places.find(x=>x.k===r.k);
    if(r.d!==last){ last=r.d; const h=document.createElement('div'); h.className='bday'; h.textContent=r.d+' · '+city.name; listEl.appendChild(h); }
    const el=document.createElement('div'); const dn=isDone(r); el.className='bk'+(dn?' done':'');
    const offi=p&&p.links?(p.links.find(l=>/공식|관광청|예약/.test(l.t)&&!/유튜브|인스타/.test(l.t))||null):null;
    const gm=p?`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(p.en+' '+city.en)}`:'';
    el.innerHTML=`<input type="checkbox" ${dn?'checked':''} ${r.st==='done'||r.st==='none'?'disabled':''} aria-label="예약 완료 체크">
      <div class="bt"><span class="tm">${esc(r.time)}</span>${esc(p?p.n:r.k)} <span class="st ${r.st}">${ST[r.st]}</span></div>
      <div class="bw">${esc(r.what)}</div>
      <div class="bn">${esc(r.note||'')}</div>
      <div class="bl">${offi?`<a href="${esc(offi.u)}" target="_blank" rel="noopener">${esc(offi.t)} ↗</a>`:''}${gm?`<a href="${gm}" target="_blank" rel="noopener">구글 지도 ↗</a>`:''}</div>`;
    const cb=el.querySelector('input');
    cb.addEventListener('click',e=>{e.stopPropagation(); try{localStorage.setItem(resKey(r),cb.checked?'1':'0');}catch(_){} buildBook(); render();});
    el.querySelectorAll('a').forEach(a=>a.addEventListener('click',e=>e.stopPropagation()));
    el.addEventListener('click',()=>{ if(CITIES[r.city]!==C){ setCity(r.city); setMode('book'); } if(p) select(p.id,true); });
    listEl.appendChild(el);
  });
  const n=document.getElementById('bookN'); if(n) n.textContent=act.filter(r=>!isDone(r)).length;
}""",1)
    s=s.replace("function build(){mode==='plan'?buildPlan():buildAll(); drawRoute();}","function build(){mode==='plan'?buildPlan():mode==='book'?buildBook():buildAll(); drawRoute();}")
    s=s.replace("  document.getElementById('tab-all').setAttribute('aria-selected',m==='all');\n  planCtl.hidden=m!=='plan'; allCtl.hidden=m!=='all';",
                "  document.getElementById('tab-all').setAttribute('aria-selected',m==='all');\n  document.getElementById('tab-book').setAttribute('aria-selected',m==='book');\n  planCtl.hidden=m!=='plan'; allCtl.hidden=m!=='all';")
    s=s.replace("  fitTo(m==='plan'?","  if(m==='book'){ const bk=window.bookKeys(); fitTo(PLACES.filter(p=>bk.has(p.k)),200); return; }\n  fitTo(m==='plan'?",1)
    s=s.replace("document.getElementById('tab-all').onclick=()=>setMode('all');","document.getElementById('tab-all').onclick=()=>setMode('all');\ndocument.getElementById('tab-book').onclick=()=>setMode('book');")
open('script.js','w',encoding='utf-8').write(s)
print('script', s.count('buildBook'), "tab-book" in s)

for f in ('script.js','gmap_core.js'):
    x=open(f,encoding='utf-8').read()
    if "mode==='book'" not in x.split('function visible')[1][:200]:
        x=x.replace("function visible(p){\n  if(mode==='plan') return dayKeys().has(p.k);","function visible(p){\n  if(mode==='plan') return dayKeys().has(p.k);\n  if(mode==='book') return (window.bookKeys?window.bookKeys():new Set()).has(p.k);",1)
    open(f,'w',encoding='utf-8').write(x)
    print(f, "mode==='book'" in x)

b=open('build.py',encoding='utf-8').read()
if "__RES__" not in b:
    b=b.replace("g=open('gmap-template.html',encoding='utf-8').read().replace('__GMAP__',open('gmap.js',encoding='utf-8').read()).replace('__CITIES__',cities_json)",
                "g=open('gmap-template.html',encoding='utf-8').read().replace('__GMAP__',open('gmap.js',encoding='utf-8').read()).replace('__CITIES__',cities_json).replace('__RES__',open('reservations.json',encoding='utf-8').read())")
    b=b.replace("html=html.replace('__CITIES__',","html=html.replace('__RES__',open('reservations.json',encoding='utf-8').read()).replace('__CITIES__',",1)
open('build.py','w',encoding='utf-8').write(b)
print('build', b.count('__RES__'))
