"""개념 설명 글(가이드) 본문 생성.

예제의 계산은 모두 Fraction으로 직접 풀고, 본문에 적은 값이 맞는지 assert로 확인해요.
값이 틀리면 빌드가 멈추니까 글을 고칠 때도 안심하고 숫자를 바꿀 수 있어요.
"""
from fractions import Fraction as Fr

SUBD = "₀₁₂₃₄₅₆₇₈₉"


def sub(n):
    return "".join(SUBD[int(d)] for d in str(n))


# ---------- 숫자 표시 ----------
def num(f):
    f = Fr(f)
    s = str(abs(f.numerator)) if f.denominator == 1 else f"{abs(f.numerator)}/{f.denominator}"
    return ("−" if f < 0 else "") + s


def par(f):
    f = Fr(f)
    return f"({num(f)})" if f < 0 else num(f)


def coef(f):
    f = Fr(f)
    return f"({num(f)})" if (f.denominator != 1 or f < 0) else num(f)


def coef_abs(f):
    a = abs(Fr(f))
    if a == 1:
        return ""
    return num(a) if a.denominator == 1 else f"({num(a)})"


def fhtml(f):
    f = Fr(f)
    sign = "−" if f < 0 else ""
    a = abs(f.numerator)
    if f.denominator == 1:
        return f"{sign}{a}"
    return f'{sign}<span class="fr"><span>{a}</span><span>{f.denominator}</span></span>'


def M_(rows):
    return [[Fr(x) for x in r] for r in rows]


def snap(M):
    return [r[:] for r in M]


def ident(n):
    return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def minor(A, i, j):
    return [[A[r][c] for c in range(len(A)) if c != j] for r in range(len(A)) if r != i]


# ---------- 행렬 HTML (계산기와 같은 스타일) ----------
def mx(M, sep=-1, big=False):
    c = len(M[0])
    cells = "".join(
        f'<span class="mx-c{" sep" if j == sep else ""}">{fhtml(v)}</span>' for r in M for j, v in enumerate(r)
    )
    return f'<span class="mx{" big" if big else ""}"><span class="mx-g" style="grid-template-columns:repeat({c},auto)">{cells}</span></span>'


def mx_text(rows):
    c = len(rows[0])
    cells = "".join(f'<span class="mx-c">{v}</span>' for r in rows for v in r)
    return f'<span class="mx"><span class="mx-g" style="grid-template-columns:repeat({c},auto)">{cells}</span></span>'


def op(s):
    return f'<span class="op">{s}</span>'


def line(s):
    return f'<span class="mline">{s}</span>'


def box(*parts):
    return '<div class="mbox">' + "".join(parts) + "</div>"


def li(i, note, ops, M, sep=-1):
    chips = f'<div class="rop">{"".join(f"<code>{o}</code>" for o in ops)}</div>' if ops else ""
    return (
        f'<li class="step"><span class="no">{i:02d}</span><div class="sb"><div class="st">{note}</div>{chips}'
        f'<div class="mbox">{mx(M, sep)}</div></div></li>'
    )


def steps_html(first_note, first_M, steps, sep=-1):
    items = [li(1, first_note, [], first_M, sep)]
    for k, (ops, M, note) in enumerate(steps, 2):
        items.append(li(k, note, ops, M, sep))
    return '<ol class="gsteps">' + "".join(items) + "</ol>"


# ---------- 소거법 ----------
# 풀이 단계 설명 문구. 영어 가이드는 guides_en.NOTES_EN을 넘겨요.
NOTES_KO = dict(
    swap="{c}열에서 피벗으로 쓸 0이 아닌 성분을 {r}행으로 올려요.",
    scale="피벗을 1로 만들기 위해 {r}행 전체를 피벗 값으로 나눠요.",
    elim="{c}열에서 피벗을 제외한 나머지 성분을 0으로 만들어요.",
    uswap="두 행을 바꾸면 행렬식의 부호가 바뀌어요.",
    uelim="{c}열의 피벗 아래를 0으로 만들어요. 이 연산은 행렬식을 바꾸지 않아요.",
)


