#!/usr/bin/env python3
"""행렬 계산기 정적 사이트 생성기. 설정을 바꾼 뒤 `python3 build.py` → dist/ 폴더가 배포본.
표준 라이브러리만 써서 Amplify 빌드 환경에서 그대로 돌아가요.

한국어 페이지는 /, 영어 페이지는 /en/ 아래에 만들어요. 페이지 함수들은 현재 언어 설정 L을 읽어요."""
import os, re, shutil, json, html, datetime
import guides, guides_en

# ===================== 설정 =====================
DOMAIN = "https://matrixstep.net"  # 끝에 / 없이
SITE = "행렬 계산기"
SITE_EN = "MatrixStep"
EMAIL = "hunni1048@gmail.com"        # 문의 이메일
OPERATOR = "김현서"                 # 개인정보처리방침에 들어갈 운영자 이름
OPERATOR_EN = "Hyunseo Kim"
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

def _ver(name):
    """파일 내용 해시로 캐시를 깨요. 배포 직후에도 브라우저가 옛 파일을 쓰지 않게."""
    import hashlib
    with open(os.path.join(HERE, "assets", name), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]
CSS_URL = "/assets/app.css?v=" + _ver("app.css")
JS_URL = "/assets/app.js?v=" + _ver("app.js")

def practice_js():
    """app.js의 계산 핵심부(const ORDER= 앞까지) + practice.src.js 를 합쳐 하나의 스크립트로 만들어요."""
    src = open(os.path.join(HERE, "assets", "app.js"), encoding="utf-8").read()
    cut = src.index("const ORDER=")
    core = src[:cut]
    extra = open(os.path.join(HERE, "assets", "practice.src.js"), encoding="utf-8").read()
    return core + extra + "\n})();\n"
PRACTICE_JS = practice_js()
PRACTICE_URL = "/assets/practice.js?v=" + __import__("hashlib").sha1(PRACTICE_JS.encode()).hexdigest()[:8]
OUT = os.path.join(HERE, "dist")
e = html.escape

