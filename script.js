const CITIES = __CITIES__;
const CATS = {
  hotel:{label:"숙소·역", v:"--hotel"},
  xmas:{label:"크리스마스 마켓", v:"--xmas"},
  sight:{label:"명소", v:"--sight"},
  food:{label:"식당", v:"--food"},
  cafe:{label:"카페", v:"--cafe"},
  night:{label:"야경·바", v:"--night"}
};
let C, PLACES, PLAN, BYK, W, H;
const MY=111200;
const P=(lat,lng)=>[(lng-C.lng0)*C.mx,(C.lat0-lat)*MY];
const NS="http://www.w3.org/2000/svg";
const svg=document.getElementById('map');
const el=(t,a,parent)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);(parent||svg).appendChild(e);return e;};
const path=pts=>pts.map((q,i)=>{const [x,y]=P(q[0],q[1]);return (i?'L':'M')+x.toFixed(0)+' '+y.toFixed(0);}).join(' ');
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const baseLayer=el('g',{}), routeLayer=el('g',{}), pinLayer=el('g',{});
let areaTexts=[], riverText=null;
function drawBase(){
  baseLayer.innerHTML=''; areaTexts=[];
  const [x0,y0]=P(C.bounds[0],C.bounds[1]), [x1,y1]=P(C.bounds[2],C.bounds[3]);
  W=x1-x0; H=y1-y0;
  el('rect',{x:-3000,y:-3000,width:W+6000,height:H+6000,fill:'var(--land)'},baseLayer);
  (C.parks||[]).forEach(([lat,lng,rx,ry,rot])=>{const [x,y]=P(lat,lng);el('ellipse',{cx:x,cy:y,rx,ry,transform:`rotate(${rot||0} ${x} ${y})`,fill:'var(--park)'},baseLayer);});
  (C.blocks||[]).forEach(([a,b,c,d])=>{const [bx1,by1]=P(a,b),[bx2,by2]=P(c,d);el('rect',{x:bx1,y:by1,width:bx2-bx1,height:by2-by1,rx:30,fill:'var(--castle)'},baseLayer);});
  el('path',{d:path(C.river),fill:'none',stroke:'var(--river)','stroke-width':C.riverW,'stroke-linecap':'round','stroke-linejoin':'round'},baseLayer);
  (C.channels||[]).forEach(ch=>el('path',{d:path(ch),fill:'none',stroke:'var(--river)','stroke-width':14},baseLayer));
  (C.bridges||[]).forEach(([a,b])=>el('path',{d:path([a,b]),stroke:'var(--muted)','stroke-width':16,opacity:.55},baseLayer));
  for(const k in C.areaPos){const [x,y]=P(...C.areaPos[k]);const t=el('text',{x,y,'text-anchor':'middle',class:'lbl'},baseLayer);t.textContent=k;areaTexts.push(t);}
  const [rx,ry]=P(C.riverLabel[0],C.riverLabel[1]);
  riverText=el('text',{x:rx,y:ry,class:'rlbl','text-anchor':'middle',transform:`rotate(${C.riverLabel[2]} ${rx} ${ry})`},baseLayer); riverText.textContent=C.riverLabel[3];
}
function makePins(){
  pinLayer.innerHTML='';
  PLACES.forEach(p=>{
    const g=el('g',{class:'pin',transform:`translate(${p.x.toFixed(0)} ${p.y.toFixed(0)})`},pinLayer);
    p.circle=el('circle',{r:40,fill:`var(${CATS[p.c].v})`},g);
    p.num=el('text',{'text-anchor':'middle',style:'fill:#fff;stroke:none;font-weight:700'},g);
    p.text=el('text',{},g); p.text.textContent=p.n;
    g.addEventListener('click',e=>{e.stopPropagation();select(p.id,false);});
    p.g=g;
  });
}

