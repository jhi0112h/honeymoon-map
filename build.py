import json, csv, urllib.parse
from xml.sax.saxutils import escape
L=lambda f: json.load(open(f,encoding='utf-8'))
CITIES={
 'paris':dict(label='파리 12/5~9',name='파리',en='Paris',
   sub='12/5(토) 18:35 도착 ~ 12/9(수) 15:20 프라하행 · 시트 일정 그대로 반영 · 숙소 목시 발 데 유럽 → 하얏트 리젠시 에투알',
   planNote='시트에 적힌 일정 그대로예요. 시간이 비어 있는 항목은 시트에도 시간이 없는 곳이에요.',startDay=2,
   lat0=49.03,lng0=2.08,mx=73300,bounds=[49.03,2.08,48.78,2.82],core=[48.84,2.27,48.89,2.38],
   areas=["공항","발 데 유럽","서쪽 (에투알)","중심가","오페라","마레","북역·동역","시테섬","라탱 지구","몽마르트르","베르사유"],
   river=[[48.8150,2.4200],[48.8270,2.3920],[48.8380,2.3720],[48.8470,2.3600],[48.8530,2.3500],[48.8565,2.3420],[48.8590,2.3320],[48.8620,2.3180],[48.8635,2.3050],[48.8600,2.2930],[48.8540,2.2850],[48.8450,2.2750],[48.8360,2.2620],[48.8350,2.2450],[48.8450,2.2250],[48.8650,2.2280],[48.8850,2.2550],[48.9050,2.2700],[48.9250,2.2650]],riverW=160,
   channels=[],bridges=[],
   parks=[[48.8620,2.2490,1300,2100,0],[48.8635,2.3270,450,140,-10],[48.8040,2.1080,1900,900,0],[48.8722,2.7758,700,500,0]],
   blocks=[],
   areaPos={"파리 시내":[48.8790,2.3480],"디즈니 · 발 데 유럽":[48.8640,2.7750],"베르사유":[48.7930,2.1250],"샤를 드골 공항":[49.0200,2.5480]},
   riverLabel=[48.8575,2.3000,-15,'센강 Seine'],
   places=L('paris.json'),plan=L('paris-itinerary.json'),kml='paris-places.kml',csv='paris-places.csv'),
 'prague':dict(label='프라하 12/9~13',name='프라하',en='Prague',
   sub='12/9(수) 저녁 도착 ~ 12/13(일) 12:36 빈행 기차 · 숙소 마에스트로 바이 아드레즈',
   planNote='12월 일몰 15:58 기준으로 짰어요.',startDay=1,
   lat0=50.101,lng0=14.380,mx=71700,bounds=[50.101,14.380,50.058,14.460],core=[50.078,14.38,50.1,14.436],
   areas=["신시가","구시가","카를교","유대인지구","말라스트라나","흐라드차니","레트나","비셰흐라드","비노흐라디","지슈코프"],
   river=[[50.0580,14.4180],[50.0620,14.4160],[50.0645,14.4150],[50.0705,14.4120],[50.0755,14.4120],[50.0812,14.4105],[50.0840,14.4108],[50.0865,14.4115],[50.0883,14.4128],[50.0900,14.4140],[50.0918,14.4162],[50.0932,14.4205],[50.0942,14.4270],[50.0952,14.4330],[50.0972,14.4385],[50.1000,14.4430],[50.1040,14.4450]],riverW=170,
   channels=[[[50.0876,14.4096],[50.0862,14.4088],[50.0846,14.4090]]],
   bridges=[[[50.08648,14.4090],[50.08630,14.4136]],[[50.0897,14.4122],[50.0890,14.4152]],[[50.0811,14.4092],[50.0812,14.4120]],[[50.0757,14.4105],[50.0756,14.4136]],[[50.0926,14.4170],[50.0912,14.4180]]],
   parks=[[50.0828,14.3965,420,850,8],[50.0960,14.4190,900,260,-4],[50.0645,14.4195,260,210,0],[50.0790,14.4432,230,170,0],[50.0900,14.4020,300,120,0]],
   blocks=[[50.0915,14.3960,50.0898,14.4045]],
   areaPos={"흐라드차니":[50.0935,14.3945],"말라스트라나":[50.0848,14.4035],"구시가":[50.0858,14.4245],"유대인지구":[50.0912,14.4215],"신시가":[50.0772,14.4225],"레트나":[50.0985,14.4185],"비셰흐라드":[50.0622,14.4220],"비노흐라디":[50.0760,14.4440],"지슈코프":[50.0840,14.4500]},
   riverLabel=[50.0730,14.4110,-80,'블타바 강 Vltava'],
   places=L('places.json'),plan=L('itinerary.json'),kml='prague-places.kml',csv='prague-places.csv'),
 'dresden':dict(label='드레스덴 12/11',name='드레스덴',en='Dresden',
   sub='12/11(금) 당일치기 · 12:55 도착 → 19:50 플릭스버스로 프라하 복귀 (21:40 도착)',
   planNote='12월 일몰 15:55 기준, 머무는 시간 약 6시간 반.',startDay=0,
   lat0=51.072,lng0=13.715,mx=70060,bounds=[51.072,13.715,51.035,13.775],core=[51.044,13.725,51.062,13.752],
   areas=["중앙역","알트슈타트","노이슈타트"],
   river=[[51.0700,13.7950],[51.0660,13.7850],[51.0640,13.7760],[51.0600,13.7660],[51.0565,13.7575],[51.0550,13.7470],[51.0553,13.7405],[51.0567,13.7340],[51.0589,13.7290],[51.0620,13.7220],[51.0660,13.7150],[51.0690,13.7080]],riverW=130,
   channels=[],
   bridges=[[[51.0540,13.7400],[51.0567,13.7408]],[[51.0537,13.7465],[51.0562,13.7475]],[[51.0577,13.7280],[51.0601,13.7300]],[[51.0553,13.7568],[51.0578,13.7582]]],
   parks=[[51.0380,13.7640,950,420,-10],[51.0605,13.7500,260,90,-20]],
   blocks=[[51.0537,13.7322,51.0524,13.7350],[51.0530,13.7355,51.0518,13.7380]],
   areaPos={"알트슈타트":[51.0470,13.7330],"노이슈타트":[51.0630,13.7470],"중앙역":[51.0385,13.7270]},
   riverLabel=[51.0583,13.7618,-33,'엘베 강 Elbe'],
   places=L('dresden.json'),plan=L('dresden-itinerary.json'),kml='dresden-places.kml',csv='dresden-places.csv'),
 'vienna':dict(label='빈 12/13~16',name='비엔나',en='Vienna',
   sub='12/13(일) 16:19 프라하발 기차 도착 ~ 12/16(수) 10:00 부다페스트행 · 숙소 아디나 아파트먼트 호텔 비엔나 벨베데레',
   planNote='12월 일몰 약 16:00 기준. 시트의 12/15 쇤브룬·카페 자허 일정을 반영했어요.',startDay=0,
   lat0=48.222,lng0=16.300,mx=73400,bounds=[48.222,16.300,48.172,16.405],core=[48.195,16.355,48.215,16.385],
   areas=["중앙역·벨베데레","카를스플라츠","마리아힐퍼 거리","링 도로","구시가 (슈테판플라츠)","구시가 (호프부르크)","란트슈트라세","쇤브룬","바덴 (빈 근교)"],
   river=[[48.2450,16.3700],[48.2300,16.3780],[48.2200,16.3850],[48.2120,16.3920],[48.2060,16.4000],[48.2000,16.4100],[48.1950,16.4200]],riverW=70,
   channels=[],bridges=[],
   parks=[[48.1800,16.3100,700,500,0],[48.1925,16.3810,180,450,0],[48.2160,16.4000,500,700,-20],[48.2065,16.3640,160,180,0],[48.2045,16.3780,180,230,0]],
   blocks=[[48.2088,16.3640,48.2050,16.3700]],
   areaPos={"구시가":[48.2125,16.3720],"벨베데레":[48.1955,16.3850],"쇤브룬":[48.1890,16.3060],"중앙역":[48.1820,16.3720]},
   riverLabel=[48.2230,16.3820,-40,'도나우 운하'],
   places=L('vienna.json'),plan=L('vienna-itinerary.json'),kml='vienna-places.kml',csv='vienna-places.csv'),
 'budapest':dict(label='부다페스트 12/16~19',name='부다페스트',en='Budapest',
   sub='12/16(수) 빈발 기차 도착 ~ 12/19(토) 19:30 출국 (12/20 14:10 인천) · 숙소 노보텔 부다페스트 다누베',
   planNote='12월 일몰 약 15:55 기준. 시트의 대성당 크리스마스 마켓과 마지막 쇼핑을 반영했어요.',startDay=0,
   lat0=47.530,lng0=19.020,mx=75200,bounds=[47.530,19.020,47.430,19.260],core=[47.484,19.028,47.520,19.090],
   areas=["부다 강변","부다 성 지구","부다 남쪽","도나우 강","페스트 강변","페스트 중심","언드라시 거리","유대인 지구","페스트 남쪽","페스트 동쪽","시민공원","공항"],
   river=[[47.5400,19.0450],[47.5250,19.0480],[47.5150,19.0470],[47.5080,19.0440],[47.5020,19.0430],[47.4960,19.0445],[47.4900,19.0500],[47.4850,19.0560],[47.4780,19.0640],[47.4680,19.0700],[47.4550,19.0750]],riverW=330,
   channels=[],
   bridges=[[[47.4990,19.0400],[47.4990,19.0475]],[[47.4860,19.0520],[47.4858,19.0595]],[[47.5130,19.0430],[47.5130,19.0510]]],
   parks=[[47.5160,19.0810,700,500,0],[47.4870,19.0450,500,400,0],[47.5250,19.0500,250,900,0]],
   blocks=[[47.5030,19.0320,47.4950,19.0410]],
   areaPos={"부다":[47.5000,19.0280],"페스트":[47.5030,19.0620],"시민공원":[47.5200,19.0860],"공항":[47.4400,19.2400]},
   riverLabel=[47.5190,19.0470,-80,'도나우 강 Duna'],
   places=L('budapest.json'),plan=L('budapest-itinerary.json'),kml='budapest-places.kml',csv='budapest-places.csv'),
}
import glob
SRC={}
for f in glob.glob('sources/links-*.json'): SRC.update(L(f))
OV=L('sources/overrides.json')
SOC={}
for f in glob.glob('sources/social-*.json'): SOC.update(L(f))
MENU=L('menus.json')
for f in glob.glob('sources/menus-*.json'): MENU.update(L(f))
REV=L('reviews.json')
REV.update(L('reviews2.json'))
GUIDE=L('guides.json')
for f in glob.glob('sources/guides-*.json'): GUIDE.update(L(f))
for c in CITIES.values():
    for p in c['places']:
        s=SRC.get(p['k'],{}); o=OV.get(p['k'],{})
        links=(p.get('links') or [])+[dict(x) for x in s.get('links',[]) if not any(x['u']==y['u'] for y in (p.get('links') or []))]
        for x in links: x['u']=x['u'].replace('wikipedia.com/','wikipedia.org/')
        for x in links: x['t']=o.get('relabel',{}).get(x['t'],x['t'])
        if p.get('w') and not any('wikipedia.org' in x['u'] for x in links):
            links.append({'t':'위키백과','u':'https://en.wikipedia.org/wiki/'+urllib.parse.quote(p['w'].replace(' ','_'))})
        for x in SOC.get(p['k'],[]):
            if x.get('u') and not any(x['u']==y['u'] for y in links): links.append(dict(x))
        p['links']=links
        if p['k'] in MENU: p['menu']=MENU[p['k']]
        if p['k'] in GUIDE: p['guide']=GUIDE[p['k']]
        if p['k'] in REV:
            p['rev']=REV[p['k']]
            if not any('tripadvisor' in x['u'] for x in p['links']): p['links'].append({'t':'트립어드바이저 리뷰','u':REV[p['k']]['u']})
        n=o.get('note',s.get('note',''))
        if n: p['note']=n