# ===================== 계산기 내용 (한국어) =====================
OPS_KO = [
 dict(key="inverse", slug="inverse", label="역행렬",
  title="역행렬 계산기 - 분수로 정확하게, 풀이 과정까지", h1="역행렬 계산기",
  meta="역행렬을 분수로 정확하게 계산하고 가우스-조던 소거법의 행 연산을 한 단계씩 보여줘요. 2×2부터 6×6까지, 가입 없이 무료로 써요.",
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
  title="행렬식 계산기 - 2×2부터 6×6, 풀이 과정까지", h1="행렬식 계산기",
  meta="행렬식을 분수로 정확하게 계산해요. 2×2 공식, 3×3 여인수 전개, 4×4 이상 행 소거까지 풀이 과정을 단계별로 보여줘요.",
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
  title="행렬 곱셈 계산기 - 성분별 계산 과정 보기", h1="행렬 곱셈 계산기",
  meta="두 행렬의 곱 AB를 계산하고, 각 성분을 A의 행과 B의 열로 어떻게 구하는지 보여줘요. 분수와 소수도 입력할 수 있어요.",
  desc="AB의 각 성분을 A의 행과 B의 열로 어떻게 계산하는지 하나씩 보여드려요.",
  card="AB의 각 성분 계산 과정 보기",
  ch="행렬 곱셈의 규칙",
  cb=["A가 m×n, B가 n×p이면 AB는 m×p 행렬이에요. (AB)ᵢⱼ는 A의 i행과 B의 j열을 성분끼리 곱해 모두 더한 값이에요."],
  tip="A의 열 수와 B의 행 수가 같아야 곱할 수 있어요. 일반적으로 AB ≠ BA 예요.",
  faq=[("왜 B의 행 수가 자동으로 바뀌나요?","곱셈이 가능하려면 A의 열 수와 B의 행 수가 같아야 해서, A의 열을 바꾸면 B의 행이 함께 맞춰져요."),
       ("BA를 계산하려면?","A와 B에 들어갈 행렬을 서로 바꿔 입력하면 돼요.")]),
 dict(key="add", slug="addition", label="덧셈",
  title="행렬 덧셈 계산기 - 분수까지 정확하게", h1="행렬 덧셈 계산기",
  meta="크기가 같은 두 행렬의 합 A + B를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요.",
  desc="크기가 같은 두 행렬을 같은 위치의 성분끼리 더해요.",
  card="같은 위치의 성분끼리 더하기",
  ch="행렬 덧셈", cb=["크기가 같은 두 행렬만 더할 수 있어요. 같은 위치에 있는 성분끼리 더하면 돼요."],
  tip="A + B = B + A 처럼 교환법칙과 결합법칙이 성립해요.",
  faq=[("크기가 다른 행렬은 더할 수 없나요?","네. 행과 열의 수가 모두 같아야 해요. 그래서 B의 크기는 A에 맞춰 자동으로 정해져요.")]),
 dict(key="sub", slug="subtraction", label="뺄셈",
  title="행렬 뺄셈 계산기 - 분수까지 정확하게", h1="행렬 뺄셈 계산기",
  meta="크기가 같은 두 행렬의 차 A − B를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요.",
  desc="크기가 같은 두 행렬을 같은 위치의 성분끼리 빼요.",
  card="같은 위치의 성분끼리 빼기",
  ch="행렬 뺄셈", cb=["크기가 같은 두 행렬만 뺄 수 있어요. A − B는 A + (−1)B 와 같아요."],
  tip="A − B ≠ B − A 이니 순서에 주의하세요.",
  faq=[("음수는 어떻게 입력하나요?","숫자 앞에 - 를 붙이면 돼요. 예: -3, -1/2")]),
 dict(key="scalar", slug="scalar-multiplication", label="스칼라배",
  title="행렬 스칼라배 계산기 - kA를 바로 계산", h1="스칼라배 계산기",
  meta="행렬의 모든 성분에 수 k를 곱한 kA를 분수까지 정확하게 계산해요. 성분별 계산 과정도 함께 보여줘요.",
  desc="행렬의 모든 성분에 같은 수 k를 곱해요.",
  card="모든 성분에 k 곱하기",
  ch="스칼라배", cb=["kA는 A의 모든 성분에 k를 곱한 행렬이에요. 크기는 그대로예요."],
  tip="n×n 행렬이면 det(kA) = kⁿ·det(A) 예요.",
  faq=[("k에 분수를 넣어도 되나요?","네. 3/2 나 0.5 처럼 분수와 소수 모두 입력할 수 있어요.")]),
 dict(key="transpose", slug="transpose", label="전치",
  title="전치행렬 계산기 - 행과 열을 바꿔 Aᵀ 구하기", h1="전치행렬 계산기",
  meta="행렬의 행과 열을 바꾼 전치행렬 Aᵀ를 바로 구하고, 행이 어느 열로 옮겨지는지 단계별로 보여줘요.",
  desc="행과 열을 맞바꿔 Aᵀ를 만들어요.",
  card="행과 열을 바꿔 Aᵀ 만들기",
  ch="전치행렬", cb=["Aᵀ는 A의 행과 열을 바꾼 행렬로, (Aᵀ)ᵢⱼ = Aⱼᵢ 예요. m×n 행렬의 전치는 n×m 행렬이에요.", "Aᵀ = A 이면 대칭행렬이라고 해요."],
  tip="(AB)ᵀ = BᵀAᵀ 처럼 곱의 전치는 순서가 뒤바뀌어요.",
  faq=[("대칭행렬인지 어떻게 확인하나요?","전치한 결과가 원래 행렬과 같으면 대칭행렬이에요.")]),
 dict(key="rref", slug="rref", label="RREF",
  title="RREF 계산기 - 기약 행사다리꼴과 계수(rank)", h1="RREF 계산기",
  meta="행렬을 기약 행사다리꼴(RREF)로 바꾸는 행 연산을 단계별로 보여주고, 계수와 피벗 열까지 알려줘요.",
  desc="행 연산으로 기약 행사다리꼴을 만들고 계수와 피벗 열을 알려드려요.",
  card="기약 행사다리꼴과 계수 구하기",
  ch="기약 행사다리꼴 (RREF)",
  cb=["각 행의 첫 번째 0이 아닌 성분(피벗)이 1이고, 피벗이 있는 열의 다른 성분이 모두 0인 형태예요. 영행은 맨 아래에 와요.",
      "어떤 행렬이든 RREF는 하나로 정해져서, 계수나 연립방정식의 해를 판단할 때 기준이 돼요."],
  tip="피벗의 개수가 곧 행렬의 계수예요.",
  faq=[("행사다리꼴(REF)과 기약 행사다리꼴(RREF)은 뭐가 다른가요?","REF는 피벗 아래만 0이면 되지만, RREF는 피벗이 1이고 피벗 위아래가 모두 0이어야 해요. REF는 여러 가지가 나올 수 있지만 RREF는 하나로 정해져요."),
       ("교재 풀이와 행 연산 순서가 달라요.","행 연산 순서는 사람마다 다를 수 있지만 최종 RREF는 항상 같아요.")]),
 dict(key="solve", slug="linear-system", label="연립방정식",
  title="연립방정식 행렬 계산기 - 해와 일반해까지", h1="연립방정식 계산기",
  meta="Ax = b 연립방정식을 소거법으로 풀어 해가 하나인지, 없는지, 무수히 많은지 알려주고 일반해까지 보여줘요.",
  desc="Ax = b를 첨가행렬로 바꿔 소거하고, 해가 하나인지·없는지·무수히 많은지 판단해요.",
  card="Ax = b의 해와 일반해 구하기",
  ch="연립방정식과 첨가행렬",
  cb=["Ax = b를 첨가행렬 [A | b]로 쓰고 기약 행사다리꼴로 바꾸면 해를 바로 읽을 수 있어요.",
      "0 = (0이 아닌 수) 꼴의 행이 생기면 해가 없고, 피벗이 없는 변수(자유변수)가 있으면 해가 무수히 많아요."],
  tip="계수(rank) = 미지수 개수이고 모순이 없으면 해가 하나뿐이에요.",
  faq=[("식의 개수와 미지수 개수가 달라도 되나요?","네. 행(식)과 열(미지수)을 따로 조절할 수 있어요."),
       ("해가 무수히 많을 때 t는 무엇인가요?","자유변수를 나타내는 매개변수예요. t에 어떤 수를 넣어도 방정식을 만족하는 해가 돼요.")]),
 dict(key="rank", slug="rank", label="계수",
  title="행렬 계수(rank) 계산기 - 계수·영공간 차원·피벗 열까지", h1="행렬 계수(rank) 계산기",
  meta="행렬의 계수(rank)를 행 연산 과정과 함께 구하고, 영공간의 차원(nullity)과 피벗 열, 열공간의 기저까지 알려줘요. 분수도 정확하게 계산해요.",
  desc="행 연산으로 피벗을 찾아 계수를 구하고, 영공간의 차원과 피벗 열을 알려드려요.",
  card="계수와 영공간 차원 구하기",
  ch="계수(rank)란?",
  cb=["계수(rank)는 행렬에서 서로 독립인 행(또는 열)의 개수예요. 기약 행사다리꼴로 바꿨을 때 피벗의 개수와 같아요.",
      "계수-영공간 차원 정리: rank(A) + nullity(A) = 열의 수. nullity는 Ax = 0의 해 공간의 차원이에요."],
  tip="n×n 행렬의 계수가 n이면 역행렬이 있고 행렬식이 0이 아니에요.",
  faq=[("계수와 행렬식은 어떤 관계인가요?","정사각행렬에서 행렬식이 0이 아니면 계수가 최대(n)예요. 행렬식이 0이면 계수가 n보다 작아요."),
       ("열공간의 기저는 어떻게 구하나요?","RREF에서 피벗이 있는 열 번호를 찾고, 원래 행렬 A의 그 열들을 가져오면 돼요. RREF의 열을 쓰면 안 돼요."),
       ("행 계수와 열 계수가 다를 수 있나요?","아니요. 항상 같아요. 그래서 rank(A) = rank(Aᵀ)예요.")]),
 dict(key="power", slug="power", label="거듭제곱",
  title="행렬 거듭제곱 계산기 - Aⁿ을 분수로 정확하게", h1="행렬 거듭제곱 계산기",
  meta="정사각행렬의 거듭제곱 Aⁿ(n = 0~12)을 분수로 정확하게 계산하고, A², A³, … 을 차례로 보여줘요. 피보나치 행렬 같은 점화식 계산에도 써요.",
  desc="A를 n번 곱한 Aⁿ을 구하고, 중간 결과 A², A³, …을 차례로 보여드려요.",
  card="Aⁿ을 중간 결과와 함께 구하기",
  ch="행렬의 거듭제곱",
  cb=["Aⁿ은 정사각행렬 A를 n번 곱한 행렬이에요. A⁰은 단위행렬 I로 정해요.",
      "대각행렬의 거듭제곱은 대각 성분을 각각 n제곱하면 되고, 일반 행렬은 대각화 A = PDP⁻¹를 이용하면 Aⁿ = PDⁿP⁻¹로 빠르게 구할 수 있어요."],
  tip="[[1, 1], [1, 0]]ⁿ의 성분은 피보나치 수예요. 점화식 문제에서 자주 나와요.",
  faq=[("음수 지수도 되나요?","이 계산기는 0 이상의 정수 지수만 지원해요. A⁻ⁿ은 역행렬을 구한 뒤 n제곱하면 돼요."),
       ("정사각행렬이 아니면 안 되나요?","네. A·A가 정의되려면 A의 열 수와 행 수가 같아야 해서 정사각행렬만 거듭제곱할 수 있어요.")]),
 dict(key="adj", slug="adjugate", label="수반행렬",
  title="수반행렬(여인수행렬) 계산기 - adj(A)와 역행렬 공식", h1="수반행렬 계산기",
  meta="여인수 Cᵢⱼ를 하나씩 구해 여인수행렬과 수반행렬 adj(A)를 만들고, A⁻¹ = adj(A)/det(A) 공식으로 역행렬까지 이어서 보여줘요.",
  desc="소행렬식과 여인수를 하나씩 구해 여인수행렬 C와 수반행렬 adj(A) = Cᵀ를 만들어요.",
  card="여인수행렬과 adj(A) 구하기",
  ch="수반행렬이란?",
  cb=["성분 aᵢⱼ의 여인수는 Cᵢⱼ = (−1)ⁱ⁺ʲMᵢⱼ예요. 여기서 Mᵢⱼ는 i행과 j열을 지운 소행렬식이에요.",
      "여인수를 모은 행렬을 전치한 것이 수반행렬 adj(A)이고, A·adj(A) = det(A)·I가 성립해요. 그래서 det(A) ≠ 0이면 A⁻¹ = adj(A)/det(A)예요."],
  tip="2×2에서 adj([[a, b], [c, d]]) = [[d, −b], [−c, a]]예요. 대각 성분을 바꾸고 나머지 부호를 바꿔요.",
  faq=[("수반행렬과 여인수행렬은 뭐가 다른가요?","여인수행렬 C는 여인수를 같은 위치에 둔 행렬이고, 수반행렬은 그것을 전치한 Cᵀ예요. 전치를 빼먹는 실수가 많아요."),
       ("역행렬을 구할 때 소거법과 수반행렬 중 뭐가 빠른가요?","2×2, 3×3은 수반행렬 공식이 빠르고, 4×4 이상은 소거법이 훨씬 빨라요.")]),
 dict(key="eigen", slug="eigenvalues", label="고윳값",
  title="고윳값 계산기 - 특성다항식과 고유벡터까지 단계별로", h1="고윳값·고유벡터 계산기",
  meta="특성다항식 det(λI − A)를 분수로 정확하게 구하고 고윳값과 고유벡터를 단계별로 풀어요. 2×2는 근의 공식으로 정확한 값을, 중복도와 대각화 가능 여부도 알려줘요.",
  desc="특성다항식을 구해 고윳값을 찾고, (A − λI)v = 0을 풀어 고유벡터를 구해요.",
  card="특성다항식, 고윳값, 고유벡터 구하기",
  ch="고윳값과 고유벡터",
  cb=["Av = λv를 만족하는 0이 아닌 벡터 v가 고유벡터, 수 λ가 고윳값이에요. 고윳값은 특성다항식 det(λI − A) = 0의 근이에요.",
      "유리수 고윳값은 정확하게 구하고, 2×2는 근의 공식으로 (a ± √b)/c 꼴까지 보여줘요. 3×3 이상에서 유리수가 아닌 근은 소수로 근사해요."],
  tip="고윳값의 합은 대각합 tr(A), 곱은 행렬식 det(A)예요. 검산할 때 써요.",
  faq=[("고윳값이 소수로 나오는 건 왜 그런가요?","특성다항식의 근이 유리수가 아니면 정확한 표기가 복잡해져서, 3×3 이상에서는 수치적으로 근사해 ≈로 표시해요. 2×2는 √를 써서 정확하게 보여줘요."),
       ("복소 고윳값이 나오면요?","실수 고윳값이 없다는 뜻이에요. 2×2에서는 a ± bi 꼴로 정확히 보여주고, 그 이상은 근사값으로 보여줘요."),
       ("대각화 가능 여부는 어떻게 판단하나요?","각 고윳값의 기하적 중복도(고유벡터 개수)의 합이 n이면 대각화할 수 있어요. 모든 고윳값이 정확히 구해진 경우에만 판단해요.")]),
 dict(key="diag", slug="diagonalization", label="대각화",
  title="행렬 대각화 계산기 - P, D, P⁻¹을 단계별로", h1="행렬 대각화 계산기",
  meta="A = PDP⁻¹ 꼴로 행렬을 대각화해요. 고윳값과 고유벡터를 분수로 정확하게 구해 P와 D를 만들고, P⁻¹까지 계산해 PDP⁻¹ = A를 검산해요. 대각화가 안 되는 경우도 이유를 알려줘요.",
  desc="고윳값과 고유벡터를 구해 A = PDP⁻¹의 P, D, P⁻¹을 만들어요.",
  card="A = PDP⁻¹의 P, D, P⁻¹ 구하기",
  ch="대각화란?",
  cb=["정방행렬 A에 대해 가역행렬 P와 대각행렬 D가 있어서 A = PDP⁻¹이 되면 A는 대각화 가능해요. P의 열은 고유벡터, D의 대각 성분은 같은 순서의 고윳값이에요.",
      "서로 독립인 고유벡터가 n개 있어야 P가 가역이 돼요. 고윳값이 n개 모두 다르면 항상 가능하고, 중복 고윳값이 있으면 기하적 중복도를 확인해야 해요."],
  tip="대각화하면 Aᵏ = PDᵏP⁻¹이라 거듭제곱이 쉬워져요. Dᵏ는 대각 성분을 k제곱하면 끝이에요.",
  faq=[("대각화가 안 된다고 나오는 이유는 뭔가요?","두 가지예요. 고윳값이 유리수가 아니어서 이 계산기가 정확한 P를 쓸 수 없거나, 중복 고윳값의 고유벡터가 중복도보다 적은 경우(결함 행렬)예요. 후자는 어떤 방법으로도 대각화할 수 없어요."),
       ("P의 열 순서가 교재와 다른데 괜찮나요?","괜찮아요. 고윳값의 순서만 D에서 같게 맞추면 어떤 순서든 A = PDP⁻¹이 성립해요. 고유벡터에 0이 아닌 수를 곱해도 돼요."),
       ("대칭행렬은 항상 대각화되나요?","네. 실수 대칭행렬은 항상 직교 대각화할 수 있어요. 고유벡터를 정규화하면 P⁻¹ = Pᵀ가 돼요.")]),
 dict(key="axb", slug="matrix-equation", label="AX = B",
  title="행렬방정식 AX = B 계산기 - X = A⁻¹B를 단계별로", h1="행렬방정식 AX = B 계산기",
  meta="행렬방정식 AX = B의 해 X를 분수로 정확하게 구해요. 첨가행렬 [A | B]를 가우스-조던 소거법으로 풀어 과정을 보여주고, A가 특이행렬이면 해가 없는지 무수히 많은지 알려줘요.",
  desc="첨가행렬 [A | B]를 기약 행사다리꼴로 만들어 X = A⁻¹B를 구해요.",
  card="AX = B의 해 X 구하기",
  ch="행렬방정식 AX = B",
  cb=["A가 가역이면 X = A⁻¹B가 유일한 해예요. 역행렬을 따로 구하지 않고 [A | B]를 소거하면 오른쪽에 바로 X가 나와요.",
      "B의 열 하나하나가 연립방정식 Ax = b의 우변이에요. 그래서 AX = B는 우변이 여러 개인 연립방정식을 한 번에 푸는 것과 같아요."],
  tip="XA = B 꼴은 양변을 전치해서 AᵀXᵀ = Bᵀ로 바꾸면 같은 방법으로 풀 수 있어요.",
  faq=[("XA = B는 어떻게 푸나요?","전치하면 AᵀXᵀ = Bᵀ예요. Aᵀ와 Bᵀ를 입력해 Xᵀ를 구한 뒤 다시 전치하세요."),
       ("A가 정방행렬이 아니면요?","이 계산기는 정방행렬 A만 받아요. 직사각형이면 연립방정식 계산기에서 열별로 풀거나 최소제곱 문제가 돼요."),
       ("B가 단위행렬이면요?","X = A⁻¹이 나와요. 역행렬 계산기가 하는 일과 같아요.")]),
 dict(key="gs", slug="gram-schmidt", label="그람-슈미트",
  title="그람-슈미트 직교화 계산기 - 직교 기저를 단계별로", h1="그람-슈미트 직교화 계산기",
  meta="그람-슈미트 과정으로 열벡터를 직교 기저로 바꿔요. 각 단계의 정사영과 뺄셈을 분수로 정확하게 보여주고, 종속인 벡터는 걸러내요. 정규화를 위한 길이의 제곱도 알려줘요.",
  desc="열벡터 v₁, v₂, …에서 정사영을 빼며 서로 직교하는 u₁, u₂, …를 만들어요.",
  card="열벡터를 직교 기저로 바꾸기",
  ch="그람-슈미트 과정이란?",
  cb=["주어진 벡터들에서 앞서 만든 벡터 방향의 성분(정사영)을 빼면 서로 수직인 벡터들이 나와요. uₖ = vₖ − Σ (vₖ·uⱼ)/(uⱼ·uⱼ) uⱼ 가 그 식이에요.",
      "결과를 각자의 길이로 나누면 정규직교 기저가 돼요. 길이에 √가 들어가는 경우가 많아서 계산기는 정규화 전의 u와 ‖u‖²를 보여줘요."],
  tip="uₖ가 0이 되면 vₖ는 앞 벡터들의 일차결합이에요. 기저에서 빼고 다음 벡터로 넘어가요.",
  faq=[("벡터는 어디에 입력하나요?","행렬의 각 열이 벡터 하나예요. 3차원 벡터 두 개면 3×2 행렬을 입력하세요."),
       ("정규직교 기저는 안 나오나요?","정규화하면 √가 들어가 분수로 정확히 쓸 수 없어서, 직교 벡터 u와 길이의 제곱 ‖u‖²를 보여줘요. u를 √(‖u‖²)로 나누면 정규직교 기저예요."),
       ("QR 분해와는 어떤 관계인가요?","그람-슈미트로 얻은 정규직교 벡터를 열로 세운 것이 Q이고, R = QᵀA예요.")]),
 dict(key="lu", slug="lu", label="LU 분해",
  title="LU 분해 계산기 - A = LU를 단계별로", h1="LU 분해 계산기",
  meta="행렬을 하삼각행렬 L과 상삼각행렬 U의 곱 A = LU로 분해해요. 소거 과정과 배수를 분수로 정확하게 보여주고, 행 교환이 필요하면 치환행렬 P를 써서 PA = LU로 알려줘요.",
  desc="가우스 소거의 배수를 L에, 결과를 U에 담아 A = LU(또는 PA = LU)를 만들어요.",
  card="A = LU의 L, U 구하기",
  ch="LU 분해란?",
  cb=["가우스 소거로 상삼각행렬 U를 만들 때 사용한 배수 lᵢⱼ를 하삼각행렬 L에 적으면 A = LU예요. 이 계산기는 L의 대각선이 1인 둘리틀(Doolittle) 방식이에요.",
      "피벗이 0이 되면 행을 바꿔야 해요. 바꾼 행을 치환행렬 P에 기록하면 PA = LU가 성립해요."],
  tip="LU가 있으면 Ax = b를 Ly = b, Ux = y 두 번의 대입으로 풀 수 있어서, 우변 b가 여러 개일 때 특히 효율적이에요.",
  faq=[("왜 PA = LU라고 나오나요?","소거 중에 피벗이 0이어서 행을 바꿨기 때문이에요. P는 그 행 교환을 나타내는 치환행렬이고, PA를 분해한 결과가 L, U예요."),
       ("det(A)를 LU로 구할 수 있나요?","네. det(A) = ±(U의 대각 성분의 곱)이에요. 부호는 행 교환 횟수가 홀수면 −예요."),
       ("특이행렬도 분해되나요?","분해는 돼요. U의 마지막 대각 성분이 0으로 나오고, 그러면 det(A) = 0이에요.")]),
]

