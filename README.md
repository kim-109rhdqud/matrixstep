# matrixstep.net · 행렬 계산기

역행렬, 행렬식, 곱셈, RREF, 연립방정식 등을 분수로 정확하게 계산하고 단계별 풀이를 보여주는 정적 사이트예요.

## 구조
- `assets/app.js` · 계산 로직과 화면 동작 (분수 연산, 가우스-조던 소거, 풀이 생성)
- `assets/app.css` · 디자인 (라이트/다크 모드)
- `build.py` · 페이지 생성기. 맨 위 **설정** 부분에 도메인, 이메일, 애드센스 ID 등을 넣어요.
- `guides.py`, `guides_a.py`, `guides_b.py` · 한국어 가이드 글. 예제 숫자는 Python 분수로 계산하고 assert로 검산해요.
- `guides_en.py` · 영어 가이드 글 (/en/guide/). 같은 예제를 영어로 설명해요.
- 영어판은 `/en/` 아래에 생성돼요. 화면 문구는 `build.py`의 `UI_EN`/`OPS_EN`, 계산기 풀이 문구는 `assets/app.js`의 `STR.en`에 있어요.
- `tests/check_app.py` · `app.js`의 계산을 무작위 행렬 1,700여 개로 독립 검증해요(한국어·영어 문구 모두). 배포 전에 자동 실행돼요.
- `static/` · 파비콘, 공유 미리보기 이미지
- `tools/make_images.py` · `static/` 이미지를 다시 만들 때만 사용
- `amplify.yml` · AWS Amplify 빌드 설정

## 배포
`main` 브랜치에 푸시하면 Amplify가 `python3 tests/check_app.py`로 계산을 검증한 뒤 `python3 build.py`를 실행하고 `dist/`를 배포해요. 검증에 실패하면 배포되지 않아요.

## 로컬에서 확인
```
python3 tests/check_app.py
python3 build.py
python3 -m http.server -d dist 8000
```
브라우저에서 http://localhost:8000 을 열어요.
