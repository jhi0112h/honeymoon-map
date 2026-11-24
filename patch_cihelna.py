import json
P=json.load(open('places.json'))
if 'cihelna' not in [p['k'] for p in P]:
    i=[p['k'] for p in P].index('kafkam')
    P.insert(i+1,{"k":"cihelna","n":"치헬나 강변 (헤르게토바 치헬나)","en":"Hergetova Cihelna Prague","c":"night","a":"말라스트라나","lat":50.0879,"lng":14.4113,"t":"카를교를 북쪽에서 정면으로 보는 강변 · 카프카 박물관 옆","tip":"옛 벽돌공장 자리의 강변 테라스. 카를교와 구시가 교탑이 옆으로 길게 보이는 구도. 카프카 박물관 마당(오줌싸개 동상)과 붙어 있어 같이 보기 좋음","links":[{"t":"위키백과 (카프카 박물관·헤르게토바 치헬나)","u":"https://en.wikipedia.org/wiki/Franz_Kafka_Museum"}]})
json.dump(P,open('places.json','w'),ensure_ascii=False,indent=0)
G=json.load(open('guides.json'))
G['cihelna']={"d":"15~20분","tk":["무료"],"fr":["무료 (카프카 박물관 내부만 유료)"],"rt":["쿤스트할레 카페(클라로프) → 강변 따라 남쪽으로 5분 → 카프카 박물관 마당 → 치헬나 강변 → 말라스트라나 광장 방향"],"see":["옆에서 보는 카를교 아치와 구시가 교탑","카프카 박물관 마당의 오줌싸개 동상(다비드 체르니 작품)"],"ph":["강가 난간에서 카를교를 대각선으로 길게","겨울 오후 2시 무렵 역광 없이 다리가 잘 보임"],"wn":["강변 바람이 차가움","테라스 일부는 레스토랑 좌석이라 통로 쪽에서 촬영"]}
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/12': continue
    new=[]
    for s in D['stops']:
        if s['k']=='nicholas':
            new.append({"time":"14:10","k":"cihelna","note":"강변에서 카를교 옆모습 사진 · 카프카 박물관 마당 오줌싸개 동상"})
            s['time']='14:35'
        if s['k']=='aria': s['time']='14:50'
        if s['k']=='lennon': s['time']='15:05'
        if s['k']=='xm-kampa': s['time']='15:15'
        if s['k']=='savoy': s['time']='15:45'
        new.append(s)
    D['stops']=new
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('ok')
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/10': continue
    if any(s['k']=='havel' for s in D['stops']): break
    new=[]
    for s in D['stops']:
        if s['k']=='porks-v':
            new.append({"time":"12:05","k":"havel","note":"점심 가는 길에 기념품 노점 구경 (구시가 광장 남쪽, 15분)"})
        new.append(s)
    D['stops']=new
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('havel ok')
