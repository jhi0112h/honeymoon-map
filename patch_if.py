import json
P=json.load(open('places.json'))
if 'ifcafe' not in [p['k'] for p in P]:
    i=[p['k'] for p in P].index('imperial')
    P.insert(i+1,{"k":"ifcafe","n":"IF 카페 (틸로보 광장점)","en":"IF Cafe Tylovo namesti Prague","c":"cafe","a":"비노흐라디","lat":50.0741,"lng":14.4322,"t":"프렌치 파티스리 디저트 카페 · 매일 8~20시 · 숙소에서 도보 8분","tip":"파티시에 이베타 파베쇼바의 디저트 카페. 지점이 여러 곳(캄파 섬 베리흐 빌라, 마사리치카역, 융만노바 등)인데 출발일 아침 동선엔 숙소와 가까운 틸로보 광장점이 맞음. 브런치 메뉴도 있음","links":[{"t":"카페 정보 (In Your Pocket)","u":"https://www.inyourpocket.com/czech-republic/prague/venues/if-cafe"},{"t":"프라하 관광청 (베리흐 빌라점)","u":"https://prague.eu/en/objevujte/iveta-fabesova-cafe-werich-villa/"},{"t":"프라하 관광청 (마사리치카점)","u":"https://prague.eu/en/objevujte/iveta-fabesova-cafe-masarycka/"}]})
json.dump(P,open('places.json','w'),ensure_ascii=False,indent=0)
M=json.load(open('menus.json')); M['ifcafe']=["에클레어·타르트 등 프렌치 디저트","브런치 플레이트","홈메이드 아이스크림"]; json.dump(M,open('menus.json','w'),ensure_ascii=False,indent=0)
G=json.load(open('guides.json'))
G['riegrovy']={"d":"20~30분","tk":["무료"],"fr":["무료"],"rt":["IF 카페 → 비노흐라드스카 거리 → 공원 윗길 전망 잔디밭 → 공원 북서쪽 출구로 시내 방향"],"see":["언덕 위에서 보는 프라하 성·구시가 첨탑 스카이라인 (성이 정면으로 멀리 보임)","현지인이 산책하는 동네 공원 분위기"],"ph":["전망 잔디밭 난간 쪽에서 프라하 성 방향 (아침엔 순광이라 선명)"],"wn":["유명한 비어가든은 겨울 휴업","원래 일몰 명소지만 이번 일정엔 아침 산책으로 넣음"]}
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']=='12/10' and not any(s['k']=='nase' for s in D['stops']):
        new=[]
        for s in D['stops']:
            if s['k']=='lokal':
                new.append({"time":"18:15","k":"nase","note":"미트로프나 버거 1개를 둘이 나눠 먹기 (정육점 식당, 로칼에서 도보 1분)"})
                s.update(time='19:00',note='맥주펍 · 탱크 필스너 + 가벼운 안주 (예약 추천)')
            new.append(s)
        D['stops']=new
    if D['d']=='12/13':
        D['stops']=[
         {"time":"08:30","k":"ifcafe","note":"아침 겸 디저트 (숙소에서 도보 8분)"},
         {"time":"09:20","k":"riegrovy","note":"아침 공원 산책 · 언덕에서 프라하 성 스카이라인 (카페에서 도보 12분)"},
         {"time":"10:15","k":"mucha","note":"무하 박물관 · 50분 (공원에서 도보 약 25분 또는 트램)"},
         {"time":"11:10","k":"xm-wen","note":"마지막 마켓 산책·기념품 (도보 3분)"},
         {"time":"11:30","k":"hotel","note":"체크아웃 → 중앙역 도보 10분, 12:36 기차"}]
        D['title']='IF 카페 · 리에그로비 사디 · 무하 박물관 → 빈'
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('ok')
