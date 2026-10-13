#!/usr/bin/env python3
"""행렬 계산기 정적 사이트 생성기. 설정을 바꾼 뒤 `python3 build.py` → dist/ 폴더가 배포본.
표준 라이브러리만 써서 Amplify 빌드 환경에서 그대로 돌아가요."""
import os, shutil, json, html, datetime

# ===================== 설정 =====================
DOMAIN = "https://matrixstep.net"  # 끝에 / 없이
SITE = "행렬 계산기"
EMAIL = "contact@example.com"    # 문의 이메일
OPERATOR = "행렬 계산기 운영자"     # 개인정보처리방침에 들어갈 운영자 이름
ADSENSE_CLIENT = ""              # 예: "ca-pub-1234567890123456"
AD_SLOT = ""                     # 애드센스 광고 단위 ID (승인 후)
GA_ID = ""                       # 예: "G-XXXXXXXXXX"
GOOGLE_VERIFY = ""               # Search Console HTML 태그 content 값
NAVER_VERIFY = ""                # 네이버 서치어드바이저 HTML 태그 content 값
TODAY = datetime.date(2026, 10, 13).isoformat()
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

def topbar():
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="/"><span class="mark" aria-hidden="true">[ ]</span>{SITE}</a>
<nav class="top-nav" aria-label="사이트"><a href="/#all">모든 계산기</a><a href="/about/">소개</a></nav>
</div></header>
'''

def footer():
    return f'''<footer class="wrap foot"><span>© 2026 {SITE}. 모든 계산은 브라우저 안에서 처리되고 입력값은 전송되지 않아요.</span>
<nav aria-label="사이트 정보"><a href="/about/">소개</a><a href="/about/#contact">문의</a><a href="/privacy/">개인정보처리방침</a></nav></footer>
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
<p class="hint">정수, 분수(<code>1/3</code>), 소수(<code>0.25</code>)를 입력할 수 있어요. 빈칸은 0으로 계산해요. <kbd>Enter</kbd> 다음 칸 · <kbd>↑</kbd><kbd>↓</kbd> 위아래 칸</p>
<div class="photo"><div class="photo-t"><svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg><div><strong>사진으로 행렬 입력</strong><span>교재나 필기 사진에서 숫자를 읽어 칸을 채워요</span></div></div><span class="soon">준비 중</span></div>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">결과</h2><div class="seg" role="group" aria-label="숫자 표시 방식"><button type="button" data-mode="frac" aria-pressed="true">분수</button><button type="button" data-mode="dec" aria-pressed="false">소수</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="copyTex">LaTeX 복사</button></div>
<div class="steps"><h3>단계별 풀이</h3><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div>
</section>
</div>
'''

HOWTO = '''<section class="more-sec" aria-labelledby="howH"><h2 id="howH">사용 방법</h2><ol class="howto">
<li>행·열 버튼으로 행렬 크기를 정해요. 최대 6×6까지 입력할 수 있어요.</li>
<li>칸에 숫자를 입력하면 바로 계산돼요. 분수는 <code>1/3</code>, 음수는 <code>-2</code>처럼 입력해요.</li>
<li>오른쪽 ‘단계별 풀이’에서 과정을 확인하고, 필요하면 ‘LaTeX 복사’로 과제에 붙여넣어요.</li>
</ol></section>
'''

def concept(o):
    return (f'<section class="concept" aria-labelledby="cH"><h2 id="cH">{e(o["ch"])}</h2><div class="body">'
            + "".join(f"<p>{e(x)}</p>" for x in o["cb"])
            + f'</div><div class="tip"><b>시험 팁</b>{e(o["tip"])}</div></section>\n')

def faq(o):
    return ('<section class="more-sec" aria-labelledby="fH"><h2 id="fH">자주 묻는 질문</h2><div class="faq">'
            + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in o["faq"])
            + "</div></section>\n")

def grid():
    return ('<section class="more-sec" id="all" aria-labelledby="gH"><h2 id="gH">모든 계산기</h2><div class="grid-ops">'
            + "".join(f'<a href="/{o["slug"]}/"><b>{o["h1"]}</b><span>{e(o["card"])}</span></a>' for o in OPS)
            + "</div></section>\n")

def ld(o, path):
    d = {"@context": "https://schema.org", "@type": "WebApplication", "name": o["h1"], "url": DOMAIN + path,
         "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ko",
         "description": o["meta"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def write(path, text):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/") or path.endswith("/"): full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)

def op_page(o):
    path = f'/{o["slug"]}/'
    s = head(o["title"] + " | " + SITE, o["meta"], path, ld(o, path))
    s += f'<body data-op="{o["key"]}">\n' + topbar() + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{e(o["h1"])}</h1><p>{e(o["desc"])}</p></div>\n' + opsnav(o["key"]) + "\n" + CALC + ad()
    s += concept(o) + HOWTO + faq(o) + grid() + "</main>\n" + footer()
    s += '<div class="toast" id="toast" role="status" hidden></div>\n<script src="/assets/app.js" defer></script>\n</body>\n</html>\n'
    write(path, s)

def home():
    o = OPS[0]
    meta = "역행렬, 행렬식, 행렬 곱셈, RREF, 연립방정식까지. 분수로 정확하게 계산하고 풀이 과정을 단계별로 보여주는 깔끔한 무료 행렬 계산기예요."
    s = head(f"{SITE} - 역행렬·행렬식·RREF 단계별 풀이", meta, "/",
             ld(dict(h1=SITE, meta=meta), "/"))
    s += '<body data-op="inverse">\n' + topbar() + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{SITE}</h1><p>역행렬부터 연립방정식까지, 분수로 정확하게 계산하고 풀이 과정을 단계별로 보여드려요. 아래는 역행렬 계산기예요. 다른 연산은 버튼을 눌러 바꿀 수 있어요.</p></div>\n'
    s += opsnav("inverse", home=True) + "\n" + CALC + ad() + grid() + concept(o) + HOWTO
    s += "</main>\n" + footer()
    s += '<div class="toast" id="toast" role="status" hidden></div>\n<script src="/assets/app.js" defer></script>\n</body>\n</html>\n'
    write("/", s)

def doc_page(path, title, meta, body):
    s = head(title + " | " + SITE, meta, path) + "<body>\n" + topbar()
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write(path, s)

def about():
    body = f'''<h1>{SITE} 소개</h1><p class="meta">마지막 업데이트 {TODAY}</p>
