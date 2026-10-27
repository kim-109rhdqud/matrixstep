"""English guide: diagonalization and matrix powers. Every figure is checked with assert."""
from fractions import Fraction as Fr

from guides import (M_, box, det2, gj, ident, line, matmul, mx, mx_text, op)
from guides_en import NOTES_EN
from guides_b import vec


def faq(*items):
    return ('<h2>FAQ</h2><div class="faq">'
            + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>")


def mpow(A, n):
    P = ident(len(A))
    for _ in range(n):
        P = matmul(P, A)
    return P


def inv2(A):
    d = det2(A)
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


# =====================================================================
# Diagonalization and matrix powers
# =====================================================================
def art_diag():
    A = M_([[4, 1], [2, 3]])
    lam2, lam5 = Fr(2), Fr(5)
    v2, v5 = [Fr(1), Fr(-2)], [Fr(1), Fr(1)]
    for l, v in ((lam2, v2), (lam5, v5)):
        assert [sum(A[i][j] * v[j] for j in range(2)) for i in range(2)] == [l * x for x in v]
    P = M_([[1, 1], [-2, 1]])
    D = M_([[2, 0], [0, 5]])
    Pi = inv2(P)
    assert Pi == M_([[Fr(1, 3), Fr(-1, 3)], [Fr(2, 3), Fr(1, 3)]])
    assert matmul(matmul(P, D), Pi) == A
    assert matmul(matmul(Pi, A), P) == D
    # closed form Aⁿ = 1/3 [[2ⁿ + 2·5ⁿ, −2ⁿ + 5ⁿ], [−2·2ⁿ + 2·5ⁿ, 2·2ⁿ + 5ⁿ]]
    def formula(n):
        a, b = Fr(2) ** n, Fr(5) ** n
        return [[(a + 2 * b) / 3, (-a + b) / 3], [(-2 * a + 2 * b) / 3, (2 * a + b) / 3]]
    for n in range(0, 8):
        assert formula(n) == mpow(A, n)
    A5 = mpow(A, 5)
    assert A5 == M_([[2094, 1031], [2062, 1063]])
    D5 = M_([[32, 0], [0, 3125]])
    assert mpow(D, 5) == D5
    # not diagonalizable: J = [[1,1],[0,1]]
    J = M_([[1, 1], [0, 1]])
    for n in range(0, 7):
        assert mpow(J, n) == M_([[1, n], [0, 1]])
    Jm, _, _, rk = gj(M_([[0, 1], [0, 0]]), 2, NOTES_EN)
    assert rk == 1
    # Fibonacci
    Fm = M_([[1, 1], [1, 0]])
    fib = [0, 1]
    for _ in range(12):
        fib.append(fib[-1] + fib[-2])
    for n in range(1, 12):
        assert mpow(Fm, n) == M_([[fib[n + 1], fib[n]], [fib[n], fib[n - 1]]])
    F10 = mpow(Fm, 10)
    assert F10 == M_([[89, 55], [55, 34]])

    body = f"""
<p class="lead">Nobody computes A¹⁰⁰ by multiplying a hundred times. Diagonalizing a matrix turns powers of A into powers of its diagonal entries, so you can write a closed form for Aⁿ at once. This guide follows a 2×2 example from diagonalization to the formula for Aⁿ.</p>

<h2>What is diagonalization?</h2>
<p>A square matrix A is diagonalizable when it can be written as <strong>A = PDP⁻¹</strong>, where D is a diagonal matrix and P is invertible. Rearranged, this is the same as P⁻¹AP = D.</p>
<p>The diagonal entries of D are the eigenvalues of A, and the columns of P are the corresponding eigenvectors. So the condition for diagonalization is <strong>having n linearly independent eigenvectors</strong>. Distinct eigenvalues guarantee this; a repeated eigenvalue must supply as many independent eigenvectors as its multiplicity.</p>

<h2>Example: diagonalizing a 2×2 matrix</h2>
{box(line("A ="), mx(A))}
<h3>Step 1: eigenvalues and eigenvectors</h3>
<p>The characteristic equation λ² − 7λ + 10 = (λ − 2)(λ − 5) = 0 gives the eigenvalues λ = 2 and 5. Their eigenvectors are shown below; the full working is in the <a href="/en/guide/eigenvalues-2x2/">eigenvalue guide</a>.</p>
{box(line("λ = 2:"), vec(v2), line("λ = 5:"), vec(v5))}
<h3>Step 2: build P and D</h3>
<p>Put the eigenvectors in the columns of P, and put the eigenvalues on the diagonal of D <strong>in the same order</strong>. Mismatched order gives a wrong answer.</p>
{box(line("P ="), mx(P), line("D ="), mx(D))}
<h3>Step 3: find P⁻¹</h3>
<p>Since det(P) = 1·1 − 1·(−2) = 3, the 2×2 inverse formula gives P⁻¹ directly.</p>
{box(line("P⁻¹ ="), mx(Pi))}
<h3>Check</h3>
<p>Multiply PDP⁻¹ and confirm that A comes back.</p>
{box(mx(P), op("·"), mx(D), op("·"), mx(Pi), op("="), mx(A))}

<h2>Using it for powers: Aⁿ = PDⁿP⁻¹</h2>
<p>In Aⁿ = (PDP⁻¹)(PDP⁻¹)…(PDP⁻¹), every inner P⁻¹P collapses to I, leaving Aⁿ = PDⁿP⁻¹. Raising a diagonal matrix to a power just raises each diagonal entry to that power.</p>
{box(line("Dⁿ ="), mx_text([["2ⁿ", "0"], ["0", "5ⁿ"]]))}
<p>Multiplying PDⁿP⁻¹ symbolically gives the closed form for Aⁿ.</p>
{box(line("Aⁿ = PDⁿP⁻¹ = 1/3 ·"), mx_text([["2ⁿ + 2·5ⁿ", "−2ⁿ + 5ⁿ"], ["−2·2ⁿ + 2·5ⁿ", "2·2ⁿ + 5ⁿ"]]))}
<p>With n = 1 this gives (2 + 10)/3 = 4, (−2 + 5)/3 = 1, (−4 + 10)/3 = 2 and (4 + 5)/3 = 3, which is A. Let's try n = 5.</p>
{box(line("D⁵ ="), mx(D5), line("A⁵ = PD⁵P⁻¹ ="), mx(A5))}
<p>Multiplying A by itself five times gives the same result. Enter A and n = 5 in the <a href="/en/power/">matrix power calculator</a> to see the intermediate results A², A³ and A⁴ as well.</p>

<h2>When diagonalization fails</h2>
{box(line("J ="), mx(J))}
<p>The characteristic equation is (λ − 1)² = 0, so the eigenvalue 1 is repeated (algebraic multiplicity 2). But J − I = [[0, 1], [0, 0]] has rank 1, so there is only one direction of eigenvectors (geometric multiplicity 1). With fewer than two independent eigenvectors, J cannot be diagonalized.</p>
<p>For a matrix like this, multiply directly and look for a pattern: J² = [[1, 2], [0, 1]], J³ = [[1, 3], [0, 1]], … so Jⁿ = [[1, n], [0, 1]].</p>
{box(line("J⁶ ="), mx(mpow(J, 6)))}

<h2>Fibonacci numbers and matrix powers</h2>
<p>Powers of F = [[1, 1], [1, 0]] produce the Fibonacci numbers: Fⁿ = [[Fₙ₊₁, Fₙ], [Fₙ, Fₙ₋₁]].</p>
{box(line("F¹⁰ ="), mx(F10))}
<p>You can read off F₁₀ = 55 and F₁₁ = 89. The eigenvalues of F are the irrational numbers (1 ± √5)/2, and diagonalizing gives Binet's formula Fₙ = (φⁿ − ψⁿ)/√5. The irrational arithmetic is tedious by hand, so for a specific n the power calculator gives the exact integers much faster.</p>

<h2>Common mistakes</h2>
<ul>
<li>Putting the columns of P and the diagonal of D in different orders. Each eigenvalue must sit in the same position as its eigenvector.</li>
<li>Using Pᵀ instead of P⁻¹. They are equal only when P is an orthogonal matrix.</li>
<li>Writing Aⁿ = PⁿDⁿ(P⁻¹)ⁿ. P is not raised to a power.</li>
<li>Declaring a matrix non-diagonalizable as soon as an eigenvalue repeats. It is diagonalizable if the repeated eigenvalue has enough eigenvectors; the identity matrix, for example, has the eigenvalue 1 repeated n times and is already diagonal.</li>
</ul>

{faq(("Can I diagonalize when the eigenvalues are irrational?", "Yes, but P and D then contain square roots, which makes hand calculation tedious. For 2×2 matrices the <a href='/en/eigenvalues/'>eigenvalue calculator</a> shows the exact form (a ± √b)/c."),
      ("What is diagonalization used for?", "Besides matrix powers: systems of recurrences, long-run states of Markov chains, solutions of linear differential equations, and classifying quadratic forms. All of them need Aⁿ or e^A to be easy to compute."),
      ("Is P unique?", "No. Any nonzero multiple of an eigenvector is still an eigenvector, so there are many valid choices of P. Every one of them gives the same PDP⁻¹ = A."))}
"""
    return dict(
        slug="diagonalization-matrix-power",
        title="Matrix Diagonalization and Powers Aⁿ, Step by Step (2×2 Example)",
        h1="Matrix Diagonalization and Powers Aⁿ, Step by Step",
        meta="How to diagonalize a matrix as A = PDP⁻¹ and get a closed form for Aⁿ = PDⁿP⁻¹, with a worked 2×2 example, a non-diagonalizable case and the Fibonacci matrix.",
        desc="Diagonalize A = PDP⁻¹ and turn it into a formula for Aⁿ = PDⁿP⁻¹.",
        min=8, calc=("Matrix power calculator", "/power/"), body=body,
        related=["eigenvalues-2x2", "matrix-multiplication", "special-matrices"],
    )


ARTICLES = [art_diag()]