# ===================== 계산기 내용 (영어) =====================
OPS_EN = [
 dict(key="inverse", slug="inverse", label="Inverse",
  title="Inverse Matrix Calculator - Exact Fractions, Step by Step", h1="Inverse Matrix Calculator",
  meta="Find the inverse of a 2×2 to 6×6 matrix in exact fractions and see every row operation of Gauss-Jordan elimination. Free, no sign-up.",
  desc="Computes A⁻¹ by Gauss-Jordan elimination and shows each row operation.",
  card="A⁻¹ by Gauss-Jordan elimination",
  ch="What is an inverse matrix?",
  cb=["The inverse A⁻¹ is the matrix with AA⁻¹ = A⁻¹A = I. It exists only for square matrices whose determinant is not zero.",
      "Gauss-Jordan elimination applies row operations to [A | I] until the left half becomes the identity. The right half is then A⁻¹."],
  tip="For a 2×2 matrix, A⁻¹ = 1/(ad − bc) · [d −b; −c a] is the fastest route.",
  faq=[("How do I know a matrix has no inverse?","If the determinant is 0 there is no inverse. During elimination this shows up as a row of zeros on the left half."),
       ("Can I see the result as decimals?","Press ‘Decimal’ above the result to round to four decimal places. The calculation itself always uses exact fractions."),
       ("How can I check that AA⁻¹ = I?","Enter A and the inverse into the matrix multiplication calculator and confirm the product is the identity matrix.")]),
 dict(key="det", slug="determinant", label="Determinant",
  title="Determinant Calculator - 2×2 to 6×6 with Steps", h1="Determinant Calculator",
  meta="Compute the determinant exactly as a fraction. See the 2×2 formula, cofactor expansion for 3×3 and row reduction for larger matrices, step by step.",
  desc="Uses the formula for 2×2, cofactor expansion for 3×3, and row reduction for 4×4 and larger.",
  card="det(A) by cofactor expansion or row reduction",
  ch="What is a determinant?",
  cb=["The determinant is a single number attached to a square matrix. Geometrically it tells how much the matrix scales area or volume.",
      "If the determinant is 0, the matrix has no inverse and Ax = b does not have a unique solution."],
  tip="Swapping two rows flips the sign; adding a multiple of one row to another leaves the determinant unchanged.",
  faq=[("Can I use the rule of Sarrus for 3×3?","Yes, the result is the same. This calculator shows cofactor expansion because it also works for 4×4 and larger."),
       ("What does a negative determinant mean?","The transformation flips orientation. Use the absolute value for the scale factor."),
       ("Do rectangular matrices have determinants?","No. Determinants are defined only for square matrices.")]),
 dict(key="mul", slug="multiplication", label="Multiply",
  title="Matrix Multiplication Calculator - Every Entry Explained", h1="Matrix Multiplication Calculator",
  meta="Multiply two matrices and see how each entry of AB comes from a row of A and a column of B. Fractions and decimals welcome.",
  desc="Shows how each entry of AB is computed from a row of A and a column of B.",
  card="See how each entry of AB is computed",
  ch="Rules of matrix multiplication",
  cb=["If A is m×n and B is n×p, then AB is m×p. The entry (AB)ᵢⱼ is the sum of the products of row i of A and column j of B."],
  tip="The number of columns of A must equal the number of rows of B. In general AB ≠ BA.",
  faq=[("Why does the row count of B change automatically?","The product is only defined when the column count of A equals the row count of B, so B follows A."),
       ("How do I compute BA?","Swap the matrices you enter as A and B.")]),
 dict(key="add", slug="addition", label="Add",
  title="Matrix Addition Calculator - Exact Fractions", h1="Matrix Addition Calculator",
  meta="Add two matrices of the same size in exact fractions and see the entry-by-entry work.",
  desc="Adds the corresponding entries of two matrices of the same size.",
  card="Add corresponding entries",
  ch="Matrix addition", cb=["Only matrices of the same size can be added. Add the entries in the same position."],
  tip="Addition is commutative and associative: A + B = B + A.",
  faq=[("Can I add matrices of different sizes?","No. Both the row and column counts must match, so the size of B follows A automatically.")]),
 dict(key="sub", slug="subtraction", label="Subtract",
  title="Matrix Subtraction Calculator - Exact Fractions", h1="Matrix Subtraction Calculator",
  meta="Subtract two matrices of the same size in exact fractions and see the entry-by-entry work.",
  desc="Subtracts the corresponding entries of two matrices of the same size.",
  card="Subtract corresponding entries",
  ch="Matrix subtraction", cb=["Only matrices of the same size can be subtracted. A − B is the same as A + (−1)B."],
  tip="A − B ≠ B − A, so keep the order straight.",
  faq=[("How do I enter negative numbers?","Put a minus sign in front: -3, -1/2.")]),
 dict(key="scalar", slug="scalar-multiplication", label="Scalar",
  title="Scalar Multiplication Calculator - kA in One Step", h1="Scalar Multiplication Calculator",
  meta="Multiply every entry of a matrix by a number k in exact fractions and see the work for each entry.",
  desc="Multiplies every entry of the matrix by the same number k.",
  card="Multiply every entry by k",
  ch="Scalar multiplication", cb=["kA is the matrix obtained by multiplying every entry of A by k. The size stays the same."],
  tip="For an n×n matrix, det(kA) = kⁿ·det(A).",
  faq=[("Can k be a fraction?","Yes. Fractions like 3/2 and decimals like 0.5 both work.")]),
 dict(key="transpose", slug="transpose", label="Transpose",
  title="Matrix Transpose Calculator - Swap Rows and Columns", h1="Transpose Calculator",
  meta="Find the transpose Aᵀ instantly and see which row becomes which column.",
  desc="Swaps rows and columns to form Aᵀ.",
  card="Swap rows and columns to get Aᵀ",
  ch="The transpose", cb=["Aᵀ is A with rows and columns swapped: (Aᵀ)ᵢⱼ = Aⱼᵢ. The transpose of an m×n matrix is n×m.", "If Aᵀ = A, the matrix is symmetric."],
  tip="The transpose of a product reverses the order: (AB)ᵀ = BᵀAᵀ.",
  faq=[("How do I check whether a matrix is symmetric?","If the transpose equals the original matrix, it is symmetric.")]),
 dict(key="rref", slug="rref", label="RREF",
  title="RREF Calculator - Reduced Row Echelon Form and Rank", h1="RREF Calculator",
  meta="Reduce any matrix to reduced row echelon form with every row operation shown, and get the rank and pivot columns.",
  desc="Applies row operations to reach reduced row echelon form and reports the rank and pivot columns.",
  card="Reduced row echelon form and rank",
  ch="Reduced row echelon form (RREF)",
  cb=["The first nonzero entry of each row (the pivot) is 1, every other entry in a pivot column is 0, and zero rows sit at the bottom.",
      "Every matrix has exactly one RREF, which makes it the standard tool for finding rank and solving linear systems."],
  tip="The number of pivots is the rank of the matrix.",
  faq=[("What is the difference between REF and RREF?","REF only needs zeros below each pivot. RREF also needs pivots equal to 1 and zeros above them. A matrix has many REFs but only one RREF."),
       ("My textbook uses a different order of row operations.","The order can differ from person to person, but the final RREF is always the same.")]),
 dict(key="solve", slug="linear-system", label="Linear system",
  title="System of Linear Equations Solver - Matrix Method with Steps", h1="Linear System Solver",
  meta="Solve Ax = b by Gauss-Jordan elimination. See whether the system has one solution, none or infinitely many, with the general solution written out.",
  desc="Reduces the augmented matrix [A | b] and tells whether there is one solution, none, or infinitely many.",
  card="Solve Ax = b, including the general solution",
  ch="Linear systems and the augmented matrix",
  cb=["Write Ax = b as the augmented matrix [A | b] and reduce it to RREF; the solution can be read off directly.",
      "A row of the form 0 = (nonzero) means no solution. A variable without a pivot (a free variable) means infinitely many solutions."],
  tip="If the rank equals the number of unknowns and there is no contradiction, the solution is unique.",
  faq=[("Can the number of equations differ from the number of unknowns?","Yes. Rows (equations) and columns (unknowns) can be set independently."),
       ("What is t in the general solution?","A parameter standing for a free variable. Any value of t gives a solution of the system.")]),
 dict(key="rank", slug="rank", label="Rank",
  title="Matrix Rank Calculator - Rank, Nullity and Pivot Columns", h1="Matrix Rank Calculator",
  meta="Find the rank of a matrix with every row operation shown, plus the nullity, the pivot columns and a basis of the column space. Exact fraction arithmetic.",
  desc="Finds the pivots by row reduction to get the rank, and reports the nullity and pivot columns.",
  card="Rank and nullity",
  ch="What is the rank?",
  cb=["The rank is the number of linearly independent rows (or columns) of a matrix. It equals the number of pivots in the reduced row echelon form.",
      "Rank-nullity theorem: rank(A) + nullity(A) = number of columns, where the nullity is the dimension of the solution space of Ax = 0."],
  tip="An n×n matrix with rank n is invertible and has a nonzero determinant.",
  faq=[("How are rank and determinant related?","For a square matrix, a nonzero determinant means full rank n. A zero determinant means the rank is less than n."),
       ("How do I find a basis of the column space?","Take the pivot column numbers from the RREF and use those columns of the original matrix A, not the columns of the RREF."),
       ("Can row rank and column rank differ?","No. They are always equal, so rank(A) = rank(Aᵀ).")]),
 dict(key="power", slug="power", label="Power",
  title="Matrix Power Calculator - Aⁿ in Exact Fractions", h1="Matrix Power Calculator",
  meta="Raise a square matrix to a power n from 0 to 12 in exact fractions and see A², A³, … one after another. Handy for recurrences such as the Fibonacci matrix.",
  desc="Computes Aⁿ by repeated multiplication and shows the intermediate powers A², A³, …",
  card="Aⁿ with every intermediate power",
  ch="Powers of a matrix",
  cb=["Aⁿ is the square matrix A multiplied by itself n times, with A⁰ defined as the identity I.",
      "For a diagonal matrix, raise each diagonal entry to the n-th power. For a general matrix, diagonalization A = PDP⁻¹ gives Aⁿ = PDⁿP⁻¹ quickly."],
  tip="The entries of [[1, 1], [1, 0]]ⁿ are Fibonacci numbers, a classic recurrence example.",
  faq=[("Are negative exponents supported?","No, only integers from 0 to 12. For A⁻ⁿ, invert the matrix first and raise the inverse to the n-th power."),
       ("Why must the matrix be square?","A·A is only defined when the number of columns of A equals its number of rows.")]),
 dict(key="adj", slug="adjugate", label="Adjugate",
  title="Adjugate Matrix Calculator - Cofactors and the Inverse Formula", h1="Adjugate Matrix Calculator",
  meta="Compute every cofactor Cᵢⱼ, build the cofactor matrix and the adjugate adj(A), and continue to the inverse with A⁻¹ = adj(A)/det(A).",
  desc="Finds each minor and cofactor to build the cofactor matrix C and the adjugate adj(A) = Cᵀ.",
  card="Cofactor matrix and adj(A)",
  ch="What is the adjugate?",
  cb=["The cofactor of the entry aᵢⱼ is Cᵢⱼ = (−1)ⁱ⁺ʲMᵢⱼ, where the minor Mᵢⱼ is the determinant after deleting row i and column j.",
      "The adjugate adj(A) is the transpose of the cofactor matrix, and A·adj(A) = det(A)·I. So when det(A) ≠ 0, A⁻¹ = adj(A)/det(A)."],
  tip="For 2×2, adj([[a, b], [c, d]]) = [[d, −b], [−c, a]]: swap the diagonal entries and negate the others.",
  faq=[("What is the difference between the cofactor matrix and the adjugate?","The cofactor matrix C holds each cofactor in its own position; the adjugate is its transpose Cᵀ. Forgetting the transpose is a common mistake."),
       ("Elimination or the adjugate formula for inverses?","For 2×2 and 3×3 the adjugate formula is quick. From 4×4 up, elimination is much faster.")]),
 dict(key="eigen", slug="eigenvalues", label="Eigenvalues",
  title="Eigenvalue Calculator - Characteristic Polynomial and Eigenvectors with Steps", h1="Eigenvalue and Eigenvector Calculator",
  meta="Get the characteristic polynomial det(λI − A) in exact fractions, then the eigenvalues and eigenvectors step by step. Exact 2×2 roots, multiplicities and whether the matrix is diagonalizable.",
  desc="Finds the characteristic polynomial, solves it for the eigenvalues, and solves (A − λI)v = 0 for the eigenvectors.",
  card="Characteristic polynomial, eigenvalues, eigenvectors",
  ch="Eigenvalues and eigenvectors",
  cb=["A nonzero vector v with Av = λv is an eigenvector and the number λ is its eigenvalue. The eigenvalues are the roots of the characteristic polynomial det(λI − A) = 0.",
      "Rational eigenvalues are found exactly, and 2×2 matrices get exact roots of the form (a ± √b)/c. For 3×3 and larger, irrational roots are approximated numerically."],
  tip="The eigenvalues add up to the trace tr(A) and multiply to det(A). Use this to check your work.",
  faq=[("Why are some eigenvalues shown as decimals?","When the roots of the characteristic polynomial are not rational, an exact expression gets unwieldy for 3×3 and larger, so they are approximated and marked with ≈. For 2×2 the exact form with √ is shown."),
       ("What if the eigenvalues are complex?","Then there are no real eigenvalues. For 2×2 they are shown exactly as a ± bi; for larger matrices as approximations."),
       ("How is diagonalizability decided?","A matrix is diagonalizable when the geometric multiplicities (numbers of eigenvectors) add up to n. The verdict is given only when every eigenvalue was found exactly.")]),
 dict(key="diag", slug="diagonalization", label="Diagonalize",
  title="Matrix Diagonalization Calculator - P, D and P⁻¹ with Steps", h1="Matrix diagonalization calculator",
  meta="Diagonalize a matrix as A = PDP⁻¹. Eigenvalues and eigenvectors are found in exact fractions to build P and D, then P⁻¹ is computed and PDP⁻¹ = A is verified. Explains why a matrix is not diagonalizable.",
  desc="Finds eigenvalues and eigenvectors, then builds P, D and P⁻¹ with A = PDP⁻¹.",
  card="P, D and P⁻¹ with A = PDP⁻¹",
  ch="What is diagonalization?",
  cb=["A square matrix A is diagonalizable when there is an invertible P and a diagonal D with A = PDP⁻¹. The columns of P are eigenvectors and the diagonal of D holds the eigenvalues in the same order.",
      "P is invertible only if there are n linearly independent eigenvectors. Distinct eigenvalues guarantee this; repeated eigenvalues need their geometric multiplicity checked."],
  tip="Once diagonalized, Aᵏ = PDᵏP⁻¹, and Dᵏ just raises each diagonal entry to the k-th power.",
  faq=[("Why does it say not diagonalizable?","Two reasons: the eigenvalues are not rational, so this calculator cannot write P exactly, or a repeated eigenvalue has fewer eigenvectors than its multiplicity (a defective matrix). The second case cannot be diagonalized by any method."),
       ("My textbook orders the columns of P differently. Is that fine?","Yes. Any order works as long as D uses the same order. Eigenvectors may also be scaled by any nonzero number."),
       ("Is a symmetric matrix always diagonalizable?","Yes. A real symmetric matrix is always orthogonally diagonalizable; with normalized eigenvectors, P⁻¹ = Pᵀ.")]),
 dict(key="axb", slug="matrix-equation", label="AX = B",
  title="Matrix Equation AX = B Calculator - X = A⁻¹B with Steps", h1="Matrix equation AX = B calculator",
  meta="Solve the matrix equation AX = B in exact fractions. Reduces the augmented matrix [A | B] by Gauss-Jordan elimination with every step shown, and tells you when a singular A gives no solution or infinitely many.",
  desc="Reduces [A | B] to RREF to find X = A⁻¹B.",
  card="Solve AX = B for X",
  ch="The matrix equation AX = B",
  cb=["If A is invertible the unique solution is X = A⁻¹B. Instead of computing the inverse, reduce [A | B]: X appears on the right.",
      "Each column of B is the right-hand side of a linear system Ax = b, so AX = B solves several systems with the same coefficient matrix at once."],
  tip="For XA = B, transpose both sides: AᵀXᵀ = Bᵀ, which has the same form.",
  faq=[("How do I solve XA = B?","Transpose to get AᵀXᵀ = Bᵀ. Enter Aᵀ and Bᵀ, solve for Xᵀ, then transpose the result."),
       ("What if A is not square?","This calculator takes a square A. For rectangular A, solve column by column with the linear system calculator, or it becomes a least-squares problem."),
       ("What if B is the identity?","Then X = A⁻¹, which is exactly what the inverse calculator does.")]),
 dict(key="gs", slug="gram-schmidt", label="Gram-Schmidt",
  title="Gram-Schmidt Calculator - Orthogonal Basis with Steps", h1="Gram-Schmidt orthogonalization calculator",
  meta="Turn column vectors into an orthogonal basis with the Gram-Schmidt process. Every projection and subtraction is shown in exact fractions, dependent vectors are dropped, and squared lengths are given for normalization.",
  desc="Subtracts projections from v₁, v₂, … to build mutually orthogonal u₁, u₂, ….",
  card="Orthogonal basis from column vectors",
  ch="What is the Gram-Schmidt process?",
  cb=["Subtracting from each vector its components along the previously built vectors leaves mutually perpendicular vectors: uₖ = vₖ − Σ (vₖ·uⱼ)/(uⱼ·uⱼ) uⱼ.",
      "Dividing each result by its length gives an orthonormal basis. Since lengths usually involve square roots, the calculator shows the unnormalized u and ‖u‖²."],
  tip="If uₖ comes out as 0, vₖ is a combination of the earlier vectors: drop it and move on.",
  faq=[("Where do I enter the vectors?","Each column of the matrix is one vector. For two vectors in ℝ³, enter a 3×2 matrix."),
       ("Why no orthonormal basis?","Normalizing introduces square roots that cannot be written as exact fractions, so the calculator gives the orthogonal u and ‖u‖². Divide u by √(‖u‖²) to normalize."),
       ("How does this relate to QR?","The normalized vectors as columns form Q, and R = QᵀA.")]),
 dict(key="lu", slug="lu", label="LU",
  title="LU Decomposition Calculator - A = LU with Steps", h1="LU decomposition calculator",
  meta="Factor a matrix into a lower triangular L and an upper triangular U with A = LU. Every elimination step and multiplier is shown in exact fractions; when a row swap is needed, a permutation matrix P gives PA = LU.",
  desc="Stores the Gaussian elimination multipliers in L and the result in U so that A = LU (or PA = LU).",
  card="L and U with A = LU",
  ch="What is LU decomposition?",
  cb=["Record the multipliers lᵢⱼ used while reducing A to an upper triangular U in a lower triangular L, and A = LU. This calculator uses the Doolittle form, with 1s on the diagonal of L.",
      "If a pivot is 0, rows must be swapped. Recording the swaps in a permutation matrix P gives PA = LU."],
  tip="With LU in hand, Ax = b becomes two substitutions, Ly = b then Ux = y, which is efficient for many right-hand sides.",
  faq=[("Why does it show PA = LU?","A pivot was 0 during elimination, so rows were swapped. P is the permutation matrix for those swaps, and L, U factor PA."),
       ("Can I get det(A) from LU?","Yes: det(A) = ±(product of the diagonal of U), with a minus sign for an odd number of row swaps."),
       ("Does a singular matrix have an LU factorization?","Yes. The last diagonal entry of U comes out 0, which means det(A) = 0.")]),
]

