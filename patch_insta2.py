import json
def S(t,k,n): return {"time":t,"k":k,"note":n}
L=lambda t,u:{"t":t,"u":u}
# ---------- PRAGUE ----------
P=json.load(open('places.json'))
ks=[p['k'] for p in P]
add=[
{"k":"ramovani","n":"라모바니-흐라치키 (기념품 가게)","en":"Ramovani-Hracky Havelska 512","c":"sight","a":"구시가","lat":50.0848,"lng":14.4216,"t":"하벨 시장 거리 기념품 가게 · 구글 평점 4.8","tip":"여러 기념품 가게를 비교한 릴스 기준 같은 제품도 가장 저렴했던 곳. 패트와 매트 열쇠고리 약 6,000원. Havelská 512 (호텔 콜로세움 건물), 19시 영업 종료(구글 지도 기준)","links":[L("인스타그램 릴스: 프라하 여행 꿀팁·기념품 가게 (d_berlin_k)","https://www.instagram.com/reel/Db2uTPPo752/")]},
{"k":"kozlovna","n":"코즐로브나 아프로포스","en":"Kozlovna Apropos","c":"food","m":"점심·저녁","a":"구시가","lat":50.0886,"lng":14.4155,"t":"코젤 맥주 직영 펍 · 폭립","tip":"릴스 추천: 폭립(Roasted Pork Ribs) + 비프 타르타르, 작은 샐러드 곁들이기. 굴라쉬는 비추천이라는 후기. 코즐로브나는 지점이 여러 곳이라 방문 지점 확인","links":[L("인스타그램 릴스: 코즐로브나 폭립 추천 (d_berlin_k)","https://www.instagram.com/reel/Db2uTPPo752/")]},
{"k":"jazzdock","n":"재즈독","en":"JazzDock Prague","c":"night","a":"신시가","lat":50.0745,"lng":14.4108,"t":"블타바 강 위 선상 재즈 바","tip":"강변 유리창 너머 야경과 라이브 재즈. 공연 일정·예약은 공식 사이트 확인","links":[L("인스타그램 릴스: 프라하 4박 5일 일정표 (by_lalahyun)","https://www.instagram.com/reel/DeBRLDuJJlU/")]},
{"k":"palladium","n":"팔라디움 쇼핑몰","en":"Palladium Praha","c":"sight","a":"구시가","lat":50.0893,"lng":14.4290,"t":"공화국 광장 대형 쇼핑몰","tip":"비 오거나 추울 때 실내 쇼핑. 화약탑·시민회관 바로 옆","links":[L("인스타그램 릴스: 프라하 4박 5일 일정표 (by_lalahyun)","https://www.instagram.com/reel/DeBRLDuJJlU/")]},
{"k":"planetum","n":"플라네툼 (돔 영화관)","en":"Planetum Prague Planetarium","c":"night","a":"레트나","lat":50.1049,"lng":14.4249,"t":"천문관 돔에서 보는 영화·별자리 프로그램","tip":"스트로모프카 공원 안이라 시내 동선과 떨어져 있음. 프로그램에 따라 영화가 아니라 강의 같았다는 후기도 있어 상영 내용 확인 후 예약","links":[L("인스타그램 릴스: 별빛 아래 영화관 플라네툼 (thesewinj)","https://www.instagram.com/reel/DeglhaOhRnB/")]}]
for x in add:
    if x['k'] not in ks: P.append(x)
