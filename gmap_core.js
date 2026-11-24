const CITIES = __CITIES__;
const CATS = {
  hotel:{label:"숙소·역", v:"--hotel"},
  xmas:{label:"크리스마스 마켓", v:"--xmas"},
  sight:{label:"명소", v:"--sight"},
  food:{label:"식당", v:"--food"},
  cafe:{label:"카페", v:"--cafe"},
  night:{label:"야경·바", v:"--night"}
};
let C, PLACES, PLAN, BYK;
const P=(lat,lng)=>[lng,lat]; // kept for shared list code
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cssVar=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim()||'#555';
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

// ---------- Google Maps ----------
let gmap=null, routeLine=null, walkRenderers=[], ready=false;
const KEY_STORE='gmapsKey';
function getKey(){ if(window.GMAPS_KEY) return window.GMAPS_KEY; try{return localStorage.getItem(KEY_STORE)||'';}catch(e){return '';} }
function showSetup(msg){
  const s=document.getElementById('setup'); s.hidden=false;
  if(msg) document.getElementById('setupMsg').textContent=msg;
}
document.getElementById('keySave').onclick=()=>{
  const v=document.getElementById('keyInput').value.trim(); if(!v)return;
  try{localStorage.setItem(KEY_STORE,v);}catch(e){}
  location.reload();
};
document.getElementById('keyReset').onclick=()=>{try{localStorage.removeItem(KEY_STORE);}catch(e){} location.reload();};
window.gm_authFailure=()=>showSetup('API 키 인증에 실패했어요. 키가 맞는지, Maps JavaScript API가 사용 설정됐는지, 웹사이트 제한에 http://localhost:8000/* 이 들어 있는지 확인해 주세요.');
function loadMaps(){
  const k=getKey(); if(!k){showSetup();return;}
  const s=document.createElement('script');
  s.src=`https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(k)}&callback=initMap&language=ko&region=KR&v=weekly`;
  s.async=true; s.onerror=()=>showSetup('구글 지도 스크립트를 불러오지 못했어요. 인터넷 연결을 확인해 주세요.');
  document.head.appendChild(s);
}
window.initMap=function(){
  gmap=new google.maps.Map(document.getElementById('gmap'),{center:{lat:50.087,lng:14.42},zoom:14,mapTypeControl:false,streetViewControl:true,fullscreenControl:true,zoomControlOptions:{position:google.maps.ControlPosition.RIGHT_TOP},streetViewControlOptions:{position:google.maps.ControlPosition.RIGHT_TOP},fullscreenControlOptions:{position:google.maps.ControlPosition.TOP_RIGHT},clickableIcons:true,gestureHandling:'greedy'});
  gmap.addListener('click',()=>{selected=null;card.hidden=true;markList();render();});
  ready=true;
  setCity(startCity);
};
function drawBase(){ /* Google basemap handles geography */ }
function makePins(){
  Object.values(CITIES).forEach(c=>c.places.forEach(p=>{ if(p.marker){p.marker.setMap(null);p.marker=null;} }));
  if(!ready) return;
  PLACES.forEach(p=>{
    p.marker=new google.maps.Marker({position:{lat:p.lat,lng:p.lng},map:gmap,title:p.n});
    p.marker.addListener('click',()=>select(p.id,false));
  });
}
function drawRoute(){
  if(routeLine){routeLine.setMap(null);routeLine=null;}
  clearWalk();
  if(!ready||mode!=='plan')return;
  const pts=PLAN[day].stops.map(s=>BYK[s.k]).filter(Boolean).map(p=>({lat:p.lat,lng:p.lng}));
  routeLine=new google.maps.Polyline({path:pts,map:gmap,strokeOpacity:0,icons:[{icon:{path:'M 0,-1 0,1',strokeOpacity:.9,strokeColor:PLAN[day].color,scale:3},offset:'0',repeat:'14px'}]});
}
function clearWalk(){ walkRenderers.forEach(r=>r.setMap(null)); walkRenderers=[]; const b=document.getElementById('walkBtn'); if(b) b.setAttribute('aria-pressed','false'); }
async function showWalk(){
  if(!ready||mode!=='plan')return;
  if(walkRenderers.length){clearWalk(); if(routeLine)routeLine.setMap(gmap); return;}
  const pts=[]; PLAN[day].stops.forEach(s=>{const p=BYK[s.k]; if(p && !(pts.length&&pts[pts.length-1].k===p.k)) pts.push(p);});
  if(pts.length<2)return;
  const svc=new google.maps.DirectionsService();
  const chunks=[]; for(let i=0;i<pts.length-1;i+=24) chunks.push(pts.slice(i,Math.min(i+25,pts.length)));
  const btn=document.getElementById('walkBtn'); btn.setAttribute('aria-pressed','true');
  for(const ch of chunks){
    try{
      const res=await svc.route({origin:{lat:ch[0].lat,lng:ch[0].lng},destination:{lat:ch.at(-1).lat,lng:ch.at(-1).lng},waypoints:ch.slice(1,-1).map(p=>({location:{lat:p.lat,lng:p.lng},stopover:true})),travelMode:google.maps.TravelMode.WALKING});
      const r=new google.maps.DirectionsRenderer({map:gmap,directions:res,suppressMarkers:true,preserveViewport:true,polylineOptions:{strokeColor:PLAN[day].color,strokeWeight:5,strokeOpacity:.85}});
      walkRenderers.push(r);
    }catch(e){ alertBox('도보 경로를 불러오지 못했어요. Directions API가 사용 설정돼 있는지 확인해 주세요.'); break; }
  }
  if(routeLine&&walkRenderers.length) routeLine.setMap(null);
}
function alertBox(t){const n=document.getElementById('notice'); n.textContent=t; n.hidden=false; setTimeout(()=>n.hidden=true,6000);}
function render(){
  if(!ready)return;
  const order={}; if(mode==='plan'){PLAN[day].stops.forEach((s,i)=>{(order[s.k]=order[s.k]||[]).push(i+1);});}
  PLACES.forEach((p,i)=>{
    if(!p.marker)return;
    const v=visible(p); p.marker.setVisible(v); if(!v)return;
    const sel=selected===i, numbered=mode==='plan'&&order[p.k];
    const color=numbered?(p.c==='hotel'?cssVar('--hotel'):PLAN[day].color):cssVar(CATS[p.c].v);
    p.marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:numbered?11:(sel?9:7),fillColor:color,fillOpacity:1,strokeColor:sel?'#111':'#fff',strokeWeight:sel?3:2,labelOrigin:new google.maps.Point(0,0)});
    p.marker.setLabel(numbered?{text:p.c==='hotel'?'H':String(order[p.k][0]),color:'#fff',fontSize:'11px',fontWeight:'700'}:null);
    p.marker.setZIndex(sel?1000:(numbered?500:100));
  });
}
function fitTo(list){
  if(!ready||!list.length)return;
  if(list.length===1){gmap.setCenter({lat:list[0].lat,lng:list[0].lng});gmap.setZoom(16);const sb=(window.sheetHeight?window.sheetHeight():0); if(sb) gmap.panBy(0,sb/2); render();return;}
  const b=new google.maps.LatLngBounds(); list.forEach(p=>b.extend({lat:p.lat,lng:p.lng}));
  const sb=(window.sheetHeight?window.sheetHeight():0); gmap.fitBounds(b,{top:50,right:50,bottom:Math.max(40,sb+30),left:30}); render();
}
document.getElementById('zall').onclick=()=>fitTo(PLACES.filter(visible));
document.getElementById('walkBtn').onclick=()=>showWalk();

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
