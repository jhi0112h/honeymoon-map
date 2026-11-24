s=open('script.js',encoding='utf-8').read()
if 'segHtml' not in s:
    helper = r'''
const hav=(a,b)=>{const R=6371,t=x=>x*Math.PI/180;const dl=t(b.lat-a.lat),dn=t(b.lng-a.lng);const h=Math.sin(dl/2)**2+Math.cos(t(a.lat))*Math.cos(t(b.lat))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(h));};
function segHtml(a,b){
  if(!a||!b||a.k===b.k) return '';
  const km=hav(a,b), walkMin=Math.round(km*1.3/4.8*60);
  const gurl=`https://www.google.com/maps/dir/?api=1&origin=${a.lat},${a.lng}&destination=${b.lat},${b.lng}&travelmode=`;
  if(km<0.9) return `<div class="seg walk">↓ 도보 약 ${Math.max(1,walkMin)}분 <a href="${gurl}walking" target="_blank" rel="noopener">길찾기 ↗</a></div>`;
  return `<div class="seg ride"><span>↓ 약 ${km.toFixed(1)}km · 교통편 필요 (도보면 약 ${walkMin}분)</span>
    <span class="segbtns">${window.showTransit?`<button class="tbtn" data-from="${a.k}" data-to="${b.k}">추천 이동 방법</button>`:''}<a href="${gurl}transit" target="_blank" rel="noopener">구글 지도 대중교통 ↗</a></span>
    <div class="tres" hidden></div></div>`;
}
'''
    s=s.replace("function buildPlan(){",helper+"function buildPlan(){",1)
    s=s.replace("""  D.stops.forEach((s,i)=>{
    const p=BYK[s.k]; if(!p)return;""","""  let prevP=null;
  D.stops.forEach((s,i)=>{
    const p=BYK[s.k]; if(!p)return;
    if(prevP){ const sg=document.createElement('div'); sg.innerHTML=segHtml(prevP,p); const el=sg.firstElementChild; if(el){ listEl.appendChild(el); const bt=el.querySelector('.tbtn'); if(bt) bt.onclick=ev=>{ev.stopPropagation(); window.showTransit(prevStop(bt.dataset.from),p,D.d,s.time,el.querySelector('.tres'),bt);}; } }
    prevP=p;""",1)
    s=s.replace("function buildPlan(){","const prevStop=k=>BYK[k];\nfunction buildPlan(){",1)
open('script.js','w',encoding='utf-8').write(s)
print('script', s.count('segHtml'))

g=open('gmap_core.js',encoding='utf-8').read()
if 'window.showTransit' not in g:
    g+=r'''
// transit directions between stops (Google Directions, TRANSIT mode)
const VEH={SUBWAY:'지하철',METRO_RAIL:'지하철',TRAM:'트램',BUS:'버스',INTERCITY_BUS:'시외버스',HEAVY_RAIL:'기차',COMMUTER_TRAIN:'교외열차',HIGH_SPEED_TRAIN:'고속열차',RAIL:'열차',FUNICULAR:'푸니쿨라',FERRY:'페리',CABLE_CAR:'케이블카',TROLLEYBUS:'트롤리버스',MONORAIL:'모노레일',SHARE_TAXI:'합승택시',OTHER:'교통'};
const tCache={};
window.showTransit=function(a,b,d,time,box,btn){
  if(!ready){ box.hidden=false; box.textContent='구글 지도가 로드된 뒤에 사용할 수 있어요.'; return; }
  if(!box.hidden && box.dataset.loaded){ box.hidden=true; return; }
  box.hidden=false; box.textContent='경로를 찾는 중...';
  const key=a.k+'>'+b.k+'@'+d+time;
  const show=html=>{ box.innerHTML=html; box.dataset.loaded='1'; };
  if(tCache[key]) return show(tCache[key]);
  const req={origin:{lat:a.lat,lng:a.lng},destination:{lat:b.lat,lng:b.lng},travelMode:google.maps.TravelMode.TRANSIT};
  const m=/^(\d{1,2}):(\d{2})$/.exec(time||''); const dm=/^(\d{1,2})\/(\d{1,2})$/.exec(d||'');
  if(m&&dm){ req.transitOptions={arrivalTime:new Date(Date.UTC(2026,+dm[1]-1,+dm[2],+m[1]-1,+m[2]))}; }
  new google.maps.DirectionsService().route(req).then(res=>{
    const leg=res.routes[0].legs[0];
    const steps=leg.steps.map(st=>{
      if(st.travel_mode==='TRANSIT'&&st.transit){ const t=st.transit, ln=t.line||{}; const v=VEH[(ln.vehicle||{}).type]||'교통';
        return `<li><b>${v} ${esc(ln.short_name||ln.name||'')}</b> ${t.headsign?esc(t.headsign)+' 방향':''}<br>${esc(t.departure_stop.name)} → ${esc(t.arrival_stop.name)} · ${t.num_stops}정거장 · ${esc(st.duration.text)}${t.departure_time?` · ${esc(t.departure_time.text)} 출발`:''}</li>`; }
      return `<li>도보 ${esc(st.duration.text)} <span class="muted">(${esc(st.distance.text)})</span></li>`; }).join('');
    const html=`<div class="tsum">총 ${esc(leg.duration.text)}${leg.departure_time?` · ${esc(leg.departure_time.text)} 출발 → ${esc(leg.arrival_time.text)} 도착`:''}</div><ol>${steps}</ol><div class="muted">구글 대중교통 경로 기준 · 현지 시간 · 짐이 많거나 늦은 밤이면 택시·우버도 고려</div>`;
    tCache[key]=html; show(html);
  }).catch(()=>{ show(`대중교통 경로를 찾지 못했어요. 택시·우버나 구글 지도 앱 길찾기를 이용하세요.`); });
};
'''
open('gmap_core.js','w',encoding='utf-8').write(g)
print('gmap', 'window.showTransit' in g)

t=open('template.html',encoding='utf-8').read()
if '.seg{' not in t:
    t=t.replace('.ob{','''.seg{padding:4px 18px 4px 72px;font-size:11.5px;color:var(--muted);border-bottom:1px dashed var(--line);display:grid;gap:4px}
.seg a{color:var(--sight)}
.seg.ride{background:var(--bg)}
.segbtns{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.tbtn{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:6px;padding:5px 9px;font:inherit;font-size:12px;font-weight:700;cursor:pointer;min-height:32px}
.tres{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:var(--fg);font-size:12.5px}
.tres ol{margin:6px 0;padding-left:18px;display:grid;gap:5px;line-height:1.45}
.tres .tsum{font-weight:700}.tres .muted{color:var(--muted);font-size:11.5px}
@media (max-width:760px){.seg{padding-left:64px}}
.ob{''',1)
open('template.html','w',encoding='utf-8').write(t)
print('css ok')
