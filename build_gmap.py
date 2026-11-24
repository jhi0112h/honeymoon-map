import re, json
src=open('script.js',encoding='utf-8').read().split('\n')
def seg(start_pat, end_pat):
    s=next(i for i,l in enumerate(src) if l.startswith(start_pat))
    e=next(i for i,l in enumerate(src) if i>s and l.startswith(end_pat))
    return '\n'.join(src[s:e])
helpers=seg('// links & card','function select(')
sel=seg('function select(','function markList(')
sel=re.sub(r"if\(fromList\)\{.*?\}\n", "if(fromList&&ready){gmap.panTo({lat:p.lat,lng:p.lng}); if(gmap.getZoom()<15) gmap.setZoom(16); const ch=matchMedia('(max-width:760px)').matches?card.getBoundingClientRect().height:0; if(ch) setTimeout(()=>gmap.panBy(0,ch/2),50);}\n", sel, flags=re.S)
lists=seg('function markList(','// controls')
controls='\n'.join(src[next(i for i,l in enumerate(src) if l.startswith('// controls')):])
controls=controls.replace("new ResizeObserver(()=>render()).observe(svg);","")
controls=controls.replace("function setCity(key){","function setCity(key){\n  window.curCity=key; clearWalk();")
controls=controls.replace("setCity(startCity);","setCity(startCity);\nloadMaps();")
core=open('gmap_core.js',encoding='utf-8').read().replace("setCity(startCity);\n};","setCity(window.curCity||startCity);\n};")
js=core+'\n'+helpers+'\n'+sel+'\n'+lists+'\n'+controls
open('gmap.js','w',encoding='utf-8').write(js)

t=open('template.html',encoding='utf-8').read()
t=t.replace('<title>프라하·드레스덴 허니문 지도</title>','<title>허니문 구글 지도</title>')
t=re.sub(r'<svg id="map"[^>]*></svg>','<div id="gmap"></div>',t)
t=re.sub(r'<div class="legend">.*?</div>','',t,flags=re.S)
t=t.replace('<button id="zin" aria-label="확대">+</button>\n      <button id="zout" aria-label="축소">−</button>\n','')
t=t.replace('<button id="zall" class="wide" aria-label="전체 보기">전체</button>','<button id="zall" class="wide" aria-label="전체 보기">전체</button>\n      <button id="walkBtn" class="wide" aria-pressed="false" aria-label="실제 도보 경로">도보<br>경로</button>')
t=t.replace('<div class="card" id="card" hidden></div>','''<div class="card" id="card" hidden></div>
    <div class="notice" id="notice" hidden></div>
    <div class="setup" id="setup" hidden>
      <h2>구글 지도 API 키 입력</h2>
      <p id="setupMsg">이 페이지는 구글 지도 JavaScript API로 실제 지도를 보여줘요. 본인 구글 클라우드 계정의 API 키를 한 번만 입력하면 이 브라우저에 저장돼요 (파일에는 저장되지 않음).</p>
      <ol>
        <li>console.cloud.google.com 에서 프로젝트 만들기 → 결제 계정 연결</li>
        <li>'Maps JavaScript API'와 (도보 경로용) 'Directions API' 사용 설정</li>
        <li>사용자 인증 정보 → API 키 만들기 → 웹사이트 제한에 <code>http://localhost:8000/*</code> 추가</li>
        <li>터미널에서 <code>cd ~/honeymoon-prague && python3 -m http.server 8000</code> 실행 후 <code>http://localhost:8000/honeymoon-map.html</code> 접속</li>
      </ol>
      <div class="keyrow"><input id="keyInput" type="password" placeholder="API 키 붙여넣기" autocomplete="off"><button id="keySave">저장하고 지도 열기</button></div>
      <button id="keyReset" class="link">저장된 키 지우기</button>
    </div>''')
t=t.replace('.mapwrap{','#gmap{width:100%;height:100%}\n.setup{position:absolute;inset:0;background:var(--surface);padding:28px max(20px,env(safe-area-inset-left,0px));overflow:auto;display:grid;align-content:start;gap:12px;max-width:640px}\n.setup h2{margin:0;font-family:var(--font-display)}.setup p,.setup li{line-height:1.6;color:var(--muted)}.setup code{background:var(--bg);padding:1px 5px;border-radius:4px;color:var(--fg)}\n.keyrow{display:flex;gap:8px;flex-wrap:wrap}.keyrow input{flex:1;min-width:200px;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);font:inherit}\n.keyrow button,.link{padding:9px 14px;border-radius:8px;border:0;background:var(--fg);color:var(--surface);font:inherit;font-weight:700;cursor:pointer}.link{background:none;color:var(--muted);text-decoration:underline;font-weight:400;justify-self:start;padding:0}\n.notice{position:absolute;left:50%;transform:translateX(-50%);top:12px;background:var(--fg);color:var(--surface);padding:8px 14px;border-radius:8px;font-size:13px;z-index:5}\n.ctl button[aria-pressed="true"]{background:var(--fg);color:var(--surface)}\n.ctl{top:auto!important;bottom:calc(110px + env(safe-area-inset-bottom,0px))}\n.mapwrap{',1)
t=t.replace('__SCRIPT__','<script>\n__GMAP__\n</script>') if '<script>\n__SCRIPT__' not in t else t.replace('__SCRIPT__','__GMAP__')
open('gmap-template.html','w',encoding='utf-8').write(t)
print('ok', len(js))
