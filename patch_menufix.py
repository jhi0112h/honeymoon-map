import json,glob
# key -> (korean list, original list)  — verified against Google Maps popular dishes / review keywords (2026-11-25)
FIX={
"p-chartier":(["에스카르고 (부르고뉴식 달팽이, 리뷰 키워드 상위)","뵈프 부르기뇽 또는 콩피 드 카나르 (오리 다리 콩피)","프로피트롤 (초콜릿 소스 슈, 인기 디저트)"],["Escargots de Bourgogne","Bœuf bourguignon / Confit de canard","Profiteroles"]),
"p-remy":(["라따뚜이를 곁들인 그릴 스테이크 + 감자튀김 (대표 메인)","라따뚜이 (프로방스식 채소 요리)","디저트 코스"],["Steak grillé, ratatouille et frites","Ratatouille","Dessert"]),
"porks-v":(["꼴레뇨 (2인 1개)","꼴레뇨 샌드위치 (버터 롤빵에 찢은 꼴레뇨)","맥주 아이스크림 (리뷰 키워드)"],["Pečené vepřové koleno","Trhané koleno v máslovém rohlíku","Pivní zmrzlina"]),
"porks":(["꼴레뇨 (2인 1개)","꼴레뇨 샌드위치 (버터 롤빵에 찢은 꼴레뇨)","흑맥주 + 감자튀김"],["Pečené vepřové koleno","Trhané koleno v máslovém rohlíku","Tmavé pivo + hranolky"]),
"flek":(["자가양조 흑맥주 (13°)","굴라쉬","스비치코바 (크림소스 소고기 + 크네들리키)"],["Flekovský tmavý ležák 13°","Guláš","Svíčková na smetaně"]),
"mlejnice":(["꼴레뇨","빵 그릇 맥주 굴라쉬","코젤 흑맥주"],["Vepřové koleno","Pivní guláš v bochníku","Kozel černý"]),
"kroka":(["굴라쉬 (리뷰 언급 1위)","스비치코바","마늘 수프 (체스네치카)"],["Guláš","Svíčková na smetaně","Česnečka"]),
"nase":(["비프 타르타르 + 빵 (리뷰 언급 1위)","치즈버거","파스트라미 샌드위치"],["Náš tatarák s chlebem","Cheeseburger","Pastrami sendvič"]),
"kolkovna":(["꼴레뇨","굴라쉬","옛 체코식 모둠 플래터 (오리·돼지·소시지)"],["Vepřové koleno","Guláš","Staročeský talíř Kolkovna"]),
"mincovna":(["감자 팬케이크 곁들인 굴라쉬","오리 다리 구이","꼴레뇨"],["Guláš s bramboráčky","Pečené kachní stehno","Vepřové koleno"]),
"krcma":(["꼴레뇨","굴라쉬 수프","체코 생맥주"],["Vepřové koleno","Gulášová polévka","Točené pivo"]),
"havelk":(["스비치코바","굴라쉬","파프리카 크림소스 닭고기"],["Svíčková na smetaně","Guláš","Kuře na paprice"]),
"kantyna":(["비프 타르타르 (리뷰 언급 1위)","티본 스테이크","비프 카르파초"],["Tatarský biftek","T-bone steak","Hovězí carpaccio"]),
"parl":(["굴라쉬","꼴레뇨","양파 수프 (치불라치카)"],["Guláš","Vepřové koleno","Cibulačka"]),
"kampap":(["시즌 코스","농어 요리 (모르스키 블크)","디저트"],["Sezónní menu","Mořský vlk","Dezert"]),
"modra":(["오리구이 (대표 메뉴)","사슴고기 크림 수프","푸아그라"],["Pečená kachna","Krémová polévka ze zvěřiny","Foie gras"]),
"pho":(["소고기 쌀국수 (퍼 보)","분짜","분보남보 (소고기 비빔 쌀국수)"],["Phở bò","Bún chả","Bún bò Nam Bộ"]),
"louvre":(["체코식 아침 식사","사과 슈트루델","자허토르테"],["Česká snídaně","Jablečný štrúdl","Sachrův dort"]),
"savoy":(["크루아상","핫초코","에그 베네딕트"],["Croissant","Horká čokoláda","Vejce Benedikt"]),
"imperial":(["비프 웰링턴","레드와인 송아지 볼살 찜","임페리얼 아침 식사"],["Beef Wellington","Telecí líčka na červeném víně","Snídaně Imperial"]),
"orient":(["큐비즘 크림 링 (쿠비스티츠키 베네치에크)","꿀 케이크 (메도브니크)","커피 (현금 결제 언급 많음)"],["Kubistický věneček","Medovník","Káva"]),
"kunst":(["오리 가슴살 요리","카푸치노","케이크"],["Kachní prso","Cappuccino","Dort"]),
"cukr":(["케이크","사과 슈트루델","파스타"],["Dort","Jablečný štrúdl","Těstoviny"]),
"kozlovna":(["굴라쉬 (리뷰 언급 1위)","꼴레뇨","코젤 다크 생맥주"],["Guláš","Vepřové koleno","Kozel černý"]),
"ifcafe":(["에클레어·타르트 등 프렌치 디저트","케이크 (시즌 디저트)","커피"],["Éclairs, tartes","Dort","Káva"]),
"dd-gaense":(["자우어브라텐 (새콤한 소고기 찜)","거위 구이 (겨울 시즌)","브라우마이스터 슈니첼 + 감자튀김"],["Sauerbraten","Gänsebraten","Braumeisterschnitzel mit Pommes frites"]),
"dd-sophien":(["애저구이 (새끼돼지 통구이)","오리 반 마리 구이 (뼈 발라 나옴)","자우어브라텐"],["Spanferkel","Halbe ausgelöste Ente","Sauerbraten"]),
"dd-pulver":(["애저구이 (새끼돼지 통구이)","작센식 감자 수프","작센 맥주"],["Spanferkel","Sächsische Kartoffelsuppe","Sächsisches Bier"]),
"v-plachutta":(["타펠슈피츠 (냄비째 나오는 삶은 소고기)","골수 토스트 (뼈 골수를 빵에 발라 먹기)","비프 타르타르"],["Tafelspitz","Markknochen mit Schwarzbrot","Beef Tatar"]),
"v-ribs":(["스페어립 (양념 골라 먹는 대형 립)","양송이 튀김 (리뷰 키워드)","생맥주 (립과 찰떡궁합)"],["Spare Ribs","Gebackene Champignons","Bier vom Fass"]),
"v-demel":(["사과 슈트루델","에두아르트 자허토르테 (데멜식 자허토르테)","카이저슈마른 (찢은 팬케이크와 자두 콤포트)"],["Apfelstrudel","Eduard-Sacher-Torte","Kaiserschmarrn mit Zwetschkenröster"]),
"v-landtmann":(["사과 슈트루델","카이저슈마른","비너 슈니첼"],["Apfelstrudel","Kaiserschmarrn","Wiener Schnitzel"]),
"b-hungarikum":(["굴라시 수프 (파프리카 소고기 스튜 수프)","팔링커 (헝가리 과일 브랜디)","사과 파이 (헝가리식 할머니 디저트)"],["Gulyásleves","Pálinka","Almás pite"]),
"b-getto":(["굴라시 (빵 그릇 또는 수프로 나오는 대표 메뉴)","골수 토스트 (리뷰 키워드)","송아지 파프리카시"],["Gulyás","Velős pirítós","Borjúpaprikás"]),
"b-menza":(["굴라시 수프 (레트로 분위기 속 정통 맛)","마늘 크림 수프","망갈리차 돼지고기 요리"],["Gulyásleves","Fokhagymakrémleves","Mangalica"]),
"b-pestbuda":(["굴라시 수프 (성 지구에서 먹는 전통 수프)","오리다리 콩피","염소 치즈 샐러드"],["Gulyásleves","Konfitált kacsacomb","Kecskesajtos saláta"]),
"b-gerbeaud":(["도보시 토르타 (리뷰 언급 1위, 캐러멜 코팅 레이어 케이크)","제르보 케이크 (살구잼·호두 층층이 초콜릿 케이크)","자허 토르타"],["Dobos torta","Gerbeaud szelet","Sacher torta"]),
}
ORIG=json.load(open('menus_orig.json'))
files=['menus.json']+sorted(glob.glob('sources/menus-*.json'))
data={f:json.load(open(f)) for f in files}
for k,(ko,orig) in FIX.items():
    assert len(ko)==len(orig),k
    hit=[f for f in files if k in data[f]]
    assert hit,k
    for f in hit: data[f][k]=ko
    ORIG[k]=orig