for p in P:
    if p['k']=='petrin':
        p['t']='미니 에펠탑 · 푸니쿨라 2026.9.22 재개통'
        p['tip']='푸니쿨라 약 2년 만에 재개통(차량·선로 새로 교체). 탑승장 Újezd(트램 22번), 매일 07:00~22:15, 약 10분 간격. 1회권 100코루나(PID 앱 90), 24·72시간권 소지 시 추가요금 없음. 오전 9시 전 추천(10:30엔 100명 넘게 줄). 카페 사보이 바로 옆 정류장'
        p.setdefault('links',[]).append(L("인스타그램 릴스: 페트르진 푸니쿨라 재개통 (morningprague)","https://www.instagram.com/reel/DdoirRHA131/"))
    if p['k']=='xm-old':
        p['t']='11/28~1/6 · 10:00~22:00 · 라이트 쇼 매일 16:30~21:30 매시 30분'
        p['tip']='라이트 쇼는 16:30 첫 회가 일몰 직후 푸른 하늘+트리 조명이라 가장 예쁨. 17:30~19:30이 가장 붐비니 피하기. 프라하 햄은 100g 단위 과금이라 주문할 때 "조금만" 요청. 포토 명당: 트리 전망대(무료), 틴 성당 맞은편, 구시청사 탑(유료, 정각 시계→30분 라이트 쇼)'
        p.setdefault('links',[]).append(L("인스타그램: 2026 프라하 크리스마스 마켓 가이드 (mbtij.zip)","https://www.instagram.com/p/DgFPoMeH5zd/"))
    if p['k']=='charles':
        p['tip']=p['tip'].replace('해 진 직후(12월 16시대)가 가장 예쁨','해 진 직후(12월 16시대)가 가장 예쁨. ⚠ 가스등 점등식은 올해 12월이 아니라 2027년 1월 9~31일로 변경(프라하 관광청)')
        p.setdefault('links',[]).append(L("프라하 관광청: 카를교 램프 라이터 (2027.1.9~31)","https://prague.eu/en/akce/lamp-lighter-on-the-charles-bridge"))
json.dump(P,open('places.json','w'),ensure_ascii=False,indent=0)
G=json.load(open('guides.json'))
g=G['charles']
g['see']=[x for x in g['see'] if not x.startswith('전통 가스등 점등식')]
g['wn']=[x for x in g['wn'] if not x.startswith('램프 라이터')]
g['wn'].insert(0,'가스등 점등식(램프 라이터)은 2026년엔 12월이 아니라 2027년 1월 9~31일로 변경돼 이번 여행에선 볼 수 없음 (프라하 관광청 공식 페이지)')
g['rt']=['구시가 교탑에서 노을 → 해 진 직후 다리 건너며 성 쪽 야경 → 돌아와 구시가 광장 라이트 쇼']
gx=G['xm-old']
gx['tk']=['무료 · 11/28~1/6 · 10:00~22:00','라이트 쇼: 매일 16:30~21:30 매시 30분 (총 6회)']
gx['rt']=['16:30 첫 라이트 쇼 → 트리 전망대 → 틴 성당 맞은편 사진 → 17:30 전에 빠지기 → 20:30 늦은 라이트 쇼 다시 보기']
gx['ph']=['트리 전망대 (무료)','틴 성당 맞은편: 첨탑+트리 한 프레임','구시청사 탑 (유료): 정각 천문시계 → 30분 라이트 쇼 내려다보기']
gx['wn']=['17:30~19:30 피크, 주말 저녁 최고 혼잡 → 16:30 첫 회나 20:30 이후 추천','프라하 햄은 100g 단위 과금, 주문할 때 "조금만" 꼭 말하기','스바르작 컵 보증금 있음','인파 많아 소매치기 주의']
G['ramovani']={"d":"15~20분","tk":["구글 지도 기준 19시 영업 종료"],"fr":["무료 입장 (쇼핑)"],"rt":["하벨 시장 노점 구경 → 같은 거리 라모바니-흐라치키 → 포크스 점심"],"see":["패트와 매트 열쇠고리·인형","마리오네트·나무 장난감"],"ph":["가게 앞 쇼윈도"],"wn":["같은 제품도 가게마다 가격 차이가 커서 여기서 가격 기준 잡고 비교","카드 결제 가능 여부는 현장 확인"]}
json.dump(G,open('guides.json','w'),ensure_ascii=False,indent=0)
M=json.load(open('menus.json'))
M['kozlovna']=["폭립 (Roasted Pork Ribs)","비프 타르타르","코젤 다크 생맥주"]
M['xm-old']=["트르들로 (굴뚝빵, 시나몬 설탕)","스바르작 (체코식 뱅쇼)","소시지(클로바사)·프라하 햄 구이 (100g 단위 과금 주의)"]
json.dump(M,open('menus.json','w'),ensure_ascii=False,indent=0)
it=json.load(open('itinerary.json'))
for D in it:
    if D['d']!='12/10': continue
    st=D['stops']
    if not any(s['k']=='ramovani' for s in st):
        i=[s['k'] for s in st].index('havel')
        st.insert(i+1,S('12:15','ramovani','가성비 기념품 가게 · 패트와 매트 열쇠고리 (하벨 시장 같은 거리)'))
    keep=[s for s in st if s['k'] not in('btower','charles','novot','xm-old','nase','lokal') and not (s['k']=='hotel' and s['time']>='20:00')]
    keep+= [S('15:25','btower','노을 지는 카를교·프라하 성 (일몰 15:58)'),
            S('16:00','charles','해 진 직후 카를교 산책 · 성 쪽 야경 (가스등 점등식은 1월로 변경돼 없음)'),
            S('16:30','xm-old','16:30 첫 라이트 쇼 · 푸른 하늘+트리 · 트리 전망대·틴 성당 맞은편 사진 · 굴뚝빵'),
            S('17:30','nase','피크(17:30~19:30) 피해 이른 저녁 · 1개 나눠 먹기'),
            S('18:15','lokal','맥주펍 · 탱크 필스너 + 가벼운 안주 (예약 추천)'),
            S('20:20','xm-old','한산해진 늦은 라이트 쇼(20:30) 다시 보기'),
            S('20:50','novot','카를교+프라하 성 야경 정면 사진'),
            S('21:30','hotel','도보 25분 또는 택시')]
    D['stops']=keep
    print([s['time']+' '+s['k'] for s in keep])