# 계산기 → 관련 가이드 (영어판에는 있는 글만 보여줘요)
GUIDE_FOR = {"inverse": "inverse-gauss-jordan", "det": "determinant-3x3", "rref": "rank-and-rref", "solve": "linear-system-solutions",
             "mul": "matrix-multiplication", "add": "matrix-add-subtract-scalar", "sub": "matrix-add-subtract-scalar",
             "scalar": "matrix-add-subtract-scalar", "transpose": "matrix-transpose-properties",
             "rank": "rank-and-rref", "power": "diagonalization-matrix-power", "adj": "inverse-adjugate-cofactor", "eigen": "eigenvalues-2x2",
             "diag": "diagonalization-matrix-power", "axb": "inverse-gauss-jordan", "gs": "linear-independence", "lu": "elementary-matrices"}
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
    "rank": ["rank-and-rref", "null-space-column-space", "linear-independence"],
    "power": ["diagonalization-matrix-power", "matrix-multiplication", "eigenvalues-2x2"],
    "adj": ["inverse-adjugate-cofactor", "determinant-3x3", "determinant-properties"],
    "eigen": ["eigenvalues-2x2", "diagonalization-matrix-power", "determinant-3x3"],
    "diag": ["diagonalization-matrix-power", "eigenvalues-2x2", "linear-independence"],
    "axb": ["inverse-gauss-jordan", "linear-system-solutions", "matrix-multiplication"],
    "gs": ["linear-independence", "null-space-column-space", "matrix-transpose-properties"],
    "lu": ["elementary-matrices", "inverse-gauss-jordan", "determinant-properties"],
}

# ===================== 화면 문구 =====================
CALC_KO = '''<div class="work">
<section class="panel in" aria-labelledby="inH">
<div class="panel-head"><h2 id="inH">INPUT · 입력</h2><div class="acts"><button type="button" class="ghost" id="exBtn">예제 넣기</button><button type="button" class="ghost" id="clrBtn">모두 지우기</button></div></div>
<div id="inputs"><noscript><p class="err">계산기를 쓰려면 브라우저에서 자바스크립트를 켜 주세요.</p></noscript></div>
<p class="hint">정수, 분수(<code>1/3</code>), 소수(<code>0.25</code>)를 쓸 수 있어요. 빈칸은 0이에요. 엑셀이나 교재에서 복사한 숫자를 첫 칸에 붙여넣으면 행렬이 한 번에 채워져요.</p>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">RESULT · 결과</h2><div class="seg" role="group" aria-label="숫자 표시 방식"><button type="button" data-mode="frac" aria-pressed="true">분수</button><button type="button" data-mode="dec" aria-pressed="false">소수</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="shareBtn">공유 링크</button><button type="button" class="ghost" id="copyTex">LaTeX 복사</button><p class="texnote">LaTeX는 과제·논문(Overleaf), 노션 수식 블록, 워드 수식 편집기에 붙여넣는 수식 코드예요.</p></div>
</section>
</div>
<details class="fold steps-fold" id="stepsD" hidden><summary><h2>단계별 풀이</h2><span class="cnt" id="stepCount"></span></summary>
<div class="fold-b"><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div></details>
'''
CALC_EN = '''<div class="work">
<section class="panel in" aria-labelledby="inH">
<div class="panel-head"><h2 id="inH">INPUT</h2><div class="acts"><button type="button" class="ghost" id="exBtn">Load example</button><button type="button" class="ghost" id="clrBtn">Clear all</button></div></div>
<div id="inputs"><noscript><p class="err">Please enable JavaScript in your browser to use the calculator.</p></noscript></div>
<p class="hint">Integers, fractions (<code>1/3</code>) and decimals (<code>0.25</code>) are accepted. Empty cells count as 0. Paste a block of numbers from a spreadsheet or textbook into the first cell to fill the whole matrix.</p>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">RESULT</h2><div class="seg" role="group" aria-label="Number format"><button type="button" data-mode="frac" aria-pressed="true">Fraction</button><button type="button" data-mode="dec" aria-pressed="false">Decimal</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="shareBtn">Share link</button><button type="button" class="ghost" id="copyTex">Copy LaTeX</button><p class="texnote">LaTeX is the math code you can paste into Overleaf, Notion equation blocks or Word's equation editor.</p></div>
</section>
</div>
<details class="fold steps-fold" id="stepsD" hidden><summary><h2>Steps</h2><span class="cnt" id="stepCount"></span></summary>
<div class="fold-b"><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div></details>
'''

HOWTO_KO = '''<ol class="howto">
<li>행·열 버튼으로 행렬 크기를 정해요. 최대 6×6까지 입력할 수 있어요.</li>
<li>칸에 숫자를 입력하면 바로 계산돼요. 분수는 <code>1/3</code>, 음수는 <code>-2</code>처럼 입력해요.</li>
<li><kbd>Enter</kbd>는 다음 칸, <kbd>←</kbd> <kbd>→</kbd> <kbd>↑</kbd> <kbd>↓</kbd> 방향키로 칸 사이를 이동해요.</li>
<li>‘단계별 풀이’를 누르면 계산 과정이 펼쳐져요. ‘LaTeX 복사’는 Overleaf, 노션 수식 블록, 워드 수식 편집기에 붙여넣을 수 있는 수식 코드를 복사해요.</li>
</ol>'''
HOWTO_EN = '''<ol class="howto">
<li>Set the matrix size with the row and column buttons. Up to 6×6 is supported.</li>
<li>Type numbers into the cells and the result updates instantly. Enter fractions as <code>1/3</code> and negatives as <code>-2</code>.</li>
<li><kbd>Enter</kbd> moves to the next cell; the <kbd>←</kbd> <kbd>→</kbd> <kbd>↑</kbd> <kbd>↓</kbd> arrow keys move between cells.</li>
<li>Open ‘Steps’ to see the full working. ‘Copy LaTeX’ copies the result as math code you can paste into Overleaf, a Notion equation block or Word's equation editor.</li>
</ol>'''

