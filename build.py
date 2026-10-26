#!/usr/bin/env python3
"""행렬 계산기 정적 사이트 생성기. 설정을 바꾼 뒤 `python3 build.py` → dist/ 폴더가 배포본.
표준 라이브러리만 써서 Amplify 빌드 환경에서 그대로 돌아가요."""
import os, shutil, json, html, datetime
import guides

# ===================== 설정 =====================
DOMAIN = "https://matrixstep.net"  # 끝에 / 없이
SITE = "행렬 계산기"
EMAIL = "hunni1048@gmail.com"        # 문의 이메일
OPERATOR = "김현서"                 # 개인정보처리방침에 들어갈 운영자 이름
ADSENSE_CLIENT = "ca-pub-8152428278847928"  # 애드센스 게시자 ID
AD_SLOT = ""                     # 애드센스 광고 단위 ID (승인 후)
GA_ID = "G-C9HEVN1K5G"          # Google Analytics 측정 ID
GOOGLE_VERIFY = "RbHYlcklifwfjHGu8-Gsei87Nz5d7G33nOIyOQZuzvE"  # Search Console HTML 태그 content 값
NAVER_VERIFY = "47b17112975f4850acd04b4dc30e856d9028e899"  # 네이버 서치어드바이저 HTML 태그 content 값
TODAY = datetime.date(2026, 10, 26).isoformat()   # 내용을 고칠 때 올려요 (가이드·소개 "업데이트" 날짜, sitemap lastmod)
PRIVACY_DATE = "2026-10-13"                        # 개인정보처리방침 시행일 (방침을 바꿀 때만 올려요)
FIRST_PUBLISHED = "2026-10-13"                     # 가이드 최초 게시일
# ================================================

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dist")
e = html.escape