// state
let vb={x:0,y:0,w:1000,h:1000};
let mode='plan', day=0;
const active=new Set(Object.keys(CATS));
let query='', selected=null;
const dayKeys=()=>new Set(PLAN[day].stops.map(s=>s.k));
function visible(p){
  if(mode==='plan') return dayKeys().has(p.k);
  if(mode==='book') return (window.bookKeys?window.bookKeys():new Set()).has(p.k);
  if(!active.has(p.c))return false;
  if(!query)return true;
  return (p.n+' '+p.en+' '+p.t+' '+(p.tip||'')+' '+p.a+' '+(p.m||'')+' '+CATS[p.c].label).toLowerCase().includes(query);
}
function drawRoute(){
  routeLayer.innerHTML='';
  if(mode!=='plan')return;
  const pts=PLAN[day].stops.map(s=>BYK[s.k]).filter(Boolean);
  el('path',{d:pts.map((p,i)=>(i?'L':'M')+p.x.toFixed(0)+' '+p.y.toFixed(0)).join(' '),fill:'none',stroke:PLAN[day].color,'stroke-linejoin':'round','stroke-linecap':'round',opacity:.8,class:'route'},routeLayer);
}
function render(){
  const r=svg.getBoundingClientRect(); const sw=r.width||800, sh=r.height||600, asp=sw/sh;
  if(vb.w/vb.h>asp){const nh=vb.w/asp;vb.y-=(nh-vb.h)/2;vb.h=nh;}else{const nw=vb.h*asp;vb.x-=(nw-vb.w)/2;vb.w=nw;}
  svg.setAttribute('viewBox',`${vb.x} ${vb.y} ${vb.w} ${vb.h}`);
  const k=vb.w/sw, showLabels=k<1.9||mode==='plan';
  const order={}; if(mode==='plan'){PLAN[day].stops.forEach((s,i)=>{(order[s.k]=order[s.k]||[]).push(i+1);});}
  const rp=routeLayer.querySelector('.route'); if(rp){rp.setAttribute('stroke-width',4*k);rp.setAttribute('stroke-dasharray',`${10*k} ${6*k}`);}
  PLACES.forEach((p,i)=>{
    const v=visible(p); p.g.style.display=v?'':'none'; if(!v)return;
    const sel=selected===i, numbered=mode==='plan'&&order[p.k];
    const rad=numbered?10:(sel?9:6.5);
    p.circle.setAttribute('r',rad*k);
    p.circle.setAttribute('stroke-width',(sel?2.5:1.5)*k);
    if(numbered){p.circle.setAttribute('fill',p.c==='hotel'?'var(--hotel)':PLAN[day].color);p.num.textContent=p.c==='hotel'?'H':order[p.k][0];}
    else{p.circle.setAttribute('fill',`var(${CATS[p.c].v})`);p.num.textContent='';}
    p.num.setAttribute('font-size',10.5*k); p.num.setAttribute('y',3.8*k);
    p.text.setAttribute('font-size',12*k); p.text.setAttribute('x',(rad+4)*k); p.text.setAttribute('y',4*k); p.text.setAttribute('stroke-width',3*k);
    p.text.style.display=(showLabels||sel)?'':'none';
    p.g.classList.toggle('sel',sel);
  });
  if(selected!==null)pinLayer.appendChild(PLACES[selected].g);
  areaTexts.forEach(t=>t.setAttribute('font-size',Math.min(15*k,140)));
  if(riverText)riverText.setAttribute('font-size',13*k);
}
function fitTo(list,pad){
  if(!list.length)return;
  const xs=list.map(p=>p.x), ys=list.map(p=>p.y), m=pad||250;
  vb={x:Math.min(...xs)-m,y:Math.min(...ys)-m,w:Math.max(...xs)-Math.min(...xs)+2*m,h:Math.max(...ys)-Math.min(...ys)+2*m};
  render();
}
function zoomAt(f,cx,cy){
  const nw=Math.min(Math.max(vb.w*f,250),W*1.6), ff=nw/vb.w;
  vb.x=cx-(cx-vb.x)*ff; vb.y=cy-(cy-vb.y)*ff; vb.w*=ff; vb.h*=ff; render();
}
const toMap=(cx,cy)=>{const r=svg.getBoundingClientRect();return [vb.x+(cx-r.left)/r.width*vb.w, vb.y+(cy-r.top)/r.height*vb.h];};
svg.addEventListener('wheel',e=>{e.preventDefault();const [mx,my]=toMap(e.clientX,e.clientY);zoomAt(Math.exp(e.deltaY*0.0015),mx,my);},{passive:false});
const ptrs=new Map(); let lastDist=null, moved=0;
svg.addEventListener('pointerdown',e=>{svg.setPointerCapture(e.pointerId);ptrs.set(e.pointerId,[e.clientX,e.clientY]);moved=0;svg.classList.add('drag');});
svg.addEventListener('pointermove',e=>{
  if(!ptrs.has(e.pointerId))return;
  const prev=ptrs.get(e.pointerId); ptrs.set(e.pointerId,[e.clientX,e.clientY]);
  const r=svg.getBoundingClientRect();
  if(ptrs.size===1){const dx=e.clientX-prev[0], dy=e.clientY-prev[1]; moved+=Math.abs(dx)+Math.abs(dy); vb.x-=dx/r.width*vb.w; vb.y-=dy/r.height*vb.h; render();}
  else if(ptrs.size===2){const [a,b]=[...ptrs.values()]; const d=Math.hypot(a[0]-b[0],a[1]-b[1]); if(lastDist){const [mx,my]=toMap((a[0]+b[0])/2,(a[1]+b[1])/2);zoomAt(lastDist/d,mx,my);} lastDist=d; moved+=10;}
});
const up=e=>{ptrs.delete(e.pointerId);if(ptrs.size<2)lastDist=null;if(!ptrs.size)svg.classList.remove('drag');};
svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);
svg.addEventListener('click',e=>{if(moved<5&&!e.target.closest('.pin')){selected=null;card.hidden=true;markList();render();}});
document.getElementById('zin').onclick=()=>zoomAt(0.6,vb.x+vb.w/2,vb.y+vb.h/2);
document.getElementById('zout').onclick=()=>zoomAt(1.6,vb.x+vb.w/2,vb.y+vb.h/2);
document.getElementById('zall').onclick=()=>fitTo(PLACES.filter(visible));