json.dump(it,open('itinerary.json','w'),ensure_ascii=False,indent=1)

# ---------- PARIS ----------
PA=json.load(open('paris.json'))
if 'p-champs' not in [p['k'] for p in PA]:
    PA.append({"k":"p-champs","n":"샹젤리제 크리스마스 마켓","en":"Champs-Elysees Christmas Market","c":"xmas","a":"샹젤리제","lat":48.8672,"lng":2.3165,"t":"10년 만에 다시 열리는 마켓 · 2026.11.22~2027.1.4","tip":"샹젤리제~콩코르드 광장 사이. 월~목 10~22시, 금~일 10~23시, 12/24 20시 종료·12/31 휴장. 공예품 오두막, 뱅쇼, 공연, 아이스링크","links":[L("인스타그램 릴스: 2026 샹젤리제 크리스마스 마켓 (dailyhyunjung)","https://www.instagram.com/reel/DgBGD7nNLP8/")]})
json.dump(PA,open('paris.json','w'),ensure_ascii=False,indent=0)
pi=json.load(open('paris-itinerary.json'))
for D in pi:
    if D['d']=='12/7' and not any(s['k']=='p-champs' for s in D['stops']):
        st=D['stops']; i=[s['k'] for s in st].index('p-tuileries')
        st.insert(i,S('21:00','p-champs','10년 만의 샹젤리제 마켓 (월요일 22시 종료) · 선착장에서 콩코르드 방향'))
        st[i+1]['time']='21:40'; st[i+1]['note']='콩코르드 광장 건너 튈르리 마켓 (시트 일정)'
json.dump(pi,open('paris-itinerary.json','w'),ensure_ascii=False,indent=1)