OPS = [
 dict(key="inverse", slug="inverse", label="역행렬",
  title="역행렬 계산기 - 가우스-조던 단계별 풀이", h1="역행렬 계산기",
  meta="2×2부터 6×6까지 역행렬을 분수로 정확하게 계산하고, 가우스-조던 소거법의 행 연산 과정을 단계별로 보여주는 무료 역행렬 계산기예요.",
  desc="가우스-조던 소거법으로 A⁻¹을 구하고, 행 연산을 하나씩 보여드려요.",
  card="가우스-조던 소거법으로 A⁻¹ 구하기",
  ch="역행렬이란?",
  cb=["역행렬 A⁻¹은 AA⁻¹ = A⁻¹A = I 를 만족하는 행렬이에요. 정사각행렬이면서 행렬식이 0이 아닐 때만 존재해요.",
      "가우스-조던 소거법은 [A | I]에 행 연산을 반복해 왼쪽을 단위행렬로 만들면, 오른쪽에 A⁻¹이 남는다는 원리를 이용해요."],
  tip="2×2라면 A⁻¹ = 1/(ad − bc) · [d −b; −c a] 공식이 가장 빨라요.",
  faq=[("역행렬이 없는 행렬은 어떻게 알 수 있나요?","행렬식이 0이면 역행렬이 없어요. 소거 과정에서 왼쪽 부분에 모든 성분이 0인 행이 생기는 것으로도 확인할 수 있어요."),
       ("결과가 분수로 나오는데 소수로 볼 수 있나요?","결과 영역의 ‘소수’ 버튼을 누르면 소수 넷째 자리까지 반올림해 보여드려요. 계산 자체는 항상 분수로 정확하게 해요."),
       ("AA⁻¹ = I 인지 직접 확인하려면?","행렬 곱셈 계산기에 A와 구한 A⁻¹을 넣어 곱해 보면 단위행렬이 나오는지 확인할 수 있어요.")]),
 dict(key="det", slug="determinant", label="행렬식",
  title="행렬식 계산기 - 여인수 전개·행 소거 풀이", h1="행렬식 계산기",
  meta="행렬식(determinant)을 분수로 정확하게 계산해요. 2×2는 공식, 3×3은 여인수 전개, 4×4 이상은 행 소거로 풀이 과정을 단계별로 보여드려요.",
  desc="2×2는 공식으로, 3×3은 여인수 전개로, 4×4 이상은 행 소거로 풀어요.",
  card="여인수 전개와 행 소거로 det(A) 구하기",
  ch="행렬식이란?",
  cb=["행렬식은 정사각행렬에 대응하는 하나의 수예요. 기하학적으로는 그 행렬이 넓이나 부피를 몇 배로 바꾸는지를 나타내요.",
      "행렬식이 0이면 역행렬이 없고, Ax = b의 해가 하나로 정해지지 않아요."],
  tip="두 행을 바꾸면 부호가 바뀌고, 한 행에 다른 행의 상수배를 더해도 값은 그대로예요.",
  faq=[("3×3 행렬식은 사러스 법칙으로 풀어도 되나요?","네, 결과는 같아요. 이 계산기는 4×4 이상으로도 이어지는 여인수 전개로 보여드려요."),
       ("행렬식이 음수면 무슨 뜻인가요?","행렬이 나타내는 변환이 방향(좌우)을 뒤집는다는 뜻이에요. 크기는 절댓값으로 봐요."),
       ("직사각행렬도 행렬식이 있나요?","아니요. 행렬식은 정사각행렬에서만 정의돼요.")]),
 dict(key="mul", slug="multiplication", label="곱셈",
  title="행렬 곱셈 계산기 - 성분별 계산 과정", h1="행렬 곱셈 계산기",
  meta="두 행렬의 곱 AB를 계산하고, 각 성분을 A의 행과 B의 열로 어떻게 구하는지 단계별로 보여주는 행렬 곱셈 계산기예요.",
  desc="AB의 각 성분을 A의 행과 B의 열로 어떻게 계산하는지 하나씩 보여드려요.",
  card="AB의 각 성분 계산 과정 보기",
  ch="행렬 곱셈의 규칙",
  cb=["A가 m×n, B가 n×p이면 AB는 m×p 행렬이에요. (AB)ᵢⱼ는 A의 i행과 B의 j열을 성분끼리 곱해 모두 더한 값이에요."],
  tip="A의 열 수와 B의 행 수가 같아야 곱할 수 있어요. 일반적으로 AB ≠ BA 예요.",
  faq=[("왜 B의 행 수가 자동으로 바뀌나요?","곱셈이 가능하려면 A의 열 수와 B의 행 수가 같아야 해서, A의 열을 바꾸면 B의 행이 함께 맞춰져요."),
       ("BA를 계산하려면?","A와 B에 들어갈 행렬을 서로 바꿔 입력하면 돼요.")]),
 dict(key="add", slug="addition", label="덧셈",
  title="행렬 덧셈 계산기", h1="행렬 덧셈 계산기",
  meta="크기가 같은 두 행렬의 합 A + B를 분수까지 정확하게 계산하고 성분별 과정을 보여주는 행렬 덧셈 계산기예요.",
  desc="크기가 같은 두 행렬을 같은 위치의 성분끼리 더해요.",
  card="같은 위치의 성분끼리 더하기",
  ch="행렬 덧셈", cb=["크기가 같은 두 행렬만 더할 수 있어요. 같은 위치에 있는 성분끼리 더하면 돼요."],
  tip="A + B = B + A 처럼 교환법칙과 결합법칙이 성립해요.",
  faq=[("크기가 다른 행렬은 더할 수 없나요?","네. 행과 열의 수가 모두 같아야 해요. 그래서 B의 크기는 A에 맞춰 자동으로 정해져요.")]),
 dict(key="sub", slug="subtraction", label="뺄셈",
  title="행렬 뺄셈 계산기", h1="행렬 뺄셈 계산기",
  meta="크기가 같은 두 행렬의 차 A − B를 분수까지 정확하게 계산하고 성분별 과정을 보여주는 행렬 뺄셈 계산기예요.",
  desc="크기가 같은 두 행렬을 같은 위치의 성분끼리 빼요.",
  card="같은 위치의 성분끼리 빼기",
  ch="행렬 뺄셈", cb=["크기가 같은 두 행렬만 뺄 수 있어요. A − B는 A + (−1)B 와 같아요."],
  tip="A − B ≠ B − A 이니 순서에 주의하세요.",
  faq=[("음수는 어떻게 입력하나요?","숫자 앞에 - 를 붙이면 돼요. 예: -3, -1/2")]),
 dict(key="scalar", slug="scalar-multiplication", label="스칼라배",
  title="행렬 스칼라배 계산기", h1="스칼라배 계산기",
  meta="행렬의 모든 성분에 수 k를 곱하는 스칼라배 kA를 분수까지 정확하게 계산하는 계산기예요.",
  desc="행렬의 모든 성분에 같은 수 k를 곱해요.",
  card="모든 성분에 k 곱하기",
  ch="스칼라배", cb=["kA는 A의 모든 성분에 k를 곱한 행렬이에요. 크기는 그대로예요."],
  tip="n×n 행렬이면 det(kA) = kⁿ·det(A) 예요.",
  faq=[("k에 분수를 넣어도 되나요?","네. 3/2 나 0.5 처럼 분수와 소수 모두 입력할 수 있어요.")]),
 dict(key="transpose", slug="transpose", label="전치",
  title="전치행렬 계산기", h1="전치행렬 계산기",
  meta="행렬의 행과 열을 바꾼 전치행렬 Aᵀ를 구하고 과정을 보여주는 전치행렬 계산기예요.",
  desc="행과 열을 맞바꿔 Aᵀ를 만들어요.",
  card="행과 열을 바꿔 Aᵀ 만들기",
  ch="전치행렬", cb=["Aᵀ는 A의 행과 열을 바꾼 행렬로, (Aᵀ)ᵢⱼ = Aⱼᵢ 예요. m×n 행렬의 전치는 n×m 행렬이에요.", "Aᵀ = A 이면 대칭행렬이라고 해요."],
  tip="(AB)ᵀ = BᵀAᵀ 처럼 곱의 전치는 순서가 뒤바뀌어요.",
  faq=[("대칭행렬인지 어떻게 확인하나요?","전치한 결과가 원래 행렬과 같으면 대칭행렬이에요.")]),
 dict(key="rref", slug="rref", label="RREF",
  title="RREF 계산기 - 기약 행사다리꼴 단계별 풀이", h1="RREF 계산기",
  meta="행렬을 기약 행사다리꼴(RREF)로 바꾸는 행 연산 과정을 단계별로 보여주고, 랭크와 피벗 열을 알려주는 RREF 계산기예요.",
  desc="행 연산으로 기약 행사다리꼴을 만들고 랭크와 피벗 열을 알려드려요.",
  card="기약 행사다리꼴과 랭크 구하기",
  ch="기약 행사다리꼴 (RREF)",
  cb=["각 행의 첫 번째 0이 아닌 성분(피벗)이 1이고, 피벗이 있는 열의 다른 성분이 모두 0인 형태예요. 영행은 맨 아래에 와요.",
      "어떤 행렬이든 RREF는 하나로 정해져서, 랭크나 연립방정식의 해를 판단할 때 기준이 돼요."],
  tip="피벗의 개수가 곧 행렬의 랭크예요.",
  faq=[("행사다리꼴(REF)과 기약 행사다리꼴(RREF)은 뭐가 다른가요?","REF는 피벗 아래만 0이면 되지만, RREF는 피벗이 1이고 피벗 위아래가 모두 0이어야 해요. REF는 여러 가지가 나올 수 있지만 RREF는 하나로 정해져요."),
       ("교재 풀이와 행 연산 순서가 달라요.","행 연산 순서는 사람마다 다를 수 있지만 최종 RREF는 항상 같아요.")]),
 dict(key="solve", slug="linear-system", label="연립방정식",
  title="연립방정식 행렬 계산기 - 가우스 소거법 풀이", h1="연립방정식 계산기",
  meta="Ax = b 연립일차방정식을 첨가행렬과 가우스-조던 소거법으로 풀고, 해가 하나인지·없는지·무수히 많은지 판단해 일반해까지 보여주는 계산기예요.",
  desc="Ax = b를 첨가행렬로 바꿔 소거하고, 해가 하나인지·없는지·무수히 많은지 판단해요.",
  card="Ax = b의 해와 일반해 구하기",
  ch="연립방정식과 첨가행렬",
  cb=["Ax = b를 첨가행렬 [A | b]로 쓰고 기약 행사다리꼴로 바꾸면 해를 바로 읽을 수 있어요.",
      "0 = (0이 아닌 수) 꼴의 행이 생기면 해가 없고, 피벗이 없는 변수(자유변수)가 있으면 해가 무수히 많아요."],
  tip="랭크 = 미지수 개수이고 모순이 없으면 해가 하나뿐이에요.",
  faq=[("식의 개수와 미지수 개수가 달라도 되나요?","네. 행(식)과 열(미지수)을 따로 조절할 수 있어요."),
       ("해가 무수히 많을 때 t는 무엇인가요?","자유변수를 나타내는 매개변수예요. t에 어떤 수를 넣어도 방정식을 만족하는 해가 돼요.")]),
]

