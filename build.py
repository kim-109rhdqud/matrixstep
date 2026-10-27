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
  title="RREF 계산기 - 기약 행사다리꼴과 랭크", h1="RREF 계산기",
  meta="행렬을 기약 행사다리꼴(RREF)로 바꾸는 행 연산을 단계별로 보여주고, 랭크와 피벗 열까지 알려줘요.",
  desc="행 연산으로 기약 행사다리꼴을 만들고 랭크와 피벗 열을 알려드려요.",
  card="기약 행사다리꼴과 랭크 구하기",
  ch="기약 행사다리꼴 (RREF)",
  cb=["각 행의 첫 번째 0이 아닌 성분(피벗)이 1이고, 피벗이 있는 열의 다른 성분이 모두 0인 형태예요. 영행은 맨 아래에 와요.",
      "어떤 행렬이든 RREF는 하나로 정해져서, 랭크나 연립방정식의 해를 판단할 때 기준이 돼요."],
  tip="피벗의 개수가 곧 행렬의 랭크예요.",
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
  tip="랭크 = 미지수 개수이고 모순이 없으면 해가 하나뿐이에요.",
  faq=[("식의 개수와 미지수 개수가 달라도 되나요?","네. 행(식)과 열(미지수)을 따로 조절할 수 있어요."),
       ("해가 무수히 많을 때 t는 무엇인가요?","자유변수를 나타내는 매개변수예요. t에 어떤 수를 넣어도 방정식을 만족하는 해가 돼요.")]),
 dict(key="rank", slug="rank", label="랭크",
  title="행렬 랭크 계산기 - 랭크·영공간 차원·피벗 열까지", h1="행렬 랭크 계산기",
  meta="행렬의 랭크를 행 연산 과정과 함께 구하고, 영공간의 차원(nullity)과 피벗 열, 열공간의 기저까지 알려줘요. 분수도 정확하게 계산해요.",
  desc="행 연산으로 피벗을 찾아 랭크를 구하고, 영공간의 차원과 피벗 열을 알려드려요.",
  card="랭크와 영공간 차원 구하기",
  ch="랭크란?",
  cb=["랭크는 행렬에서 서로 독립인 행(또는 열)의 개수예요. 기약 행사다리꼴로 바꿨을 때 피벗의 개수와 같아요.",
      "랭크-영공간 차원 정리: rank(A) + nullity(A) = 열의 수. nullity는 Ax = 0의 해 공간의 차원이에요."],
  tip="n×n 행렬의 랭크가 n이면 역행렬이 있고 행렬식이 0이 아니에요.",
  faq=[("랭크와 행렬식은 어떤 관계인가요?","정사각행렬에서 행렬식이 0이 아니면 랭크가 최대(n)예요. 행렬식이 0이면 랭크가 n보다 작아요."),
       ("열공간의 기저는 어떻게 구하나요?","RREF에서 피벗이 있는 열 번호를 찾고, 원래 행렬 A의 그 열들을 가져오면 돼요. RREF의 열을 쓰면 안 돼요."),
       ("행 랭크와 열 랭크가 다를 수 있나요?","아니요. 항상 같아요. 그래서 rank(A) = rank(Aᵀ)예요.")]),
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
]

# 계산기 → 관련 가이드 (영어판에는 있는 글만 보여줘요)
GUIDE_FOR = {"inverse": "inverse-gauss-jordan", "det": "determinant-3x3", "rref": "rank-and-rref", "solve": "linear-system-solutions",
             "mul": "matrix-multiplication", "add": "matrix-add-subtract-scalar", "sub": "matrix-add-subtract-scalar",
             "scalar": "matrix-add-subtract-scalar", "transpose": "matrix-transpose-properties",
             "rank": "rank-and-rref", "power": "diagonalization-matrix-power", "adj": "inverse-adjugate-cofactor", "eigen": "eigenvalues-2x2"}
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
}

