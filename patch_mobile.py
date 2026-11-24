t=open('template.html',encoding='utf-8').read()
old_mq=t[t.index('@media (max-width:760px){'):t.index('@media (prefers-reduced-motion')]
new_mq='''.grab{display:none}
@media (max-width:760px){
  html,body{height:100%;overflow:hidden}
  .app{display:block;height:100dvh}
  .mapwrap{position:fixed;inset:0;height:auto}
  .legend{display:none}
  .side{position:fixed;left:0;right:0;bottom:0;width:auto;height:var(--sheet-h,50dvh);border-left:0;border-top:1px solid var(--line);border-radius:16px 16px 0 0;box-shadow:0 -6px 24px rgba(0,0,0,.18);z-index:20;transition:height .25s ease;padding-bottom:env(safe-area-inset-bottom,0px)}
  .side.dragging{transition:none}
  .grab{display:flex;justify-content:center;align-items:center;width:100%;height:26px;border:0;background:transparent;cursor:grab;touch-action:none;flex:none}
  .grab span{width:44px;height:5px;border-radius:3px;background:var(--line)}
  header.head{padding-block:2px 10px;gap:8px}
  h1{font-size:18px}
  .sub{font-size:12px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  #cityTabs{overflow-x:auto;scrollbar-width:none}
  #cityTabs::-webkit-scrollbar,.days::-webkit-scrollbar{display:none}
  #cityTabs button{flex:none;padding:8px 12px;white-space:nowrap}
  .tabs button{min-height:40px}
  .days{scrollbar-width:none}
  .day{min-height:44px;padding:6px 12px}
  .chip{min-height:36px;padding:6px 12px}
  input#q{font-size:16px;min-height:42px}
  .stop{grid-template-columns:42px 22px 1fr 48px;gap:8px;padding:11px 14px}
  .item{padding:11px 14px}
  .thumb{width:48px;height:48px}
  .area{padding:10px 14px 6px}
  .card{position:fixed;left:max(8px,env(safe-area-inset-left,0px));right:max(8px,env(safe-area-inset-right,0px));bottom:calc(var(--sheet-h,50dvh) + 8px);max-width:none;max-height:calc(100dvh - var(--sheet-h,50dvh) - 70px);z-index:30;border-radius:12px}
  .card img{height:120px}
  .card .x{width:36px;height:36px;font-size:22px}
  .ctl{top:auto!important;bottom:calc(var(--sheet-h,50dvh) + 12px)!important;right:max(10px,env(safe-area-inset-right,0px))!important}
  .ctl button{width:44px;height:44px}
  .notice{top:calc(10px + env(safe-area-inset-top,0px))}
}
'''
t=t.replace(old_mq,new_mq)
if 'id="grab"' not in t:
    t=t.replace('<aside class="side">','<aside class="side">\n    <button class="grab" id="grab" aria-label="목록 크기 바꾸기"><span></span></button>',1)
open('template.html','w',encoding='utf-8').write(t)

s=open('script.js',encoding='utf-8').read()
if '// mobile sheet' not in s:
    s+='''
// mobile sheet
(function(){
  const side=document.querySelector('.side'), grab=document.getElementById('grab'), head=document.querySelector('header.head');
  const mq=matchMedia('(max-width:760px)'); let state='half';
  const hFor=st=>{const vh=innerHeight; if(st==='peek') return Math.min(head.offsetHeight+30, vh*0.45); if(st==='full') return vh*0.88; return vh*0.5;};
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
'''
open('script.js','w',encoding='utf-8').write(s)

g=open('gmap_core.js',encoding='utf-8').read()
g=g.replace("mapTypeControl:false,streetViewControl:true,fullscreenControl:true,","mapTypeControl:false,streetViewControl:true,fullscreenControl:true,zoomControlOptions:{position:google.maps.ControlPosition.RIGHT_TOP},streetViewControlOptions:{position:google.maps.ControlPosition.RIGHT_TOP},fullscreenControlOptions:{position:google.maps.ControlPosition.TOP_RIGHT},")
g=g.replace("gmap.fitBounds(b,{top:40,right:40,bottom:40,left:40}); render();","const sb=(window.sheetHeight?window.sheetHeight():0); gmap.fitBounds(b,{top:50,right:50,bottom:Math.max(40,sb+30),left:30}); render();")
g=g.replace("if(list.length===1){gmap.setCenter({lat:list[0].lat,lng:list[0].lng});gmap.setZoom(16);render();return;}","if(list.length===1){gmap.setCenter({lat:list[0].lat,lng:list[0].lng});gmap.setZoom(16);const sb=(window.sheetHeight?window.sheetHeight():0); if(sb) gmap.panBy(0,sb/2); render();return;}")
open('gmap_core.js','w',encoding='utf-8').write(g)
# when selecting from list on mobile in google version, offset pan so pin isn't under card
b=open('build_gmap.py',encoding='utf-8').read()
b=b.replace('if(fromList&&ready){gmap.panTo({lat:p.lat,lng:p.lng}); if(gmap.getZoom()<15) gmap.setZoom(16);}','if(fromList&&ready){gmap.panTo({lat:p.lat,lng:p.lng}); if(gmap.getZoom()<15) gmap.setZoom(16); const ch=matchMedia("(max-width:760px)").matches?card.getBoundingClientRect().height:0; if(ch) setTimeout(()=>gmap.panBy(0,ch/2),50);}')
open('build_gmap.py','w',encoding='utf-8').write(b)
print('ok')