# 검색 결과에 보이는 제목·설명 (제목은 사이트 이름 앞에서 30자 안쪽, 설명은 90자 안쪽으로)
SNIP = {
 "inverse": ("역행렬 계산기 - 분수로 정확하게, 풀이 과정까지", "역행렬을 분수로 정확하게 계산하고 가우스-조던 소거법의 행 연산을 한 단계씩 보여줘요. 2×2부터 6×6까지, 가입 없이 무료로 써요."),
 "det": ("행렬식 계산기 - 2×2부터 6×6, 풀이 과정까지", "행렬식을 분수로 정확하게 계산해요. 2×2 공식, 3×3 여인수 전개, 4×4 이상 행 소거까지 풀이 과정을 단계별로 보여줘요."),
 "mul": ("행렬 곱셈 계산기 - 성분별 계산 과정 보기", "두 행렬의 곱 AB를 계산하고, 각 성분을 A의 행과 B의 열로 어떻게 구하는지 보여줘요. 분수와 소수도 입력할 수 있어요."),
 "add": ("행렬 덧셈 계산기 - 분수까지 정확하게", "크기가 같은 두 행렬의 합 A + B를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요."),
 "sub": ("행렬 뺄셈 계산기 - 분수까지 정확하게", "크기가 같은 두 행렬의 차 A − B를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요."),
 "scalar": ("행렬 스칼라배 계산기 - kA를 바로 계산", "행렬의 모든 성분에 수 k를 곱한 kA를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요."),
 "transpose": ("전치행렬 계산기 - 행과 열을 바꿔 Aᵀ 구하기", "행렬의 행과 열을 바꾼 전치행렬 Aᵀ를 바로 구하고, 행이 어느 열로 옮겨지는지 단계별로 보여줘요."),
 "rref": ("RREF 계산기 - 기약 행사다리꼴과 랭크", "행렬을 기약 행사다리꼴(RREF)로 바꾸는 행 연산을 단계별로 보여주고, 랭크와 피벗 열까지 알려줘요."),
 "solve": ("연립방정식 행렬 계산기 - 해와 일반해까지", "Ax = b 연립방정식을 소거법으로 풀어 해가 하나인지, 없는지, 무수히 많은지 알려주고 일반해까지 보여줘요."),
}
for _o in OPS:
    _o["title"], _o["meta"] = SNIP[_o["key"]]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">'

