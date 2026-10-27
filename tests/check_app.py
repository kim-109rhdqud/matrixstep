#!/usr/bin/env python3
"""assets/app.js 계산 결과를 Python fractions로 독립 검증해요.

사용: python3 tests/check_app.py [seed] [ko|en]
tests/run_app.js가 무작위 행렬에 대해 계산기 코드를 실행한 결과(LaTeX)를 받아,
여기서 따로 구현한 분수 연산으로 다시 계산해 비교해요.
"""
import json, re, subprocess, sys, os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
seed = sys.argv[1] if len(sys.argv) > 1 else "20261013"
lang = sys.argv[2] if len(sys.argv) > 2 else "ko"
raw = subprocess.run(["node", os.path.join(HERE, "run_app.js"), seed, lang], capture_output=True, text=True, check=True).stdout
data = json.loads(raw)
assert data["lang"] == lang

# 결과 칩 문구 (언어별)
CH = {
    "ko": dict(singular="비가역 행렬", noinv="역행렬 없음", none="해 없음", unique="유일한 해",
               free=lambda n: f"자유변수 {n}개", piv=lambda s: f"피벗 열 {s}",
               full="최대 계수", deficient="계수 부족", diag="대각화 가능", notdiag="대각화 불가능", diagok="대각화 완료"),
    "en": dict(singular="Singular matrix", noinv="Not invertible", none="No solution", unique="Unique solution",
               free=lambda n: f"{n} free variable" + ("s" if n > 1 else ""), piv=lambda s: f"Pivot columns {s}",
               full="Full rank", deficient="Rank deficient", diag="Diagonalizable", notdiag="Not diagonalizable", diagok="Diagonalized"),
}[lang]