UI_KO = dict(
    nav=[("calc", "/calculators/", "계산기"), ("practice", "/practice/", "연습 문제"), ("guide", "/guide/", "가이드"), ("about", "/about/", "소개")],
    nav_aria="사이트", switch="EN", switch_title="English", theme="라이트/다크 전환",
    foot_note="", foot_aria="사이트 정보",
    foot=[("/calculators/", "계산기"), ("/practice/", "연습 문제"), ("/guide/", "가이드"), ("/about/", "소개"), ("/about/#contact", "문의"), ("/privacy/", "개인정보처리방침")],
    ops_aria="연산 선택", extras_aria="더 알아보기", calc=CALC_KO, howto=HOWTO_KO,
    fold_howto="사용 방법", fold_faq="자주 묻는 질문", fold_related="관련 가이드", fold_about="행렬 계산기 소개",
    more_guide="자세한 설명과 예제: {t}", tip="시험 팁",
    crumb_home="홈", crumb_calc="계산기", crumb_guide="가이드",
    home_title="행렬 계산기 - 역행렬·행렬식·RREF를 분수로 정확하게",
    home_meta="역행렬, 행렬식, 곱셈, RREF, 연립방정식, 고윳값까지 분수로 정확하게 계산하고 풀이 과정을 단계별로 보여주는 깔끔한 무료 행렬 계산기예요.",
    home_h1="행렬 계산기", home_intro="역행렬부터 연립방정식까지, 분수로 정확하게 계산하고 풀이 과정을 보여드려요.",
    home_about=("<p>{site}는 대학 선형대수에서 자주 쓰는 행렬 계산을 분수로 정확하게 풀고, 풀이 과정을 단계별로 보여주는 무료 계산기예요. "
                "반올림 오차 없이 1/3 같은 정확한 값으로 계산하고, 결과 행렬은 LaTeX로 복사할 수 있어요.</p>"
                "<p>제공하는 계산기: {ops}</p>"
                '<p><a href="{p}/calculators/">모든 계산기 보기</a> · <a href="{p}/guide/">개념 가이드 보기</a></p>'),
    home_faq=[("몇 × 몇 행렬까지 계산할 수 있나요?", "최대 6×6까지 입력할 수 있어요. 곱셈과 연립방정식은 계산기마다 가능한 크기가 조금씩 달라요."),
              ("계산 결과는 정확한가요?", "모든 값을 분수로 저장해 계산하기 때문에 반올림 오차가 생기지 않아요. 소수 버튼은 보여주는 방식만 바꿔요."),
              ("입력한 행렬이 서버로 전송되나요?", "아니요. 계산은 모두 브라우저 안에서 이루어지고 입력값은 어디에도 전송되지 않아요.")],
    hub_title="행렬 계산기 모음 - 17가지 연산", hub_h1="행렬 계산기 모음", hub_ld="행렬 계산기 모음",
    hub_meta="덧셈·뺄셈·곱셈·거듭제곱·전치부터 역행렬, 행렬식, 수반행렬, RREF, 계수(rank), 연립방정식, AX = B, LU 분해, 고윳값, 대각화, 그람-슈미트까지 행렬 계산기 17종을 한곳에 모았어요. 모두 분수로 정확하게 계산하고 풀이 과정을 보여줘요.",
    hub_intro='필요한 연산을 골라 바로 계산해 보세요. 개념이 헷갈리면 <a href="{p}/guide/">가이드</a>도 있어요.',
    groups=[("기본 연산", ["add", "sub", "scalar", "mul", "power", "transpose"]), ("역행렬과 행렬식", ["inverse", "det", "adj"]),
            ("소거법과 연립방정식", ["rref", "rank", "solve", "axb", "lu"]), ("고윳값과 직교화", ["eigen", "diag", "gs"])],
    gi_title="행렬 가이드", gi_h1="가이드", gi_intro="시험 범위에서 자주 헷갈리는 개념을 예제와 함께 정리했어요. 모든 예제는 계산기로 바로 확인할 수 있어요.",
    gi_groups=[("기초 연산", ["matrix-multiplication", "matrix-add-subtract-scalar", "matrix-transpose-properties", "special-matrices"]),
               ("역행렬과 행렬식", ["inverse-gauss-jordan", "determinant-3x3", "determinant-properties", "inverse-adjugate-cofactor", "cramer-rule", "elementary-matrices"]),
               ("소거법과 벡터 공간", ["rank-and-rref", "linear-system-solutions", "null-space-column-space", "linear-independence"]),
               ("고윳값과 대각화", ["eigenvalues-2x2", "diagonalization-matrix-power"])], gi_other="그 밖의 글",
    gi_meta="역행렬, 행렬식, 계수와 RREF, 연립방정식의 해를 예제와 함께 단계별로 설명한 선형대수 가이드 모음이에요.",
    g_meta="", cta_t="직접 계산해 보세요", cta_s="", cta_b="{c} 열기", rel_h2="함께 보면 좋은 글", toc="목차", min="{m}분",
    about_title="소개 및 문의", privacy_title="개인정보처리방침",
    pr_title="행렬 연습 문제 생성기 - 채점·인쇄·워드 다운로드", pr_h1="연습 문제", pr_ld="행렬 연습 문제 생성기",
    pr_meta="행렬식, 역행렬, 곱셈, RREF, 연립방정식, 계수, 고윳값 연습 문제를 무작위로 만들어요. 웹에서 바로 채점하고, 문제지와 정답지를 PDF로 인쇄하거나 워드(.docx) 파일로 내려받을 수 있어요.",
    pr_intro="주제와 크기를 고르면 문제가 만들어져요. 답을 입력해 채점하고, 틀린 문제는 계산기에서 단계별 풀이를 볼 수 있어요. 수업용으로는 인쇄하거나 워드 파일로 내려받으세요.",
    pr_topic="주제", pr_size="크기", pr_count="문제 수", pr_tools="문제지 만들기", pr_name="이름: ____________    날짜: ____________",
    pr_note="같은 링크를 열면 같은 문제가 나와요. 학생에게 링크를 보내면 같은 문제 세트를 풀 수 있어요. 워드 파일의 행렬은 수식 개체라 워드에서 바로 편집할 수 있어요.",
    pr_faq=[("문제는 어떻게 만들어지나요?", "정수 행렬을 무작위로 만들되, 역행렬 문제는 답이 대부분 정수가 되도록, 연립방정식은 해가 유일하고 정수가 되도록, 고윳값 문제는 고윳값이 정수가 되도록 설계했어요."),
            ("답은 어떤 형식으로 입력하나요?", "정수, 분수(1/3), 소수(0.25) 모두 돼요. 고윳값은 쉼표로 구분해 입력하고 순서는 상관없어요."),
            ("PDF는 어떻게 저장하나요?", "인쇄 버튼을 누른 뒤 프린터 대신 'PDF로 저장'을 고르면 돼요. '정답지 포함'을 켜면 마지막 장에 정답이 붙어요.")],
    nf_title="페이지를 찾을 수 없어요", nf_meta="요청한 페이지가 없어요.",
)
UI_EN = dict(
    nav=[("calc", "/calculators/", "Calculators"), ("practice", "/practice/", "Practice"), ("guide", "/guide/", "Guides"), ("about", "/about/", "About")],
    nav_aria="Site", switch="한국어", switch_title="Korean", theme="Toggle light/dark",
    foot_note="", foot_aria="Site links",
    foot=[("/calculators/", "Calculators"), ("/practice/", "Practice"), ("/guide/", "Guides"), ("/about/", "About"), ("/about/#contact", "Contact"), ("/privacy/", "Privacy")],
    ops_aria="Choose an operation", extras_aria="More", calc=CALC_EN, howto=HOWTO_EN,
    fold_howto="How to use", fold_faq="FAQ", fold_related="Related guides", fold_about="About MatrixStep",
    more_guide="Full explanation with examples: {t}", tip="Exam tip",
    crumb_home="Home", crumb_calc="Calculators", crumb_guide="Guides",
    home_title="Matrix Calculator with Steps - Inverse, Determinant, RREF",
    home_meta="Free matrix calculator that works in exact fractions and shows every step: inverse, determinant, multiplication, RREF, linear systems and eigenvalues. Clean and fast, no sign-up.",
    home_h1="Matrix Calculator", home_intro="From inverses to linear systems: exact fractions, every step shown.",
    home_about=("<p>{site} is a free matrix calculator for the computations you meet in a linear algebra course. It works in exact fractions, so 1/3 stays 1/3 instead of 0.3333…, and it shows every step of the working. "
                "Results can be copied as LaTeX.</p>"
                "<p>Calculators: {ops}</p>"
                '<p><a href="{p}/calculators/">All calculators</a> · <a href="{p}/guide/">Concept guides</a></p>'),
    home_faq=[("What is the largest matrix I can enter?", "Up to 6×6. For multiplication and linear systems the exact limits depend on the operation."),
              ("Are the results exact?", "Yes. Every value is stored as a fraction, so there is no rounding error. The Decimal button only changes how results are displayed."),
              ("Is my matrix sent to a server?", "No. Everything is computed in your browser and nothing you type is transmitted anywhere.")],
    hub_title="All Matrix Calculators - 17 Operations", hub_h1="All matrix calculators", hub_ld="Matrix calculators",
    hub_meta="Seventeen matrix calculators in one place: addition, subtraction, multiplication, powers, transpose, inverse, determinant, adjugate, RREF, rank, linear systems, AX = B, LU, eigenvalues, diagonalization and Gram-Schmidt. All in exact fractions with steps.",
    hub_intro='Pick an operation and start calculating. If a concept is unclear, the <a href="{p}/guide/">guides</a> explain it with examples.',
    groups=[("Basic operations", ["add", "sub", "scalar", "mul", "power", "transpose"]), ("Inverse and determinant", ["inverse", "det", "adj"]),
            ("Elimination and linear systems", ["rref", "rank", "solve", "axb", "lu"]), ("Eigenvalues and orthogonalization", ["eigen", "diag", "gs"])],
    gi_title="Linear Algebra Guides", gi_h1="Guides", gi_intro="Short, example-driven explanations of the ideas behind the calculators. Every example can be checked in the calculator.",
    gi_groups=[("Basic operations", ["matrix-multiplication", "matrix-add-subtract-scalar", "matrix-transpose-properties", "special-matrices"]),
               ("Inverse and determinant", ["inverse-gauss-jordan", "determinant-3x3", "determinant-properties", "inverse-adjugate-cofactor", "cramer-rule", "elementary-matrices"]),
               ("Elimination and vector spaces", ["rank-and-rref", "linear-system-solutions", "null-space-column-space", "linear-independence"]),
               ("Eigenvalues and diagonalization", ["eigenvalues-2x2", "diagonalization-matrix-power"])], gi_other="More guides",
    gi_meta="Sixteen linear algebra guides with fully worked examples: matrix operations, inverses and determinants, RREF and linear systems, vector spaces, eigenvalues and diagonalization.",
    g_meta="", cta_t="Try it yourself", cta_s="", cta_b="Open the {c}", rel_h2="Related guides", toc="Contents", min="{m} min",
    about_title="About and Contact", privacy_title="Privacy Policy",
    pr_title="Matrix Practice Problems - Graded Online, Print or Word", pr_h1="Practice problems", pr_ld="Matrix practice problem generator",
    pr_meta="Generate random practice problems on determinants, inverses, multiplication, RREF, linear systems, rank and eigenvalues. Grade them online, print a worksheet with an answer key as PDF, or download a Word (.docx) file.",
    pr_intro="Pick a topic and size to generate a set. Enter your answers to grade them, and open any problem in the calculator for step-by-step working. For class, print the sheet or download it as Word.",
    pr_topic="Topic", pr_size="Size", pr_count="Problems", pr_tools="Worksheet", pr_name="Name: ____________    Date: ____________",
    pr_note="The same link always gives the same problems, so you can send a set to students. Matrices in the Word file are equation objects and can be edited in Word.",
    pr_faq=[("How are the problems generated?", "Random integer matrices, designed so that inverse problems mostly have integer answers, linear systems have a unique integer solution, and eigenvalue problems have integer eigenvalues."),
            ("How do I enter answers?", "Integers, fractions (1/3) and decimals (0.25) all work. Enter eigenvalues separated by commas, in any order."),
            ("How do I save a PDF?", "Click Print and choose 'Save as PDF' instead of a printer. Turn on 'Include answer key' to append the answers as the last page.")],
    nf_title="Page not found", nf_meta="The requested page does not exist.",
)

LANGS = {
    "ko": dict(code="ko", prefix="", site=SITE, locale="ko_KR", ops=OPS_KO, ui=UI_KO, guides=guides, operator=OPERATOR),
    "en": dict(code="en", prefix="/en", site=SITE_EN, locale="en_US", ops=OPS_EN, ui=UI_EN, guides=guides_en, operator=OPERATOR_EN),
}
L = LANGS["ko"]   # 현재 언어 (main에서 바꿔요)
U = UI_KO

def use(code):
    global L, U
    L = LANGS[code]; U = L["ui"]

def P(path):
    """현재 언어의 경로. 한국어는 그대로, 영어는 /en 을 앞에 붙여요."""
    return L["prefix"] + path

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'

def head(title, meta, path, extra="", alt=True):
    """path는 언어 접두사가 없는 논리 경로예요 (예: /inverse/). alt=False면 다른 언어 페이지가 없는 거예요."""
    url = DOMAIN + P(path)
    s = f'''<!doctype html>
<html lang="{L["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{var t=localStorage.getItem("mx-theme");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<title>{e(title)}</title>
<meta name="description" content="{e(meta)}">
<link rel="canonical" href="{url}">
'''
    if alt:
        s += (f'<link rel="alternate" hreflang="ko" href="{DOMAIN}{path}">\n'
              f'<link rel="alternate" hreflang="en" href="{DOMAIN}/en{path}">\n'
              f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/en{path}">\n')
    rss = f'<link rel="alternate" type="application/rss+xml" title="{e(SITE)} 가이드" href="{DOMAIN}/rss.xml">\n' if L["code"] == "ko" else ""
    s += f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="{L["site"]}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og.png">
<meta property="og:locale" content="{L["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F4FD8">
{rss}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{CSS_URL}">
'''
    if GOOGLE_VERIFY: s += f'<meta name="google-site-verification" content="{e(GOOGLE_VERIFY)}">\n'
    if NAVER_VERIFY: s += f'<meta name="naver-site-verification" content="{e(NAVER_VERIFY)}">\n'
    if ADSENSE_CLIENT: s += f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n'
    if GA_ID: s += f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>\n'
    return s + extra + "</head>\n"

def topbar(cur="", path="/", alt=True):
    links = "".join(f'<a href="{P(h)}"' + (' aria-current="page"' if k == cur else "") + f">{t}</a>" for k, h, t in U["nav"])
    other = "en" if L["code"] == "ko" else "ko"
    target = (LANGS[other]["prefix"] + path) if alt else (LANGS[other]["prefix"] + "/")
    links += f'<a class="lang" href="{target}" lang="{other}" hreflang="{other}" title="{U["switch_title"]}">{U["switch"]}</a>'
    links += (f'<button type="button" class="theme" id="themeBtn" aria-label="{U["theme"]}" title="{U["theme"]}">'
              '<svg class="sun" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
              '<svg class="moon" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>'
              '<script>(function(){var b=document.getElementById("themeBtn");b.addEventListener("click",function(){var r=document.documentElement,dark=r.dataset.theme==="dark"||(!r.dataset.theme&&matchMedia("(prefers-color-scheme: dark)").matches);r.dataset.theme=dark?"light":"dark";try{localStorage.setItem("mx-theme",r.dataset.theme)}catch(e){}})})();</script>')
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="{P("/")}"><span class="mark" aria-hidden="true">[ ]</span>{L["site"]}</a>
<nav class="top-nav" aria-label="{U["nav_aria"]}">{links}</nav>
</div></header>
'''

def footer():
    return sc_footer(SC[L["code"]])

def ad():
    if not (ADSENSE_CLIENT and AD_SLOT): return ""
    return f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>\n'

def opsnav(cur, home=False):
    out = []
    for o in L["ops"]:
        a = ""
        if o["key"] == cur: a = ' class="on"' if home else ' aria-current="page"'
        out.append(f'<a href="{P("/" + o["slug"] + "/")}"{a}>{o["label"]}</a>')
    return f'<nav class="ops" aria-label="{U["ops_aria"]}">' + "".join(out) + "</nav>"

def fold(title, body, cls=""):
    return f'<details class="fold {cls}"><summary><h2>{title}</h2></summary><div class="fold-b">{body}</div></details>\n'

def extras(o):
    """계산기 아래 접이식 설명. 기본은 모두 접혀 있고, 사용자가 열 때만 보여요."""
    G = L["guides"].BY_SLUG
    g = G.get(GUIDE_FOR.get(o["key"], ""))
    more = f'<p><a href="{P("/guide/" + g["slug"] + "/")}">{e(U["more_guide"].format(t=g["title"]))}</a></p>' if g else ""
    concept = "".join(f"<p>{e(x)}</p>" for x in o["cb"]) + more + f'<p class="tip"><b>{U["tip"]}</b>{e(o["tip"])}</p>'
    qa = "".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in o["faq"])
    rel = "".join(f'<li><a href="{P("/guide/" + x + "/")}">{e(G[x]["h1"])}</a><span>{e(G[x]["desc"])}</span></li>' for x in GUIDES_FOR.get(o["key"], []) if x in G)
    return (f'<section class="extras" aria-label="{U["extras_aria"]}">\n' + fold(e(o["ch"]), concept) + fold(U["fold_howto"], U["howto"])
            + fold(U["fold_faq"], f'<dl class="qa">{qa}</dl>')
            + (fold(U["fold_related"], f'<ul class="rel-list">{rel}</ul>') if rel else "") + "</section>\n")