def head(title, meta, path, extra=""):
    url = DOMAIN + path
    s = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(meta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F4FD8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/app.css">
'''
    if GOOGLE_VERIFY: s += f'<meta name="google-site-verification" content="{e(GOOGLE_VERIFY)}">\n'
    if NAVER_VERIFY: s += f'<meta name="naver-site-verification" content="{e(NAVER_VERIFY)}">\n'
    if ADSENSE_CLIENT: s += f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n'
    if GA_ID: s += f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>\n'
    return s + extra + "</head>\n"

def topbar(cur=""):
    items = [("calc", "/calculators/", "계산기"), ("guide", "/guide/", "가이드"), ("about", "/about/", "소개")]
    links = "".join(f'<a href="{h}"' + (' aria-current="page"' if k == cur else "") + f">{t}</a>" for k, h, t in items)
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="/"><span class="mark" aria-hidden="true">[ ]</span>{SITE}</a>
<nav class="top-nav" aria-label="사이트">{links}</nav>
</div></header>
'''

def footer():
    return f'''<footer class="wrap foot"><span>© 2026 {SITE}. 계산은 모두 브라우저 안에서 처리돼요.</span>
<nav aria-label="사이트 정보"><a href="/calculators/">계산기</a><a href="/guide/">가이드</a><a href="/about/">소개</a><a href="/about/#contact">문의</a><a href="/privacy/">개인정보처리방침</a></nav></footer>
'''

def ad():
    if not (ADSENSE_CLIENT and AD_SLOT): return ""
    return f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>\n'

def opsnav(cur, home=False):
    out = []
    for o in OPS:
        a = ""
        if o["key"] == cur: a = ' class="on"' if home else ' aria-current="page"'
        out.append(f'<a href="/{o["slug"]}/"{a}>{o["label"]}</a>')
    return '<nav class="ops" aria-label="연산 선택">' + "".join(out) + "</nav>"

CALC = '''<div class="work">
<section class="panel in" aria-labelledby="inH">
<div class="panel-head"><h2 id="inH">입력</h2><div class="acts"><button type="button" class="ghost" id="exBtn">예제 넣기</button><button type="button" class="ghost" id="clrBtn">모두 지우기</button></div></div>
<div id="inputs"><noscript><p class="err">계산기를 쓰려면 브라우저에서 자바스크립트를 켜 주세요.</p></noscript></div>
<p class="hint">정수, 분수(<code>1/3</code>), 소수(<code>0.25</code>)를 쓸 수 있어요. 빈칸은 0이에요.</p>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">결과</h2><div class="seg" role="group" aria-label="숫자 표시 방식"><button type="button" data-mode="frac" aria-pressed="true">분수</button><button type="button" data-mode="dec" aria-pressed="false">소수</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="copyTex">LaTeX 복사</button></div>
</section>
</div>
<details class="fold steps-fold" id="stepsD" hidden><summary><h2>단계별 풀이 보기</h2><span class="cnt" id="stepCount"></span></summary>
<div class="fold-b"><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div></details>
'''

HOWTO = '''<ol class="howto">
<li>행·열 버튼으로 행렬 크기를 정해요. 최대 6×6까지 입력할 수 있어요.</li>
<li>칸에 숫자를 입력하면 바로 계산돼요. 분수는 <code>1/3</code>, 음수는 <code>-2</code>처럼 입력해요.</li>
<li><kbd>Enter</kbd>는 다음 칸, <kbd>↑</kbd> <kbd>↓</kbd>는 위아래 칸으로 이동해요.</li>
<li>‘단계별 풀이 보기’를 누르면 계산 과정이 펼쳐지고, ‘LaTeX 복사’로 과제에 붙여넣을 수 있어요.</li>
</ol>'''

# 계산기 → 관련 가이드
GUIDE_FOR = {"inverse": "inverse-gauss-jordan", "det": "determinant-3x3", "rref": "rank-and-rref", "solve": "linear-system-solutions",
             "mul": "matrix-multiplication", "add": "matrix-add-subtract-scalar", "sub": "matrix-add-subtract-scalar",
             "scalar": "matrix-add-subtract-scalar", "transpose": "matrix-transpose-properties"}
GUIDES_FOR = {
    "inverse": ["inverse-gauss-jordan", "inverse-adjugate-cofactor", "elementary-matrices"],
    "det": ["determinant-3x3", "determinant-properties", "cramer-rule", "eigenvalues-2x2"],
    "mul": ["matrix-multiplication", "elementary-matrices", "special-matrices"],
    "add": ["matrix-add-subtract-scalar", "matrix-multiplication"],
    "sub": ["matrix-add-subtract-scalar", "matrix-multiplication"],
    "scalar": ["matrix-add-subtract-scalar", "matrix-multiplication"],
    "transpose": ["matrix-transpose-properties", "special-matrices"],
    "rref": ["rank-and-rref", "null-space-column-space", "linear-independence"],
    "solve": ["linear-system-solutions", "cramer-rule", "rank-and-rref"],
}

def fold(title, body, cls=""):
    return f'<details class="fold {cls}"><summary><h2>{title}</h2></summary><div class="fold-b">{body}</div></details>\n'

def extras(o):
    """계산기 아래 접이식 설명. 기본은 모두 접혀 있고, 사용자가 열 때만 보여요."""
    g = guides.BY_SLUG.get(GUIDE_FOR.get(o["key"], ""))
    more = f'<p><a href="/guide/{g["slug"]}/">자세한 설명과 예제: {e(g["title"])}</a></p>' if g else ""
    concept = "".join(f"<p>{e(x)}</p>" for x in o["cb"]) + more + f'<p class="tip"><b>시험 팁</b>{e(o["tip"])}</p>'
    qa = "".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in o["faq"])
    rel = "".join(f'<li><a href="/guide/{x}/">{e(guides.BY_SLUG[x]["h1"])}</a><span>{e(guides.BY_SLUG[x]["desc"])}</span></li>' for x in GUIDES_FOR.get(o["key"], []))
    return ('<section class="extras" aria-label="더 알아보기">\n' + fold(e(o["ch"]), concept) + fold("사용 방법", HOWTO)
            + fold("자주 묻는 질문", f'<dl class="qa">{qa}</dl>')
            + (fold("관련 가이드", f'<ul class="rel-list">{rel}</ul>') if rel else "") + "</section>\n")