for f in files: json.dump(data[f],open(f,'w'),ensure_ascii=False,indent=1)
json.dump(ORIG,open('menus_orig.json','w'),ensure_ascii=False,indent=0)

# IF Café: Tylovo náměstí branch is now IPPA Café -> Masaryčka branch
P=json.load(open('places.json'))
for p in P:
    if p['k']=='ifcafe':
        p['n']='이베타 파베쇼바 카페 (마사리치카점)'
        p['en']='Iveta Fabešová Masaryčka Na Florenci Prague'
        p['w']='Iveta Fabešová – Masaryčka'
        p['a']='노베 메스토'
        p['lat']=50.0896; p['lng']=14.4356
        p['t']='프렌치 파티스리 디저트 카페 (구 IF 카페) · 구글 4.5★ · 20시까지 · 숙소에서 도보 약 10분'
        p['tip']='파티시에 이베타 파베쇼바의 디저트 카페. 숙소 근처 틸로보 광장점은 구글 지도에서 IPPA Café로 바뀌어 있어, 마사리치카역 옆 Na Florenci 지점으로 변경. 개점 시간은 방문 전 구글 지도에서 확인'
        p['links']=[l for l in p.get('links',[]) if 'inyourpocket' not in l['u']]
        p['links'].insert(0,{"t":"구글 지도 (마사리치카점)","u":"https://www.google.com/maps/search/?api=1&query=Iveta+Fabe%C5%A1ov%C3%A1+Masary%C4%8Dka+Na+Florenci+2139%2F4+Praha"})
json.dump(P,open('places.json','w'),ensure_ascii=False,indent=0)
I=open('itinerary.json',encoding='utf-8').read()
I=I.replace('"note": "아침 겸 디저트 (숙소에서 도보 8분)"','"note": "아침 겸 디저트 · 이베타 파베쇼바 마사리치카점 (숙소에서 도보 약 10분)"',1)
I=I.replace('(카페에서 도보 12분)','(카페에서 도보 약 20분 · 트램 이용 가능)',1)
open('itinerary.json','w',encoding='utf-8').write(I)
print('ok',len(FIX))