def ld(o, path):
    d = {"@context": "https://schema.org", "@type": "WebApplication", "name": o["h1"], "url": DOMAIN + P(path),
         "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": L["code"],
         "description": o["meta"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW" if L["code"] == "ko" else "USD"}}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def crumbs(items):
    d = {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + P(p)} for i, (n, p) in enumerate(items)]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def website_ld():
    d = {"@context": "https://schema.org", "@type": "WebSite", "name": L["site"], "url": DOMAIN + P("/"), "inLanguage": L["code"],
         "alternateName": ["matrixstep", "MatrixStep"] if L["code"] == "ko" else ["Matrix Calculator", "matrixstep.net"]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"

def write(path, text):
    """path는 언어 접두사가 없는 논리 경로. 현재 언어에 맞는 폴더에 저장해요."""
    full = os.path.join(OUT, P(path).lstrip("/"))
    if path.endswith("/"): full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)

PAGE_END = f'<div class="toast" id="toast" role="status" hidden></div>\n<script src="{JS_URL}" defer></script>\n</body>\n</html>\n'

def op_page(o):
    """계산기 페이지: 제목 → 연산 선택 → 계산기·결과. 나머지는 접이식."""
    path = f'/{o["slug"]}/'
    s = head(o["title"] + " | " + L["site"], o["meta"], path, ld(o, path) + crumbs([(U["crumb_home"], "/"), (U["crumb_calc"], "/calculators/"), (o["h1"], path)]))
    s += f'<body data-op="{o["key"]}">\n' + topbar("calc", path) + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{e(o["h1"])}</h1><p>{e(o["desc"])}</p></div>\n' + opsnav(o["key"]) + "\n" + U["calc"] + ad()
    s += extras(o) + "</main>\n" + footer() + PAGE_END
    write(path, s)

def home_extras():
    ops = " · ".join(f'<a href="{P("/" + o["slug"] + "/")}">{o["label"]}</a>' for o in L["ops"])
    about = U["home_about"].format(site=L["site"], ops=ops, p=L["prefix"])
    dl = "".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in U["home_faq"])
    return (f'<section class="extras" aria-label="{U["extras_aria"]}">\n' + fold(U["fold_about"], about) + fold(U["fold_howto"], U["howto"])
            + fold(U["fold_faq"], f'<dl class="qa">{dl}</dl>') + "</section>\n")

def home():
    meta = U["home_meta"]
    title = U["home_title"] if L["code"] == "ko" else U["home_title"] + " | " + L["site"]
    s = head(title, meta, "/", website_ld() + ld(dict(h1=L["site"] if L["code"] == "ko" else "MatrixStep Matrix Calculator", meta=meta), "/"))
    s += '<body data-op="inverse">\n' + topbar("", "/") + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{U["home_h1"]}</h1><p>{U["home_intro"]}</p></div>\n'
    s += opsnav("inverse", home=True) + "\n" + U["calc"] + ad() + home_extras() + "</main>\n" + footer() + PAGE_END
    write("/", s)

OP_SYM = {"inverse": "A⁻¹", "det": "|A|", "mul": "A·B", "add": "A + B", "sub": "A − B", "scalar": "kA", "transpose": "Aᵀ", "rref": "[I|·]", "solve": "Ax = b",
          "rank": "rank", "power": "Aⁿ", "adj": "adj(A)", "eigen": "λ", "diag": "PDP⁻¹", "axb": "AX = B", "gs": "u⊥v", "lu": "LU"}

def calc_hub():
    by = {o["key"]: o for o in L["ops"]}
    ldj = {"@context": "https://schema.org", "@type": "ItemList", "name": U["hub_ld"],
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + P("/" + o["slug"] + "/"), "name": o["h1"]} for i, o in enumerate(L["ops"])]}
    s = head(U["hub_title"] + " | " + L["site"], U["hub_meta"], "/calculators/", '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + "</script>\n")
    s += "<body>\n" + topbar("calc", "/calculators/") + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{U["hub_h1"]}</h1><p>{U["hub_intro"].format(p=L["prefix"])}</p></div>\n'
    for title, keys in U["groups"]:
        s += f'<section class="hub-g"><h2>{title}</h2><div class="grid-ops">'
        s += "".join(f'<a href="{P("/" + by[k]["slug"] + "/")}"><span class="sym">{OP_SYM[k]}</span><b>{by[k]["h1"]}</b><span>{e(by[k]["card"])}</span></a>' for k in keys)
        s += "</div></section>\n"
    s += "</main>\n" + footer() + "</body>\n</html>\n"
    write("/calculators/", s)

def guide_page(g):
    path = f'/guide/{g["slug"]}/'
    alt = g["slug"] in guides.BY_SLUG and g["slug"] in guides_en.BY_SLUG
    ldj = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "inLanguage": L["code"],
           "description": g["meta"], "datePublished": g.get("published", FIRST_PUBLISHED), "dateModified": TODAY,
           "author": {"@type": "Organization", "name": L["site"]}, "publisher": {"@type": "Organization", "name": L["site"]},
           "mainEntityOfPage": DOMAIN + P(path)}
    # 본문의 h2에 id를 붙이고 목차를 만들어요
    heads = []
    def _id(m):
        heads.append(m.group(1))
        return f'<h2 id="s{len(heads)}">{m.group(1)}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", _id, g["body"])
    toc = (f'<aside class="toc" aria-label="{U["toc"]}"><span class="lbl">{U["toc"]}</span>'
           + "".join(f'<a href="#s{i + 1}">{re.sub(r"<[^>]+>", "", h)}</a>' for i, h in enumerate(heads)) + "</aside>") if heads else ""
    s = head(g["title"] + " | " + L["site"], g["meta"], path, '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + "</script>\n"
             + crumbs([(U["crumb_home"], "/"), (U["crumb_guide"], "/guide/"), (g["h1"], path)]), alt=alt)
    s += "<body>\n" + topbar("guide", path, alt) + '<main class="wrap guide-wrap"><article class="doc guide">'
    s += f'<p class="crumb"><a href="{P("/guide/")}">{U["crumb_guide"]}</a><span class="sep" aria-hidden="true">·</span><span class="rt">{U["min"].format(m=g["min"])}</span></p><h1>{e(g["h1"])}</h1>'
    s += body
    s += f'<div class="cta-box"><b>{U["cta_t"]}</b><a class="cta" href="{P(g["calc"][1])}">{e(U["cta_b"].format(c=g["calc"][0]))}</a></div>'
    G = L["guides"].BY_SLUG
    rel = [G[x] for x in g["related"] if x in G]
    if rel:
        s += f'<p class="lbl rel-h">{U["rel_h2"]}</p><ul class="rel">' + "".join(
            f'<li><a href="{P("/guide/" + r["slug"] + "/")}">{e(r["h1"])}</a></li>' for r in rel) + "</ul>"
    s += "</article>" + toc + "</main>\n" + footer() + "</body>\n</html>\n"
    write(path, s)

def guide_index():
    G = L["guides"].BY_SLUG
    placed = set()
    groups = []
    for title, slugs in U["gi_groups"]:
        items = [G[x] for x in slugs if x in G]
        placed.update(g["slug"] for g in items)
        if items: groups.append((title, items))
    rest = [g for g in L["guides"].ARTICLES if g["slug"] not in placed]
    if rest: groups.append((U["gi_other"], rest))
    body = f'<h1>{U["gi_h1"]}</h1><p class="meta">{U["gi_intro"]}</p>'
    for title, items in groups:
        body += f'<section class="glist-g"><h2 class="lbl">{title}</h2><ul class="glist">' + "".join(
            f'<li><a href="{P("/guide/" + g["slug"] + "/")}"><b>{e(g["h1"])}</b><span>{e(g["desc"])}</span><em>{U["min"].format(m=g["min"])}</em></a></li>' for g in items) + "</ul></section>"
    s = head(U["gi_title"] + " | " + L["site"], U["gi_meta"], "/guide/") + "<body>\n" + topbar("guide", "/guide/")
    s += f'<main class="wrap"><article class="doc index">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write("/guide/", s)

def practice():
    path = "/practice/"
    T = {"ko": dict(topics=[("mix", "종합"), ("det", "행렬식"), ("inverse", "역행렬"), ("mul", "곱셈"), ("addsub", "덧셈·뺄셈"), ("power", "거듭제곱"), ("rref", "RREF"), ("solve", "연립방정식"), ("rank", "계수(rank)"), ("eigen", "고윳값")],
                     sizes=[("mix", "섞어서"), ("2", "2×2"), ("3", "3×3")], new="새 문제", grade="전체 채점", show="정답 보기", print="인쇄 · PDF 저장", docx="워드(.docx) 내려받기", key="정답지 포함", share="문제 링크 복사", answers="정답"),
         "en": dict(topics=[("mix", "Mixed"), ("det", "Determinant"), ("inverse", "Inverse"), ("mul", "Multiplication"), ("addsub", "Add & subtract"), ("power", "Powers"), ("rref", "RREF"), ("solve", "Linear systems"), ("rank", "Rank"), ("eigen", "Eigenvalues")],
                     sizes=[("mix", "Mixed"), ("2", "2×2"), ("3", "3×3")], new="New set", grade="Grade all", show="Show answers", print="Print · Save as PDF", docx="Download Word (.docx)", key="Include answer key", share="Copy link", answers="Answers")}[L["code"]]
    opts = lambda xs: "".join(f'<option value="{v}">{e(t)}</option>' for v, t in xs)
    ld_ = ld(dict(h1=U["pr_ld"], meta=U["pr_meta"]), path) + crumbs([(U["crumb_home"], "/"), (U["pr_h1"], path)])
    qa = "".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in U["pr_faq"])
    s = head(U["pr_title"] + " | " + L["site"], U["pr_meta"], path, ld_) + "<body>\n" + topbar("practice", path) + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{e(U["pr_h1"])}</h1><p>{e(U["pr_intro"])}</p></div>\n'
    seg = lambda id_, xs, aria: f'<div class="seg pr-seg" id="{id_}" role="group" aria-label="{e(aria)}">' + "".join(f'<button type="button" data-v="{v}" aria-pressed="false">{e(t)}</button>' for v, t in xs) + "</div>"
    pills = "".join(f'<button type="button" data-v="{v}" aria-pressed="false">{e(t)}</button>' for v, t in T["topics"])
    ico = dict(new='<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 0 1 15.5-6.3L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.3L3 16M3 21v-5h5"/></svg>',
               print='<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v7H6z"/></svg>',
               docx='<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M7 10l5 5 5-5M4 21h16"/></svg>',
               share='<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5"/></svg>')
    s += f'''<section class="pr-top" aria-label="{e(U["pr_tools"])}">
<nav class="pr-topics" id="topic" aria-label="{e(U["pr_topic"])}">{pills}</nav>
<div class="pr-ctl">
<div class="pr-ctl-l">
<span class="pr-f"><span class="lbl">{e(U["pr_size"])}</span>{seg("size", T["sizes"], U["pr_size"])}</span>
<span class="pr-f"><span class="lbl">{e(U["pr_count"])}</span>{seg("count", [("5", "5"), ("10", "10"), ("20", "20")], U["pr_count"])}</span>
<button type="button" class="ghost" id="newBtn">{ico["new"]}{e(T["new"])}</button>
</div>
<div class="pr-ctl-r">
<button type="button" class="ghost" id="printBtn">{ico["print"]}{e(T["print"])}</button>
<button type="button" class="ghost" id="docxBtn">{ico["docx"]}{e(T["docx"])}</button>
<label class="pr-chk"><input type="checkbox" id="withAns"> {e(T["key"])}</label>
<button type="button" class="ghost" id="shareBtn">{ico["share"]}{e(T["share"])}</button>
</div>
</div>
</section>
<div class="sheet">
<header class="sheet-h">
<div class="sheet-t"><span class="lbl" id="sheetL"></span><h2 id="sheetT"></h2><p class="sheet-name">{e(U["pr_name"])}</p></div>
<div class="pr-bar"><span class="score" id="score" aria-live="polite"></span><button type="button" class="ghost" id="showAns">{e(T["show"])}</button><button type="button" class="ghost primary" id="gradeBtn">{e(T["grade"])}</button></div>
</header>
<div id="plist" class="pgrid"><noscript><p class="err">JavaScript</p></noscript></div>
<section class="keysheet" aria-label="{e(T["answers"])}"><h2>{e(T["answers"])}</h2><div id="keylist"></div></section>
</div>
<p class="hint pr-note">{e(U["pr_note"])}</p>
{ad()}<section class="extras" aria-label="{U["extras_aria"]}">{fold(U["fold_faq"], f'<dl class="qa">{qa}</dl>')}</section>
</main>
''' + footer() + f'<div class="toast" id="toast" role="status" hidden></div>\n<script src="{PRACTICE_URL}" defer></script>\n</body>\n</html>\n'
    write(path, s)