<p>{SITE}는 대학 선형대수와 공업수학 수업에서 자주 쓰는 행렬 계산을 깔끔한 화면에서 할 수 있도록 만든 무료 도구예요. 기능을 넓게 늘리기보다 행렬 계산 하나에 집중해 정확하고 읽기 쉬운 풀이를 보여주는 것을 목표로 해요.</p>
<h2>특징</h2><ul>
<li><strong>분수로 정확한 계산</strong>: 0.3333… 같은 반올림 오차 없이 1/3처럼 정확한 값으로 계산해요.</li>
<li><strong>단계별 풀이</strong>: 행 연산 하나하나와 그때의 행렬을 순서대로 보여줘서 손으로 푼 과정과 비교할 수 있어요.</li>
<li><strong>개인정보 걱정 없음</strong>: 모든 계산은 사용자의 브라우저 안에서 이루어지고, 입력한 행렬은 서버로 전송되지 않아요.</li>
<li><strong>LaTeX 복사</strong>: 결과 행렬을 LaTeX 코드로 복사해 과제나 노트에 바로 붙여넣을 수 있어요.</li></ul>
<h2>제공하는 계산기</h2><ul>{"".join(f'<li><a href="/{o["slug"]}/">{o["h1"]}</a> · {e(o["card"])}</li>' for o in OPS)}</ul>
<h2 id="contact">문의</h2>
<p>오류 제보, 기능 제안, 제휴 문의는 아래 이메일로 보내 주세요. 계산 결과가 틀렸다면 입력한 행렬을 함께 적어 주시면 빠르게 확인할 수 있어요.</p>
<p><strong>{e(EMAIL)}</strong></p>'''
    doc_page("/about/", "소개 및 문의", f"{SITE}의 특징과 제공하는 계산기, 문의 방법을 안내해요.", body)

def privacy():
    body = f'''<h1>개인정보처리방침</h1><p class="meta">시행일 {TODAY}</p>
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
    urls = ["/"] + [f'/{o["slug"]}/' for o in OPS] + ["/about/", "/privacy/"]
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
    home()
    for o in OPS: op_page(o)
    about(); privacy(); notfound(); seo_files()
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    main()