// links & card
const q=s=>encodeURIComponent(s);
const menuHtml=p=>p.menu?`<div class="menu"><b>추천 메뉴</b><ol>${p.menu.map(m=>`<li>${esc(m)}</li>`).join('')}</ol></div>`:'';
const PRICE={'$':'€ 저렴','$$ - $$$':'€€ 보통','$$$$':'€€€ 고급'};
function revHtml(p){const v=p.rev; if(!v)return '';
  const row=(lab,x)=>x==null?'':`<div class="sr"><span>${lab}</span><span class="bar"><i style="width:${(x/5*100).toFixed(0)}%"></i></span><b>${x.toFixed(1)}</b></div>`;
  return `<div class="rev"><div class="rh"><b>리뷰 점수</b><span>★ ${v.r.toFixed(1)} · 리뷰 ${v.c.toLocaleString()}개${v.p?' · '+(PRICE[v.p]||v.p):''}</span></div>
    ${row('맛',v.F)}${row('분위기',v.A)}${row('서비스',v.S)}${row('가성비',v.V)}
    ${v.ko?`<p class="rs">${esc(v.ko)}</p>`:''}<div class="credit">트립어드바이저 세부 평점 · 요약은 트립어드바이저 AI 리뷰 요약을 한국어로 정리</div></div>`;}
const revLine=p=>p.rev?`<div class="rl">★${p.rev.r.toFixed(1)} (${p.rev.c.toLocaleString()}) · 맛 ${p.rev.F??'-'} · 분위기 ${p.rev.A??'-'} · 서비스 ${p.rev.S??'-'} · 가성비 ${p.rev.V??'-'}</div>`:'';
function guideHtml(p){const g=p.guide; if(!g)return '';
  const sec=(lab,arr)=>arr&&arr.length?`<div class="gs"><b>${lab}</b><ul>${arr.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`:'';
  return `<details class="guide" open><summary>상세 가이드</summary>
    ${g.d?`<div class="gs"><b>소요 시간</b><p>${esc(g.d)}</p></div>`:''}
    ${sec('무료 · 유료 구분',g.fr)}${sec('티켓 · 예약 · 운영',g.tk)}${sec('추천 관람 순서',g.rt)}${sec('꼭 볼 것',g.see)}${sec('포토 스팟',g.ph)}${sec('주의 · 겨울 팁',g.wn)}
  </details>`;}
