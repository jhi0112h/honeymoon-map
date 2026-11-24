import json,shutil,glob,os
T='/Users/johyeon-il/.claude/jobs/cb006fdf/tmp'
for f in glob.glob(T+'/guides-*.json')+glob.glob(T+'/menus-*.json')+glob.glob(T+'/links-vienna.json')+glob.glob(T+'/links-budapest.json')+glob.glob(T+'/links-paris.json'):
    shutil.copy(f,'sources/')
# Budapest fixes
B=json.load(open('budapest.json'))
for p in B:
    if p['k']=='b-ruszwurm': p['t']='⚠ 2025년 8월 폐업 (재개장 소식 없음)'; p['tip']='임대 분쟁으로 2025년 8월 문을 닫음. 동선에서 제외'
    if p['k']=='b-hotel': p['t']='숙소 12/16~12/19 · Bem rakpart 33-34 · 체크인 15:00 / 체크아웃 12:00'
    if p['k']=='b-dohany': p['tip']='겨울 금요일 10:00~14:00, 일~목 10:00~16:00, 토요일 휴관. 남성은 키파 착용'
json.dump(B,open('budapest.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('budapest-itinerary.json'))
def S(t,k,n): return {"time":t,"k":k,"note":n}
for D in it:
    if D['d']=='12/16':
        D['stops']=[s for s in D['stops'] if s['k']!='b-ruszwurm']
        for s in D['stops']:
            if s['k']=='b-fisherman': s['note']='일몰 15:55 · 국회의사당 뷰 (아래층 테라스 무료, 위층은 19시 이후 무료)'
            if s['k']=='b-castle': s['time']='16:30'
    if D['d']=='12/17':
        D['stops']=[
         S('09:00','b-parliament','국회의사당 가이드 투어 약 45분 (jegymester.hu 예약, 15분 전 도착)'),
         S('10:15','b-shoes','도나우 강변의 신발'),
         S('10:45','b-basilica','성당 + 돔 전망대'),
         S('12:00','b-opera','언드라시 거리 · 오페라극장 외관'),
         S('12:30','b-menza','점심 · 레트로 헝가리 식당'),
         S('14:00','b-heroes','지하철 M1 · 영웅 광장'),
         S('14:15','b-szechenyi','야외 온천 2시간 30분 · 김 서린 겨울 야외탕'),
         S('17:00','b-icerink','저녁 세션 스케이트 (평일은 오전·저녁 세션만, 선택)'),
         S('18:45','b-getto','저녁 · 굴라시·파프리카시 (예약 추천)'),
         S('20:15','b-xm-basilica','대성당 마켓 · 외벽 프로젝션 쇼 (시트)'),
         S('21:15','b-hotel','')]
    if D['d']=='12/18':
        D['stops']=[
         S('09:00','b-central','2층 랑고시 아침 · 파프리카 기념품'),
         S('10:15','b-dohany','금요일은 14시에 닫아서 오전에 (트램+도보 15분)'),
         S('11:30','b-newyork','커피·디저트만 추천 (음식은 비싸고 평범하다는 평)'),
         S('12:45','b-forsale','점심 · 양 많으니 2인 1~2메뉴'),
         S('14:15','b-liberty','자유의 다리 건너기'),
         S('14:30','b-gellert','시타델라에서 일몰 15:55 · 다리들 야경 (추우면 택시로 올라가기)'),
         S('16:45','b-vorosmarty','마지막 쇼핑 · 마켓과 바치 거리 (시트: 마지막 쇼핑)'),
         S('18:30','b-borkonyha','허니문 디너 · 미쉐린 와인 키친 (몇 주 전 예약)'),
         S('20:30','b-cruise','도나우 강 야경 크루즈 1시간'),
         S('21:45','b-hotel','')]
    if D['d']=='12/19':
        for s in D['stops']:
            if s['k']=='b-gerbeaud': s['time']='09:30'; s['note']='아침 · 케이크 (분위기 위주, 가격은 높은 편)'
            if s['k']=='b-hotel': s['note']='짐 찾기 (체크아웃 12:00이라 아침에 체크아웃하고 짐 맡기기)'
        if D['stops'][0]['k']!='b-hotel':
            D['stops'].insert(0,S('09:00','b-hotel','체크아웃 후 짐 맡기기 (체크아웃 12:00)'))
json.dump(it,open('budapest-itinerary.json','w'),ensure_ascii=False,indent=1)
# build loader changes
b=open('build.py').read()
if 'guides-*.json' not in b:
    b=b.replace("GUIDE=L('guides.json')","GUIDE=L('guides.json')\nfor f in glob.glob('sources/guides-*.json'): GUIDE.update(L(f))")
    b=b.replace("MENU=L('menus.json')","MENU=L('menus.json')\nfor f in glob.glob('sources/menus-*.json'): MENU.update(L(f))")
    b=b.replace("REV=L('reviews.json')","REV=L('reviews.json')\nREV.update(L('reviews2.json'))")
    b=b.replace("        links=p.get('links') or [dict(x) for x in s.get('links',[])]","        links=(p.get('links') or [])+[dict(x) for x in s.get('links',[]) if not any(x['u']==y['u'] for y in (p.get('links') or []))]\n        for x in links: x['u']=x['u'].replace('wikipedia.com/','wikipedia.org/')")
open('build.py','w').write(b)
# city configs for vienna/budapest
if "'vienna':" not in b:
    add = """ 'vienna':dict(label='빈 12/13~16',name='비엔나',en='Vienna',
   sub='12/13(일) 16:19 프라하발 기차 도착 ~ 12/16(수) 10:00 부다페스트행 · 숙소 아디나 아파트먼트 호텔 비엔나 벨베데레',
   planNote='12월 일몰 약 16:00 기준. 시트의 12/15 쇤브룬·카페 자허 일정을 반영했어요.',startDay=0,
   lat0=48.222,lng0=16.300,mx=73400,bounds=[48.222,16.300,48.172,16.405],core=[48.195,16.355,48.215,16.385],
   areas=["중앙역·벨베데레","카를스플라츠","링 도로","구시가 (슈테판플라츠)","구시가 (호프부르크)","란트슈트라세","쇤브룬"],
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
CAT ="""
    b=b.replace("}\nimport glob",add.replace("}\nCAT =","}\nimport glob"),1)
open('build.py','w').write(b)
print('ok', "'vienna':" in b, 'guides-*' in b)