def gj(M0, split, notes=NOTES_KO):
    M = snap(M0)
    R = len(M)
    steps, piv, r = [], [], 0
    for c in range(split):
        if r >= R:
            break
        pr = -1
        for i in range(r, R):
            if M[i][c] != 0:
                if pr < 0:
                    pr = i
                if M[i][c] == 1:
                    pr = i
                    break
        if pr < 0:
            continue
        if pr != r:
            M[pr], M[r] = M[r], M[pr]
            steps.append(([f"R{sub(r + 1)} ↔ R{sub(pr + 1)}"], snap(M),
                          notes["swap"].format(c=c + 1, r=r + 1)))
        pv = M[r][c]
        if pv != 1:
            iv = 1 / pv
            M[r] = [x * iv for x in M[r]]
            steps.append(([f"R{sub(r + 1)} ← {coef(iv)}R{sub(r + 1)}"], snap(M),
                          notes["scale"].format(r=r + 1)))
        ops = []
        for i in range(R):
            if i == r or M[i][c] == 0:
                continue
            f = M[i][c]
            M[i] = [x - f * y for x, y in zip(M[i], M[r])]
            ops.append(f"R{sub(i + 1)} ← R{sub(i + 1)} {'+' if f < 0 else '−'} {coef_abs(f)}R{sub(r + 1)}")
        if ops:
            steps.append((ops, snap(M), notes["elim"].format(c=c + 1)))
        piv.append(c)
        r += 1
    return M, steps, piv, r


def upper(A0, notes=NOTES_KO):
    M = snap(A0)
    n = len(M)
    steps, sign = [], 1
    for c in range(n):
        pr = next((i for i in range(c, n) if M[i][c] != 0), -1)
        if pr < 0:
            return Fr(0), M, steps
        if pr != c:
            M[pr], M[c] = M[c], M[pr]
            sign = -sign
            steps.append(([f"R{sub(c + 1)} ↔ R{sub(pr + 1)}"], snap(M), notes["uswap"]))
        ops = []
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            if f == 0:
                continue
            M[i] = [x - f * y for x, y in zip(M[i], M[c])]
            ops.append(f"R{sub(i + 1)} ← R{sub(i + 1)} {'+' if f < 0 else '−'} {coef_abs(f)}R{sub(c + 1)}")
        if ops:
            steps.append((ops, snap(M), notes["uelim"].format(c=c + 1)))
    d = Fr(sign)
    for i in range(n):
        d *= M[i][i]
    return d, M, steps


def lin(c0, terms):
    s = "" if c0 == 0 else num(c0)
    for f, name in terms:
        if f == 0:
            continue
        co = coef_abs(f)
        if s == "":
            s = ("−" if f < 0 else "") + co + name
        else:
            s = f"{s} {'−' if f < 0 else '+'} {co}{name}"
    return s or "0"


