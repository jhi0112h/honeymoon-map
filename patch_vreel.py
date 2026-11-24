import json
P=json.load(open('vienna.json'))
add=[
{"k":"v-albterrace","n":"알베르티나 테라스","en":"Albertina terrace Albertinaplatz","c":"night","a":"구시가 (호프부르크)","lat":48.2045,"lng":16.3685,"t":"오페라극장이 한눈에 보이는 야경 전망 (무료)","tip":"오페라극장 맞은편 알베르티나 미술관 앞 에스컬레이터를 타고 테라스로 올라가면 조명 켜진 오페라극장 전경. 참고 릴스 동선의 첫 포인트","links":[{"t":"인스타그램 릴스: 빈 겨울밤 야경 코스 (borbor.ee)","u":"https://www.instagram.com/reel/DfWxJvnhQDT/"}]},
{"k":"v-burggarten","n":"부르크가르텐 · 모차르트 동상","en":"Mozart Monument Burggarten","c":"sight","a":"구시가 (호프부르크)","lat":48.2047,"lng":16.3662,"t":"왕궁 정원의 하얀 모차르트 동상","tip":"알베르티나 테라스에서 바로 옆. 여름엔 동상 앞 높은음자리표 꽃밭이 유명하지만 겨울엔 동상만","links":[{"t":"인스타그램 릴스: 빈 겨울밤 야경 코스 (borbor.ee)","u":"https://www.instagram.com/reel/DfWxJvnhQDT/"}],"w":"Mozart Monument, Vienna"},
{"k":"v-heldenplatz","n":"영웅 광장 · 신왕궁 야경","en":"Heldenplatz Neue Burg","c":"night","a":"구시가 (호프부르크)","lat":48.2063,"lng":16.3632,"t":"조명 켜진 반원형 신왕궁과 멀리 보이는 시청사","tip":"광장 잔디밭 쪽에서 신왕궁 전체, 반대편으로는 폴크스가르텐 너머 시청사 첨탑이 보임. 여기서 시청 광장 마켓까지 걸어서 10분","links":[{"t":"인스타그램 릴스: 빈 겨울밤 야경 코스 (borbor.ee)","u":"https://www.instagram.com/reel/DfWxJvnhQDT/"}],"w":"Heldenplatz"},
{"k":"v-peterskirche","n":"성 페터 성당","en":"Peterskirche Vienna","c":"sight","a":"구시가 (슈테판플라츠)","lat":48.2093,"lng":16.3700,"t":"그라벤 옆 화려한 바로크 돔 천장","tip":"입장 무료. 돔 천장 프레스코가 참고 릴스 첫 장면. 무료 오르간 연주가 열리는 날도 있음","links":[{"t":"인스타그램 릴스: 빈 겨울밤 야경 코스 (borbor.ee)","u":"https://www.instagram.com/reel/DfWxJvnhQDT/"}],"w":"Peterskirche"}]
ks=[p['k'] for p in P]
for x in add:
    if x['k'] not in ks: P.append(x)
for p in P:
    if p['k'] in ('v-opera','v-rathaus'):
        L=p.setdefault('links',[])
        if not any('DfWxJvnhQDT' in l['u'] for l in L): L.append({"t":"인스타그램 릴스: 빈 겨울밤 야경 코스 (borbor.ee)","u":"https://www.instagram.com/reel/DfWxJvnhQDT/"})
