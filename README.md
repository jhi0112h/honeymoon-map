# 허니문 지도 (파리 · 프라하 · 드레스덴 · 빈 · 부다페스트, 2026.12)

날짜별 동선, 장소 카드(사진·팁·상세 가이드·리뷰 점수·추천 메뉴·참조 링크), 예약 목록, 디즈니 상세 일정을 담은 지도.

## 보기
```
python3 -m http.server 8000
```
브라우저에서 `http://localhost:8000/honeymoon-map.html` 접속 → 처음 한 번 Google Maps API 키 입력 (브라우저에만 저장, 파일에는 저장되지 않음).

## 수정 후 다시 만들기
데이터(`*.json`)를 고친 뒤 `python3 build.py` 실행 → `honeymoon-map.html` 재생성.

- 도시별 장소: `paris.json`, `places.json`(프라하), `dresden.json`, `vienna.json`, `budapest.json`
- 날짜별 동선: `*-itinerary.json`, `itinerary.json`(프라하)
- 예약 목록: `reservations.json` · 디즈니 상세: `disney.json`
- 가이드·메뉴·리뷰·출처: `guides.json`, `menus.json`, `reviews*.json`, `sources/`
