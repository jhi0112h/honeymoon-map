import json
OPT={
 'itinerary.json':{
   '12/10':{('xm-old','20:20'),('novot','20:50')},
   '12/12':{('sbux',None),('xm-castle',None),('nicholas',None),('national',None),('heming',None)},
   '12/13':{('riegrovy',None),('xm-wen',None)}},
 'dresden-itinerary.json':{
   '12/11':{('dd-stallhof',None),('dd-hofkirche',None),('dd-kreutzkamm',None)}},
 'vienna-itinerary.json':{
   '12/13':{('v-xm-belv',None)},
   '12/14':{('v-karlskirche',None),('v-peterskirche',None),('v-amhof',None),('v-graben','20:15')},
   '12/15':{('v-hundertwasser',None)}},
 'budapest-itinerary.json':{
   '12/17':{('b-opera',None),('b-icerink',None)},
   '12/18':{('b-dohany',None)},
   '12/19':{('b-xm-basilica',None)}},
 'paris-itinerary.json':{
   '12/9':{('p-carette',None)}},
}
for f,days in OPT.items():
    it=json.load(open(f))
    n=0
    for D in it:
        rules=days.get(D['d'],set())
        for s in D['stops']:
            s.pop('opt',None)
            for k,t in rules:
                if s['k']==k and (t is None or s['time']==t):
                    s['opt']=True; n+=1
                    s['note']=s['note'].replace(' (선택)','').replace('(선택)','').replace(', 선택)',')')
    json.dump(it,open(f,'w'),ensure_ascii=False,indent=1)
    print(f,n)

s=open('script.js',encoding='utf-8').read()
old='it.innerHTML=`<span class="tm">${s.time}</span>'
if 'class="ob"' not in s:
    s=s.replace("const it=row(p); it.className='stop';","const it=row(p); it.className='stop'+(s.opt?' opt':'');",1)
    s=s.replace('<div><div class="nm">${esc(p.n)}${p.guide?\'<span class="gb">가이드</span>\':\'\'}</div>','<div><div class="nm">${esc(p.n)}${s.opt?\'<span class="ob">선택</span>\':\'\'}${p.guide?\'<span class="gb">가이드</span>\':\'\'}</div>',1)
    s=s.replace("<p>번호는 방문 순서, 지도 선은 직선 연결이에요. ${esc(C.planNote)}</p>","<p>번호는 방문 순서, 지도 선은 직선 연결이에요. <b>선택</b> 표시는 시간이 빠듯하면 빼도 되는 곳이에요. ${esc(C.planNote)}</p>",1)
open('script.js','w',encoding='utf-8').write(s)
print('badge', s.count('class="ob"'), s.count("' opt'"))
t=open('template.html',encoding='utf-8').read()
if '.ob{' not in t:
    t=t.replace('.gb{','.ob{font-size:10.5px;font-weight:700;color:var(--muted);border:1px dashed var(--muted);border-radius:4px;padding:0 4px;margin-left:6px;vertical-align:1px}\n.stop.opt .tm,.stop.opt .nm{opacity:.72}.stop.opt .no{opacity:.6}\n.gb{',1)
open('template.html','w',encoding='utf-8').write(t)