# ===================== 화면 문구 =====================
CALC_KO = '''<div class="work">
<section class="panel in" aria-labelledby="inH">
<div class="panel-head"><h2 id="inH">INPUT · 입력</h2><div class="acts"><button type="button" class="ghost" id="exBtn">예제 넣기</button><button type="button" class="ghost" id="clrBtn">모두 지우기</button></div></div>
<div id="inputs"><noscript><p class="err">계산기를 쓰려면 브라우저에서 자바스크립트를 켜 주세요.</p></noscript></div>
<p class="hint">정수, 분수(<code>1/3</code>), 소수(<code>0.25</code>)를 쓸 수 있어요. 빈칸은 0이에요.</p>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">RESULT · 결과</h2><div class="seg" role="group" aria-label="숫자 표시 방식"><button type="button" data-mode="frac" aria-pressed="true">분수</button><button type="button" data-mode="dec" aria-pressed="false">소수</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="copyTex">LaTeX 복사</button><p class="texnote">LaTeX는 과제·논문(Overleaf), 노션 수식 블록, 워드 수식 편집기에 붙여넣는 수식 코드예요.</p></div>
</section>
</div>
<details class="fold steps-fold" id="stepsD" hidden><summary><h2>단계별 풀이</h2><span class="cnt" id="stepCount"></span></summary>
<div class="fold-b"><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div></details>
'''
CALC_EN = '''<div class="work">
<section class="panel in" aria-labelledby="inH">
<div class="panel-head"><h2 id="inH">INPUT</h2><div class="acts"><button type="button" class="ghost" id="exBtn">Load example</button><button type="button" class="ghost" id="clrBtn">Clear all</button></div></div>
<div id="inputs"><noscript><p class="err">Please enable JavaScript in your browser to use the calculator.</p></noscript></div>
<p class="hint">Integers, fractions (<code>1/3</code>) and decimals (<code>0.25</code>) are accepted. Empty cells count as 0.</p>
</section>
<section class="panel out" aria-labelledby="outH">
<div class="panel-head"><h2 id="outH">RESULT</h2><div class="seg" role="group" aria-label="Number format"><button type="button" data-mode="frac" aria-pressed="true">Fraction</button><button type="button" data-mode="dec" aria-pressed="false">Decimal</button></div></div>
<div class="res-main" id="resMain" aria-live="polite"></div>
<div class="res-actions"><button type="button" class="ghost" id="copyTex">Copy LaTeX</button><p class="texnote">LaTeX is the math code you can paste into Overleaf, Notion equation blocks or Word's equation editor.</p></div>
</section>
</div>
<details class="fold steps-fold" id="stepsD" hidden><summary><h2>Steps</h2><span class="cnt" id="stepCount"></span></summary>
<div class="fold-b"><ol id="steps"></ol><button type="button" class="ghost more" id="moreBtn" hidden></button></div></details>
'''

HOWTO_KO = '''<ol class="howto">
<li>행·열 버튼으로 행렬 크기를 정해요. 최대 6×6까지 입력할 수 있어요.</li>
<li>칸에 숫자를 입력하면 바로 계산돼요. 분수는 <code>1/3</code>, 음수는 <code>-2</code>처럼 입력해요.</li>
<li><kbd>Enter</kbd>는 다음 칸, <kbd>↑</kbd> <kbd>↓</kbd>는 위아래 칸으로 이동해요.</li>
<li>‘단계별 풀이’를 누르면 계산 과정이 펼쳐져요. ‘LaTeX 복사’는 Overleaf, 노션 수식 블록, 워드 수식 편집기에 붙여넣을 수 있는 수식 코드를 복사해요.</li>
</ol>'''
HOWTO_EN = '''<ol class="howto">
<li>Set the matrix size with the row and column buttons. Up to 6×6 is supported.</li>
<li>Type numbers into the cells and the result updates instantly. Enter fractions as <code>1/3</code> and negatives as <code>-2</code>.</li>
<li><kbd>Enter</kbd> moves to the next cell; <kbd>↑</kbd> <kbd>↓</kbd> move up and down.</li>
<li>Open ‘Steps’ to see the full working. ‘Copy LaTeX’ copies the result as math code you can paste into Overleaf, a Notion equation block or Word's equation editor.</li>
</ol>'''