CAT = {'hotel':('숙소·역','ff1c8ad9'),'xmas':('크리스마스 마켓','ff5a8316'),'sight':('명소','ffc8552f'),'food':('식당','ff2e3fc6'),'cafe':('카페','ff2b5a8a'),'night':('야경·바','ffa83a7a')}
html=open('template.html',encoding='utf-8').read().replace('__SCRIPT__',open('script.js',encoding='utf-8').read())
html=html.replace('__RES__',open('reservations.json',encoding='utf-8').read()).replace('__DISNEY__',open('disney.json',encoding='utf-8').read()).replace('__CITIES__',json.dumps({k:{kk:vv for kk,vv in v.items() if kk not in('kml','csv')} for k,v in CITIES.items()},ensure_ascii=False))
open('prague-map.html','w',encoding='utf-8').write(html)
for key,c in CITIES.items():
    P=c['places']; gm=lambda p: 'https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote(p['en']+' '+c['en'])
    with open(c['csv'],'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['이름','영문명','분류','식사','구역','위도','경도','메모','팁','추천 메뉴','트립어드바이저 평점','맛','분위기','서비스','가성비','리뷰 요약','출처 메모','참조 링크','구글지도'])
        for p in P: w.writerow([p['n'],p['en'],CAT[p['c']][0],p.get('m',''),p['a'],p['lat'],p['lng'],p['t'],p.get('tip',''),' / '.join(p.get('menu',[])),*( [p['rev'].get('r'),p['rev'].get('F'),p['rev'].get('A'),p['rev'].get('S'),p['rev'].get('V'),p['rev'].get('ko','')] if p.get('rev') else ['']*6 ),p.get('note',''),' | '.join(x['u'] for x in p['links']),gm(p)])
    k=['<?xml version="1.0" encoding="UTF-8"?>',f'<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>{c["name"]} 허니문</name>']
    for ct,(lab,col) in CAT.items(): k.append(f'<Style id="{ct}"><IconStyle><color>{col}</color><Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon></IconStyle></Style>')
    for ct,(lab,col) in CAT.items():
        items=[p for p in P if p['c']==ct]
        if not items: continue
        k.append(f'<Folder><name>{lab}</name>')
        for p in items:
            desc=escape(f"{p['en']} · {p['a']}"+(f" · {p['m']}" if p.get('m') else '')+f"\n{p['t']}\n팁: {p.get('tip','')}\n{gm(p)}")
            k.append(f'<Placemark><name>{escape(p["n"])}</name><description>{desc}</description><styleUrl>#{ct}</styleUrl><Point><coordinates>{p["lng"]},{p["lat"]},0</coordinates></Point></Placemark>')
        k.append('</Folder>')
    BY={p['k']:p for p in P}
    for D in c['plan']:
        col=D['color'].lstrip('#'); kcol='ff'+col[4:6]+col[2:4]+col[0:2]; sid='r'+D['d'].replace('/','')
        k.append(f'<Folder><name>{D["d"]} {D["title"]}</name><Style id="{sid}"><LineStyle><color>{kcol}</color><width>4</width></LineStyle></Style>')
        coords=' '.join(f'{BY[s["k"]]["lng"]},{BY[s["k"]]["lat"]},0' for s in D['stops'])
        k.append(f'<Placemark><name>{D["d"]} 동선</name><styleUrl>#{sid}</styleUrl><LineString><coordinates>{coords}</coordinates></LineString></Placemark>')
        for i,s in enumerate(D['stops'],1):
            p=BY[s['k']]
            k.append(f'<Placemark><name>{D["d"]}-{i} {s["time"]} {escape(p["n"])}</name><description>{escape(s["note"])}</description><Point><coordinates>{p["lng"]},{p["lat"]},0</coordinates></Point></Placemark>')
        k.append('</Folder>')
    k.append('</Document></kml>')
    open(c['kml'],'w',encoding='utf-8').write('\n'.join(k))
    print(key,len(P),'places')

# ---- standalone Google Maps version ----
import subprocess
subprocess.run(['python3','build_gmap.py'],check=True)
cities_json=json.dumps({k:{kk:vv for kk,vv in v.items() if kk not in('kml','csv')} for k,v in CITIES.items()},ensure_ascii=False)
g=open('gmap-template.html',encoding='utf-8').read().replace('__GMAP__',open('gmap.js',encoding='utf-8').read()).replace('__CITIES__',cities_json).replace('__RES__',open('reservations.json',encoding='utf-8').read()).replace('__DISNEY__',open('disney.json',encoding='utf-8').read())
g='<!doctype html>\n<html lang="ko">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>:root{padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}body{margin:0;font-size:14px}[hidden]{display:none!important}img{max-width:100%}</style>\n'+g
open('honeymoon-map.html','w',encoding='utf-8').write(g)
print('standalone ok')
