#!/usr/bin/env python3
"""assets/app.js 계산 결과를 Python fractions로 독립 검증해요.

사용: python3 tests/check_app.py [seed]
tests/run_app.js가 무작위 행렬에 대해 계산기 코드를 실행한 결과(LaTeX)를 받아,
여기서 따로 구현한 분수 연산으로 다시 계산해 비교해요.
"""
import json, re, subprocess, sys, os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
seed = sys.argv[1] if len(sys.argv) > 1 else "20261013"
raw = subprocess.run(["node", os.path.join(HERE, "run_app.js"), seed], capture_output=True, text=True, check=True).stdout
data = json.loads(raw)

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
                if c["latex"] is not None or "비가역 행렬" not in c["chips"]: fail(c, "특이행렬인데 역행렬을 냈어요")
            else:
                inv = tex_mat(c["latex"])
                if mul(A, inv) != I(len(A)) or mul(inv, A) != I(len(A)): fail(c, "A·A⁻¹ ≠ I")
                if f"det(A) = " not in " ".join(c["chips"]): fail(c, "det 칩 없음")
        elif op == "det":
            d = det(A)
            if tex_num(c["latex"]) != d: fail(c, f"det 불일치 (정답 {d}, 결과 {c['latex']})")
            if (d == 0) != ("역행렬 없음" in c["chips"]): fail(c, "가역 여부 칩 불일치")
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
            if piv and f"피벗 열 {', '.join(str(p + 1) for p in piv)}" not in c["chips"]: fail(c, "피벗 열 칩 불일치")
        elif op == "solve":
            b = [parse(x) for x in c["inp"]["b"]]; n = len(A[0])
            rA, rAb = rank(A), rank([r + [bi] for r, bi in zip(A, b)])
            if rA != rAb:
                if "해 없음" not in c["chips"]: fail(c, "해가 없어야 해요")
            elif rA == n:
                x = tex_mat(c["latex"])
                if mul(A, x) != [[bi] for bi in b]: fail(c, "Ax ≠ b")
                if "유일한 해" not in c["chips"]: fail(c, "유일한 해 칩 없음")
            else:
                if f"자유변수 {n - rA}개" not in c["chips"] or f"rank = {rA}" not in c["chips"]: fail(c, f"자유변수/rank 칩 불일치 (정답 자유변수 {n - rA}, rank {rA})")
        if c["steps"] < 1: fail(c, "풀이 단계가 없어요")
    except Exception as ex:  # 파싱 실패 등
        fail(c, f"예외 {type(ex).__name__}: {ex}")

# 입력 파서 경계값: 앱(JS)과 Python 규칙이 같은지
for s, got in data["parse"]:
    want = parse(s)
    want = None if want is None else f"{want.numerator}/{want.denominator}"
    if got != want: bad += 1; print("FAIL parse", repr(s), "앱:", got, "기대:", want)

total = sum(count.values())
print(f"{total} cases ({', '.join(f'{k} {v}' for k, v in count.items())}), {len(data['parse'])} parse checks, seed {seed}: {'OK' if not bad else str(bad) + ' FAILED'}")
sys.exit(1 if bad else 0)