UI_KO = dict(
    nav=[("calc", "/calculators/", "계산기"), ("guide", "/guide/", "가이드"), ("about", "/about/", "소개")],
    nav_aria="사이트", switch="EN", switch_title="English",
    foot_note="계산은 모두 브라우저 안에서 처리돼요.", foot_aria="사이트 정보",
    foot=[("/calculators/", "계산기"), ("/guide/", "가이드"), ("/about/", "소개"), ("/about/#contact", "문의"), ("/privacy/", "개인정보처리방침")],
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
    hub_title="행렬 계산기 모음 - 13가지 연산", hub_h1="행렬 계산기 모음", hub_ld="행렬 계산기 모음",
    hub_meta="덧셈·뺄셈·곱셈·거듭제곱·전치부터 역행렬, 행렬식, 수반행렬, RREF, 랭크, 연립방정식, 고윳값까지 행렬 계산기 13종을 한곳에 모았어요. 모두 분수로 정확하게 계산하고 풀이 과정을 보여줘요.",
    hub_intro='필요한 연산을 골라 바로 계산해 보세요. 개념이 헷갈리면 <a href="{p}/guide/">가이드</a>도 있어요.',
    groups=[("기본 연산", ["add", "sub", "scalar", "mul", "power", "transpose"]), ("역행렬과 행렬식", ["inverse", "det", "adj"]),
            ("소거법과 연립방정식", ["rref", "rank", "solve"]), ("고윳값", ["eigen"])],
    gi_title="행렬 가이드", gi_h1="가이드", gi_intro="시험 범위에서 자주 헷갈리는 개념을 예제와 함께 정리했어요. 모든 예제는 계산기로 바로 확인할 수 있어요.",
    gi_groups=[("기초 연산", ["matrix-multiplication", "matrix-add-subtract-scalar", "matrix-transpose-properties", "special-matrices"]),
               ("역행렬과 행렬식", ["inverse-gauss-jordan", "determinant-3x3", "determinant-properties", "inverse-adjugate-cofactor", "cramer-rule", "elementary-matrices"]),
               ("소거법과 벡터 공간", ["rank-and-rref", "linear-system-solutions", "null-space-column-space", "linear-independence"]),
               ("고윳값과 대각화", ["eigenvalues-2x2", "diagonalization-matrix-power"])], gi_other="그 밖의 글",
    gi_meta="역행렬, 행렬식, 랭크와 RREF, 연립방정식의 해를 예제와 함께 단계별로 설명한 선형대수 가이드 모음이에요.",
    g_meta="{d} 업데이트 · 읽는 시간 약 {m}분", cta_t="직접 계산해 보세요", cta_s="값을 바꾸면 결과와 단계별 풀이가 바로 나와요.", cta_b="{c} 열기", rel_h2="함께 보면 좋은 글", toc="목차", min="{m}분",
    about_title="소개 및 문의", privacy_title="개인정보처리방침",
    nf_title="페이지를 찾을 수 없어요", nf_meta="요청한 페이지가 없어요.",
)
UI_EN = dict(
    nav=[("calc", "/calculators/", "Calculators"), ("guide", "/guide/", "Guides"), ("about", "/about/", "About")],
    nav_aria="Site", switch="한국어", switch_title="Korean",
    foot_note="All calculations run in your browser.", foot_aria="Site links",
    foot=[("/calculators/", "Calculators"), ("/guide/", "Guides"), ("/about/", "About"), ("/about/#contact", "Contact"), ("/privacy/", "Privacy")],
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
    hub_title="All Matrix Calculators - 13 Operations", hub_h1="All matrix calculators", hub_ld="Matrix calculators",
    hub_meta="Thirteen matrix calculators in one place: addition, subtraction, multiplication, powers, transpose, inverse, determinant, adjugate, RREF, rank, linear systems and eigenvalues. All in exact fractions with steps.",
    hub_intro='Pick an operation and start calculating. If a concept is unclear, the <a href="{p}/guide/">guides</a> explain it with examples.',
    groups=[("Basic operations", ["add", "sub", "scalar", "mul", "power", "transpose"]), ("Inverse and determinant", ["inverse", "det", "adj"]),
            ("Elimination and linear systems", ["rref", "rank", "solve"]), ("Eigenvalues", ["eigen"])],
    gi_title="Linear Algebra Guides", gi_h1="Guides", gi_intro="Short, example-driven explanations of the ideas behind the calculators. Every example can be checked in the calculator.",
    gi_groups=[("Inverse and determinant", ["inverse-gauss-jordan", "determinant-3x3"]), ("Elimination and linear systems", ["rank-and-rref", "linear-system-solutions"])], gi_other="More guides",
    gi_meta="Step-by-step explanations of inverses, determinants, rank and RREF, and solving linear systems, each with fully worked examples.",
    g_meta="Updated {d} · about {m} min read", cta_t="Try it yourself", cta_s="Change the values and the result and steps update instantly.", cta_b="Open the {c}", rel_h2="Related guides", toc="Contents", min="{m} min",
    about_title="About and Contact", privacy_title="Privacy Policy",
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
<link rel="stylesheet" href="/assets/app.css">
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
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="{P("/")}"><span class="mark" aria-hidden="true">[ ]</span>{L["site"]}</a>
<nav class="top-nav" aria-label="{U["nav_aria"]}">{links}</nav>
</div></header>
'''

def footer():
    nav = "".join(f'<a href="{P(h)}">{t}</a>' for h, t in U["foot"])
    return f'''<footer class="wrap foot"><span>© 2026 {L["site"]}. {U["foot_note"]}</span>
<nav aria-label="{U["foot_aria"]}">{nav}</nav></footer>
'''

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

PAGE_END = '<div class="toast" id="toast" role="status" hidden></div>\n<script src="/assets/app.js" defer></script>\n</body>\n</html>\n'

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

def calc_hub():
    by = {o["key"]: o for o in L["ops"]}
    ldj = {"@context": "https://schema.org", "@type": "ItemList", "name": U["hub_ld"],
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + P("/" + o["slug"] + "/"), "name": o["h1"]} for i, o in enumerate(L["ops"])]}
    s = head(U["hub_title"] + " | " + L["site"], U["hub_meta"], "/calculators/", '<script type="application/ld+json">' + json.dumps(ldj, ensure_ascii=False) + "</script>\n")
    s += "<body>\n" + topbar("calc", "/calculators/") + '<main class="wrap">\n'
    s += f'<div class="intro"><h1>{U["hub_h1"]}</h1><p>{U["hub_intro"].format(p=L["prefix"])}</p></div>\n'
    for title, keys in U["groups"]:
        s += f'<section class="hub-g"><h2>{title}</h2><div class="grid-ops">'
        s += "".join(f'<a href="{P("/" + by[k]["slug"] + "/")}"><b>{by[k]["h1"]}</b><span>{e(by[k]["card"])}</span></a>' for k in keys)
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
    s += f'<p class="crumb"><a href="{P("/guide/")}">{U["crumb_guide"]}</a></p><h1>{e(g["h1"])}</h1><p class="meta">{U["g_meta"].format(d=TODAY, m=g["min"])}</p>'
    s += body
    s += f'<div class="cta-box"><div><b>{U["cta_t"]}</b><span>{U["cta_s"]}</span></div><a class="cta" href="{P(g["calc"][1])}">{e(U["cta_b"].format(c=g["calc"][0]))}</a></div>'
    G = L["guides"].BY_SLUG
    rel = [G[x] for x in g["related"] if x in G]
    if rel:
        s += f'<p class="lbl rel-h">{U["rel_h2"]}</p><ul class="rel">' + "".join(
            f'<li><a href="{P("/guide/" + r["slug"] + "/")}">{e(r["h1"])}<span>{U["min"].format(m=r["min"])}</span></a></li>' for r in rel) + "</ul>"
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

def doc_page(path, title, meta, body, cur=""):
    s = head(title + " | " + L["site"], meta, path) + "<body>\n" + topbar(cur, path)
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    write(path, s)

def about():
    ncal, ngd = len(L["ops"]), len(L["guides"].ARTICLES)
    ops_list = "".join(f'<li><a href="{P("/" + o["slug"] + "/")}"><b>{o["h1"]}</b><span>{e(o["card"])}</span></a></li>' for o in L["ops"])
    if L["code"] == "ko":
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
<p>계산기 코드는 배포할 때마다 자동 검사를 거쳐요. 무작위로 만든 행렬 2,400여 개를 계산기와 똑같이 풀게 한 뒤, 별도로 작성한 분수 계산 코드로 역행렬은 원래 행렬과 곱해 단위행렬이 되는지, 연립방정식의 해는 원래 식에 대입해 맞는지, 행렬식과 RREF는 독립 계산 결과와 같은지 확인해요. 검사를 통과하지 못하면 배포되지 않아요. 가이드에 실린 예제도 글을 쓸 때 같은 방식으로 다시 계산해 숫자를 맞춘 뒤 올려요. 그래도 틀린 곳을 발견하면 아래 이메일로 알려 주세요. 입력한 행렬을 함께 적어 주시면 빠르게 확인하고 고칠 수 있어요.</p>
<h2>제공하는 계산기 {ncal}종</h2><ul class="oplist">{ops_list}</ul>
<h2>가이드 {ngd}편</h2>
<p>계산기만으로는 부족한 개념은 <a href="/guide/">가이드</a>에서 예제와 함께 설명해요. 역행렬과 행렬식 같은 기본부터 랭크, 영공간, 선형독립, 고윳값까지, 시험에서 자주 헷갈리는 순서로 정리했어요. 모든 글은 직접 손으로 따라 풀 수 있는 작은 예제로 시작하고, 마지막에는 계산기로 바로 확인할 수 있게 이어져요.</p>
<h2 id="contact">문의</h2>
<p>오류 제보, 기능 제안, 제휴 문의는 아래 이메일로 보내 주세요.</p>
<div class="contact"><a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a><span>운영자 {e(OPERATOR)} · <a href="/privacy/">개인정보처리방침</a></span></div>'''
        meta = f"{SITE}가 행렬을 분수로 정확하게 계산하는 방법, 결과를 검증하는 방식, 제공하는 계산기 {ncal}종과 가이드 {ngd}편, 문의 방법을 안내해요."
    else:
        body = f'''<h1>About {SITE_EN}</h1><p class="meta">Last updated {TODAY}</p>
<p>{SITE_EN} (matrixstep.net) is a free matrix calculator built for the computations that come up in linear algebra and engineering math courses. Rather than piling on features, it focuses on one thing: giving an exact answer and a working you can actually read. There is nothing to install and no account to create.</p>
<h2>Why it exists</h2>
<p>In matrix problems the method matters more than the answer, yet most calculators either show only the answer or round everything to decimals, which makes it hard to compare with work done by hand. Many are also crowded with ads and menus that bury the calculator itself. {SITE_EN} shows the calculator and the result first; explanations unfold only when you ask for them.</p>
<h2>How it calculates</h2><ul>
<li><strong>Exact fractions</strong>: every value is stored as an integer numerator and denominator. You get 1/3, not 0.3333…, and the Decimal button only changes the display.</li>
<li><strong>Textbook methods</strong>: Gauss-Jordan elimination for inverses and RREF; the 2×2 formula, 3×3 cofactor expansion and row reduction for larger determinants. The same order you learn in class.</li>
<li><strong>Step-by-step working</strong>: each row operation is shown together with the matrix after it, so you can see exactly where a hand calculation went wrong.</li>
<li><strong>Everything in your browser</strong>: the matrices you type are never sent to a server. All computation happens locally.</li>
<li><strong>LaTeX export</strong>: copy any result matrix as LaTeX and paste it straight into your notes or homework.</li></ul>
<h2>How accuracy is checked</h2>
<p>Every deployment runs an automated check. About 2,400 randomly generated matrices are pushed through the calculator code, and an independent fraction-arithmetic implementation verifies the results: inverses are multiplied back to confirm they give the identity, solutions of linear systems are substituted into the original equations, and determinants and RREFs are compared against the independent computation. If any check fails, the site is not deployed. The examples in the guides are recomputed the same way when they are written. If you still find an error, please email the address below with the matrix you entered and it will be fixed promptly.</p>
<h2>Calculators ({ncal})</h2><ul class="oplist">{ops_list}</ul>
<h2>Guides ({ngd})</h2>
<p>For the ideas behind the calculators, the <a href="/en/guide/">guides</a> explain inverses, determinants, rank and RREF, and the solution sets of linear systems with fully worked examples. Each one starts from a small example you can follow by hand and ends with a link to check it in the calculator. The Korean edition of the site has more guides, and they are being translated.</p>
<h2 id="contact">Contact</h2>
<p>For bug reports, feature requests or partnership enquiries, email:</p>
<div class="contact"><a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a><span>Operated by {e(OPERATOR_EN)} · <a href="/en/privacy/">Privacy policy</a></span></div>'''
        meta = f"How {SITE_EN} computes matrices in exact fractions, how results are verified, the {ncal} calculators and {ngd} guides it offers, and how to get in touch."
    doc_page("/about/", U["about_title"], meta, body, "about")

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
    body = ('<h1>페이지를 찾을 수 없어요</h1><p>주소가 바뀌었거나 없는 페이지예요. 아래에서 원하는 계산기를 골라 주세요.</p><ul class="oplist">' + ko_ops + "</ul>"
            '<p lang="en"><strong>Page not found.</strong> The address may have changed. Go to the <a href="/en/">English matrix calculator</a> or <a href="/en/calculators/">all calculators</a>.</p>')
    s = head("페이지를 찾을 수 없어요 | " + SITE, "요청한 페이지가 없어요.", "/404.html", '<meta name="robots" content="noindex">\n', alt=False) + "<body>\n" + topbar("", "/", alt=False)
    s += f'<main class="wrap"><article class="doc">{body}</article></main>\n' + footer() + "</body>\n</html>\n"
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(s)

def seo_files():
    def urls_for(code):
        Lx = LANGS[code]; p = Lx["prefix"]
        return ([p + "/", p + "/calculators/"] + [f'{p}/{o["slug"]}/' for o in Lx["ops"]] + [p + "/guide/"]
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
    home(); calc_hub()
    for o in L["ops"]: op_page(o)
    guide_index()
    for g in L["guides"].ARTICLES: guide_page(g)
    about(); privacy()

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(HERE, "static")):
        shutil.copy(os.path.join(HERE, "static", f), OUT)
    build_lang("ko")
    build_lang("en")
    use("ko")
    notfound(); seo_files()
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    main()