# ---------- 입력 파싱 (앱과 같은 규칙) ----------
def parse(s):
    s = str(s).strip().replace("−", "-").replace("–", "-").replace(" ", "")
    if s == "": return Fr(0)
    m = re.fullmatch(r"([+-]?)(\d+)/(\d+)", s)
    if m:
        if int(m.group(3)) == 0: return None
        return Fr(int(m.group(1) + m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"([+-]?)(\d+)?(?:\.(\d*))?", s)
    if not m or (not m.group(2) and not m.group(3)): return None
    fr = m.group(3) or ""
    return Fr(int(m.group(1) + (m.group(2) or "0") + fr), 10 ** len(fr))

M = lambda rows: [[parse(x) for x in r] for r in rows]

# ---------- LaTeX 결과 파싱 ----------
def tex_num(t):
    t = t.strip()
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", t)
    if m: return Fr(int(m.group(1) + m.group(2)), int(m.group(3)))
    return Fr(int(t))
def tex_mat(t):
    m = re.fullmatch(r"\\begin\{bmatrix\} (.*?) \\end\{bmatrix\}", t.strip())
    assert m, t
    return [[tex_num(x) for x in row.split("&")] for row in m.group(1).split("\\\\")]

# ---------- 독립 구현 ----------
def det(A):
    n = len(A)
    if n == 1: return A[0][0]
    return sum(((-1) ** j) * A[0][j] * det([r[:j] + r[j + 1:] for r in A[1:]]) for j in range(n) if A[0][j] != 0) or Fr(0)
def rref(A):
    A = [r[:] for r in A]; R, C = len(A), len(A[0]); r = 0; piv = []
    for c in range(C):
        if r >= R: break
        p = next((i for i in range(r, R) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(R):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    return A, piv
rank = lambda A: len(rref(A)[1])
mul = lambda A, B: [[sum(a * b for a, b in zip(r, col)) for col in zip(*B)] for r in A]
I = lambda n: [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
fr = lambda s: Fr(s)                                   # "n/d" → Fraction
def peval(c, x):                                       # c[k] = λ^k 계수
    r = Fr(0)
    for a in reversed(c): r = r * x + a
    return r
def deflate(c, r):
    n = len(c) - 1; q = [Fr(0)] * n; q[n - 1] = c[n]
    for i in range(n - 1, 0, -1): q[i - 1] = c[i] + r * q[i]
    return q, c[0] + r * q[0]
def divisors(n):
    n = abs(n); out = set(); i = 1
    while i * i <= n:
        if n % i == 0: out.add(i); out.add(n // i)
        i += 1
    return out
def charpoly(A):
    # det(λI − A) 를 λ = 0..n 보간 (라그랑주) → 계수 리스트 c[k] = λ^k
    n = len(A); xs = list(range(n + 1))
    ys = [det([[(Fr(x) if i == j else Fr(0)) - A[i][j] for j in range(n)] for i in range(n)]) for x in xs]
    c = [Fr(0)] * (n + 1)
    for i, xi in enumerate(xs):
        term = [Fr(1)]; denom = Fr(1)
        for j, xj in enumerate(xs):
            if j == i: continue
            term = [Fr(0)] + term; 
            for k in range(len(term) - 1): term[k] -= xj * term[k + 1]
            denom *= (xi - xj)
        for k in range(len(term)): c[k] += ys[i] * term[k] / denom
    return c
def rational_roots(c):
    """유리근 정리로 모든 유리수 근(중복 포함) 찾기. 상수항이 너무 크면 None."""
    from math import lcm
    L = 1
    for a in c: L = lcm(L, a.denominator)
    ic = [int(a * L) for a in c]
    roots = []
    while len(ic) > 1 and ic[0] == 0:                  # λ = 0
        roots.append(Fr(0)); ic = ic[1:]
    if len(ic) > 1:
        if abs(ic[0]) > 10 ** 9: return None
        cands = {Fr(sp * p, q) for p in divisors(ic[0]) for q in divisors(ic[-1]) for sp in (1, -1)}
        cc = [Fr(a) for a in ic]
        for r in sorted(cands):
            while len(cc) > 1 and peval(cc, r) == 0:
                roots.append(r); cc, rem = deflate(cc, r); assert rem == 0
    return roots

bad = 0; count = {}
def fail(c, why):
    global bad; bad += 1
    print("FAIL", c["op"], why, json.dumps(c["inp"], ensure_ascii=False)[:200])

for c in data["cases"]:
    op = c["op"]; count[op] = count.get(op, 0) + 1
    A = M(c["inp"]["A"])
    try:
        if op == "inverse":
            d = det(A)
            if d == 0:
                if c["latex"] is not None or CH["singular"] not in c["chips"]: fail(c, "특이행렬인데 역행렬을 냈어요")
            else:
                inv = tex_mat(c["latex"])
                if mul(A, inv) != I(len(A)) or mul(inv, A) != I(len(A)): fail(c, "A·A⁻¹ ≠ I")
                if f"det(A) = " not in " ".join(c["chips"]): fail(c, "det 칩 없음")
        elif op == "det":
            d = det(A)
            if tex_num(c["latex"]) != d: fail(c, f"det 불일치 (정답 {d}, 결과 {c['latex']})")
            if (d == 0) != (CH["noinv"] in c["chips"]): fail(c, "가역 여부 칩 불일치")
        elif op == "transpose":
            if tex_mat(c["latex"]) != [list(r) for r in zip(*A)]: fail(c, "전치 불일치")
        elif op == "scalar":
            k = parse(c["inp"]["k"])
            if tex_mat(c["latex"]) != [[k * x for x in r] for r in A]: fail(c, "스칼라배 불일치")
        elif op == "mul":
            if tex_mat(c["latex"]) != mul(A, M(c["inp"]["B"])): fail(c, "곱셈 불일치")
        elif op in ("add", "sub"):
            B = M(c["inp"]["B"]); s = 1 if op == "add" else -1
            if tex_mat(c["latex"]) != [[x + s * y for x, y in zip(r1, r2)] for r1, r2 in zip(A, B)]: fail(c, "덧셈/뺄셈 불일치")
        elif op == "rref":
            R, piv = rref(A)
            if tex_mat(c["latex"]) != R: fail(c, "RREF 불일치")
            if f"rank = {len(piv)}" not in c["chips"]: fail(c, f"rank 칩 불일치 (정답 {len(piv)})")
            if piv and CH["piv"](", ".join(str(p + 1) for p in piv)) not in c["chips"]: fail(c, "피벗 열 칩 불일치")
        elif op == "solve":
            b = [parse(x) for x in c["inp"]["b"]]; n = len(A[0])
            rA, rAb = rank(A), rank([r + [bi] for r, bi in zip(A, b)])
            if rA != rAb:
                if CH["none"] not in c["chips"]: fail(c, "해가 없어야 해요")
            elif rA == n:
                x = tex_mat(c["latex"])
                if mul(A, x) != [[bi] for bi in b]: fail(c, "Ax ≠ b")
                if CH["unique"] not in c["chips"]: fail(c, "유일한 해 칩 없음")
            else:
                if CH["free"](n - rA) not in c["chips"] or f"rank = {rA}" not in c["chips"]: fail(c, f"자유변수/rank 칩 불일치 (정답 자유변수 {n - rA}, rank {rA})")
        elif op == "power":
            k = int(c["inp"]["k"]); P = I(len(A))
            for _ in range(k): P = mul(P, A)
            if tex_mat(c["latex"]) != P: fail(c, "거듭제곱 불일치")
            if f"n = {k}" not in c["chips"]: fail(c, "n 칩 없음")
        elif op == "adj":
            n = len(A); adj = [[fr(x) for x in r] for r in c["data"]["adj"]]; d = det(A)
            if tex_mat(c["latex"]) != adj: fail(c, "latex와 data 불일치")
            if n == 1:
                if adj != [[Fr(1)]]: fail(c, "1×1 수반행렬은 [1]")
            else:
                dI = [[d * x for x in r] for r in I(n)]
                if mul(adj, A) != dI or mul(A, adj) != dI: fail(c, "adj(A)·A ≠ det(A)·I")
            if f"det(A) = " not in " ".join(c["chips"]): fail(c, "det 칩 없음")
            if (d == 0) != (CH["noinv"] in c["chips"]): fail(c, "가역 여부 칩 불일치")
        elif op == "rank":
            R, piv = rref(A); r = len(piv); m, n = len(A), len(A[0]); D = c["data"]
            if (D["rank"], D["nullity"], D["piv"]) != (r, n - r, piv): fail(c, f"rank/nullity/piv 불일치 (정답 {r}, {n - r}, {piv})")
            if c["latex"] != str(r): fail(c, "latex rank 불일치")
            full = r == min(m, n)
            if (CH["full"] in c["chips"]) != full or (CH["deficient"] in c["chips"]) == full: fail(c, "최대 랭크 칩 불일치")
        elif op == "eigen":
            n = len(A); D = c["data"]; poly = [fr(x) for x in D["poly"]]
            if len(poly) != n + 1 or poly[n] != 1: fail(c, "특성다항식 차수/최고차 계수")
            # p(λ) = det(λI − A) 를 λ = 0..n 에서 독립 계산과 비교
            for lam in range(n + 1):
                Ml = [[(Fr(lam) if i == j else Fr(0)) - A[i][j] for j in range(n)] for i in range(n)]
                if peval(poly, Fr(lam)) != det(Ml): fail(c, f"p({lam}) ≠ det({lam}I − A)"); break
            # 유리수 근: 정확한 근이고 중복도가 맞는지, 빠진 유리수 근이 없는지
            q = poly[:]; got = []
            for rs, mlt in D["rational"]:
                r = fr(rs)
                for _ in range(mlt):
                    if peval(q, r) != 0: fail(c, f"유리수 근 {rs} 가 근이 아니거나 중복도 과다"); break
                    q, rem = deflate(q, r); got.append(r)
                if len(q) > 1 and peval(q, r) == 0: fail(c, f"유리수 근 {rs} 중복도 부족")
            ref = rational_roots(poly)
            if ref is not None and sorted(ref) != sorted(got): fail(c, f"유리수 근 집합 불일치 (정답 {sorted(ref)}, 결과 {sorted(got)})")
            # 남은 이차식
            if D["quad"]:
                if len(q) != 3: fail(c, "quad 정보가 있는데 남은 차수가 2가 아님")
                else:
                    b, cc = q[1], q[0]; disc = b * b - 4 * cc
                    Q = D["quad"]
                    if fr(Q["D"]) != disc or fr(Q["re"]) != -b / 2: fail(c, "판별식/실수부 불일치")
                    k, m = fr(Q["k"]), int(Q["m"])
                    if k * k * m * 4 != abs(disc): fail(c, "√ 단순화 불일치 (k²·m·4 ≠ |D|)")
                    if m > 1 and any(m % (f * f) == 0 for f in range(2, min(int(m ** 0.5) + 1, 1000))): fail(c, "√ 안에 제곱인수가 남음")
            elif len(q) == 3: fail(c, "남은 이차식이 있는데 quad 정보 없음")
            # 수치 근
            if D["numeric"]:
                if len(q) < 4: fail(c, "차수 3 미만인데 수치 근 사용")
                if len(D["numeric"]) != len(q) - 1: fail(c, "수치 근 개수 불일치")
                qf = [float(a) for a in q]
                for re_, im_ in D["numeric"]:
                    z = complex(re_, im_); v = sum(a * z ** k for k, a in enumerate(qf))
                    if abs(v) > 1e-6 * max(1.0, abs(z)) ** (len(q) - 1) * max(1.0, max(abs(a) for a in qf)): fail(c, f"수치 근 {z} 이 근이 아님 |q(z)|={abs(v):.2e}"); break
            elif len(q) >= 4: fail(c, "남은 고차식이 있는데 수치 근 없음")
            # 고유벡터
            if [fr(v[0]) for v in D["vecs"]] != [fr(rs) for rs, _ in D["rational"]]: fail(c, "고유벡터 λ 목록 불일치")
            for ls, vecs in D["vecs"]:
                lam = fr(ls); Ml = [[A[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
                V = [[fr(x) for x in v] for v in vecs]
                if len(V) != n - rank(Ml): fail(c, f"λ={ls} 고유벡터 개수 ≠ nullity"); continue
                for v in V:
                    if all(x == 0 for x in v) or any(x != 0 for r in mul(Ml, [[x] for x in v]) for x in r): fail(c, f"λ={ls} 고유벡터가 (A−λI)v=0 을 만족하지 않음"); break
                if V and rank(V) != len(V): fail(c, f"λ={ls} 고유벡터가 선형종속")
            # 대각화 칩
            if CH["diag"] in c["chips"] or CH["notdiag"] in c["chips"]:
                if D["quad"] and fr(D["quad"]["D"]) < 0: fail(c, "복소 고윳값인데 대각화 칩")
                elif sum(m for _, m in D["rational"]) == n:
                    geo = sum(len(v) for _, v in D["vecs"]); want = CH["diag"] if geo == n else CH["notdiag"]
                    if want not in c["chips"]: fail(c, f"대각화 칩 오류 (기하 {geo}, n {n})")
        elif op == "diag":
            n = len(A); D = c["data"]
            # 특성다항식은 eigen 검사에서 이미 검증 → 여기서는 유리수 근 완전성으로 가능 여부 판정
            cp = charpoly(A); ref = rational_roots(cp)
            if D["ok"]:
                P = [[fr(x) for x in r] for r in D["P"]]; dv = [fr(x) for x in D["D"]]; Pi = [[fr(x) for x in r] for r in D["Pi"]]
                if mul(P, Pi) != I(n): fail(c, "P·P⁻¹ ≠ I")
                Dm = [[dv[i] if i == j else Fr(0) for j in range(n)] for i in range(n)]
                if mul(mul(P, Dm), Pi) != A: fail(c, "PDP⁻¹ ≠ A")
                if CH["diagok"] not in c["chips"]: fail(c, "대각화 완료 칩 없음")
            else:
                if CH["notdiag"] not in c["chips"]: fail(c, "대각화 불가능 칩 없음")
                if ref is not None and len(ref) == n:
                    geo = sum(n - rank([[A[i][j] - (r if i == j else 0) for j in range(n)] for i in range(n)]) for r in set(ref))
                    if geo == n: fail(c, "대각화 가능한데 불가능이라 함")
                    if D["reason"] != "defective": fail(c, "불가능 사유가 달라요")
                elif D["reason"] != "irrational": fail(c, "유리수 근이 부족한데 사유가 irrational 이 아님")
        elif op == "axb":
            B = M(c["inp"]["B"]); n = len(A); D = c["data"]
            rA = rank(A); rAB = rank([r + rb for r, rb in zip(A, B)])
            if rA != rAB:
                if D["kind"] != "none" or CH["none"] not in c["chips"]: fail(c, "해가 없어야 해요")
            else:
                X = [[fr(x) for x in r] for r in D["X"]]
                if mul(A, X) != B: fail(c, "AX ≠ B")
                if tex_mat(c["latex"]) != X: fail(c, "latex와 data 불일치")
                want = "unique" if rA == n else "inf"
                if D["kind"] != want: fail(c, f"해의 종류 불일치 (정답 {want})")
                if want == "unique" and CH["unique"] not in c["chips"]: fail(c, "유일한 해 칩 없음")
                if want == "inf" and CH["free"](n - rA) not in c["chips"]: fail(c, "자유변수 칩 불일치")
        elif op == "gs":
            D = c["data"]; U = [[fr(x) for x in u] for u in D["U"]]; kept = D["kept"]
            cols = [list(cl) for cl in zip(*A)]
            if len(U) != rank(A): fail(c, f"직교 벡터 개수 ≠ rank (정답 {rank(A)})")
            for i, u in enumerate(U):
                if all(x == 0 for x in u): fail(c, "영벡터가 남아 있어요"); break
                for v in U[:i]:
                    if sum(a * b for a, b in zip(u, v)) != 0: fail(c, "직교하지 않아요"); break
                # span(u_1..u_i) == span(v_kept[0..i])
                if rank(U[:i + 1] + cols[:kept[i] + 1]) != i + 1: fail(c, "생성 공간이 달라요"); break
            if len(U) and tex_mat(c["latex"]) != [list(r) for r in zip(*U)]: fail(c, "latex와 data 불일치")
        elif op == "lu":
            n = len(A); D = c["data"]; L = [[fr(x) for x in r] for r in D["L"]]; U = [[fr(x) for x in r] for r in D["U"]]; perm = D["perm"]
            if any(L[i][j] != (1 if i == j else 0) for i in range(n) for j in range(i, n)): fail(c, "L이 단위 하삼각이 아님")
            if any(U[i][j] != 0 for i in range(n) for j in range(i)): fail(c, "U가 상삼각이 아님")
            PA = [A[p] for p in perm]
            if mul(L, U) != PA: fail(c, "LU ≠ PA")
            if sorted(perm) != list(range(n)): fail(c, "perm이 치환이 아님")
        if c["steps"] < 1: fail(c, "풀이 단계가 없어요")
    except Exception as ex:  # 파싱 실패 등
        fail(c, f"예외 {type(ex).__name__}: {ex}")

# 입력 파서 경계값: 앱(JS)과 Python 규칙이 같은지
for s, got in data["parse"]:
    want = parse(s)
    want = None if want is None else f"{want.numerator}/{want.denominator}"
    if got != want: bad += 1; print("FAIL parse", repr(s), "앱:", got, "기대:", want)

total = sum(count.values())
print(f"[{lang}] {total} cases ({', '.join(f'{k} {v}' for k, v in count.items())}), {len(data['parse'])} parse checks, seed {seed}: {'OK' if not bad else str(bad) + ' FAILED'}")
sys.exit(1 if bad else 0)