def doc_page(path, title, meta, body, cur=""):
    s = head(title + " | " + L["site"], meta, path) + "<body>\n" + topbar(cur, path)
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write(path, s)

def about():
    ncal, ngd = len(L["ops"]), len(L["guides"].ARTICLES)
    if L["code"] == "ko":
        story = dict(
            intro=f"{SITE}(matrixstep.net)는 대학 선형대수와 공업수학 수업에서 자주 쓰는 행렬 계산을 깔끔한 화면에서 할 수 있도록 만든 무료 도구예요. 기능을 넓게 늘리기보다 행렬 계산 하나에 집중해, 정확한 답과 읽기 쉬운 풀이 과정을 보여주는 것을 목표로 해요. 가입이나 설치 없이 바로 쓸 수 있어요.",
            why_h="왜 만들었나요", why_q="답보다 과정이 중요한데, 계산기들은 답만 보여줬어요.",
            why_p="기존 계산기는 답만 보여주거나 소수로 반올림해 손으로 푼 풀이와 비교하기 어려웠어요. 광고와 메뉴가 많아 정작 계산기를 찾기 힘든 경우도 많았고요. 그래서 계산기와 결과만 먼저 보이고, 설명은 필요할 때 펼쳐 보는 단순한 페이지로 만들었어요.",
            how_h="어떻게 계산하나요",
            how=[("분수로 정확한 계산", "모든 값을 정수 분자·분모로 저장해 계산해요. 0.3333… 같은 반올림 오차 없이 1/3처럼 정확한 값이 나오고, 소수 표시는 보여주는 방식만 바꿔요."),
                 ("교과서와 같은 방법", "역행렬과 RREF는 가우스-조던 소거법, 행렬식은 2×2 공식·3×3 여인수 전개·4×4 이상은 행 소거로 계산해요. 수업에서 배우는 순서 그대로예요."),
                 ("단계별 풀이", "행 연산 하나하나와 그때의 행렬을 순서대로 보여줘서, 어디서 계산이 틀렸는지 바로 찾을 수 있어요."),
                 ("브라우저 안에서만 계산", "입력한 행렬은 서버로 전송되지 않아요. 계산은 모두 사용 중인 브라우저에서 이루어져요."),
                 ("LaTeX 복사", "결과 행렬을 LaTeX 코드로 복사해 과제나 노트에 바로 붙여넣을 수 있어요.")],
            acc_h="정확성은 어떻게 확인하나요",
            acc=[("4,060", "무작위 행렬", "배포할 때마다 무작위로 만든 행렬 4,000여 개를 계산기 코드로 풀어요."),
                 ("×2", "독립 검산", "별도로 작성한 분수 계산 코드가 역행렬은 곱해서 단위행렬이 되는지, 해는 대입해 맞는지, 행렬식·RREF는 같은지 확인해요."),
                 ("0", "허용 오류", "하나라도 틀리면 배포되지 않아요. 가이드의 예제도 글을 쓸 때 같은 방식으로 다시 계산해요.")],
            acc_p="그래도 틀린 곳을 발견하면 아래 이메일로 알려 주세요. 입력한 행렬을 함께 적어 주시면 빠르게 확인하고 고칠 수 있어요.",
            what=[(f"/calculators/", f"계산기 {ncal}종", "역행렬부터 LU 분해, 그람-슈미트까지"), ("/guide/", f"가이드 {ngd}편", "예제와 함께 개념 정리"), ("/practice/", "연습 문제", "채점 · 인쇄 · 워드 다운로드")],
            contact_h="문의", contact_p="오류 제보, 기능 제안, 제휴 문의는 아래 이메일로 보내 주세요.", op=f"운영자 {OPERATOR}", privacy="개인정보처리방침")
        meta = f"{SITE}가 행렬을 분수로 정확하게 계산하는 방법, 결과를 검증하는 방식, 제공하는 계산기 {ncal}종과 가이드 {ngd}편, 문의 방법을 안내해요."
    else:
        story = dict(
            intro=f"{SITE_EN} (matrixstep.net) is a free matrix calculator built for the computations that come up in linear algebra and engineering math courses. Rather than piling on features, it focuses on one thing: giving an exact answer and a working you can actually read. There is nothing to install and no account to create.",
            why_h="Why it exists", why_q="The method matters more than the answer, yet calculators showed only the answer.",
            why_p="Most calculators either show only the answer or round everything to decimals, which makes it hard to compare with work done by hand. Many are also crowded with ads and menus that bury the calculator itself. So this one shows the calculator and the result first; explanations unfold only when you ask for them.",
            how_h="How it calculates",
            how=[("Exact fractions", "Every value is stored as an integer numerator and denominator. You get 1/3, not 0.3333…, and the Decimal button only changes the display."),
                 ("Textbook methods", "Gauss-Jordan elimination for inverses and RREF; the 2×2 formula, 3×3 cofactor expansion and row reduction for larger determinants. The same order you learn in class."),
                 ("Step-by-step working", "Each row operation is shown together with the matrix after it, so you can see exactly where a hand calculation went wrong."),
                 ("Everything in your browser", "The matrices you type are never sent to a server. All computation happens locally."),
                 ("LaTeX export", "Copy any result matrix as LaTeX and paste it straight into your notes or homework.")],
            acc_h="How accuracy is checked",
            acc=[("4,060", "random matrices", "Every deployment pushes about 4,000 randomly generated matrices through the calculator code."),
                 ("×2", "independent check", "A separate fraction-arithmetic implementation multiplies inverses back to the identity, substitutes solutions into the equations, and compares determinants and RREFs."),
                 ("0", "errors allowed", "If any check fails, the site is not deployed. The examples in the guides are recomputed the same way when they are written.")],
            acc_p="If you still find an error, please email the address below with the matrix you entered and it will be fixed promptly.",
            what=[("/calculators/", f"{ncal} calculators", "From inverses to LU and Gram-Schmidt"), ("/guide/", f"{ngd} guides", "Concepts with worked examples"), ("/practice/", "Practice problems", "Grade · print · Word download")],
            contact_h="Contact", contact_p="For bug reports, feature requests or partnership enquiries, email:", op=f"Operated by {OPERATOR_EN}", privacy="Privacy policy")
        meta = f"How {SITE_EN} computes matrices in exact fractions, how results are verified, the {ncal} calculators and {ngd} guides it offers, and how to get in touch."
    showcase_page(story, meta)

def story_html(st):
    how = "".join(f'<div class="sc-how"><span class="sc-no">{i+1:02d}</span><b>{e(t)}</b><p>{e(d)}</p></div>' for i, (t, d) in enumerate(st["how"]))
    acc = "".join(f'<div class="sc-step"><span class="sc-big">{e(n)}</span><b>{e(t)}</b><p>{e(d)}</p></div>' for n, t, d in st["acc"])
    what = "".join(f'<a href="{P(h)}" class="sc-what"><b>{e(t)}</b><span>{e(d)}</span><i aria-hidden="true">→</i></a>' for h, t, d in st["what"])
    return f'''<div class="sc-story">
<p class="sc-intro">{e(st["intro"])}</p>
<section class="sc-s sc-why"><div class="sc-s-h"><span class="lbl">01</span><h2>{e(st["why_h"])}</h2></div><div class="sc-split"><p class="sc-quote">{e(st["why_q"])}</p><p>{e(st["why_p"])}</p></div></section>
<section class="sc-s"><div class="sc-s-h"><span class="lbl">02</span><h2>{e(st["how_h"])}</h2></div><div class="sc-hows">{how}</div></section>
<section class="sc-s"><div class="sc-s-h"><span class="lbl">03</span><h2>{e(st["acc_h"])}</h2></div><div class="sc-steps">{acc}</div><p class="sc-note">{e(st["acc_p"])}</p></section>
<section class="sc-s"><div class="sc-whats">{what}</div></section>
<section class="sc-s" id="contact"><div class="sc-s-h"><span class="lbl">04</span><h2>{e(st["contact_h"])}</h2></div><p class="sc-note">{e(st["contact_p"])}</p>
<div class="sc-contact"><a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a><span>{e(st["op"])} · <a href="{P("/privacy/")}">{e(st["privacy"])}</a></span></div></section>
</div>'''

SC = {
 "ko": dict(eyebrow="17 CALCULATORS · EXACT FRACTIONS", h1a="행렬을", h1b="정확하게.",
   lead="반올림 없는 분수 계산, 한 줄씩 보이는 행 연산. 역행렬·행렬식·고윳값·대각화·LU까지, 선형대수 수업에 필요한 전부.",
   cta="지금 계산하기", cta2="연습 문제", cards_h="17가지 계산기", all="모두 보기 →",
   fl1="A⁻¹ · 3×3", fl2="λ · 고윳값", fl2b="p(λ) = λ² − 7λ + 10", fl3="R₂ ← R₂ − 2R₁",
   feats=[("1/3", "0.333…이 아니라 1/3", "모든 값을 분수로 들고 있어서 반올림 오차가 아예 생기지 않아요."),
          ("08", "모든 단계를 한 줄씩", "어떤 행에 무엇을 곱해 뺐는지, 시험지에 옮겨 적을 수 있게 보여줘요."),
          ("0 ms", "서버 없음, 전송 없음", "계산은 전부 브라우저 안에서. 입력한 행렬은 어디에도 가지 않아요.")],
   desc={"inverse": "가우스-조던 · 수반행렬", "det": "여인수 · 사루스 · 소거", "rref": "기약 행사다리꼴", "eigen": "특성다항식 · 고유벡터",
         "diag": "P, D, P⁻¹ 검산까지", "lu": "둘리틀 · PA = LU", "gs": "직교 기저"},
   pr="연습 문제", pr_d="채점 · 인쇄 · 워드", more="더 알아보기",
   f_tag="분수 그대로, 단계별로.", f_sub="계산은 전부 브라우저 안에서 끝나고 입력값은 어디에도 전송되지 않아요.",
   f_cols=[("CALCULATORS", [("/inverse/", "역행렬"), ("/determinant/", "행렬식"), ("/rref/", "RREF · 연립방정식"), ("/eigenvalues/", "고윳값 · 대각화"), ("/calculators/", "17가지 모두 보기 →")]),
           ("LEARN", [("/guide/", "가이드 16편"), ("/practice/", "연습 문제"), ("/practice/", "문제지 인쇄 · 워드")]),
           ("ABOUT", [("/about/", "소개"), ("/about/#contact", "문의"), ("/privacy/", "개인정보처리방침")])],
   f_badge="4,060 케이스 자동 검증 통과"),
 "en": dict(eyebrow="17 CALCULATORS · EXACT FRACTIONS", h1a="Matrices,", h1b="exactly.",
   lead="Exact fractions with no rounding, and every row operation shown one line at a time. Inverses, determinants, eigenvalues, diagonalization, LU: everything a linear algebra course needs.",
   cta="Start calculating", cta2="Practice problems", cards_h="17 calculators", all="See all →",
   fl1="A⁻¹ · 3×3", fl2="λ · eigenvalues", fl2b="p(λ) = λ² − 7λ + 10", fl3="R₂ ← R₂ − 2R₁",
   feats=[("1/3", "1/3, not 0.333…", "Every value is kept as a fraction, so rounding error never appears."),
          ("08", "Every step, one line each", "Which row, multiplied by what, subtracted from where: ready to copy onto your exam paper."),
          ("0 ms", "No server, nothing sent", "All computation happens in your browser. The matrices you type never leave it.")],
   desc={"inverse": "Gauss-Jordan · adjugate", "det": "Cofactors · Sarrus · elimination", "rref": "Reduced row echelon form", "eigen": "Characteristic polynomial · eigenvectors",
         "diag": "P, D, P⁻¹ with a check", "lu": "Doolittle · PA = LU", "gs": "Orthogonal basis"},
   pr="Practice", pr_d="Grade · print · Word", more="Learn more",
   f_tag="Exact fractions, step by step.", f_sub="Everything is computed in your browser and nothing you type is sent anywhere.",
   f_cols=[("CALCULATORS", [("/inverse/", "Inverse"), ("/determinant/", "Determinant"), ("/rref/", "RREF · linear systems"), ("/eigenvalues/", "Eigenvalues · diagonalization"), ("/calculators/", "All 17 →")]),
           ("LEARN", [("/guide/", "16 guides"), ("/practice/", "Practice problems"), ("/practice/", "Print · Word worksheets")]),
           ("ABOUT", [("/about/", "About"), ("/about/#contact", "Contact"), ("/privacy/", "Privacy")])],
   f_badge="4,060 random cases verified on every deploy"),
}
SC_SYM = {"inverse": "A⁻¹", "det": "|A|", "rref": "[I|·]", "eigen": "λ", "diag": "PDP⁻¹", "lu": "LU", "gs": "u⊥v"}

def mxh(rows, cls=""):
    c = len(rows[0])
    return (f'<span class="mx {cls}"><span class="mx-g" style="grid-template-columns:repeat({c},auto)">'
            + "".join(f'<span class="mx-c">{v}</span>' for r in rows for v in r) + "</span></span>")

