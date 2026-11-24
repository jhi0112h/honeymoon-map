import json
it=json.load(open('itinerary.json'))
def S(t,k,n): return {"time":t,"k":k,"note":n}
for D in it:
    if D['d']=='12/10':
        st=[s for s in D['stops'] if s['k']!='ema']
        new=[]
        for s in st:
            if s['k']=='powder':
                new.append(S('09:10','ema','커피+간단한 빵 (숙소에서 도보 10분, 화약탑 가는 길)'))
                s.update(time='09:30')
            if s['k']=='ots': s.update(time='09:45')
            new.append(s)
        D['stops']=new
    if D['d']=='12/11':
        for s in D['stops']:
            if s['k']=='hotel' and s['time']=='10:15': s['note']='10:45 드레스덴행 출발 · 버스가 2시간이라 커피·빵 테이크아웃해서 출발 (지도의 드레스덴 탭에 상세 동선)'
    if D['d']=='12/12':
        D['stops']=[
         S('09:00','hotel','출발 · 트램 22번 (I. P. Pavlova 정류장) → Pohořelec, 약 25분'),
         S('09:30','strahov','도서관 (오전이라 비교적 한산)'),
         S('10:15','loreta','외관 감상 (종 연주는 정각이라 이번 동선에선 지나감)'),
         S('10:35','sbux','간식 타임 · 커피+빵, 테라스에서 시내 전망'),
         S('10:55','castle','11:00 정문 근위병 교대식 → Circuit B 통합권'),
         S('11:15','vitus','무하 스테인드글라스 (토요일 OK)'),
         S('12:15','xm-castle','성 이르지 광장 크리스마스 마켓'),
         S('12:30','golden','황금소로 22번지'),
         S('13:00','stairs','옛 성 계단 파노라마 → 하산'),
         S('13:15','kunst','점심 겸 카페 (시트 추천)'),
         S('14:25','cihelna','강변에서 카를교 옆모습 사진 · 카프카 박물관 마당 오줌싸개 동상'),
         S('14:50','nicholas','말라스트라나 광장 · 성 니콜라스'),
         S('15:05','aria','아리아 호텔 루프탑 (겨울 운영 여부 확인, 시간 부족하면 생략)'),
         S('15:15','lennon','존 레논 벽'),
         S('15:25','xm-kampa','캄파 크리스마스 마켓 구경 · 체르토프카 물레방아 (일몰 15:52)'),
         S('15:55','savoy','디저트 타임 · 사과 슈트루델+커피 (주말이라 예약 추천)'),
         S('16:45','dancing','조명 켜진 외관 · 시간 되면 꼭대기 글래스 바에서 강변 야경'),
         S('17:40','national','강변 따라 산책 · 조명 켜진 국립극장, 레기 다리에서 프라하 성 야경'),
         S('18:15','mlynec','저녁 · 카를교 뷰 레스토랑 믈리네츠 (창가석·허니문 메모)'),
         S('20:00','charles','디너 후 조명 켜진 카를교 야경 산책 (식당 바로 옆)'),
         S('20:30','heming','2차 칵테일 (도보 3분)'),
         S('22:00','hotel','')]
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)
G=json.load(open('guides.json'))
G['castle']['see'][0]='정문 근위병 교대식: 매시 정각(7~18시), 정오 12:00 제1광장 대교대식(팡파르, 약 15분) · 이번 동선은 11:00 정문 교대식'
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
for D in it:
    if D['d'] in ('12/10','12/12'): print(D['d'],[s['time']+' '+s['k'] for s in D['stops']][:7])