json.dump(P,open('vienna.json','w'),ensure_ascii=False,indent=0)
G={}
try: G=json.load(open('sources/guides-vienna.json'))
except: pass
G['v-albterrace']={"d":"15분","tk":["무료 (미술관 입장 안 해도 테라스는 올라갈 수 있음)"],"fr":["무료"],"rt":["오페라극장 정면 → 길 건너 알베르티나 광장 → 에스컬레이터로 테라스 → 오페라극장 방향 난간"],"see":["조명 켜진 오페라극장 전경","링 도로와 케른트너 거리 야경"],"ph":["테라스 난간에서 오페라극장 정면 (해 진 뒤 16:30 이후)"],"wn":["테라스 바닥이 미끄러울 수 있음","릴스 동선 그대로 다음은 바로 옆 부르크가르텐"]}
G['v-burggarten']={"d":"10분","tk":["무료 · 정원 개방 시간 안에만 출입 (겨울엔 일찍 닫을 수 있음)"],"fr":["무료"],"rt":["알베르티나 테라스 → 정원 입구 → 모차르트 동상 → 신왕궁 방향 출구"],"see":["하얀 대리석 모차르트 동상"],"ph":["동상 정면 계단 아래에서 올려다보기"],"wn":["정원 문이 닫혔으면 링 도로 쪽에서 울타리 너머로 보고 바로 영웅 광장으로"]}
G['v-heldenplatz']={"d":"15분","tk":["무료"],"fr":["무료"],"rt":["부르크가르텐 → 신왕궁 앞 → 광장 잔디밭 → 폴크스가르텐 방향으로 시청사 바라보며 걷기 → 시청 광장"],"see":["반원형 신왕궁 야간 조명","광장 건너편으로 보이는 시청사 첨탑"],"ph":["광장 가운데 기마상 옆에서 신왕궁 전체","폴크스가르텐 쪽에서 시청사를 정면에 두고"],"wn":["넓고 어두운 광장이라 밤엔 큰길 쪽으로 걷기"]}
G['v-peterskirche']={"d":"15분","tk":["입장 무료"],"fr":["무료"],"rt":["슈테판 대성당 → 그라벤 거리 → 골목 안 성 페터 성당"],"see":["타원형 돔 천장 프레스코","금빛 바로크 제단"],"ph":["성당 중앙에서 돔 천장 올려다보기"],"wn":["미사 중엔 관광 자제"]}
json.dump(G,open('sources/guides-vienna.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('vienna-itinerary.json'))
def S(t,k,n): return {"time":t,"k":k,"note":n}
for D in it:
    if D['d']=='12/13':
        D['title']='빈 도착 · 릴스 야경 코스 · 시청 광장 마켓'
        D['stops']=[
         S('16:19','v-hbf','프라하발 기차 도착 (12:36 출발)'),
         S('16:40','v-hotel','체크인 (중앙역에서 도보 5분)'),
         S('17:15','v-opera','지하철 U1 카를스플라츠역 · 조명 켜진 오페라극장 (참고 릴스 코스 시작)'),
         S('17:30','v-albterrace','에스컬레이터로 올라가 오페라극장 전경'),
         S('17:50','v-burggarten','모차르트 동상'),
         S('18:05','v-heldenplatz','신왕궁 야경 → 시청사 바라보며 걷기'),
         S('18:30','v-rathaus','시청 광장 크리스마스 마켓 (시트) · 저녁은 마켓 먹거리로'),
         S('20:15','v-hotel','트램 D로 숙소 복귀')]
    if D['d']=='12/14':
        st=[s for s in D['stops'] if s['k']!='v-opera']
        new=[]
        for s in st:
            if s['k']=='v-graben':
                new.append(S('14:15','v-peterskirche','그라벤 옆 바로크 돔 천장 (무료)'))
                s.update(time='14:30',note='그라벤·콜마르크트 거리 (밤엔 샹들리에 조명)')
            if s['k']=='v-demel': s['time']='14:45'
            if s['k']=='v-hofburg': s['time']='15:30'
            if s['k']=='v-albertina': s.update(time='16:00',note='미술관 내부 관람 (모네~피카소) · 테라스는 12/13 밤에 다녀옴')
            if s['k']=='v-amhof': s['time']='17:30'
            new.append(s)
            if s['k']=='v-plachutta':
                new.append(S('20:15','v-graben','디너 후 샹들리에 조명 켜진 그라벤 거리 야경 산책'))
        D['stops']=new
json.dump(it,open('vienna-itinerary.json','w'),ensure_ascii=False,indent=1)
for D in it[:2]: print(D['d'],[s['time']+' '+s['k'] for s in D['stops']])