const menuLine=p=>p.menu?`<div class="mn">추천 · ${p.menu.map(esc).join(' · ')}</div>`:'';
function links(p){
  const src=(p.links||[]).map(l=>`<a href="${esc(l.u)}" target="_blank" rel="noopener">${esc(l.t)} ↗</a>`).join('');
  const nav=`<a href="https://www.google.com/maps/search/?api=1&query=${q(p.en+' '+C.en)}" target="_blank" rel="noopener">구글 지도에서 길찾기 ↗</a>`;
  return `${p.note?`<div class="tip"><b>출처 확인</b> ${esc(p.note)}</div>`:''}
    <div class="meta">참조 링크</div><div class="links">${src||'<span class="meta">확인된 출처 없음</span>'}</div>
    <div class="links">${nav}</div>`;
}
const thumb=p=>p.img?`<img class="thumb" src="${p.img}" alt="" loading="lazy">`:`<div class="thumb ph">사진<br>링크</div>`;
const card=document.getElementById('card');
const listEl=document.getElementById('list');
function select(i,fromList){
  selected=i; const p=PLACES[i];
  card.hidden=false;
  card.innerHTML=`<button class="x" aria-label="닫기">×</button>
    ${p.img?`<img src="${p.img}" alt="${esc(p.n)}"><div class="credit">사진: Wikimedia Commons (위키백과 대표 이미지)</div>`:''}
    <h2><span style="width:10px;height:10px;border-radius:50%;background:var(${CATS[p.c].v});display:inline-block"></span>${esc(p.n)}${p.m?`<span class="meal">${p.m}</span>`:''}</h2>
    <div class="meta">${esc(p.en)} · ${esc(p.a)} · ${CATS[p.c].label}</div>
    <p>${esc(p.t)}</p>${(p.k==='p-disney'||p.k==='p-daw'||p.k==='p-remy')?'<button class="dbtn" onclick="openDisney()">디즈니 상세 일정 보기</button>':''}
    ${guideHtml(p)}
    ${revHtml(p)}
    ${menuHtml(p)}
    ${p.tip?`<div class="tip"><b>팁</b> ${esc(p.tip)}</div>`:''}
    ${links(p)}`;
  card.querySelector('.x').onclick=()=>{selected=null;card.hidden=true;markList();render();};
  if(fromList){const w=Math.min(vb.w,1400), r=svg.getBoundingClientRect(); vb={x:p.x-w/2,y:p.y-w*(r.height/r.width)/2,w,h:w*(r.height/r.width)};}
  markList(!fromList); render();
}
function markList(scroll){
  listEl.querySelectorAll('[data-id]').forEach(it=>{
    const s=+it.dataset.id===selected; it.classList.toggle('sel',s);
    if(s&&scroll)it.scrollIntoView({block:'nearest'});
  });
}
function row(p){
  const it=document.createElement('div'); it.tabIndex=0; it.dataset.id=p.id;
  it.onclick=()=>select(p.id,true); it.onkeydown=e=>{if(e.key==='Enter')select(p.id,true);};
  return it;
}

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
const prevStop=k=>BYK[k];
function buildPlan(){
  listEl.innerHTML='';
  const D=PLAN[day];
  const h=document.createElement('div');h.className='dayhead';
  h.innerHTML=`<h3>${D.d} (${D.w}) ${esc(D.title)}</h3>${D.stops.some(x=>x.k==='p-disney')?'<button class="dbtn" onclick="openDisney()">디즈니 상세 일정 보기</button>':''}<p>번호는 방문 순서, 지도 선은 직선 연결이에요. <b>선택</b> 표시는 시간이 빠듯하면 빼도 되는 곳이에요. ${esc(C.planNote)}</p>`;
  listEl.appendChild(h);
  let prevP=null;
  D.stops.forEach((s,i)=>{
    const p=BYK[s.k]; if(!p)return;
    if(prevP){ const sg=document.createElement('div'); sg.innerHTML=segHtml(prevP,p); const el=sg.firstElementChild; if(el){ listEl.appendChild(el); const bt=el.querySelector('.tbtn'); if(bt) bt.onclick=ev=>{ev.stopPropagation(); window.showTransit(prevStop(bt.dataset.from),p,D.d,s.time,el.querySelector('.tres'),bt);}; } }
    prevP=p;
    const it=row(p); it.className='stop'+(s.opt?' opt':'');
    it.innerHTML=`<span class="tm">${s.time}</span><span class="no" style="background:${p.c==='hotel'?'var(--hotel)':D.color}">${p.c==='hotel'?'H':i+1}</span>
      <div><div class="nm">${esc(p.n)}${s.opt?'<span class="ob">선택</span>':''}${p.guide?'<span class="gb">가이드</span>':''}</div><div class="nt">${esc(s.note)}</div>${menuLine(p)}${revLine(p)}</div>${thumb(p)}`;
    listEl.appendChild(it);
  });
  listEl.appendChild(foot());
  markList();
}
function buildAll(){
  listEl.innerHTML=''; let shown=0;
  const order={hotel:0,xmas:1,sight:2,night:3,food:4,cafe:5};
  C.areas.forEach(a=>{
    const items=PLACES.filter(p=>p.a===a&&visible(p)); if(!items.length)return;
    const h=document.createElement('div');h.className='area';h.textContent=a+'  '+items.length;listEl.appendChild(h);
    items.sort((x,y)=>order[x.c]-order[y.c]).forEach(p=>{
      shown++; const it=row(p); it.className='item';
      it.innerHTML=`<span class="dot" style="background:var(${CATS[p.c].v})"></span>
        <div class="nm">${esc(p.n)}<span class="en">${esc(p.en)}</span>${p.m?`<span class="meal">${p.m}</span>`:''}</div>
        <div class="tp">${esc(p.t)}${menuLine(p)}${revLine(p)}</div>${thumb(p)}`;
      listEl.appendChild(it);
    });
  });
  if(!shown){const e=document.createElement('p');e.className='src';e.style.padding='18px';e.textContent='조건에 맞는 장소가 없어요. 검색어를 바꾸거나 위의 분류를 다시 켜 보세요.';listEl.appendChild(e);}
  listEl.appendChild(foot()); markList();
}
function foot(){
  const s=document.createElement('p');s.className='src';s.style.padding='14px 18px';
  s.textContent='지도는 위치 감을 잡기 위한 간략도이고 핀 좌표는 근사치예요. 사진은 위키백과에 대표 이미지가 있는 곳만 넣었고, 나머지는 카드의 참조 링크와 구글 지도에서 확인하세요. 영업시간·마켓 일정은 출발 전 다시 확인하세요.';
  return s;
}
function build(){mode==='plan'?buildPlan():mode==='book'?buildBook():buildAll(); drawRoute();}

