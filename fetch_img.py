import re, time, json, urllib.request, urllib.parse, os, sys
FN=sys.argv[1] if len(sys.argv)>1 else 'places.json'
P=json.load(open(FN,encoding='utf-8'))
UA={'User-Agent':'honeymoon-map/1.0 (personal trip planner)'}
done={}
credits={}
for p in P:
    w=p.get('w')
    if not w: continue
    out=f"img/{p['k']}.jpg"
    if os.path.exists(out) and w not in done:
        p['img']=out; done[w]=out; continue
    if w in done:
        p['img']=done[w]; continue
    time.sleep(3)
    try:
        u='https://en.wikipedia.org/api/rest_v1/page/summary/'+urllib.parse.quote(w.replace(' ','_'))
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=20))
        src=(d.get('thumbnail') or {}).get('source')
        if not src: print('noimg',w); continue
        src=re.sub(r'/\d+px-','/500px-',src)
        data=urllib.request.urlopen(urllib.request.Request(src,headers=UA),timeout=30).read()
        open(out,'wb').write(data)
        p['img']=out; done[w]=out
        credits[p['k']]=d.get('content_urls',{}).get('desktop',{}).get('page','')
        print('ok',w,len(data))
    except Exception as e:
        print('ERR',w,e)
json.dump(P,open(FN,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
pass
