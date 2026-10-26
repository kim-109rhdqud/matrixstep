"""가이드 5~10편. 예제 수치는 모두 assert로 검산해요 (guides.py와 같은 방식)."""
from fractions import Fraction as Fr

import guides as g
from guides import (M_, box, det2, gj, ident, line, matmul, minor, mx, mx_text, num, op, par, steps_html, sub)


def faq(*items):
    return ('<h2>자주 묻는 질문</h2><div class="faq">'
            + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>")


def dot_text(A, B, i, j):
    terms = " + ".join(f"{par(A[i][k])}·{par(B[k][j])}" for k in range(len(B)))
    return f"{terms} = {num(matmul(A, B)[i][j])}"


def T(M):
    return [list(r) for r in zip(*M)]


def tr_det3(A):
    return (A[0][0] * det2(minor(A, 0, 0)) - A[0][1] * det2(minor(A, 0, 1)) + A[0][2] * det2(minor(A, 0, 2)))


# =====================================================================
# 5. 행렬 곱셈
# =====================================================================
def art_mul():
    A = M_([[1, 2, 3], [4, 5, 6]])
    B = M_([[7, 8], [9, 10], [11, 12]])
    AB, BA = matmul(A, B), matmul(B, A)
    assert AB == M_([[58, 64], [139, 154]])
    assert BA == M_([[39, 54, 69], [49, 68, 87], [59, 82, 105]])
    C, D = M_([[1, 2], [3, 4]]), M_([[0, 1], [1, 0]])
    CD, DC = matmul(C, D), matmul(D, C)
    assert CD == M_([[2, 1], [4, 3]]) and DC == M_([[3, 4], [1, 2]]) and CD != DC
    P, Q = M_([[1, 0], [0, 0]]), M_([[0, 0], [0, 1]])
    assert matmul(P, Q) == M_([[0, 0], [0, 0]])
    assert matmul(C, ident(2)) == C == matmul(ident(2), C)
    X = M_([[1, 1], [0, 1]])
    assert matmul(matmul(C, D), X) == matmul(C, matmul(D, X))

    entries = "".join(box(line(f"(AB){sub(i + 1)}{sub(j + 1)} = {dot_text(A, B, i, j)}")) for i in range(2) for j in range(2))
    body = f"""
<p class="lead">행렬 곱셈은 성분끼리 곱하는 연산이 아니에요. 앞 행렬의 행과 뒤 행렬의 열을 짝지어 곱하고 더하는 규칙이라서, 처음에는 헷갈리기 쉬워요. 크기 조건부터 예제까지 순서대로 정리했어요.</p>

<h2>곱할 수 있는 조건</h2>
<p>A가 m×n 행렬이고 B가 n×p 행렬이면 곱 AB를 만들 수 있고, 결과는 m×p 행렬이에요. <strong>A의 열 수와 B의 행 수가 같아야</strong> 해요. 가운데 숫자가 같으면 곱할 수 있고, 바깥 숫자 둘이 결과의 크기가 된다고 외우면 편해요.</p>
{box(line("(m × n) · (n × p) = (m × p)"))}
<p>예를 들어 2×3 행렬에 3×2 행렬을 곱하면 2×2 행렬이 나오고, 2×3 행렬에 2×3 행렬을 곱하는 것은 정의되지 않아요.</p>

<h2>성분을 구하는 방법</h2>
<p>결과 행렬의 i행 j열 성분은 A의 i행과 B의 j열을 같은 순서로 곱해서 모두 더한 값이에요. 이 값을 두 벡터의 내적으로 볼 수 있어요.</p>
{box(line("(AB)ᵢⱼ = aᵢ₁b₁ⱼ + aᵢ₂b₂ⱼ + … + aᵢₙbₙⱼ"))}

<h2>예제: 2×3 행렬과 3×2 행렬</h2>
{box(line("A ="), mx(A), line("B ="), mx(B))}
<p>A는 2×3, B는 3×2라서 곱할 수 있고 결과는 2×2예요. 성분을 하나씩 계산해요.</p>
{entries}
{box(line("AB ="), mx(AB))}

<h2>순서를 바꾸면 결과가 달라져요</h2>
<p>같은 두 행렬이라도 BA를 계산하면 B가 3×2, A가 2×3이라서 3×3 행렬이 나와요. 크기부터 다르니 AB와 BA는 비교조차 안 돼요.</p>
{box(line("BA ="), mx(BA))}
<p>두 행렬이 모두 정사각행렬이라서 둘 다 곱할 수 있는 경우에도 보통 AB ≠ BA예요.</p>
{box(mx(C), op("×"), mx(D), op("="), mx(CD), line("그런데"), mx(D), op("×"), mx(C), op("="), mx(DC))}
<p>왼쪽에서 곱하는 것과 오른쪽에서 곱하는 것은 서로 다른 연산이에요. 그래서 “A에 B를 곱한다”고 할 때 어느 쪽에 곱하는지가 중요해요.</p>

<h2>알아 두면 좋은 성질</h2>
<ul>
<li>결합법칙: (AB)C = A(BC)</li>
<li>분배법칙: A(B + C) = AB + AC, (A + B)C = AC + BC</li>
<li>상수배: (kA)B = k(AB) = A(kB)</li>
<li>단위행렬: AI = IA = A. 단위행렬은 곱셈에서 숫자 1과 같은 역할을 해요.</li>
<li>전치: (AB)ᵀ = BᵀAᵀ. 순서가 뒤집히는 것에 주의하세요.</li>
</ul>

<h2>숫자와 다르게 동작하는 것들</h2>
<ul>
<li><strong>교환법칙이 없어요.</strong> 일반적으로 AB ≠ BA예요.</li>
<li><strong>AB = 0이어도 A = 0이거나 B = 0이 아닐 수 있어요.</strong> 아래 두 행렬은 둘 다 영행렬이 아닌데 곱이 영행렬이에요.</li>
</ul>
{box(mx(P), op("×"), mx(Q), op("="), mx(matmul(P, Q)))}
<ul>
<li><strong>약분이 안 돼요.</strong> AB = AC라고 해서 B = C라고 할 수 없어요. A에 역행렬이 있을 때만 양변에 A⁻¹을 곱해서 B = C를 얻을 수 있어요.</li>
</ul>

<h2>자주 하는 실수</h2>
<ul>
<li>같은 위치의 성분끼리 곱해요. 그건 행렬 곱셈이 아니라 아다마르 곱이라는 다른 연산이에요.</li>
<li>크기를 확인하지 않고 계산을 시작해요. 곱하기 전에 안쪽 두 숫자가 같은지 먼저 봐요.</li>
<li>행과 열을 거꾸로 짝지어요. A는 행, B는 열을 가져와요.</li>
<li>(AB)ᵀ를 AᵀBᵀ로 써요. 순서가 뒤집혀 BᵀAᵀ가 맞아요.</li>
</ul>

{faq(("AB는 계산되는데 BA는 안 되는 경우가 있나요?", "있어요. A가 2×3이고 B가 3×3이면 AB는 2×3으로 계산되지만, BA는 B의 열 수 3과 A의 행 수 2가 달라서 계산할 수 없어요."),
     ("행렬을 여러 개 곱할 때 어느 것부터 계산해도 되나요?", "결합법칙이 성립해서 어떤 묶음으로 계산해도 결과가 같아요. 다만 순서를 바꾸는 것은 안 돼요. 크기가 맞는 쪽부터 계산하면 중간 계산이 줄어들 때가 많아요."),
     ("정사각행렬을 여러 번 곱하면요?", "AA를 A²으로 써요. A²은 A가 정사각행렬일 때만 정의돼요. 대각행렬은 대각 성분만 거듭제곱하면 돼서 계산이 쉬워요."))}
"""
    return dict(
        slug="matrix-multiplication", title="행렬 곱셈 규칙과 계산 방법 (AB ≠ BA인 이유)",
        h1="행렬 곱셈 규칙과 계산 방법 (AB ≠ BA인 이유)",
        meta="행렬 곱셈이 가능한 조건과 성분을 구하는 방법을 2×3, 3×2 예제로 단계별로 설명해요. 교환법칙이 성립하지 않는 이유와 자주 하는 실수도 정리했어요.",
        desc="곱할 수 있는 조건, 성분 계산법, AB와 BA가 다른 이유를 예제로 정리했어요.",
        min=6, calc=("행렬 곱셈 계산기", "/multiplication/"), body=body,
        related=["matrix-add-subtract-scalar", "matrix-transpose-properties"],
    )


# =====================================================================
# 6. 덧셈·뺄셈·스칼라배
# =====================================================================
def art_add():
    A, B = M_([[1, 2], [3, 4]]), M_([[5, 6], [7, 8]])
    S = [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
    Df = [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]
    K = [[3 * A[i][j] for j in range(2)] for i in range(2)]
    L = [[2 * A[i][j] - B[i][j] for j in range(2)] for i in range(2)]
    assert S == M_([[6, 8], [10, 12]]) and Df == M_([[-4, -4], [-4, -4]])
    assert K == M_([[3, 6], [9, 12]]) and L == M_([[-3, -2], [-1, 0]])
    assert [[B[i][j] + A[i][j] for j in range(2)] for i in range(2)] == S

    def cells(f, sym):
        return "".join(box(line(f"c{sub(i + 1)}{sub(j + 1)} = {par(A[i][j])} {sym} {par(B[i][j])} = {num(f[i][j])}"))
                       for i in range(2) for j in range(2))

    body = f"""
<p class="lead">행렬의 덧셈, 뺄셈, 스칼라배는 같은 위치의 성분끼리 계산하면 돼서 행렬 연산 중 가장 쉬워요. 그래도 크기 조건과 부호 실수 때문에 점수를 잃는 경우가 많아서, 규칙과 예제를 한 번에 정리했어요.</p>

<h2>덧셈과 뺄셈</h2>
<p>두 행렬의 <strong>크기가 같을 때만</strong> 더하거나 뺄 수 있어요. 결과 행렬의 i행 j열 성분은 두 행렬의 i행 j열 성분을 더하거나 뺀 값이에요.</p>
{box(line("(A ± B)ᵢⱼ = aᵢⱼ ± bᵢⱼ"))}
<p>2×2 행렬 두 개로 계산해 봐요.</p>
{box(line("A ="), mx(A), line("B ="), mx(B))}
<h3>A + B</h3>
{cells(S, "+")}
{box(line("A + B ="), mx(S))}
<h3>A − B</h3>
{cells(Df, "−")}
{box(line("A − B ="), mx(Df))}
<p>크기가 다른 행렬은 짝지을 성분이 없어서 덧셈과 뺄셈이 정의되지 않아요. 2×2 행렬에 2×3 행렬을 더하는 것은 불가능해요.</p>

<h2>스칼라배</h2>
<p>행렬에 수 k를 곱하면 모든 성분에 k를 곱해요. 행렬 전체에 곱하는 것이지 첫 성분에만 곱하는 게 아니에요.</p>
{box(line("3A ="), mx(K))}

<h2>섞어서 계산하기</h2>
<p>2A − B처럼 스칼라배와 뺄셈이 같이 나오면, 스칼라배를 먼저 하고 그 결과끼리 같은 위치로 빼요.</p>
{box(line("2A ="), mx([[2 * A[i][j] for j in range(2)] for i in range(2)]), line("2A − B ="), mx(L))}

<h2>성질</h2>
<ul>
<li>교환법칙: A + B = B + A</li>
<li>결합법칙: (A + B) + C = A + (B + C)</li>
<li>영행렬: A + O = A, A − A = O</li>
<li>분배법칙: k(A + B) = kA + kB, (k + l)A = kA + lA</li>
<li>스칼라배의 결합: k(lA) = (kl)A</li>
</ul>
<p>곱셈과 달리 덧셈에는 교환법칙이 성립해요. 위 예제에서 B + A를 계산해도 A + B와 같은 행렬이 나와요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>크기가 다른 행렬을 더하려고 해요. 먼저 크기부터 확인해요.</li>
<li>뺄셈에서 음수 성분의 부호를 틀려요. 5 − (−2) = 7처럼 괄호를 쳐서 계산해요.</li>
<li>스칼라배를 한 행이나 첫 성분에만 적용해요. 모든 성분에 곱해요.</li>
<li>−A를 “부호만 하나 바꾸는 것”으로 오해해요. 모든 성분의 부호가 바뀌어요.</li>
</ul>

{faq(("행렬에 수를 더할 수도 있나요?", "행렬에 수를 더하는 연산은 정의되지 않아요. A + 3처럼 쓰고 싶다면 3I(단위행렬의 3배)를 더하는 것으로 써야 해요."),
     ("영행렬은 뭔가요?", "모든 성분이 0인 행렬이에요. 덧셈에서 숫자 0처럼 동작해서 A + O = A가 돼요."),
     ("소수나 분수가 섞여도 같은 규칙인가요?", "네, 같아요. 분수는 통분해서 더하고, 소수는 자릿수를 맞춰서 계산해요. 계산기에서는 분수로 정확하게 처리해요."))}
"""
    return dict(
        slug="matrix-add-subtract-scalar", title="행렬 덧셈·뺄셈·스칼라배 계산 규칙과 예제",
        h1="행렬 덧셈·뺄셈·스칼라배 계산 규칙과 예제",
        meta="행렬을 더하고 빼려면 크기가 같아야 하는 이유, 스칼라배, 2A − B 같은 혼합 계산을 예제와 함께 정리했어요. 성질과 자주 하는 실수도 알려드려요.",
        desc="크기 조건, 성분별 계산, 스칼라배와 혼합 계산을 예제로 정리했어요.",
        min=5, calc=("행렬 덧셈 계산기", "/addition/"), body=body,
        related=["matrix-multiplication", "matrix-transpose-properties"],
    )


# =====================================================================
# 7. 전치행렬
# =====================================================================
def art_transpose():
    A = M_([[1, 2, 3], [4, 5, 6]])
    At = T(A)
    assert At == M_([[1, 4], [2, 5], [3, 6]]) and T(At) == A
    C, D = M_([[1, 2], [3, 4]]), M_([[0, 1], [1, 0]])
    lhs = T(matmul(C, D))
    rhs = matmul(T(D), T(C))
    wrong = matmul(T(C), T(D))
    assert lhs == rhs == M_([[2, 4], [1, 3]]) and wrong != lhs
    S = M_([[2, -1, 0], [-1, 3, 4], [0, 4, 5]])
    assert T(S) == S
    K = M_([[0, 2, -1], [-2, 0, 3], [1, -3, 0]])
    assert T(K) == [[-x for x in r] for r in K]
    N = M_([[1, 2], [3, 4]])
    Sym = [[N[i][j] + T(N)[i][j] for j in range(2)] for i in range(2)]
    assert Sym == M_([[2, 5], [5, 8]]) and T(Sym) == Sym

    body = f"""
<p class="lead">전치행렬은 행과 열을 맞바꾼 행렬이에요. 개념은 간단하지만 곱의 전치, 대칭행렬, 반대칭행렬처럼 시험에 자주 나오는 성질이 많아서 한 번 정리해 두면 좋아요.</p>

<h2>전치행렬의 정의</h2>
<p>m×n 행렬 A의 전치행렬 Aᵀ는 n×m 행렬이에요. A의 i행 j열 성분이 Aᵀ의 j행 i열 성분이 돼요.</p>
{box(line("(Aᵀ)ⱼᵢ = aᵢⱼ"))}
<p>2×3 행렬을 전치하면 3×2 행렬이 돼요. 첫 번째 행이 첫 번째 열로 눕는다고 생각하면 쉬워요.</p>
{box(line("A ="), mx(A), op("→"), line("Aᵀ ="), mx(At))}
<p>두 번 전치하면 원래대로 돌아와요. (Aᵀ)ᵀ = A예요.</p>

<h2>전치의 기본 성질</h2>
<ul>
<li>(A + B)ᵀ = Aᵀ + Bᵀ</li>
<li>(kA)ᵀ = kAᵀ</li>
<li>(AB)ᵀ = BᵀAᵀ <strong>(순서가 뒤집혀요)</strong></li>
<li>(A⁻¹)ᵀ = (Aᵀ)⁻¹</li>
<li>det(Aᵀ) = det(A)</li>
<li>rank(Aᵀ) = rank(A)</li>
</ul>

<h2>곱의 전치: (AB)ᵀ = BᵀAᵀ</h2>
<p>이 성질이 가장 많이 틀려요. 두 행렬을 직접 곱해서 확인해 봐요.</p>
{box(line("C ="), mx(C), line("D ="), mx(D))}
{box(line("(CD)ᵀ ="), mx(lhs))}
{box(line("DᵀCᵀ ="), mx(T(D)), op("×"), mx(T(C)), op("="), mx(rhs))}
<p>두 결과가 같아요. 반면 순서를 그대로 둔 CᵀDᵀ는 아래처럼 다른 행렬이 나와요.</p>
{box(line("CᵀDᵀ ="), mx(wrong))}
<p>크기로도 이유를 알 수 있어요. A가 m×n, B가 n×p이면 AB는 m×p이고 (AB)ᵀ는 p×m이에요. BᵀAᵀ는 (p×n)·(n×m) = p×m이라서 크기가 맞지만, AᵀBᵀ는 (n×m)·(p×n)이라서 m과 p가 다르면 곱할 수조차 없어요.</p>

<h2>대칭행렬과 반대칭행렬</h2>
<p>전치해도 변하지 않는 행렬을 <strong>대칭행렬</strong>이라고 해요. Aᵀ = A를 만족해서 대각선을 기준으로 성분이 거울처럼 같아요.</p>
{box(line("S ="), mx(S), line("Sᵀ = S"))}
<p>전치하면 부호가 바뀌는 행렬 Aᵀ = −A는 <strong>반대칭행렬</strong>이에요. 대각 성분은 자기 자신이 −1배가 되어야 해서 모두 0이에요.</p>
{box(line("K ="), mx(K), line("Kᵀ = −K"))}

<h2>어떤 정사각행렬이든 대칭행렬로 만들기</h2>
<p>정사각행렬 N에 대해 N + Nᵀ는 항상 대칭행렬이에요.</p>
{box(line("N ="), mx(N), line("N + Nᵀ ="), mx(Sym))}
<p>N − Nᵀ는 반대칭행렬이에요. 그래서 모든 정사각행렬은 대칭행렬과 반대칭행렬의 합으로 쓸 수 있어요. N = (N + Nᵀ)/2 + (N − Nᵀ)/2예요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>(AB)ᵀ를 AᵀBᵀ로 써요. 순서가 뒤집혀 BᵀAᵀ가 맞아요.</li>
<li>직사각행렬의 전치 후 크기를 잘못 써요. 2×3의 전치는 3×2예요.</li>
<li>대칭행렬은 정사각행렬이어야 해요. 직사각행렬은 Aᵀ = A가 성립할 수 없어요.</li>
<li>반대칭행렬의 대각 성분을 0이 아닌 값으로 둬요.</li>
</ul>

{faq(("전치행렬과 역행렬은 같은 건가요?", "아니에요. 전치는 모든 행렬에 있는 연산이고 행과 열을 바꾸는 것이에요. 역행렬은 곱해서 단위행렬이 되는 행렬이고 가역행렬에만 있어요. 직교행렬만 두 개가 같아요."),
     ("전치를 해도 행렬식이 안 변하는 이유는?", "행렬식을 행으로 전개하든 열로 전개하든 값이 같기 때문이에요. 그래서 행에 대한 성질은 열에도 똑같이 성립해요."),
     ("벡터의 전치는 뭔가요?", "열벡터를 전치하면 행벡터가 돼요. 두 열벡터 u, v의 내적을 uᵀv로 쓰는 이유예요."))}
"""
    return dict(
        slug="matrix-transpose-properties", title="전치행렬의 성질과 (AB)ᵀ = BᵀAᵀ, 대칭행렬 정리",
        h1="전치행렬의 성질과 (AB)ᵀ = BᵀAᵀ, 대칭행렬 정리",
        meta="전치행렬의 정의와 기본 성질, 곱의 전치 (AB)ᵀ = BᵀAᵀ가 성립하는 이유를 예제로 확인해요. 대칭행렬과 반대칭행렬 개념까지 정리했어요.",
        desc="전치의 정의, 곱의 전치, 대칭행렬과 반대칭행렬을 예제로 정리했어요.",
        min=6, calc=("전치행렬 계산기", "/transpose/"), body=body,
        related=["matrix-multiplication", "special-matrices"],
    )


# =====================================================================
# 8. 크래머 공식
# =====================================================================
def cramer(A, b):
    n = len(A)
    d = tr_det3(A) if n == 3 else det2(A)
    out = []
    for j in range(n):
        Aj = [r[:] for r in A]
        for i in range(n):
            Aj[i][j] = b[i]
        out.append((Aj, tr_det3(Aj) if n == 3 else det2(Aj)))
    return d, out


def art_cramer():
    A2, b2 = M_([[3, 2], [1, -1]]), [Fr(7), Fr(4)]
    d2, parts2 = cramer(A2, b2)
    assert d2 == -5 and [p[1] for p in parts2] == [-15, 5]
    x2 = [p[1] / d2 for p in parts2]
    assert x2 == [3, -1] and 3 * x2[0] + 2 * x2[1] == 7 and x2[0] - x2[1] == 4
    A3, b3 = M_([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]), [Fr(8), Fr(-11), Fr(-3)]
    d3, parts3 = cramer(A3, b3)
    assert d3 == -1 and [p[1] for p in parts3] == [-2, -3, 1]
    x3 = [p[1] / d3 for p in parts3]
    assert x3 == [2, 3, -1]
    cols = ["x", "y", "z"]
    dets3 = "".join(box(line(f"A{sub(j + 1)} ="), mx(parts3[j][0]), line(f"det(A{sub(j + 1)}) = {num(parts3[j][1])}")) for j in range(3))

    body = f"""
<p class="lead">크래머 공식은 행렬식만으로 연립방정식의 해를 한 번에 쓰는 방법이에요. 식이 2~3개일 때 빠르고 깔끔해서 시험에 자주 나와요. 공식이 어떻게 쓰이는지, 언제 쓸 수 없는지까지 예제로 확인해 봐요.</p>

<h2>크래머 공식이란?</h2>
<p>미지수와 식의 개수가 같은 연립방정식 Ax = b에서 계수행렬의 행렬식 det(A)가 0이 아니면, 해는 아래처럼 정해져요.</p>
{box(line("xⱼ = det(Aⱼ) / det(A)"))}
<p>여기서 Aⱼ는 A의 j번째 열을 b로 바꾼 행렬이에요. 변수 하나당 행렬식 하나를 더 계산하는 방식이에요.</p>

<h2>예제 1: 2×2 연립방정식</h2>
{box(line("3x + 2y = 7"))}
{box(line("x − y = 4"))}
<p>먼저 계수행렬의 행렬식을 구해요. 이게 0이면 크래머 공식을 쓸 수 없어요.</p>
{box(mx(A2), line(f"det(A) = 3·(−1) − 2·1 = {num(d2)}"))}
<p>x는 첫 번째 열을 b로 바꾼 행렬을, y는 두 번째 열을 바꾼 행렬을 써요.</p>
{box(line("A₁ (1열을 b로) ="), mx(parts2[0][0]), line(f"det = 7·(−1) − 2·4 = {num(parts2[0][1])}"))}
{box(line("A₂ (2열을 b로) ="), mx(parts2[1][0]), line(f"det = 3·4 − 7·1 = {num(parts2[1][1])}"))}
{box(line(f"x = {num(parts2[0][1])} / ({num(d2)}) = {num(x2[0])}"), line(f"y = {num(parts2[1][1])} / ({num(d2)}) = {num(x2[1])}"))}
<p>대입해서 확인해요. 3·3 + 2·(−1) = 7, 3 − (−1) = 4가 모두 성립해요.</p>

<h2>예제 2: 3×3 연립방정식</h2>
{box(line("2x + y − z = 8"))}
{box(line("−3x − y + 2z = −11"))}
{box(line("−2x + y + 2z = −3"))}
<p>계수행렬의 행렬식은 {num(d3)}이에요. 0이 아니라서 해가 하나로 정해져요. 각 열을 b로 바꾼 행렬의 행렬식은 아래와 같아요.</p>
{dets3}
{box(line(f"x = {num(parts3[0][1])} / ({num(d3)}) = {num(x3[0])}"), line(f"y = {num(parts3[1][1])} / ({num(d3)}) = {num(x3[1])}"), line(f"z = {num(parts3[2][1])} / ({num(d3)}) = {num(x3[2])}"))}
<p>해는 (x, y, z) = (2, 3, −1)이에요. 같은 문제를 <a href="/guide/linear-system-solutions/">가우스-조던 소거법</a>으로 풀어도 같은 답이 나와요.</p>

<h2>크래머 공식을 쓸 수 없는 경우</h2>
<ul>
<li><strong>det(A) = 0일 때</strong>: 0으로 나눌 수 없어요. 이때는 해가 없거나 무수히 많은데, 어느 쪽인지는 크래머 공식으로 알 수 없고 소거법으로 판단해야 해요.</li>
<li><strong>식의 개수와 미지수의 개수가 다를 때</strong>: 계수행렬이 정사각행렬이 아니라서 행렬식이 없어요.</li>
</ul>

<h2>크래머 공식이 실전에서 잘 안 쓰이는 이유</h2>
<p>n개의 변수를 풀려면 n + 1개의 n×n 행렬식을 계산해야 해요. 행렬식 계산이 이미 무거워서 변수가 늘수록 계산량이 빠르게 불어나요. 시험에서는 2~3개 변수까지만 쓰는 게 좋고, 그 이상은 소거법이 훨씬 빨라요. 변수 하나만 필요한 문제라면 크래머 공식이 유리할 때도 있어요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>열을 b로 바꾸는 위치를 틀려요. x는 1열, y는 2열, z는 3열이에요.</li>
<li>det(A)가 0인지 확인하지 않고 나눠요.</li>
<li>행렬식 부호 실수를 해요. 특히 3×3 전개에서 + − +를 확인해요.</li>
<li>b를 바꾸는 대신 행을 바꿔요. 바꾸는 것은 열이에요.</li>
</ul>

{faq(("det(A) = 0이면 해가 없는 건가요?", "아니에요. 해가 없을 수도 있고 무수히 많을 수도 있어요. 소거법으로 첨가행렬을 정리해서 판단해야 해요."),
     ("크래머 공식으로 역행렬도 구할 수 있나요?", "수반행렬을 쓰는 역행렬 공식이 크래머 공식과 같은 원리예요. <a href='/guide/inverse-adjugate-cofactor/'>여인수와 수반행렬로 역행렬 구하기</a>에서 이어서 설명해요."),
     ("계산기로 확인할 수 있나요?", "연립방정식 계산기에 계수와 상수를 넣으면 같은 해를 확인할 수 있어요."))}
"""
    return dict(
        slug="cramer-rule", title="크래머 공식으로 연립방정식 푸는 법 (2×2, 3×3 예제)",
        h1="크래머 공식으로 연립방정식 푸는 법 (2×2, 3×3 예제)",
        meta="크래머 공식 xⱼ = det(Aⱼ)/det(A)를 2×2, 3×3 연립방정식 예제로 설명해요. 쓸 수 없는 경우와 소거법보다 느린 이유도 정리했어요.",
        desc="행렬식으로 해를 구하는 크래머 공식을 예제와 주의점으로 정리했어요.",
        min=7, calc=("연립방정식 계산기", "/linear-system/"), body=body,
        related=["determinant-3x3", "linear-system-solutions"],
    )


# =====================================================================
# 9. 여인수·수반행렬로 역행렬
# =====================================================================
def cof(A):
    n = len(A)
    def d(m):
        return det2(m) if len(m) == 2 else tr_det3(m)
    return [[(-1) ** (i + j) * d(minor(A, i, j)) for j in range(n)] for i in range(n)]


def art_adj():
    A = M_([[1, 2], [3, 4]])
    adj2 = M_([[4, -2], [-3, 1]])
    assert [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]] == adj2
    dA = det2(A)
    inv2 = [[x / dA for x in r] for r in adj2]
    assert dA == -2 and matmul(A, inv2) == ident(2)

    B = M_([[2, 1, 0], [1, 3, 1], [0, 1, 2]])
    dB = tr_det3(B)
    assert dB == 8
    CB = cof(B)
    assert CB == M_([[5, -2, 1], [-2, 4, -2], [1, -2, 5]])
    adjB = T(CB)
    invB = [[x / dB for x in r] for r in adjB]
    assert matmul(B, invB) == ident(3)
    assert invB == M_([[Fr(5, 8), Fr(-1, 4), Fr(1, 8)], [Fr(-1, 4), Fr(1, 2), Fr(-1, 4)], [Fr(1, 8), Fr(-1, 4), Fr(5, 8)]])
    cofs = "".join(box(line(f"C{sub(i + 1)}{sub(j + 1)} = (−1)^{i + j} · det"), mx(minor(B, i, j)), line(f"= {num(CB[i][j])}")) for i in range(3) for j in range(3))

    body = f"""
<p class="lead">역행렬을 소거법으로만 구하는 건 아니에요. 행렬식과 여인수를 이용한 수반행렬 공식도 있어요. 2×2에서는 이 공식이 가장 빠르고, 3×3에서도 시험에서 자주 나와요.</p>

<h2>수반행렬과 역행렬 공식</h2>
<p>정사각행렬 A의 i행 j열 <strong>여인수</strong> Cᵢⱼ는 i행과 j열을 지운 소행렬의 행렬식에 (−1)^(i+j)를 곱한 값이에요. 모든 여인수를 모은 행렬을 여인수행렬이라고 하고, 이것을 전치한 행렬이 <strong>수반행렬</strong> adj(A)예요.</p>
{box(line("A⁻¹ = (1 / det(A)) · adj(A)"), line("adj(A) = (여인수행렬)ᵀ"))}
<p>det(A) = 0이면 1/det(A)를 만들 수 없어서 역행렬이 없어요.</p>

<h2>2×2는 공식 하나로 끝나요</h2>
<p>A = [[a, b], [c, d]]이면 여인수행렬은 [[d, −c], [−b, a]]이고, 전치하면 수반행렬 [[d, −b], [−c, a]]가 돼요. 대각 성분은 서로 자리를 바꾸고, 나머지 두 성분은 부호만 바꾸면 돼요.</p>
{box(line("A ="), mx(A), line(f"det(A) = 1·4 − 2·3 = {num(dA)}"))}
{box(line("adj(A) ="), mx(adj2), line("A⁻¹ = −½ ·"), mx(adj2), line("="), mx(inv2))}
<p>검산은 AA⁻¹ = I를 확인하면 돼요.</p>
{box(mx(A), op("×"), mx(inv2), op("="), mx(matmul(A, inv2)))}

<h2>예제: 3×3 행렬</h2>
{box(line("B ="), mx(B))}
<p>먼저 행렬식을 구해요. 1행으로 전개하면 2·(3·2 − 1·1) − 1·(1·2 − 1·0) + 0 = 10 − 2 = {num(dB)}이에요. 0이 아니라서 역행렬이 있어요.</p>
<p>이제 아홉 개의 여인수를 구해요. 각 칸에서 해당 행과 열을 지운 2×2 소행렬의 행렬식을 구하고 부호 (+ − + / − + − / + − +)를 붙여요.</p>
{cofs}
<p>여인수행렬과 그것을 전치한 수반행렬이에요. 이 행렬은 대칭이라서 전치해도 같아요.</p>
{box(line("C ="), mx(CB), line("adj(B) = Cᵀ ="), mx(adjB))}
<p>마지막으로 수반행렬에 1/det(B) = 1/{num(dB)}을 곱해요.</p>
{box(line("B⁻¹ ="), mx(invB))}
{box(mx(B), op("×"), mx(invB), op("="), mx(matmul(B, invB)))}

<h2>소거법과 어느 쪽이 나을까요?</h2>
<ul>
<li>2×2: 공식이 압도적으로 빨라요.</li>
<li>3×3: 여인수 9개를 계산해야 해서 길어요. 계산 실수를 줄이려면 <a href="/guide/inverse-gauss-jordan/">가우스-조던 소거법</a>이 더 안정적이에요. 다만 부분 점수를 위해 공식 풀이를 요구하는 시험도 있어요.</li>
<li>4×4 이상: 소거법이 거의 필수예요.</li>
</ul>

<h2>자주 하는 실수</h2>
<ul>
<li>여인수행렬을 전치하지 않고 그대로 써요. 반드시 전치한 수반행렬을 써야 해요.</li>
<li>(−1)^(i+j) 부호를 빼먹어요. 체스판처럼 + − + / − + − / + − + 로 붙여요.</li>
<li>1/det(A)를 곱하는 것을 잊어요. 수반행렬은 역행렬이 아니에요.</li>
<li>det(A) = 0인데 계산을 계속해요. 행렬식부터 확인해요.</li>
</ul>

{faq(("수반행렬을 영어로 뭐라고 하나요?", "adjugate 또는 classical adjoint라고 불러요. 교재에 따라 adj(A)라고 써요."),
     ("A·adj(A)는 어떤 행렬이 되나요?", "A·adj(A) = det(A)·I가 돼요. 이 식을 det(A)로 나누면 역행렬 공식이 나와요."),
     ("정수 행렬의 역행렬이 항상 정수인가요?", "아니에요. det(A)가 1 또는 −1일 때만 정수 행렬이 보장돼요. 위 예제처럼 det가 8이면 분수가 나와요."))}
"""
    return dict(
        slug="inverse-adjugate-cofactor", title="여인수와 수반행렬로 역행렬 구하는 법 (2×2, 3×3)",
        h1="여인수와 수반행렬로 역행렬 구하는 법 (2×2, 3×3)",
        meta="A⁻¹ = adj(A)/det(A) 공식을 2×2 공식과 3×3 여인수 예제로 설명해요. 여인수행렬을 전치해 수반행렬을 만드는 과정과 자주 하는 실수를 정리했어요.",
        desc="여인수행렬, 수반행렬, 역행렬 공식을 2×2와 3×3 예제로 정리했어요.",
        min=8, calc=("역행렬 계산기", "/inverse/"), body=body,
        related=["inverse-gauss-jordan", "determinant-properties"],
    )


# =====================================================================
# 10. 행렬식의 성질
# =====================================================================
def art_detprop():
    A = M_([[1, 2], [3, 4]])
    dA = det2(A)
    assert dA == -2
    sw = [A[1], A[0]]
    assert det2(sw) == 2
    sc = [[3 * x for x in A[0]], A[1]]
    assert det2(sc) == -6
    ad = [A[0], [A[1][0] - 2 * A[0][0], A[1][1] - 2 * A[0][1]]]
    assert det2(ad) == -2 and ad[1] == [1, 0]
    Bm = M_([[0, 1], [1, 0]])
    assert det2(Bm) == -1 and det2(matmul(A, Bm)) == 2 == dA * det2(Bm)
    assert det2(T(A)) == dA
    A3 = M_([[2, -1, 0], [1, 3, 2], [0, 1, 4]])
    assert tr_det3(A3) == 24 and tr_det3([[2 * x for x in r] for r in A3]) == 8 * 24
    Tri = M_([[2, 5, 7], [0, 3, 1], [0, 0, 4]])
    assert tr_det3(Tri) == 24
    Dup = M_([[1, 2, 3], [4, 5, 6], [1, 2, 3]])
    assert tr_det3(Dup) == 0
    Pm = M_([[1, 2, 3], [2, 4, 6], [0, 1, 5]])
    assert tr_det3(Pm) == 0

    body = f"""
<p class="lead">행렬식을 정의대로 계산하면 금방 길어져요. 그래서 시험에서는 성질을 이용해 행을 정리한 뒤 계산하는 경우가 많아요. 자주 쓰는 성질을 예제로 하나씩 확인해 볼게요.</p>

<h2>행 연산이 행렬식에 미치는 영향</h2>
<p>소거법에서 쓰는 세 가지 행 연산은 행렬식을 각각 다른 방식으로 바꿔요. 이 세 가지만 외워도 대부분의 문제가 풀려요.</p>
<div class="tbl"><table class="gtable">
<thead><tr><th>행 연산</th><th>행렬식의 변화</th></tr></thead>
<tbody>
<tr><td>두 행을 바꾸기</td><td>부호가 바뀌어요 (−1배)</td></tr>
<tr><td>한 행에 k를 곱하기</td><td>k배가 돼요</td></tr>
<tr><td>한 행에 다른 행의 상수배를 더하기</td><td>변하지 않아요</td></tr>
</tbody></table></div>
<p>2×2 행렬로 세 경우를 모두 확인해요. 출발점은 det(A) = 1·4 − 2·3 = {num(dA)}이에요.</p>
{box(line("A ="), mx(A))}
{box(line("R₁ ↔ R₂"), op("→"), mx(sw), line(f"det = {num(det2(sw))}"))}
{box(line("R₁ ← 3R₁"), op("→"), mx(sc), line(f"det = {num(det2(sc))} = 3 × ({num(dA)})"))}
{box(line("R₂ ← R₂ − 3R₁"), op("→"), mx(ad), line(f"det = {num(det2(ad))}"))}
<p>첫 번째는 부호가 바뀌었고, 두 번째는 3배가 됐고, 세 번째는 그대로예요. 이 세 번째 성질 덕분에 행 소거로 삼각행렬을 만들어도 행렬식이 보존돼요.</p>

<h2>삼각행렬의 행렬식</h2>
<p>상삼각행렬이나 하삼각행렬의 행렬식은 대각 성분의 곱이에요.</p>
{box(mx(Tri), line("det = 2·3·4 = 24"))}
<p>그래서 행렬식 계산은 “행 소거로 삼각행렬 만들기 → 대각 성분 곱하기”로 정리돼요. 행을 바꾼 횟수만큼 부호를 고쳐 주는 것을 잊지 마세요.</p>

<h2>행렬식이 0이 되는 경우</h2>
<ul>
<li>두 행(또는 두 열)이 같아요.</li>
<li>한 행이 다른 행의 상수배예요.</li>
<li>모두 0인 행(또는 열)이 있어요.</li>
</ul>
<p>한마디로 행들이 서로 독립이 아니면 행렬식은 0이에요. 아래 두 행렬은 모두 행렬식이 0이에요.</p>
{box(mx(Dup), line("1행 = 3행"), mx(Pm), line("2행 = 2 × 1행"))}

<h2>곱과 전치, 스칼라배</h2>
<ul>
<li>det(AB) = det(A)·det(B)</li>
<li>det(Aᵀ) = det(A)</li>
<li>det(A⁻¹) = 1/det(A)</li>
<li>n×n 행렬에서 det(kA) = kⁿ·det(A)</li>
</ul>
<p>곱의 성질을 확인해 봐요. det(B) = −1이고 det(A) = −2예요.</p>
{box(mx(A), op("×"), mx(Bm), op("="), mx(matmul(A, Bm)), line(f"det = {num(det2(matmul(A, Bm)))} = ({num(dA)})·({num(det2(Bm))})"))}
<p>det(kA) = kⁿ·det(A)는 특히 자주 틀려요. 행렬 전체에 k를 곱하면 n개의 행에 모두 k가 곱해지기 때문에 k가 n번 나와요. 앞서 det = 24였던 3×3 행렬에 2를 곱하면 행렬식은 2·24가 아니라 2³·24 = 192예요.</p>
<p>또 det(A + B)는 det(A) + det(B)와 같지 않아요. 곱에는 성질이 있지만 합에는 없어요.</p>

<h2>성질을 이용한 계산 예시</h2>
<p>det(A) = −2인 2×2 행렬 A에 대해 det(3A²)을 구하면, det(3A²) = 3²·det(A)² = 9·4 = 36이에요. 정의대로 3A²을 계산하지 않아도 풀려요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>det(A + B) = det(A) + det(B)로 써요. 성립하지 않아요.</li>
<li>det(kA) = k·det(A)로 써요. 정사각행렬 크기 n에 대해 kⁿ이에요.</li>
<li>행을 바꾼 횟수를 세지 않아서 부호를 틀려요.</li>
<li>행에 k를 곱해 놓고 행렬식을 k배로 보정하지 않아요.</li>
</ul>

{faq(("행렬식이 0이면 무슨 뜻이에요?", "역행렬이 없고, 행(또는 열)들이 서로 독립이 아니라는 뜻이에요. 기하적으로는 넓이나 부피가 0으로 눌려 버린다는 의미예요."),
     ("열 연산도 같은 성질을 가지나요?", "네, det(Aᵀ) = det(A)라서 행에 대한 성질은 열에도 똑같이 성립해요."),
     ("행렬식의 값이 음수일 수 있나요?", "있어요. 부호는 방향이 뒤집히는지를 나타내고 크기는 넓이나 부피의 배율을 나타내요."))}
"""
    return dict(
        slug="determinant-properties", title="행렬식의 성질 총정리: 행 연산, 곱, kA의 행렬식",
        h1="행렬식의 성질 총정리: 행 연산, 곱, kA의 행렬식",
        meta="행 교환, 상수배, 행 더하기가 행렬식에 미치는 영향과 det(AB), det(Aᵀ), det(kA) = kⁿdet(A) 같은 성질을 예제로 확인해요. 삼각행렬 계산법도 알려드려요.",
        desc="행 연산별 행렬식 변화와 곱, 전치, 스칼라배 성질을 예제로 정리했어요.",
        min=7, calc=("행렬식 계산기", "/determinant/"), body=body,
        related=["determinant-3x3", "inverse-adjugate-cofactor"],
    )


ARTICLES = [art_mul(), art_add(), art_transpose(), art_cramer(), art_adj(), art_detprop()]