# ---------- VIENNA ----------
V=json.load(open('vienna.json'))
vk=[p['k'] for p in V]
vadd=[
{"k":"v-xm-mtp","n":"마리아 테레지엔 광장 마켓","en":"Maria-Theresien-Platz Christmas Market","c":"xmas","a":"링 도로","lat":48.2045,"lng":16.3610,"t":"2026.11.20~12.26 · 미술사·자연사 박물관 사이","tip":"두 박물관 건물 조명 사이의 마켓. 영웅 광장에서 링 도로만 건너면 바로","links":[L("인스타그램: 2026 비엔나 크리스마스 마켓 가이드 (dailyhyunjung)","https://www.instagram.com/p/Dfq2B58nQrm/")]},
{"k":"v-xm-belv","n":"벨베데레 크리스마스 마켓","en":"Belvedere Christmas Market","c":"xmas","a":"중앙역·벨베데레","lat":48.1922,"lng":16.3808,"t":"2026.11.20~12.13 · 상궁 앞 · 12/13이 마지막 날","tip":"12/13 도착일이 마켓 마지막 날이라 체크인 후 바로 들르기. 12/14 벨베데레 관람 때는 이미 끝나 있음","links":[L("인스타그램: 2026 비엔나 크리스마스 마켓 가이드 (dailyhyunjung)","https://www.instagram.com/p/Dfq2B58nQrm/")]},
{"k":"v-xm-spittel","n":"슈피텔베르크 마켓","en":"Spittelberg Christmas Market","c":"xmas","a":"링 도로","lat":48.2032,"lng":16.3545,"t":"2026.11.13~12.23 · 골목 사이 수공예 마켓","tip":"마리아 테레지엔 광장 뒤 좁은 골목. 시간 여유 있을 때","links":[L("인스타그램: 2026 비엔나 크리스마스 마켓 가이드 (dailyhyunjung)","https://www.instagram.com/p/Dfq2B58nQrm/")]}]
for x in vadd:
    if x['k'] not in vk: V.append(x)
for p in V:
    if p['k']=='v-rathaus': p.setdefault('links',[]).append(L("인스타그램: 2026 비엔나 크리스마스 마켓 가이드 (dailyhyunjung)","https://www.instagram.com/p/Dfq2B58nQrm/"))
    if p['k']=='v-stephan': p['tip']=p.get('tip','')+'. 12월엔 대성당 앞 광장에도 크리스마스 마켓'
json.dump(V,open('vienna.json','w'),ensure_ascii=False,indent=0)
mv='sources/menus-vienna.json'
MV=json.load(open(mv))
MV['v-rathaus']=["글뤼바인·푼슈 (따뜻한 와인·과일 음료)","카이저슈마렌 (잼 곁들인 오스트리아 팬케이크)","카르토펠푸퍼·케제슈페츨레 (감자전·치즈 생면)"]
MV['v-xm-mtp']=["푼슈","아펠슈트루델 (사과 파이)","프레첼"]
json.dump(MV,open(mv,'w'),ensure_ascii=False,indent=0)
vi=json.load(open('vienna-itinerary.json'))
for D in vi:
    if D['d']=='12/13':
        D['stops']=[
         S('16:19','v-hbf','프라하발 기차 도착 (12:36 출발)'),
         S('16:40','v-hotel','체크인 (중앙역에서 도보 5분)'),
         S('17:00','v-xm-belv','벨베데레 마켓 마지막 날 (숙소에서 도보 10분)'),
         S('17:30','v-opera','트램 D로 이동 · 조명 켜진 오페라극장 (릴스 코스 시작)'),
         S('17:45','v-albterrace','에스컬레이터로 올라가 오페라극장 전경'),
         S('18:05','v-burggarten','모차르트 동상'),
         S('18:20','v-heldenplatz','신왕궁 야경'),
         S('18:35','v-xm-mtp','링 도로 건너 박물관 사이 마켓'),
         S('19:10','v-rathaus','시청 광장 크리스마스 마켓 (시트) · 저녁은 마켓 먹거리로'),
         S('20:45','v-hotel','트램 D로 숙소 복귀')]
json.dump(vi,open('vienna-itinerary.json','w'),ensure_ascii=False,indent=1)
print('done')