// controls
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
  if(tab==='time') body=`<ul class="mfacts">${D.facts.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`+D.timeline.map(x=>`<div class="tl"><span class="t">${esc(x.t)}</span><span class="w${/\(선택\)/.test(x.what)?' opt':''}">${esc(x.what)}<span class="pk">${esc(x.park)}</span></span><span class="n">${esc(x.note)}</span></div>`).join('');
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
window.openDisney=openDisney;
const ST={must:'예약 필수',rec:'예약 추천',check:'확인 필요',done:'완료',none:'예약 불가',walk:'현장 탑승'};
const resKey=r=>'res:'+r.city+':'+r.d+':'+r.k+':'+r.what;
const isDone=r=>{ if(r.st==='done') return true; try{return localStorage.getItem(resKey(r))==='1';}catch(e){return false;} };
function curCityKey(){ return Object.keys(CITIES).find(k=>CITIES[k]===C); }
window.bookKeys=()=>{ const ck=curCityKey(); return new Set(RES.filter(r=>r.city===ck||(ck==='prague'&&r.city==='prague')).map(r=>r.k)); };
const dnum=d=>{const [m,dd]=d.split('/').map(Number); return m*100+dd;};
const tnum=t=>/^\d/.test(t)?parseInt(t.replace(':',''),10):9999;
function buildBook(){
  listEl.innerHTML='';
  const act=RES.filter(r=>r.st!=='none'&&r.st!=='walk');
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
    el.innerHTML=`<input type="checkbox" ${dn?'checked':''} ${r.st==='done'||r.st==='none'||r.st==='walk'?'disabled':''} aria-label="예약 완료 체크">
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
}
const planCtl=document.getElementById('planCtl'), allCtl=document.getElementById('allCtl'), chips=document.getElementById('chips');
function buildControls(){
  planCtl.innerHTML='';
  PLAN.forEach((D,i)=>{
    const b=document.createElement('button');b.className='day';b.style.setProperty('--dc',D.color);
    b.setAttribute('aria-pressed',i===day);
    b.innerHTML=`<b>${D.d} ${D.w}</b><span>${esc(D.title.split(' · ')[0])}</span>`;
    b.onclick=()=>{day=i;planCtl.querySelectorAll('.day').forEach((x,j)=>x.setAttribute('aria-pressed',j===i));selected=null;card.hidden=true;build();fitTo(PLAN[day].stops.map(s=>BYK[s.k]).filter(Boolean),220);};
    planCtl.appendChild(b);
  });
  chips.innerHTML='';
  for(const k in CATS){
    const n=PLACES.filter(p=>p.c===k).length; if(!n)continue;
    const b=document.createElement('button');b.className='chip';b.setAttribute('aria-pressed',active.has(k));
    b.innerHTML=`<span class="dot" style="background:var(${CATS[k].v})"></span>${CATS[k].label}<span class="n">${n}</span>`;
    b.onclick=()=>{active.has(k)?active.delete(k):active.add(k);b.setAttribute('aria-pressed',active.has(k));build();render();};
    chips.appendChild(b);
  }
  document.getElementById('total').textContent=PLACES.length;
}
function setMode(m){
  mode=m; selected=null; card.hidden=true;
  document.getElementById('tab-plan').setAttribute('aria-selected',m==='plan');
  document.getElementById('tab-all').setAttribute('aria-selected',m==='all');
  document.getElementById('tab-book').setAttribute('aria-selected',m==='book');
  planCtl.hidden=m!=='plan'; allCtl.hidden=m!=='all';
  build();
  if(m==='book'){ const bk=window.bookKeys(); fitTo(PLACES.filter(p=>bk.has(p.k)),200); return; }
  fitTo(m==='plan'?PLAN[day].stops.map(s=>BYK[s.k]).filter(Boolean):PLACES.filter(p=>p.lat>C.core[0]&&p.lat<C.core[2]&&p.lng>C.core[1]&&p.lng<C.core[3]),m==='plan'?220:150);
}
const cityTabs=document.getElementById('cityTabs');
function setCity(key){
  C=CITIES[key]; PLACES=C.places; PLAN=C.plan; BYK={}; day=C.startDay||0; query=''; document.getElementById('q').value='';
  PLACES.forEach((p,i)=>{p.id=i;[p.x,p.y]=P(p.lat,p.lng);BYK[p.k]=p;});
  document.getElementById('sub').textContent=C.sub;
  cityTabs.querySelectorAll('button').forEach(b=>b.setAttribute('aria-selected',b.dataset.k===key));
  drawBase(); makePins(); buildControls(); setMode('plan');
  try{localStorage.setItem('city',key);}catch(e){}
}
Object.keys(CITIES).forEach(k=>{
  const b=document.createElement('button');b.role='tab';b.dataset.k=k;b.textContent=CITIES[k].label;
  b.onclick=()=>setCity(k); cityTabs.appendChild(b);
});
document.getElementById('tab-plan').onclick=()=>setMode('plan');
document.getElementById('tab-all').onclick=()=>setMode('all');
document.getElementById('tab-book').onclick=()=>setMode('book');
document.getElementById('q').addEventListener('input',e=>{query=e.target.value.trim().toLowerCase();build();render();});
new ResizeObserver(()=>render()).observe(svg);
let startCity='prague'; try{const s=localStorage.getItem('city'); if(s&&CITIES[s])startCity=s;}catch(e){}
setCity(startCity);

// mobile sheet
(function(){
  const side=document.querySelector('.side'), grab=document.getElementById('grab'), head=document.querySelector('header.head');
  const mq=matchMedia('(max-width:760px)'); let state='half';
  const hFor=st=>{const vh=innerHeight; if(st==='peek') return Math.min(head.offsetHeight+30, vh*0.45); if(st==='full') return vh*0.88; return vh*0.56;};
  window.sheetHeight=()=>mq.matches?side.getBoundingClientRect().height:0;
  function set(st,px){
    if(!mq.matches){document.documentElement.style.removeProperty('--sheet-h');return;}
    if(st) state=st;
    document.documentElement.style.setProperty('--sheet-h',(px??hFor(state))+'px');
    side.dataset.sheet=state;
  }
  window.setSheet=set;
  const order=['peek','half','full'];
  let startY=null,startH=0,moved=0;
  grab.addEventListener('pointerdown',e=>{if(!mq.matches)return; startY=e.clientY; startH=side.getBoundingClientRect().height; moved=0; side.classList.add('dragging'); grab.setPointerCapture(e.pointerId);});
  grab.addEventListener('pointermove',e=>{if(startY===null)return; const dy=startY-e.clientY; moved=Math.max(moved,Math.abs(dy)); const h=Math.max(90,Math.min(innerHeight*0.92,startH+dy)); document.documentElement.style.setProperty('--sheet-h',h+'px');});
  const end=e=>{ if(startY===null)return; side.classList.remove('dragging');
    const h=side.getBoundingClientRect().height; startY=null;
    if(moved<6){ set(order[(order.indexOf(state)+1)%3]); return; }
    let best='half',bd=1e9; for(const st of order){const d=Math.abs(hFor(st)-h); if(d<bd){bd=d;best=st;}} set(best); };
  grab.addEventListener('pointerup',end); grab.addEventListener('pointercancel',end);
  new MutationObserver(()=>{ if(mq.matches && !card.hidden) set('peek'); }).observe(card,{attributes:true,attributeFilter:['hidden']});
  mq.addEventListener('change',()=>set()); addEventListener('resize',()=>set());
  set('half');
})();
