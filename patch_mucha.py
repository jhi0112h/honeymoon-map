import json
P=json.load(open('places.json'))
for p in P:
    if p['k']=='mucha':
        p.update(n='무하 박물관 (사바린 궁전)',en='Mucha Museum Savarin Palace',lat=50.0848,lng=14.4252,
          t='2025년 개관한 무하 재단 미술관 · 나 프르지코페 10 · 매일 10~18시',
          tip='프라하 무하 박물관은 두 곳. 이곳(사바린 궁전)이 2025년에 새로 연 더 큰 전시관이고, 1998년부터 있던 판스카 거리 원조관은 도보 3분 거리. 숙소에서 도보 8분',
          links=[{"t":"공식 사이트 (무하 재단 미술관)","u":"https://www.mucha.eu/en"},{"t":"프라하 관광청 (사바린 궁전 무하 미술관)","u":"https://prague.eu/en/objevujte/museum-of-alphonse-mucha-in-the-savarin-palace/"},{"t":"기사 (Expats.cz, 개관 소식)","u":"https://www.expats.cz/czech-news/article/mucha-museum-opens-in-renovated-savarin-palace-in-prague"},{"t":"판스카 거리 원조관 공식 사이트","u":"https://www.mucha.cz/en"}])
        p.pop('img',None); p['w']='Mucha Museum (Savarin Palace)'
json.dump(P,open('places.json','w'),ensure_ascii=False,indent=0)
G=json.load(open('guides.json'))
G['mucha']={"d":"1시간","tk":["매일 10:00~18:00 (일부 날짜 단축 운영)","현장 또는 공식 사이트 구매, 성인 약 300코루나 (출처마다 다름)"],"fr":["유료"],"rt":["10시 오픈 입장 → 상설전 'Art Nouveau & Utopia' → 기념품숍 → 바츨라프 광장 방향"],"see":["무하의 아르누보 포스터 원화 (사라 베르나르 연극 포스터 등)","궁전 리노베이션 공간 자체"],"ph":["전시실 내부 촬영 규정은 현장 안내 따르기","궁전 안뜰"],"wn":["출발일 오전이라 11:05엔 나와야 체크아웃(11:30)에 맞음","판스카 거리 원조관과 헷갈리지 않게 주소 확인 (Na Příkopě 10)"]}
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/13': continue
    for s in D['stops']:
        if s['k']=='museum': s.update(k='mucha',time='10:00',note='10시 오픈 직후 입장 · 1시간 (카페 임페리얼에서 도보 10분)')
        if s['k']=='xm-wen': s.update(time='11:05',note='마지막 마켓 산책·기념품 (무하 박물관에서 도보 3분)')
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('ok')
G=json.load(open('guides.json'))
G['dancing']={"d":"외관 15분 / 루프탑 바 +30분","tk":["외관 무료","꼭대기 글래스 바(테라스)는 음료 주문 시 입장, 전망대만 따로 유료 입장도 있음"],"fr":["무료: 외관","유료: 루프탑 글래스 바·전망 테라스"],"rt":["카페 사보이 → 레기 다리(Most Legií) 건너 강변 따라 남쪽 → 댄싱 하우스 정면 → (선택) 꼭대기 바"],"see":["프랭크 게리 설계, '진저와 프레드'라는 별명의 춤추는 두 건물","루프탑에서 보는 블타바 강과 프라하 성 방향 야경"],"ph":["건너편 강변(이라스코바 다리 쪽)에서 건물 전체","해 진 뒤 조명 켜진 외관"],"wn":["루프탑은 실내 바 공간이 작아 붐비면 대기","강변 바람이 차가움"]}
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/12': continue
    st=D['stops']
    if any(s['k']=='dancing' for s in st): break
    ch=[s for s in st if s['k']=='charles'][0]; st.remove(ch)
    new=[]
    for s in st:
        if s['k']=='hotel' and s['time']=='17:15':
            new.append({"time":"16:40","k":"dancing","note":"조명 켜진 외관 · 시간 되면 꼭대기 글래스 바에서 강변 야경 (사보이에서 도보 12분)"})
            s.update(time='17:30',note='트램·도보로 숙소 복귀, 쉬고 디너 준비')
        new.append(s)
        if s['k']=='mlynec':
            new.append({"time":"20:15","k":"charles","note":"디너 후 조명 켜진 카를교 야경 산책 (식당 바로 옆)"})
        if s['k']=='heming': s['time']='20:45'
    D['stops']=new
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('dancing ok')
