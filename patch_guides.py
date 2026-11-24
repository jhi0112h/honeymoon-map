import json
# 1) itinerary 12/12 afternoon with Savoy
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/12': continue
    new=[]
    for s in D['stops']:
        k=s['k']
        if k=='nicholas': s['time']='14:15'
        if k=='aria': s['time']='14:35'
        if k=='lennon': s['time']='14:55'
        if k=='xm-kampa': s.update(time='15:10',note='캄파 크리스마스 마켓 구경 · 체르토프카 물레방아')
        if k=='charles':
            new.append({"time":"15:40","k":"savoy","note":"디저트 타임 · 사과 슈트루델+커피 (주말이라 예약 추천, 캄파에서 도보 8분)"})
            s.update(time='16:45',note='조명 켜진 카를교 건너기 · 성 쪽 야경 돌아보기')
        if k=='hotel' and s['time']=='16:30': s.update(time='17:15',note='숙소에서 쉬고 디너 준비')
        new.append(s)
    D['stops']=new
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)

# 2) Instagram post link for castle
ov=json.load(open('sources/overrides.json'))
json.dump(ov,open('sources/overrides.json','w'),ensure_ascii=False,indent=1)
ex=json.load(open('sources/social-extra.json'))
ex.setdefault('castle',[])
if not any('Df5tJ-_n5pB' in x['u'] for x in ex['castle']):
    ex['castle'].insert(0,{"t":"인스타그램: 겨울 프라하성 관람 팁 (mbtij.zip)","u":"https://www.instagram.com/p/Df5tJ-_n5pB/"})
json.dump(ex,open('sources/social-extra.json','w'),ensure_ascii=False,indent=1)

# 3) build: merge guides
b=open('build.py').read()
if "GUIDE=" not in b:
    b=b.replace("REV=L('reviews.json')","REV=L('reviews.json')\nGUIDE=L('guides.json')")
    b=b.replace("        if p['k'] in REV:\n","        if p['k'] in GUIDE: p['guide']=GUIDE[p['k']]\n        if p['k'] in REV:\n",1)
open('build.py','w').write(b)

# 4) script: render guide
s=open('script.js',encoding='utf-8').read()
if 'guideHtml' not in s:
    s=s.replace("const menuLine=","""function guideHtml(p){const g=p.guide; if(!g)return '';
  const sec=(lab,arr)=>arr&&arr.length?`<div class="gs"><b>${lab}</b><ul>${arr.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`:'';
  return `<details class="guide" open><summary>상세 가이드</summary>
    ${g.d?`<div class="gs"><b>소요 시간</b><p>${esc(g.d)}</p></div>`:''}
    ${sec('무료 · 유료 구분',g.fr)}${sec('티켓 · 예약 · 운영',g.tk)}${sec('추천 관람 순서',g.rt)}${sec('꼭 볼 것',g.see)}${sec('포토 스팟',g.ph)}${sec('주의 · 겨울 팁',g.wn)}
  </details>`;}
const menuLine=""",1)
    s=s.replace("${revHtml(p)}\n","${guideHtml(p)}\n    ${revHtml(p)}\n",1)
    s=s.replace('<div><div class="nm">${esc(p.n)}</div>','<div><div class="nm">${esc(p.n)}${p.guide?\'<span class="gb">가이드</span>\':\'\'}</div>',1)
open('script.js','w',encoding='utf-8').write(s)

t=open('template.html',encoding='utf-8').read()
if '.guide{' not in t:
    t=t.replace(".rev{border",""".guide{border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:12.5px}
.guide summary{font-weight:700;cursor:pointer;font-size:13px}
.guide .gs{margin-top:8px}.guide .gs b{font-size:12px;color:var(--sight)}
.guide ul{margin:3px 0 0;padding-left:18px;display:grid;gap:3px;line-height:1.5}.guide p{margin:3px 0 0}
.gb{font-size:10.5px;font-weight:700;color:var(--sight);border:1px solid currentColor;border-radius:4px;padding:0 4px;margin-left:6px;vertical-align:1px}
.rev{border""",1)
open('template.html','w',encoding='utf-8').write(t)
print('ok', s.count('guideHtml'), s.count('class="gb"'))