def showcase_page(doc_body, meta):
    """소개 페이지: 검정 쇼케이스(히어로·계산기 카드·특징) + 기존 소개 글 + 4열 푸터."""
    T = SC[L["code"]]; path = "/about/"
    byk = {o["key"]: o for o in L["ops"]}
    force = '<script>document.documentElement.dataset.theme="dark"</script>\n'
    s = head(U["about_title"] + " | " + L["site"], meta, path, force + crumbs([(U["crumb_home"], "/"), (U["about_title"], path)]))
    s += '<body class="showcase">\n' + topbar("about", path)
    ops_tick = "".join(f"<span>{e(o['label'])}</span>" for o in L["ops"]) * 2
    cards = "".join(f'<a href="{P("/" + byk[k]["slug"] + "/")}" class="sc-card"><span class="sc-sym">{SC_SYM[k]}</span><b>{e(byk[k]["label"])}</b><span>{e(T["desc"][k])}</span></a>'
                    for k in ["inverse", "det", "rref", "eigen", "diag", "lu", "gs"])
    cards += f'<a href="{P("/practice/")}" class="sc-card sc-card-pr"><span class="sc-sym">∑</span><b>{e(T["pr"])}</b><span>{e(T["pr_d"])}</span></a>'
    feats = "".join(f'<div class="sc-feat"><span class="sc-big">{e(a)}</span><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in T["feats"])
    s += f'''<section class="sc-hero" aria-label="{e(U["about_title"])}">
<div class="sc-mesh" aria-hidden="true"></div><div class="sc-grid" aria-hidden="true"></div><div class="sc-dots" aria-hidden="true"></div>
<div class="wrap sc-hero-in">
<div class="sc-copy">
<span class="sc-eyebrow"><span aria-hidden="true"></span>{e(T["eyebrow"])}</span>
<h1><span class="gtxt">{e(T["h1a"])}</span><br><span class="gtxt">{e(T["h1b"])}</span></h1>
<p>{e(T["lead"])}</p>
<div class="sc-ctas"><a href="{P("/inverse/")}" class="sc-cta">{e(T["cta"])} <span aria-hidden="true">→</span></a><a href="{P("/practice/")}" class="sc-ghost">{e(T["cta2"])}</a></div>
</div>
<div class="sc-stage" aria-hidden="true">
<div class="sc-fl sc-fl1"><div class="sc-shine"></div><div class="sc-fl-l">{e(T["fl1"])}</div>{mxh([["0","0","1"],["−2","1","3"],["3","−1","−5"]])}</div>
<div class="sc-fl sc-fl2"><div class="sc-fl-l c2">{e(T["fl2"])}</div><div class="sc-fl-v">λ = 2, 5</div><div class="sc-fl-s">{e(T["fl2b"])}</div></div>
<div class="sc-fl sc-fl3"><div class="sc-fl-l c3">{e(T["fl3"])}</div>{mxh([["1","<i>½</i>"],["0","1"]])}</div>
</div>
</div>
<div class="sc-tickwrap"><div class="sc-tick" aria-hidden="true">{ops_tick}</div></div>
</section>
<main class="wrap sc-main">
<section class="sc-cards" aria-label="{e(T["cards_h"])}">
<div class="sc-cards-h"><h2>{e(T["cards_h"])}</h2><a href="{P("/calculators/")}">{e(T["all"])}</a></div>
<div class="sc-grid4">{cards}</div>
</section>
<section class="sc-feats" aria-label="{e(T["more"])}">{feats}</section>
{story_html(doc_body)}
</main>
''' + sc_footer(T) + "</body>\n</html>\n"
    write(path, s)

def sc_footer(T):
    cols = "".join(f'<nav aria-label="{c}"><span class="lbl">{c}</span>' + "".join(f'<a href="{P(h)}">{e(t)}</a>' for h, t in links) + "</nav>" for c, links in T["f_cols"])
    other = "en" if L["code"] == "ko" else "ko"
    langs = (f'<a class="on" href="{P("/about/")}">{"한국어" if L["code"] == "ko" else "English"}</a>'
             f'<a href="{LANGS[other]["prefix"]}/about/" lang="{other}" hreflang="{other}">{"English" if L["code"] == "ko" else "한국어"}</a>')
    return f'''<footer class="sc-foot">
<div class="wrap sc-foot-in">
<div class="sc-brand"><a class="brand" href="{P("/")}"><span class="mark" aria-hidden="true">[ ]</span>{L["site"]}</a><p>{e(T["f_tag"])}<br>{e(T["f_sub"])}</p><div class="sc-langs">{langs}</div></div>
{cols}
</div>
<div class="wrap sc-foot-b"><span>© 2026 {L["site"]} · matrixstep.net</span><span class="sc-badge"><span aria-hidden="true"></span>{e(T["f_badge"])}</span></div>
</footer>
'''


def privacy():
    if L["code"] == "ko":
        body = f'''<h1>개인정보처리방침</h1><p class="meta">시행일 {PRIVACY_DATE}</p>
<p>{e(OPERATOR)}(이하 ‘운영자’)는 {SITE}(이하 ‘사이트’)를 이용하는 분의 개인정보를 소중히 여기며, 「개인정보 보호법」 등 관련 법령을 지켜요. 이 방침은 사이트가 어떤 정보를 어떻게 다루는지 알려드려요.</p>
<h2>수집하는 개인정보</h2>
<p>사이트는 회원가입 없이 이용할 수 있고, 이름·연락처 같은 개인정보를 직접 수집하지 않아요. 계산을 위해 입력한 행렬 값은 이용자의 브라우저 안에서만 처리되며 운영자의 서버로 전송되지 않아요.</p>
<h2>브라우저에 저장되는 정보</h2>
<p>다른 계산기로 이동해도 입력값이 유지되도록, 입력한 행렬을 브라우저의 세션 저장소(sessionStorage)에 임시로 저장해요. 이 정보는 브라우저 탭을 닫으면 사라져요. 분수·소수 표시 설정은 브라우저의 로컬 저장소(localStorage)에 저장돼요. 이 정보들은 이용자의 기기에만 남고 운영자에게 전달되지 않아요.</p>
<h2>자동으로 수집되는 정보</h2>
<p>사이트를 제공하는 호스팅 서비스(Amazon Web Services)는 보안과 서비스 안정성을 위해 접속 IP 주소, 브라우저 종류, 접속 시간 같은 접속 기록을 자동으로 남길 수 있어요.</p>
<h2>쿠키와 외부 서비스</h2>
<p>사이트는 방문 통계 분석을 위해 Google Analytics를, 광고 게재를 위해 Google AdSense를 이용하거나 이용할 수 있어요. 이 서비스들은 쿠키를 사용해 방문 기록을 바탕으로 통계를 내거나, 이용자의 관심사에 맞는 광고를 보여줄 수 있어요.</p>
<ul><li>Google을 포함한 제3자 광고 사업자는 쿠키를 사용해 이용자의 이 사이트 및 다른 사이트 방문 기록을 기반으로 광고를 게재해요.</li>
<li>맞춤 광고는 <a href="https://adssettings.google.com" rel="noopener">Google 광고 설정</a>에서 끌 수 있어요.</li>
<li>Google이 정보를 이용하는 방식은 <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">Google 파트너 사이트 정책</a>에서 확인할 수 있어요.</li>
<li>브라우저 설정에서 쿠키 저장을 거부하거나 삭제할 수 있어요. 다만 일부 기능이나 광고 표시가 달라질 수 있어요.</li></ul>
<h2>개인정보의 보유 및 파기</h2>
<p>운영자는 개인정보를 직접 보관하지 않아요. 이메일로 문의하신 경우, 받은 이메일 주소와 문의 내용은 답변을 마친 뒤 지체 없이 삭제해요.</p>
<h2>이용자의 권리</h2>
<p>이용자는 언제든지 자신의 개인정보 처리에 대해 열람, 정정, 삭제, 처리 정지를 요청할 수 있어요. 아래 문의처로 연락해 주세요.</p>
<h2>개인정보 보호 책임자 및 문의처</h2>
<p>책임자: {e(OPERATOR)}<br>이메일: {e(EMAIL)}</p>
<p>개인정보 침해에 대한 상담이 필요하면 개인정보침해신고센터(privacy.kisa.or.kr, 국번 없이 118)에 문의할 수 있어요.</p>
<h2>방침의 변경</h2>
<p>이 방침이 바뀌면 사이트에서 시행일과 함께 알려드려요.</p>'''
        meta = f"{SITE}의 개인정보처리방침이에요."
    else:
        body = f'''<h1>Privacy Policy</h1><p class="meta">Effective {PRIVACY_DATE}</p>
<p>{e(OPERATOR_EN)} (the “operator”) runs {SITE_EN} at matrixstep.net (the “site”). This policy explains what information the site handles and how.</p>
<h2>Information we collect</h2>
<p>The site can be used without an account, and it does not ask for personal information such as your name or contact details. The matrices you enter are processed entirely in your browser and are never sent to the operator's servers.</p>
<h2>Data stored in your browser</h2>
<p>So that your input survives switching between calculators, the matrices you enter are kept temporarily in your browser's session storage (sessionStorage); this is cleared when you close the tab. Your fraction/decimal display preference is kept in local storage (localStorage). Both stay on your device and are not transmitted to the operator.</p>
<h2>Information collected automatically</h2>
<p>The hosting provider (Amazon Web Services) may automatically record access logs such as IP address, browser type and time of access for security and reliability purposes.</p>
<h2>Cookies and third-party services</h2>
<p>The site uses, or may use, Google Analytics to measure traffic and Google AdSense to serve advertising. These services use cookies to compile statistics from your visits and may show ads based on your interests.</p>
<ul><li>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website and other websites.</li>
<li>You can opt out of personalised advertising in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>.</li>
<li>How Google uses data from sites that use its services is described in <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">Google's partner sites policy</a>.</li>
<li>You can refuse or delete cookies in your browser settings; some features or ads may then behave differently.</li></ul>
<h2>Retention</h2>
<p>The operator does not keep any personal data itself. If you contact us by email, your address and message are deleted once the enquiry has been answered.</p>
<h2>Your rights</h2>
<p>You may at any time request access to, correction or deletion of, or a halt to the processing of your personal data by contacting the address below.</p>
<h2>Contact</h2>
<p>Responsible person: {e(OPERATOR_EN)}<br>Email: {e(EMAIL)}</p>
<h2>Changes to this policy</h2>
<p>If this policy changes, the new version and its effective date will be published on the site.</p>'''
        meta = f"Privacy policy for {SITE_EN} (matrixstep.net)."
    doc_page("/privacy/", U["privacy_title"], meta, body)

def notfound():
    """404는 한 파일로 모든 언어를 받아요. 한국어 안내 아래에 영어 안내를 함께 둬요."""
    ko_ops = "".join(f'<li><a href="/{o["slug"]}/"><b>{o["h1"]}</b><span>{e(o["card"])}</span></a></li>' for o in OPS_KO)
    body = ('<p class="big404" aria-hidden="true">404</p><h1>페이지를 찾을 수 없어요</h1><p>주소가 바뀌었거나 없는 페이지예요. 아래에서 원하는 계산기를 골라 주세요.</p><ul class="oplist">' + ko_ops + "</ul>"
            '<p lang="en"><strong>Page not found.</strong> The address may have changed. Go to the <a href="/en/">English matrix calculator</a> or <a href="/en/calculators/">all calculators</a>.</p>')
    s = head("페이지를 찾을 수 없어요 | " + SITE, "요청한 페이지가 없어요.", "/404.html", '<meta name="robots" content="noindex">\n', alt=False) + "<body>\n" + topbar("", "/", alt=False)
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(s)

def seo_files():
    def urls_for(code):
        Lx = LANGS[code]; p = Lx["prefix"]
        return ([p + "/", p + "/calculators/", p + "/practice/"] + [f'{p}/{o["slug"]}/' for o in Lx["ops"]] + [p + "/guide/"]
                + [f'{p}/guide/{g["slug"]}/' for g in Lx["guides"].ARTICLES] + [p + "/about/", p + "/privacy/"])
    urls = urls_for("ko") + urls_for("en")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    # 가이드 RSS (네이버 서치어드바이저 RSS 제출용). 최근 게시 순.
    def rfc822(d):
        return datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0900")
    items = sorted(guides.ARTICLES, key=lambda g: g.get("published", FIRST_PUBLISHED), reverse=True)
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
           f"<title>{e(SITE)} 가이드</title>\n<link>{DOMAIN}/guide/</link>\n"
           f"<description>역행렬, 행렬식, RREF, 연립방정식, 고윳값 등 선형대수 개념을 예제와 함께 설명하는 가이드예요.</description>\n"
           f'<language>ko</language>\n<lastBuildDate>{rfc822(TODAY)}</lastBuildDate>\n<atom:link href="{DOMAIN}/rss.xml" rel="self" type="application/rss+xml"/>\n')
    for g in items:
        rss += (f"<item>\n<title>{e(g['h1'])}</title>\n<link>{DOMAIN}/guide/{g['slug']}/</link>\n<guid isPermaLink=\"true\">{DOMAIN}/guide/{g['slug']}/</guid>\n"
                f"<description>{e(g['meta'])}</description>\n<pubDate>{rfc822(g.get('published', FIRST_PUBLISHED))}</pubDate>\n</item>\n")
    rss += "</channel>\n</rss>\n"
    open(os.path.join(OUT, "rss.xml"), "w", encoding="utf-8").write(rss)
    if ADSENSE_CLIENT:
        pub = ADSENSE_CLIENT.replace("ca-", "")
        open(os.path.join(OUT, "ads.txt"), "w").write(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")

def build_lang(code):
    use(code)
    home(); calc_hub(); practice()
    for o in L["ops"]: op_page(o)
    guide_index()
    for g in L["guides"].ARTICLES: guide_page(g)
    about(); privacy()

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"), ignore=shutil.ignore_patterns("*.src.js"))
    open(os.path.join(OUT, "assets", "practice.js"), "w", encoding="utf-8").write(PRACTICE_JS)
    for f in os.listdir(os.path.join(HERE, "static")):
        shutil.copy(os.path.join(HERE, "static", f), OUT)
    build_lang("ko")
    build_lang("en")
    use("ko")
    notfound(); seo_files()
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    main()