# =====================================================================
# 1. 역행렬
# =====================================================================
def art_inverse():
    A = M_([[2, 1], [5, 3]])
    aug = [A[i] + ident(2)[i] for i in range(2)]
    Mf, st, piv, rk = gj(aug, 2)
    inv = [r[2:] for r in Mf]
    assert inv == M_([[3, -1], [-5, 2]]) and rk == 2
    assert matmul(A, inv) == ident(2)
    assert A[0][0] * A[1][1] - A[0][1] * A[1][0] == 1
    ex1 = steps_html("A의 오른쪽에 단위행렬 I를 붙여 [A | I]를 만들어요.", aug, st, sep=2)

    B = M_([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
    augB = [B[i] + ident(3)[i] for i in range(3)]
    Mb, stb, _, rkb = gj(augB, 3)
    invB = [r[3:] for r in Mb]
    assert invB == M_([[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]) and rkb == 3
    assert matmul(B, invB) == ident(3)
    ex2 = steps_html("[B | I]를 만들어요.", augB, stb, sep=3)

    C = M_([[1, 2], [2, 4]])
    augC = [C[i] + ident(2)[i] for i in range(2)]
    Mc, stc, _, rkc = gj(augC, 2)
    assert rkc == 1 and all(x == 0 for x in Mc[1][:2])
    ex3 = steps_html("[C | I]를 만들어요.", augC, stc, sep=2)

    body = f"""
<p class="lead">역행렬은 행렬의 나눗셈에 해당하는 개념이에요. 이 글에서는 가우스-조던 소거법으로 역행렬을 구하는 과정을 2×2와 3×3 예제로 하나씩 따라가 봐요.</p>

<h2>역행렬이란?</h2>
<p>정사각행렬 A에 대해 AB = BA = I 를 만족하는 행렬 B가 있으면, B를 A의 역행렬이라고 하고 A⁻¹로 써요. I는 대각 성분이 1이고 나머지가 0인 단위행렬이에요.</p>
<p>역행렬은 모든 행렬에 있지 않아요. <strong>정사각행렬이면서 행렬식이 0이 아닐 때만</strong> 존재해요. 역행렬이 있는 행렬을 가역행렬이라고 불러요.</p>

<h2>가우스-조던 소거법 한눈에 보기</h2>
<p>A의 오른쪽에 단위행렬 I를 붙여 [A | I]를 만들어요. 여기에 행 연산을 반복해서 왼쪽을 I로 바꾸면, 오른쪽에 A⁻¹이 나타나요.</p>
{box(line("[ A | I ]"), op("→"), line("행 연산 반복"), op("→"), line("[ I | A⁻¹ ]"))}
<p>쓸 수 있는 행 연산은 세 가지예요.</p>
<ul>
<li>두 행 바꾸기: R₁ ↔ R₂</li>
<li>한 행에 0이 아닌 수 곱하기: R₁ ← 2R₁</li>
<li>한 행에 다른 행의 상수배 더하기: R₂ ← R₂ − 5R₁</li>
</ul>
<p>이 방법이 되는 이유는 이래요. 행 연산 하나는 왼쪽에서 어떤 가역행렬을 곱하는 것과 같아요. A를 I로 바꾸는 연산들을 모두 곱한 것이 A⁻¹이고, 같은 연산을 I에 적용하면 그 곱이 그대로 쌓여서 A⁻¹이 돼요.</p>

<h2>예제 1: 2×2 행렬</h2>
<p>아래 행렬의 역행렬을 구해 봐요.</p>
{box(line("A ="), mx(A))}
{ex1}
<p>왼쪽이 단위행렬이 되었으니 오른쪽이 역행렬이에요.</p>
{box(line("A⁻¹ ="), mx(inv))}
<p>2×2 행렬은 공식으로도 구할 수 있어요. A = [[a, b], [c, d]]이면 A⁻¹ = 1/(ad − bc) · [[d, −b], [−c, a]]예요. 여기서는 ad − bc = 2·3 − 1·5 = 1이라서 [[3, −1], [−5, 2]]가 되고, 소거법 결과와 같아요.</p>

<h3>검산하기</h3>
<p>AA⁻¹를 계산해서 단위행렬이 나오면 맞게 구한 거예요.</p>
{box(mx(A), op("×"), mx(inv), op("="), mx(matmul(A, inv)))}

<h2>예제 2: 3×3 행렬</h2>
<p>이번에는 3×3 행렬이에요. 방법은 똑같고 피벗이 하나 더 늘어날 뿐이에요.</p>
{box(line("B ="), mx(B))}
{ex2}
<p>왼쪽이 I가 되었어요. 그래서 B⁻¹은 아래와 같아요. 이 행렬은 행렬식이 1이라서 역행렬의 성분이 모두 정수로 나왔어요.</p>
{box(line("B⁻¹ ="), mx(invB))}

<h2>역행렬이 없는 경우</h2>
<p>소거하는 도중 왼쪽에 성분이 전부 0인 행이 생기면 단위행렬을 만들 수 없어요. 이때는 역행렬이 없다고 결론내려요.</p>
{box(line("C ="), mx(C))}
{ex3}
<p>왼쪽의 2행이 모두 0이 되었어요. 그래서 C는 역행렬이 없고, 실제로 det(C) = 1·4 − 2·2 = 0이에요. 두 번째 행이 첫 번째 행의 2배라서 생기는 일이에요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>왼쪽에만 연산을 하고 오른쪽 I에는 같은 연산을 빼먹어요. 행 전체에 적용해야 해요.</li>
<li>피벗 자리가 0인데 그냥 넘어가요. 아래 행 중에 0이 아닌 행이 있으면 행을 바꿔서 올려요.</li>
<li>분수 계산에서 부호를 틀려요. 마지막에 AA⁻¹ = I인지 꼭 검산해요.</li>
<li>행렬식이 0인데 끝까지 소거하려고 해요. 먼저 행렬식을 계산해 보면 시간을 아낄 수 있어요.</li>
</ul>

<h2>자주 묻는 질문</h2>
<div class="faq">
<details><summary>역행렬이 있는지 미리 알 수 있나요?</summary><p>행렬식이 0이 아니면 역행렬이 있어요. 3×3 행렬식은 <a href="/guide/determinant-3x3/">여인수 전개 가이드</a>를 참고하세요.</p></details>
<details><summary>4×4 이상은 어떻게 하나요?</summary><p>같은 방법으로 풀어요. 다만 손으로 하면 계산이 길어져서 실수하기 쉬우니, 계산기로 결과를 검산하는 걸 추천해요.</p></details>
<details><summary>2×2에서도 소거법을 써야 하나요?</summary><p>2×2는 공식이 더 빨라요. 3×3 이상부터는 소거법이 보통 더 정리하기 쉬워요.</p></details>
</div>
"""
    return dict(
        slug="inverse-gauss-jordan",
        title="가우스-조던 소거법으로 역행렬 구하는 법",
        h1="가우스-조던 소거법으로 역행렬 구하는 법",
        meta="[A | I]에 행 연산을 적용해 역행렬을 구하는 가우스-조던 소거법을 2×2, 3×3 예제로 설명해요. 역행렬이 없는 경우와 검산 방법도 알려드려요.",
        desc="[A | I]에 행 연산을 적용해 A⁻¹을 구하는 과정을 예제로 따라가요.",
        min=6, calc=("역행렬 계산기", "/inverse/"), body=body,
        related=["determinant-3x3", "linear-system-solutions"],
    )


# =====================================================================
# 2. 3×3 행렬식
# =====================================================================
def art_det():
    A = M_([[2, -1, 0], [1, 3, 2], [0, 1, 4]])
    mins = [minor(A, 0, j) for j in range(3)]
    mv = [det2(m) for m in mins]
    assert mv == [10, 4, 1]
    d = A[0][0] * mv[0] - A[0][1] * mv[1] + A[0][2] * mv[2]
    assert d == 24
    m21 = minor(A, 1, 0)
    assert det2(m21) == -4
    assert A[0][0] * mv[0] - A[1][0] * det2(m21) + A[2][0] * det2(minor(A, 2, 0)) == 24
    # 사러스
    a = A
    dr = a[0][0] * a[1][1] * a[2][2] + a[0][1] * a[1][2] * a[2][0] + a[0][2] * a[1][0] * a[2][1]
    dl = a[0][2] * a[1][1] * a[2][0] + a[0][0] * a[1][2] * a[2][1] + a[0][1] * a[1][0] * a[2][2]
    assert (dr, dl, dr - dl) == (24, 0, 24)
    du, Mu, stu = upper(A)
    assert du == 24

    def m2(m):
        return f"{par(m[0][0])}·{par(m[1][1])} − {par(m[0][1])}·{par(m[1][0])} = {num(det2(m))}"

    minors_html = ""
    for j in range(3):
        minors_html += box(line(f"M₁{sub(j + 1)} ="), mx(mins[j]), line(m2(mins[j])))
    elim = steps_html("행 소거로 상삼각행렬을 만들어요.", A, stu)

    body = f"""
<p class="lead">3×3 행렬식은 여인수 전개로 2×2 행렬식 세 개로 나눠서 풀 수 있어요. 이 글에서는 여인수 전개와 사러스 법칙, 그리고 행 소거로 같은 값을 구해 봐요.</p>

<h2>행렬식이란?</h2>
<p>행렬식은 정사각행렬에 하나의 수를 대응시키는 값이에요. 기하학적으로는 행렬이 나타내는 변환이 넓이(2×2)나 부피(3×3)를 몇 배로 바꾸는지를 의미해요. 행렬식이 0이면 역행렬이 없어요.</p>
<p>먼저 2×2 행렬식을 기억해 두세요. 3×3 계산에서 계속 쓰여요.</p>
{box(line("det [[a, b], [c, d]] = ad − bc"))}

<h2>여인수 전개 규칙</h2>
<p>한 행(또는 열)을 정해서 그 행의 각 성분에 <strong>소행렬식</strong>을 곱해 더하는 방법이에요. 성분 aᵢⱼ의 소행렬식 Mᵢⱼ는 i행과 j열을 지우고 남은 행렬의 행렬식이에요.</p>
<p>부호는 아래처럼 체스판 모양으로 붙어요. 위 왼쪽이 +이고, 한 칸 이동할 때마다 부호가 바뀌어요.</p>
{box(mx_text([["+", "−", "+"], ["−", "+", "−"], ["+", "−", "+"]]))}
<p>1행을 따라 전개하면 이렇게 써요.</p>
{box(line("det(A) = a₁₁M₁₁ − a₁₂M₁₂ + a₁₃M₁₃"))}

<h2>예제: 1행으로 전개하기</h2>
{box(line("A ="), mx(A))}
<p>1행의 성분은 2, −1, 0이에요. 각 성분에 해당하는 소행렬식을 먼저 구해요.</p>
{minors_html}
<p>이제 부호를 붙여 더해요.</p>
{box(line(f"det(A) = {par(A[0][0])}·{num(mv[0])} − {par(A[0][1])}·{num(mv[1])} + {par(A[0][2])}·{num(mv[2])} = {num(d)}"))}
<p>1행의 세 번째 성분이 0이라서 세 번째 항은 소행렬식을 구하지 않아도 0이에요. 이렇게 <strong>0이 많은 행이나 열을 골라 전개하면 계산이 줄어요.</strong></p>

<h3>다른 행·열로 전개해도 같아요</h3>
<p>1열은 아래 성분이 0이에요. 1열로 전개하면 a₃₁M₃₁이 0이 되어 항이 두 개만 남아요. 부호는 +, −, +예요.</p>
{box(line(f"det(A) = 2·10 − 1·M₂₁ + 0·M₃₁,  M₂₁ = {m2(m21)}"))}
{box(line("det(A) = 2·10 − 1·(−4) = 24"))}
<p>1행으로 구한 값과 같아요. 어느 행이나 열로 전개해도 결과는 같으니, 계산이 쉬운 쪽을 고르세요.</p>

<h2>사러스 법칙</h2>
<p>3×3에서만 쓸 수 있는 방법이에요. 오른쪽 아래로 향하는 대각선 세 개의 곱을 더하고, 왼쪽 아래로 향하는 대각선 세 개의 곱을 빼요.</p>
{box(line(f"오른쪽 아래: 2·3·4 + (−1)·2·0 + 0·1·1 = {num(dr)}"))}
{box(line(f"왼쪽 아래: 0·3·0 + 2·2·1 + (−1)·1·4 = {num(dl)}"))}
{box(line(f"det(A) = {num(dr)} − {num(dl)} = {num(dr - dl)}"))}
<p>사러스 법칙은 4×4 이상에는 쓸 수 없어요. 여인수 전개는 크기에 상관없이 쓸 수 있어서 함께 알아 두는 게 좋아요.</p>

<h2>행 소거로 구하기</h2>
<p>4×4 이상에서는 행 소거로 상삼각행렬을 만드는 방법이 편해요. 대각선 아래를 0으로 만들면 행렬식은 대각 성분의 곱이에요. 같은 행렬로 해 볼게요.</p>
{elim}
<p>대각 성분을 곱하면 2 · 7/2 · 24/7 = 24예요. 행을 서로 바꾸지 않았으니 부호는 그대로예요. 세 방법의 결과가 모두 같아요.</p>

<h2>행렬식의 성질</h2>
<ul>
<li>두 행(또는 열)을 서로 바꾸면 부호가 반대가 돼요.</li>
<li>한 행에 k를 곱하면 행렬식도 k배가 돼요.</li>
<li>한 행에 다른 행의 상수배를 더해도 값이 변하지 않아요.</li>
<li>det(Aᵀ) = det(A), det(AB) = det(A)·det(B)예요.</li>
<li>n×n 행렬에서 det(kA) = kⁿ·det(A)예요.</li>
<li>삼각행렬의 행렬식은 대각 성분의 곱이에요.</li>
<li>det(A) = 0이면 A는 역행렬이 없고, 행들이 선형종속이에요.</li>
</ul>

<h2>자주 하는 실수</h2>
<ul>
<li>소행렬식을 구할 때 지우는 행과 열을 헷갈려요. 성분이 있는 행과 열을 지워요.</li>
<li>체스판 부호를 빼먹어요. 가운데 성분 a₁₂는 −예요.</li>
<li>사러스 법칙을 4×4에 써요. 사러스는 3×3 전용이에요.</li>
<li>행을 바꾸고도 부호를 되돌리지 않아요.</li>
</ul>

<h2>자주 묻는 질문</h2>
<div class="faq">
<details><summary>행렬식이 음수면 무슨 뜻인가요?</summary><p>변환이 방향을 뒤집는다는 뜻이에요. 넓이나 부피가 몇 배로 변하는지는 절댓값으로 봐요.</p></details>
<details><summary>직사각행렬의 행렬식도 있나요?</summary><p>없어요. 행렬식은 정사각행렬에서만 정의돼요.</p></details>
<details><summary>행렬식을 구했는데 역행렬은 어떻게 구하나요?</summary><p><a href="/guide/inverse-gauss-jordan/">가우스-조던 소거법 가이드</a>에서 단계별로 설명하고 있어요.</p></details>
</div>
"""
    return dict(
        slug="determinant-3x3",
        title="3×3 행렬식 계산법 (여인수 전개·사러스)",
        h1="3×3 행렬식 계산법: 여인수 전개와 사러스 법칙",
        meta="3×3 행렬식을 여인수 전개, 사러스 법칙, 행 소거 세 가지 방법으로 같은 예제에 적용해 비교해요. 행렬식의 성질과 자주 하는 실수도 정리했어요.",
        desc="여인수 전개, 사러스 법칙, 행 소거로 같은 3×3 행렬식을 구해 봐요.",
        min=6, calc=("행렬식 계산기", "/determinant/"), body=body,
        related=["inverse-gauss-jordan", "rank-and-rref"],
    )


# =====================================================================
# 3. 랭크와 RREF
# =====================================================================
def art_rank():
    A = M_([[1, 2, -1, 3], [2, 4, 1, 0], [-1, -2, 2, 1]])
    Mf, st, piv, rk = gj(A, 4)
    assert Mf == M_([[1, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert piv == [0, 2, 3] and rk == 3
    ex = steps_html("주어진 행렬에서 시작해요.", A, st)

    body = f"""
<p class="lead">기약 행사다리꼴(RREF)은 행렬을 가장 단순한 모양으로 정리한 결과예요. 한 번 만들어 두면 랭크, 피벗 열, 연립방정식의 해를 한눈에 읽을 수 있어요.</p>

<h2>RREF의 조건</h2>
<p>행렬이 기약 행사다리꼴이 되려면 아래 네 가지를 모두 만족해야 해요.</p>
<ol>
<li>성분이 모두 0인 행은 맨 아래에 있어요.</li>
<li>각 행에서 처음으로 나오는 0이 아닌 성분(<strong>피벗</strong>)은 1이에요.</li>
<li>아래 행의 피벗은 위 행의 피벗보다 오른쪽에 있어요. 그래서 계단 모양이 돼요.</li>
<li>피벗이 있는 열에서 피벗을 뺀 나머지 성분은 모두 0이에요.</li>
</ol>
<p>1~3번만 만족하면 행사다리꼴(REF)이에요. 교재에 따라 피벗이 1일 필요가 없다고 정의하기도 해요. REF는 여러 모양이 나올 수 있지만, <strong>RREF는 행렬마다 딱 하나로 정해져요.</strong> 그래서 풀이 순서가 달라도 결과는 항상 같아요.</p>

<h2>예제: RREF 만들기</h2>
<p>3×4 행렬을 RREF로 바꿔 봐요.</p>
{box(line("A ="), mx(A))}
{ex}
<p>최종 결과는 아래와 같아요.</p>
{box(line("RREF(A) ="), mx(Mf))}

<h2>결과 읽는 법</h2>
<ul>
<li><strong>피벗 열</strong>은 1, 3, 4열이에요. 피벗이 있는 열이에요.</li>
<li><strong>랭크</strong>는 피벗의 개수인 3이에요.</li>
<li>피벗이 없는 2열은 <strong>자유변수</strong> 열이에요. 연립방정식으로 보면 값을 마음대로 정할 수 있는 변수예요.</li>
</ul>
<p>2열에서는 위 단계에서 아래쪽 성분이 모두 0이라 피벗을 잡을 수 없었어요. 이럴 때는 그 열을 건너뛰고 다음 열로 가서 피벗을 찾아요.</p>

<h2>랭크가 알려주는 것</h2>
<p>랭크는 행렬에서 서로 독립인 행(또는 열)이 몇 개인지를 나타내요.</p>
<ul>
<li>m×n 행렬의 랭크는 min(m, n)을 넘지 않아요.</li>
<li>행으로 센 랭크와 열로 센 랭크는 같아요. rank(A) = rank(Aᵀ)예요.</li>
<li>n×n 행렬에서 랭크가 n이면 역행렬이 있고, 행렬식이 0이 아니에요.</li>
<li><strong>랭크-영공간 차원 정리</strong>: rank(A) + nullity(A) = 열의 수예요. 여기서는 3 + 1 = 4라서 Ax = 0의 해 공간(영공간)의 차원은 1이에요.</li>
</ul>
<p>열공간의 기저를 구할 때는 한 가지를 조심하세요. RREF의 피벗 열 번호만 가져오고, 열은 <strong>원래 행렬 A의 열</strong>을 써야 해요. 이 예제에서는 A의 1, 3, 4열이 열공간의 기저예요. RREF의 열은 열공간이 달라져 있어요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>피벗을 1로 만들지 않고 멈춰요. 그러면 REF이고 RREF가 아니에요.</li>
<li>피벗 위쪽 성분을 0으로 만드는 걸 잊어요. RREF는 피벗 위아래가 모두 0이어야 해요.</li>
<li>0 열을 만났을 때 멈춰요. 다음 열로 넘어가서 피벗을 찾아요.</li>
<li>열공간의 기저를 RREF의 열로 써요. 원래 A의 열을 써야 해요.</li>
</ul>

<h2>자주 묻는 질문</h2>
<div class="faq">
<details><summary>랭크가 0인 행렬이 있나요?</summary><p>영행렬만 랭크가 0이에요. 피벗이 하나도 없어요.</p></details>
<details><summary>RREF는 어디에 쓰나요?</summary><p>연립방정식 풀이, 랭크 계산, 영공간과 열공간의 기저 구하기, 역행렬 구하기 모두 RREF를 만드는 과정이에요.</p></details>
<details><summary>연립방정식의 해와는 어떤 관계인가요?</summary><p>첨가행렬을 RREF로 바꾸면 해를 읽을 수 있어요. <a href="/guide/linear-system-solutions/">연립방정식 가이드</a>에서 이어서 설명해요.</p></details>
</div>
"""
    return dict(
        slug="rank-and-rref",
        title="행렬의 랭크와 기약 행사다리꼴(RREF) 읽는 법",
        h1="행렬의 랭크와 기약 행사다리꼴(RREF) 읽는 법",
        meta="RREF의 네 가지 조건과 만드는 과정을 예제로 보여주고, 결과에서 피벗 열, 랭크, 자유변수, 영공간의 차원을 읽어 내는 방법을 정리했어요.",
        desc="RREF를 만들고 피벗 열과 랭크, 자유변수를 읽어 내는 방법이에요.",
        min=6, calc=("RREF 계산기", "/rref/"), body=body,
        related=["linear-system-solutions", "inverse-gauss-jordan"],
    )


# =====================================================================
# 4. 연립방정식의 해
# =====================================================================
def art_system():
    # 유일한 해
    A1 = M_([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    M1, _, p1, r1 = gj(A1, 3)
    assert [row[3] for row in M1] == [2, 3, -1] and r1 == 3
    x = [row[3] for row in M1]
    for row in A1:
        assert sum(row[j] * x[j] for j in range(3)) == row[3]

    # 해 없음
    A2 = M_([[1, 1, 1, 3], [2, 2, 2, 5], [1, -1, 0, 1]])
    M2, st2, p2, r2 = gj(A2, 3)
    assert r2 == 2 and M2[2][:3] == [0, 0, 0] and M2[2][3] != 0
    ex2 = steps_html("첨가행렬 [A | b]를 만들어요.", A2, st2, sep=3)

    # 해가 무수히 많음
    A3 = M_([[1, 2, 1, 4], [2, 4, 2, 8], [1, 1, 0, 3]])
    M3, st3, p3, r3 = gj(A3, 3)
    assert r3 == 2 and p3 == [0, 1] and M3[2] == [0, 0, 0, 0]
    free = [j for j in range(3) if j not in p3]
    assert free == [2]
    names = ["x", "y", "z"]
    sol = []
    for j in range(3):
        if j in free:
            sol.append(f"{names[j]} = t")
        else:
            row = M3[p3.index(j)]
            sol.append(f"{names[j]} = " + lin(row[3], [(-row[f], "t") for f in free]))
    assert sol == ["x = 2 + t", "y = 1 − t", "z = t"]
    for t in (Fr(0), Fr(1), Fr(-3)):
        xx, yy, zz = 2 + t, 1 - t, t
        assert xx + 2 * yy + zz == 4 and 2 * xx + 4 * yy + 2 * zz == 8 and xx + yy == 3
    ex3 = steps_html("첨가행렬 [A | b]를 만들어요.", A3, st3, sep=3)

    body = f"""
<p class="lead">연립일차방정식은 해가 하나이거나, 없거나, 무수히 많아요. 세 경우는 첨가행렬을 소거해 보면 바로 구분할 수 있어요. 예제 세 개로 차이를 확인해 봐요.</p>

<h2>첨가행렬로 바꾸기</h2>
<p>연립방정식 Ax = b에서 계수행렬 A의 오른쪽에 b를 붙인 행렬 [A | b]를 첨가행렬이라고 해요. 이 행렬에 행 연산을 적용해 RREF로 바꾸면 해를 읽을 수 있어요.</p>

<h2>해의 개수를 판별하는 기준</h2>
<p>미지수의 개수를 n이라고 할 때, 소거한 결과에서 아래 기준으로 구분해요.</p>
<div class="tbl"><table class="gtable">
<thead><tr><th>조건</th><th>해의 개수</th><th>소거 결과에서 보이는 모양</th></tr></thead>
<tbody>
<tr><td>rank(A) &lt; rank([A | b])</td><td>해 없음</td><td>0 = (0이 아닌 수) 꼴의 행이 생겨요</td></tr>
<tr><td>rank(A) = rank([A | b]) = n</td><td>해가 하나</td><td>모든 변수 열에 피벗이 있어요</td></tr>
<tr><td>rank(A) = rank([A | b]) &lt; n</td><td>해가 무수히 많음</td><td>피벗이 없는 열(자유변수)이 있어요</td></tr>
</tbody></table></div>

<h2>경우 1: 해가 하나</h2>
<p>아래 연립방정식을 풀어요.</p>
{box(line("2x + y − z = 8"))}
{box(line("−3x − y + 2z = −11"))}
{box(line("−2x + y + 2z = −3"))}
<p>첨가행렬을 RREF로 바꾸면 이렇게 돼요. 중간 과정은 계산기에서 모두 볼 수 있어요.</p>
{box(mx(A1, sep=3), op("→"), mx(M1, sep=3))}
<p>세 변수 열에 모두 피벗이 있어요. rank(A) = rank([A | b]) = 3 = n이라서 해가 하나로 정해지고, 오른쪽 열이 곧 해예요.</p>
{box(line("(x, y, z) = (2, 3, −1)"))}
<p>원래 식에 대입해서 확인해요. 2·2 + 3 − (−1) = 8, −3·2 − 3 + 2·(−1) = −11, −2·2 + 3 + 2·(−1) = −3이 모두 성립해요.</p>

<h2>경우 2: 해가 없음</h2>
{box(line("x + y + z = 3"))}
{box(line("2x + 2y + 2z = 5"))}
{box(line("x − y = 1"))}
<p>첫 번째 식에 2를 곱하면 2x + 2y + 2z = 6인데, 두 번째 식은 5라고 해서 서로 모순이에요. 소거해서 확인해 봐요.</p>
{ex2}
<p>3행이 [0, 0, 0 | −1]이 되었어요. 이 행은 0 = −1을 뜻해서 성립할 수 없어요. 그래서 해가 없어요. rank(A) = 2이고 rank([A | b]) = 3이라서 rank(A) &lt; rank([A | b])예요.</p>

<h2>경우 3: 해가 무수히 많음</h2>
{box(line("x + 2y + z = 4"))}
{box(line("2x + 4y + 2z = 8"))}
{box(line("x + y = 3"))}
<p>두 번째 식은 첫 번째 식의 2배예요. 사실상 식이 두 개뿐이라는 뜻이에요.</p>
{ex3}
<p>3행이 모두 0이 되었고, 3열에는 피벗이 없어요. rank(A) = rank([A | b]) = 2이고 n = 3이라서 해가 무수히 많아요. 피벗이 없는 열에 해당하는 변수 z가 <strong>자유변수</strong>예요. z = t로 두면 나머지 변수가 t로 정해져요.</p>
{box('<div class="sol">' + "".join(f"<div>{s}</div>" for s in sol) + "</div>")}
<p>t에 어떤 수를 넣어도 세 식을 모두 만족해요. 예를 들어 t = 0이면 (2, 1, 0), t = 1이면 (3, 0, 1)이에요. 자유변수의 개수는 n − rank = 3 − 2 = 1이고, 해가 직선 위에 놓인다는 뜻이에요.</p>

<h2>자주 하는 실수</h2>
<ul>
<li>식의 개수와 미지수의 개수를 비교해서 판단해요. 식이 많아도 서로 겹치면 해가 있을 수 있고, 식이 적으면 해가 없는 게 아니라 무수히 많은 경우가 흔해요.</li>
<li>0 = 0인 행을 보고 해가 없다고 해요. 0 = 0은 문제가 없는 식이에요. 0 = (0이 아닌 수)일 때만 해가 없어요.</li>
<li>자유변수를 하나만 잡고 나머지를 빼먹어요. 피벗이 없는 열은 모두 자유변수예요.</li>
<li>일반해를 쓸 때 부호를 틀려요. 원래 식에 대입해서 확인하세요.</li>
</ul>

<h2>자주 묻는 질문</h2>
<div class="faq">
<details><summary>식이 미지수보다 많으면 항상 해가 없나요?</summary><p>아니에요. 예를 들어 같은 식이 여러 번 반복되면 해가 있어요. 랭크로 판단하세요.</p></details>
<details><summary>자유변수는 어떤 변수를 골라도 되나요?</summary><p>RREF에서 피벗이 없는 열의 변수가 자유변수예요. 소거 순서를 바꾸면 달라 보일 수 있지만, 해 전체의 집합은 같아요.</p></details>
<details><summary>Ax = 0이면 어떻게 되나요?</summary><p>x = 0은 항상 해예요. 그래서 해가 없는 경우는 없고, 자유변수가 있으면 0이 아닌 해도 무수히 많아요.</p></details>
</div>
"""
    return dict(
        slug="linear-system-solutions",
        title="연립방정식의 해가 없을 때와 무수히 많을 때 구분하는 법",
        h1="연립방정식의 해가 없을 때와 무수히 많을 때 구분하는 법",
        meta="첨가행렬을 소거해 연립방정식의 해가 하나인지, 없는지, 무수히 많은지 구분하는 방법을 랭크 기준과 예제 세 개로 설명해요. 일반해 쓰는 법도 알려드려요.",
        desc="랭크로 해의 개수를 판별하고 자유변수로 일반해를 쓰는 방법이에요.",
        min=7, calc=("연립방정식 계산기", "/linear-system/"), body=body,
        related=["rank-and-rref", "inverse-gauss-jordan"],
    )


ARTICLES = [art_inverse(), art_det(), art_rank(), art_system()]
for _a in ARTICLES: _a["published"] = "2026-10-13"

# 추가 가이드: 다른 모듈에서 불러와요 (위 도우미 함수가 모두 정의된 뒤에 가져와야 해요)
import guides_a  # noqa: E402
import guides_b  # noqa: E402
import guides_c  # noqa: E402
for _a in guides_a.ARTICLES + guides_b.ARTICLES + guides_c.ARTICLES: _a["published"] = "2026-10-26"
ARTICLES += guides_a.ARTICLES + guides_b.ARTICLES + guides_c.ARTICLES
BY_SLUG = {a["slug"]: a for a in ARTICLES}
