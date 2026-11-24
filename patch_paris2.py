import json
P=json.load(open('paris.json'))
add=[
{"k":"p-valdeurope","n":"발 데 유럽 쇼핑센터 식당가","en":"Val d'Europe shopping centre","c":"food","m":"저녁","a":"발 데 유럽","lat":48.8535,"lng":2.7820,"t":"12/5 저녁 · 숙소 근처 (시트에 식당 미정)","tip":"도착일 밤이라 멀리 가지 않고 숙소 근처에서. 쇼핑센터 식당은 일찍 닫는 곳이 있어 20시 전후 도착 시 영업시간 확인"},
{"k":"p-entrecote","n":"를레 드 랑트르코트 (마르뵈프)","en":"Le Relais de l'Entrecote Marbeuf","c":"food","m":"저녁","a":"샹젤리제","lat":48.8687,"lng":2.3036,"t":"스테이크 프리트 단일 메뉴 · 바토무슈 선착장 도보 12분","tip":"예약 안 받아서 오픈 시간(18:45 전후) 맞춰 줄 서기. 굽기만 고르면 되고 리필 한 번 더 나옴"},
{"k":"p-campana","n":"카페 캄파나 (오르세 미술관)","en":"Cafe Campana Musee d'Orsay","c":"cafe","a":"중심가","lat":48.8603,"lng":2.3258,"t":"오르세 5층 대형 시계 옆 카페","tip":"미술관 입장권 필요. 12/8 베르사유에서 넘어와 늦은 점심 겸 휴식"},
{"k":"p-chartier","n":"부용 샤르티에 (그랑 불바르)","en":"Bouillon Chartier Grands Boulevards","c":"food","m":"저녁","a":"오페라","lat":48.8719,"lng":2.3434,"t":"1896년 문을 연 가성비 프랑스 식당","tip":"예약 안 받아 줄 서지만 회전 빠름. 에스카르고·뵈프 부르기뇽. 라파예트에서 도보 10분"},
{"k":"p-painidees","n":"뒤 팽 에 데 이데","en":"Du Pain et des Idees","c":"cafe","a":"북역·동역","lat":48.8714,"lng":2.3634,"t":"피스타치오 에스카르고 빵 · 파리 동역 도보 7분","tip":"주말 휴무, 12/9 수요일은 영업. 테이크아웃 위주"},
{"k":"p-carette","n":"카레트 (보주 광장)","en":"Carette Place des Vosges","c":"cafe","a":"마레","lat":48.8556,"lng":2.3657,"t":"보주 광장 아케이드 카페 · 마카롱·핫초코","tip":"보주 광장 산책과 함께. 아침 일찍부터 영업"},
{"k":"p-asdufallafel","n":"라스 뒤 팔라펠","en":"L'As du Fallafel","c":"food","m":"점심","a":"마레","lat":48.8573,"lng":2.3590,"t":"마레 지구 팔라펠 샌드위치","tip":"보통 11시 오픈이라 12/9 동선(11시 공항 이동)과는 안 맞음. 시간이 남으면 포장"},
{"k":"p-breizh","n":"브레이즈 카페 (마레)","en":"Breizh Cafe Marais","c":"food","m":"점심","a":"마레","lat":48.8606,"lng":2.3628,"t":"메밀 갈레트·크레페","tip":"인기 많아 예약 추천"}
]
ks=[p['k'] for p in P]
for x in add:
    if x['k'] not in ks: P.append(x)
json.dump(P,open('paris.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('paris-itinerary.json'))
for D in it:
    if D['d']=='12/5':
        D['stops'][1]['note']='한인 택시로 체크인'
        if not any(s['k']=='p-valdeurope' for s in D['stops']):
            D['stops'].append({"time":"20:15","k":"p-valdeurope","note":"저녁 · 숙소 근처 (시트 20:00~22:00 저녁)"})
    if D['d']=='12/7':
        st=D['stops']
        if not any(s['k']=='p-angelina' for s in st):
            st[1]['note']='짐 맡기기'
            st.insert(2,{"time":"10:45","k":"p-angelina","note":"브런치 + 몽블랑 (시트 추천) · 루브르까지 도보 5분"})
            for s in st:
                if s['k']=='p-orangerie': s['note']='15:00~18:00 (티켓 예약 완료)'
            i=[s['k'] for s in st].index('p-bateaux')
            st.insert(i,{"time":"18:00","k":"p-entrecote","note":"저녁 · 스테이크 프리트 (예약 불가, 오픈 맞춰 줄 서기) · 선착장까지 도보 12분"})
    if D['d']=='12/8':
        st=D['stops']
        if not any(s['k']=='p-campana' for s in st):
            i=[s['k'] for s in st].index('p-orsay')
            st[i]['note']='이동 13:00~14:00 · 관람 14:00~16:00 (줄이 길어 예약 시간 맞춰)'
            st.insert(i+1,{"time":"14:00","k":"p-campana","note":"관람 중 늦은 점심 · 대형 시계 옆 카페"})
            j=[s['k'] for s in st].index('p-lafayette')
            st.insert(j+1,{"time":"18:45","k":"p-chartier","note":"저녁 · 가성비 프랑스 요리 (줄 서지만 회전 빠름)"})
    if D['d']=='12/9':
        if not any(s['k']=='p-painidees' for s in D['stops']):
            D['stops']=[
             {"time":"08:00","k":"p-hyatt","note":"체크아웃"},
             {"time":"08:30","k":"p-gareest","note":"파리 동역에 짐 맡기기"},
             {"time":"08:45","k":"p-painidees","note":"아침 빵 · 피스타치오 에스카르고 (동역에서 도보 7분)"},
             {"time":"09:30","k":"p-marais","note":"마레 지구 쇼핑 (상점은 10~11시 오픈이 많음)"},
             {"time":"10:00","k":"p-carette","note":"보주 광장 산책 + 핫초코"},
             {"time":"11:00","k":"p-gareest","note":"짐 찾고 공항 이동 (11:00~12:00, 공항 13시 도착 목표)"},
             {"time":"15:20","k":"p-cdg","note":"프라하행 출발 15:20 → 17:05 도착"}]
json.dump(it,open('paris-itinerary.json','w'),ensure_ascii=False,indent=1)
# Prague 12/13 checkout 10:00 with luggage storage
pi=json.load(open('itinerary.json'))
for D in pi:
    if D['d']=='12/13':
        st=D['stops']
        if st[0]['k']!='hotel':
            st.insert(0,{"time":"08:15","k":"hotel","note":"체크아웃(10:00 마감) 먼저 하고 짐 맡기기 · 짐 보관 가능 여부 미리 확인"})
        for s in st:
            if s['k']=='hotel' and s['time']=='11:30': s['note']='맡긴 짐 찾기 → 중앙역 도보 10분, 12:36 빈행 기차'
json.dump(pi,open('itinerary.json','w'),ensure_ascii=False,indent=1)
print('ok')