def guide_page(g):
    path = f'/guide/{g["slug"]}/'
    ldj = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "inLanguage": "ko",
           "description": g["meta"], "datePublished": g.get("published", FIRST_PUBLISHED), "dateModified": TODAY,
           "author": {"@type": "Organization", "name": SITE}, "publisher": {"@type": "Organization", "name": SITE},
           "mainEntityOfPage": DOMAIN + path}
    s = head(g["title"] + " | " + SITE, g["meta"], path, '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + "</script>\n" + crumbs([("홈", "/"), ("가이드", "/guide/"), (g["h1"], path)]))
    s += "<body>\n" + topbar("guide") + '<main class="wrap"><article class="doc guide">'
    s += f'<p class="crumb"><a href="/guide/">가이드</a></p><h1>{e(g["h1"])}</h1><p class="meta">{TODAY} 업데이트 · 읽는 시간 약 {g["min"]}분</p>'
    s += g["body"]
    s += f'<div class="cta-box"><div><b>직접 계산해 보세요</b><span>값을 바꾸면 결과와 단계별 풀이가 바로 나와요.</span></div><a class="cta" href="{g["calc"][1]}">{e(g["calc"][0])} 열기</a></div>'
    rel = [guides.BY_SLUG[x] for x in g["related"]]
    s += '<h2>함께 보면 좋은 글</h2><ul class="rel">' + "".join(f'<li><a href="/guide/{r["slug"]}/">{e(r["h1"])}</a></li>' for r in rel) + "</ul>"
    s += "</article></main>\n" + footer() + "</body>\n</html>\n"
    write(path, s)

def guide_index():
    body = '<h1>가이드</h1><p class="meta">시험 범위에서 자주 헷갈리는 개념을 예제와 함께 정리했어요.</p>'
    body += '<div class="grid-ops guide-list">' + "".join(
        f'<a href="/guide/{g["slug"]}/"><b>{e(g["h1"])}</b><span>{e(g["desc"])}</span></a>' for g in guides.ARTICLES) + "</div>"
    s = head("행렬 가이드 | " + SITE, "역행렬, 행렬식, 랭크와 RREF, 연립방정식의 해를 예제와 함께 단계별로 설명한 선형대수 가이드 모음이에요.", "/guide/") + "<body>\n" + topbar("guide")
    s += f'<main class="wrap"><article class="doc guide">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write("/guide/", s)

def ld(o, path):
    d = {"@context": "https://schema.org", "@type": "WebApplication", "name": o["h1"], "url": DOMAIN + path,
         "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ko",
         "description": o["meta"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def crumbs(items):
    d = {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(items)]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def website_ld():
    d = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "alternateName": ["matrixstep", "MatrixStep"], "url": DOMAIN + "/", "inLanguage": "ko"}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def write(path, text):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/") or path.endswith("/"): full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)

PAGE_END = '<div class="toast" id="toast" role="status" hidden></div>\n<script src="/assets/app.js" defer></script>\n</body>\n</html>\n'

def op_page(o):
    """계산기 페이지: 제목 → 연산 선택 → 계산기·결과. 나머지는 접이식."""
    path = f'/{o["slug"]}/'
    s = head(o["title"] + " | " + SITE, o["meta"], path, ld(o, path) + crumbs([("홈", "/"), ("계산기", "/calculators/"), (o["h1"], path)]))
    s += f'<body data-op="{o["key"]}">\n' + topbar("calc") + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{e(o["h1"])}</h1><p>{e(o["desc"])}</p></div>\n' + opsnav(o["key"]) + "\n" + CALC + ad()
    s += extras(o) + "</main>\n" + footer() + PAGE_END
    write(path, s)

def home_extras():
    ops = " · ".join(f'<a href="/{o["slug"]}/">{o["label"]}</a>' for o in OPS)
    about = (f"<p>{SITE}는 대학 선형대수에서 자주 쓰는 행렬 계산을 분수로 정확하게 풀고, 풀이 과정을 단계별로 보여주는 무료 계산기예요. "
             "반올림 오차 없이 1/3 같은 정확한 값으로 계산하고, 결과 행렬은 LaTeX로 복사할 수 있어요.</p>"
             f"<p>제공하는 계산기: {ops}</p>"
             '<p><a href="/calculators/">모든 계산기 보기</a> · <a href="/guide/">개념 가이드 보기</a></p>')
    qa = [("몇 × 몇 행렬까지 계산할 수 있나요?", "최대 6×6까지 입력할 수 있어요. 곱셈과 연립방정식은 계산기마다 가능한 크기가 조금씩 달라요."),
          ("계산 결과는 정확한가요?", "모든 값을 분수로 저장해 계산하기 때문에 반올림 오차가 생기지 않아요. 소수 버튼은 보여주는 방식만 바꿔요."),
          ("입력한 행렬이 서버로 전송되나요?", "아니요. 계산은 모두 브라우저 안에서 이루어지고 입력값은 어디에도 전송되지 않아요.")]
    dl = "".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in qa)
    return ('<section class="extras" aria-label="더 알아보기">\n' + fold(f"{SITE} 소개", about) + fold("사용 방법", HOWTO)
            + fold("자주 묻는 질문", f'<dl class="qa">{dl}</dl>') + "</section>\n")

def home():
    meta = "역행렬, 행렬식, 곱셈, RREF, 연립방정식을 분수로 정확하게 계산하고 풀이 과정을 단계별로 보여주는 깔끔한 무료 행렬 계산기예요."
    s = head(f"{SITE} - 역행렬·행렬식·RREF를 분수로 정확하게", meta, "/", website_ld() + ld(dict(h1=SITE, meta=meta), "/"))
    s += '<body data-op="inverse">\n' + topbar() + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{SITE}</h1><p>역행렬부터 연립방정식까지, 분수로 정확하게 계산하고 풀이 과정을 보여드려요.</p></div>\n'
    s += opsnav("inverse", home=True) + "\n" + CALC + ad() + home_extras() + "</main>\n" + footer() + PAGE_END
    write("/", s)

# 계산기 모음 페이지(/calculators/)
GROUPS = [("기본 연산", ["add", "sub", "scalar", "mul", "transpose"]),
          ("역행렬과 행렬식", ["inverse", "det"]),
          ("소거법과 연립방정식", ["rref", "solve"])]

def calc_hub():
    by = {o["key"]: o for o in OPS}
    meta = "덧셈·뺄셈·스칼라배·곱셈·전치부터 역행렬, 행렬식, RREF, 연립방정식까지 행렬 계산기 9종을 한곳에 모았어요. 모두 분수로 정확하게 계산하고 풀이 과정을 보여줘요."
    ldj = {"@context": "https://schema.org", "@type": "ItemList", "name": "행렬 계산기 모음",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{DOMAIN}/{o["slug"]}/', "name": o["h1"]} for i, o in enumerate(OPS)]}
    s = head("행렬 계산기 모음 - 9가지 연산 | " + SITE, meta, "/calculators/", '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + "</script>\n")
    s += "<body>\n" + topbar("calc") + '<main class="wrap">\n'
    s += '<div class="intro"><h1>행렬 계산기 모음</h1><p>필요한 연산을 골라 바로 계산해 보세요. 개념이 헷갈리면 <a href="/guide/">가이드</a>도 있어요.</p></div>\n'
    for title, keys in GROUPS:
        s += f'<section class="hub-g"><h2>{title}</h2><div class="grid-ops">'
        s += "".join(f'<a href="/{by[k]["slug"]}/"><b>{by[k]["h1"]}</b><span>{e(by[k]["card"])}</span></a>' for k in keys)
        s += "</div></section>\n"
    s += "</main>\n" + footer() + "</body>\n</html>\n"
    write("/calculators/", s)

def doc_page(path, title, meta, body, cur=""):
    s = head(title + " | " + SITE, meta, path) + "<body>\n" + topbar(cur)
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write(path, s)

def about():
    ncal, ngd = len(OPS), len(guides.ARTICLES)
    body = f'''<h1>{SITE} 소개</h1><p class="meta">마지막 업데이트 {TODAY}</p>
<p>{SITE}(matrixstep.net)는 대학 선형대수와 공업수학 수업에서 자주 쓰는 행렬 계산을 깔끔한 화면에서 할 수 있도록 만든 무료 도구예요. 기능을 넓게 늘리기보다 행렬 계산 하나에 집중해, 정확한 답과 읽기 쉬운 풀이 과정을 보여주는 것을 목표로 해요. 가입이나 설치 없이 바로 쓸 수 있어요.</p>
<h2>왜 만들었나요</h2>
<p>행렬 문제는 답보다 과정이 중요한데, 기존 계산기는 답만 보여주거나 소수로 반올림해 손으로 푼 풀이와 비교하기 어려웠어요. 또 광고와 메뉴가 많아 정작 계산기를 찾기 힘든 경우도 많았고요. 그래서 계산기와 결과만 먼저 보이고, 설명은 필요할 때 펼쳐 보는 단순한 페이지로 만들었어요.</p>
<h2>어떻게 계산하나요</h2><ul>
<li><strong>분수로 정확한 계산</strong>: 모든 값을 정수 분자·분모로 저장해 계산해요. 0.3333… 같은 반올림 오차 없이 1/3처럼 정확한 값이 나오고, 소수 표시는 보여주는 방식만 바꿔요.</li>
<li><strong>교과서와 같은 방법</strong>: 역행렬과 RREF는 가우스-조던 소거법, 행렬식은 2×2 공식·3×3 여인수 전개·4×4 이상은 행 소거로 계산해요. 수업에서 배우는 순서 그대로예요.</li>
<li><strong>단계별 풀이</strong>: 행 연산 하나하나와 그때의 행렬을 순서대로 보여줘서, 어디서 계산이 틀렸는지 바로 찾을 수 있어요.</li>
<li><strong>브라우저 안에서만 계산</strong>: 입력한 행렬은 서버로 전송되지 않아요. 계산은 모두 사용 중인 브라우저에서 이루어져요.</li>
<li><strong>LaTeX 복사</strong>: 결과 행렬을 LaTeX 코드로 복사해 과제나 노트에 바로 붙여넣을 수 있어요.</li></ul>
<h2>정확성은 어떻게 확인하나요</h2>
<p>계산기 코드는 배포할 때마다 자동 검사를 거쳐요. 무작위로 만든 행렬 1,700여 개를 계산기와 똑같이 풀게 한 뒤, 별도로 작성한 분수 계산 코드로 역행렬은 원래 행렬과 곱해 단위행렬이 되는지, 연립방정식의 해는 원래 식에 대입해 맞는지, 행렬식과 RREF는 독립 계산 결과와 같은지 확인해요. 검사를 통과하지 못하면 배포되지 않아요. 가이드에 실린 예제도 글을 쓸 때 같은 방식으로 다시 계산해 숫자를 맞춘 뒤 올려요. 그래도 틀린 곳을 발견하면 아래 이메일로 알려 주세요. 입력한 행렬을 함께 적어 주시면 빠르게 확인하고 고칠 수 있어요.</p>
<h2>제공하는 계산기 {ncal}종</h2><ul>{"".join(f'<li><a href="/{o["slug"]}/">{o["h1"]}</a> · {e(o["card"])}</li>' for o in OPS)}</ul>
<h2>가이드 {ngd}편</h2>
<p>계산기만으로는 부족한 개념은 <a href="/guide/">가이드</a>에서 예제와 함께 설명해요. 역행렬과 행렬식 같은 기본부터 랭크, 영공간, 선형독립, 고윳값까지, 시험에서 자주 헷갈리는 순서로 정리했어요. 모든 글은 직접 손으로 따라 풀 수 있는 작은 예제로 시작하고, 마지막에는 계산기로 바로 확인할 수 있게 이어져요.</p>
<h2>운영 원칙</h2><ul>
<li>계산기 화면에는 계산기와 결과만 두고, 설명과 광고가 계산을 가리지 않게 해요.</li>
<li>기능을 추가할 때는 "선형대수 수업에서 실제로 쓰는가"를 기준으로 골라요.</li>
<li>사이트는 무료로 운영하고, 비용은 광고로 충당해요. 광고는 계산 결과 아래에만 배치해요.</li></ul>
<h2 id="contact">문의</h2>
<p>오류 제보, 기능 제안, 제휴 문의는 아래 이메일로 보내 주세요.</p>
<p><strong>{e(EMAIL)}</strong></p>
<p>운영자: {e(OPERATOR)} · <a href="/privacy/">개인정보처리방침</a></p>'''
    doc_page("/about/", "소개 및 문의", f"{SITE}가 행렬을 분수로 정확하게 계산하는 방법, 결과를 검증하는 방식, 제공하는 계산기 {ncal}종과 가이드 {ngd}편, 문의 방법을 안내해요.", body, "about")

def privacy():
    body = f'''<h1>개인정보처리방침</h1><p class="meta">시행일 {PRIVACY_DATE}</p>
<p>{e(OPERATOR)}(이하 ‘운영자’)는 {SITE}(이하 ‘사이트’)를 이용하는 분의 개인정보를 소중히 여기며, 「개인정보 보호법」 등 관련 법령을 지켜요. 이 방침은 사이트가 어떤 정보를 어떻게 다루는지 알려드려요.</p>
<h2>1. 수집하는 개인정보</h2>
<p>사이트는 회원가입 없이 이용할 수 있고, 이름·연락처 같은 개인정보를 직접 수집하지 않아요. 계산을 위해 입력한 행렬 값은 이용자의 브라우저 안에서만 처리되며 운영자의 서버로 전송되지 않아요.</p>
<h2>2. 브라우저에 저장되는 정보</h2>
<p>다른 계산기로 이동해도 입력값이 유지되도록, 입력한 행렬을 브라우저의 세션 저장소(sessionStorage)에 임시로 저장해요. 이 정보는 브라우저 탭을 닫으면 사라져요. 분수·소수 표시 설정은 브라우저의 로컬 저장소(localStorage)에 저장돼요. 이 정보들은 이용자의 기기에만 남고 운영자에게 전달되지 않아요.</p>
<h2>3. 자동으로 수집되는 정보</h2>
<p>사이트를 제공하는 호스팅 서비스(Amazon Web Services)는 보안과 서비스 안정성을 위해 접속 IP 주소, 브라우저 종류, 접속 시간 같은 접속 기록을 자동으로 남길 수 있어요.</p>
<h2>4. 쿠키와 외부 서비스</h2>
<p>사이트는 방문 통계 분석을 위해 Google Analytics를, 광고 게재를 위해 Google AdSense를 이용하거나 이용할 수 있어요. 이 서비스들은 쿠키를 사용해 방문 기록을 바탕으로 통계를 내거나, 이용자의 관심사에 맞는 광고를 보여줄 수 있어요.</p>
<ul><li>Google을 포함한 제3자 광고 사업자는 쿠키를 사용해 이용자의 이 사이트 및 다른 사이트 방문 기록을 기반으로 광고를 게재해요.</li>
<li>맞춤 광고는 <a href="https://adssettings.google.com" rel="noopener">Google 광고 설정</a>에서 끌 수 있어요.</li>
<li>Google이 정보를 이용하는 방식은 <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">Google 파트너 사이트 정책</a>에서 확인할 수 있어요.</li>
<li>브라우저 설정에서 쿠키 저장을 거부하거나 삭제할 수 있어요. 다만 일부 기능이나 광고 표시가 달라질 수 있어요.</li></ul>
<h2>5. 개인정보의 보유 및 파기</h2>
<p>운영자는 개인정보를 직접 보관하지 않아요. 이메일로 문의하신 경우, 받은 이메일 주소와 문의 내용은 답변을 마친 뒤 지체 없이 삭제해요.</p>
<h2>6. 이용자의 권리</h2>
<p>이용자는 언제든지 자신의 개인정보 처리에 대해 열람, 정정, 삭제, 처리 정지를 요청할 수 있어요. 아래 문의처로 연락해 주세요.</p>
<h2>7. 개인정보 보호 책임자 및 문의처</h2>
<p>책임자: {e(OPERATOR)}<br>이메일: {e(EMAIL)}</p>
<p>개인정보 침해에 대한 상담이 필요하면 개인정보침해신고센터(privacy.kisa.or.kr, 국번 없이 118)에 문의할 수 있어요.</p>
<h2>8. 방침의 변경</h2>
<p>이 방침이 바뀌면 사이트에서 시행일과 함께 알려드려요.</p>'''
    doc_page("/privacy/", "개인정보처리방침", f"{SITE}의 개인정보처리방침이에요.", body)

def notfound():
    body = '<h1>페이지를 찾을 수 없어요</h1><p>주소가 바뀌었거나 없는 페이지예요. 아래에서 원하는 계산기를 골라 주세요.</p><ul>' + "".join(f'<li><a href="/{o["slug"]}/">{o["h1"]}</a></li>' for o in OPS) + "</ul>"
    s = head("페이지를 찾을 수 없어요 | " + SITE, "요청한 페이지가 없어요.", "/404.html", '<meta name="robots" content="noindex">\n') + "<body>\n" + topbar()
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(s)

def seo_files():
    urls = ["/", "/calculators/"] + [f'/{o["slug"]}/' for o in OPS] + ["/guide/"] + [f'/guide/{g["slug"]}/' for g in guides.ARTICLES] + ["/about/", "/privacy/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    if ADSENSE_CLIENT:
        pub = ADSENSE_CLIENT.replace("ca-", "")
        open(os.path.join(OUT, "ads.txt"), "w").write(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(HERE, "static")):
        shutil.copy(os.path.join(HERE, "static", f), OUT)
    home(); calc_hub()
    for o in OPS: op_page(o)
    guide_index()
    for g in guides.ARTICLES: guide_page(g)
    about(); privacy(); notfound(); seo_files()
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    main()
