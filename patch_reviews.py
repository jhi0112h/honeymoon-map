b=open('build.py').read()
b=b.replace("MENU=L('menus.json')","MENU=L('menus.json')\nREV=L('reviews.json')")
b=b.replace("        if p['k'] in MENU: p['menu']=MENU[p['k']]\n","        if p['k'] in MENU: p['menu']=MENU[p['k']]\n        if p['k'] in REV:\n            p['rev']=REV[p['k']]\n            if not any('tripadvisor' in x['u'] for x in p['links']): p['links'].append({'t':'트립어드바이저 리뷰','u':REV[p['k']]['u']})\n")
b=b.replace("'추천 메뉴','출처 메모'","'추천 메뉴','트립어드바이저 평점','맛','분위기','서비스','가성비','리뷰 요약','출처 메모'")
b=b.replace("' / '.join(p.get('menu',[])),","' / '.join(p.get('menu',[])),*( [p['rev'].get('r'),p['rev'].get('F'),p['rev'].get('A'),p['rev'].get('S'),p['rev'].get('V'),p['rev'].get('ko','')] if p.get('rev') else ['']*6 ),")
open('build.py','w').write(b)

s=open('script.js',encoding='utf-8').read()
s=s.replace("const menuLine=","""const PRICE={'$':'€ 저렴','$$ - $$$':'€€ 보통','$$$$':'€€€ 고급'};
function revHtml(p){const v=p.rev; if(!v)return '';
  const row=(lab,x)=>x==null?'':`<div class="sr"><span>${lab}</span><span class="bar"><i style="width:${(x/5*100).toFixed(0)}%"></i></span><b>${x.toFixed(1)}</b></div>`;
  return `<div class="rev"><div class="rh"><b>리뷰 점수</b><span>★ ${v.r.toFixed(1)} · 리뷰 ${v.c.toLocaleString()}개${v.p?' · '+(PRICE[v.p]||v.p):''}</span></div>
    ${row('맛',v.F)}${row('분위기',v.A)}${row('서비스',v.S)}${row('가성비',v.V)}
    ${v.ko?`<p class="rs">${esc(v.ko)}</p>`:''}<div class="credit">트립어드바이저 세부 평점 · 요약은 트립어드바이저 AI 리뷰 요약을 한국어로 정리</div></div>`;}
const revLine=p=>p.rev?`<div class="rl">★${p.rev.r.toFixed(1)} (${p.rev.c.toLocaleString()}) · 맛 ${p.rev.F??'-'} · 분위기 ${p.rev.A??'-'} · 서비스 ${p.rev.S??'-'} · 가성비 ${p.rev.V??'-'}</div>`:'';
const menuLine=""",1)
s=s.replace("${menuHtml(p)}\n","${revHtml(p)}\n    ${menuHtml(p)}\n",1)
s=s.replace("${menuLine(p)}</div></div>${thumb(p)}","${menuLine(p)}${revLine(p)}</div></div>${thumb(p)}")
s=s.replace('<div class="tp">${esc(p.t)}${menuLine(p)}</div>','<div class="tp">${esc(p.t)}${menuLine(p)}${revLine(p)}</div>')
open('script.js','w',encoding='utf-8').write(s)

t=open('template.html',encoding='utf-8').read()
t=t.replace(".menu{border",""".rev{border:1px solid var(--line);border-radius:6px;padding:8px 10px;display:grid;gap:5px}
.rev .rh{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;font-size:12px}.rev .rh span{color:var(--muted)}
.sr{display:grid;grid-template-columns:44px 1fr 28px;gap:8px;align-items:center;font-size:12px}
.sr .bar{height:6px;border-radius:3px;background:var(--bg);overflow:hidden}.sr .bar i{display:block;height:100%;background:var(--food)}
.sr b{font-variant-numeric:tabular-nums;text-align:right}
.rev .rs{font-size:12.5px;line-height:1.5;margin:2px 0 0}
.rl{font-size:11.5px;color:var(--muted);margin-top:2px;font-variant-numeric:tabular-nums}
.menu{border""",1)
open('template.html','w',encoding='utf-8').write(t)
print(s.count('revLine(p)'), s.count('revHtml(p)}'))
