"""English guides 5-10 (/en/guide/). Same verified examples as guides_a.py; every figure is checked with assert."""
from fractions import Fraction as Fr

import guides as g
from guides import (M_, box, det2, gj, ident, line, matmul, minor, mx, mx_text, num, op, par, steps_html, sub)
from guides_en import NOTES_EN


def faq(*items):
    return ('<h2>FAQ</h2><div class="faq">'
            + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>")


def dot_text(A, B, i, j):
    terms = " + ".join(f"{par(A[i][k])}·{par(B[k][j])}" for k in range(len(B)))
    return f"{terms} = {num(matmul(A, B)[i][j])}"


def T(M):
    return [list(r) for r in zip(*M)]


def tr_det3(A):
    return (A[0][0] * det2(minor(A, 0, 0)) - A[0][1] * det2(minor(A, 0, 1)) + A[0][2] * det2(minor(A, 0, 2)))


# =====================================================================
# 5. Matrix multiplication
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
<p class="lead">Matrix multiplication is not entry-by-entry multiplication. You pair each row of the first matrix with each column of the second, multiply and add, which is easy to get wrong at first. This guide covers everything in order, from the size condition to worked examples.</p>

<h2>When can two matrices be multiplied?</h2>
<p>If A is an m×n matrix and B is an n×p matrix, the product AB exists and is an m×p matrix. <strong>The number of columns of A must equal the number of rows of B.</strong> A handy way to remember it: the inner numbers must match, and the outer numbers give the size of the result.</p>
{box(line("(m × n) · (n × p) = (m × p)"))}
<p>For example, a 2×3 matrix times a 3×2 matrix gives a 2×2 matrix, while a 2×3 matrix times another 2×3 matrix is not defined.</p>

<h2>How to compute each entry</h2>
<p>The entry in row i, column j of the result is the sum of the products of row i of A and column j of B, taken in order. You can think of it as the dot product of the two vectors.</p>
{box(line("(AB)ᵢⱼ = aᵢ₁b₁ⱼ + aᵢ₂b₂ⱼ + … + aᵢₙbₙⱼ"))}

<h2>Example: a 2×3 matrix times a 3×2 matrix</h2>
{box(line("A ="), mx(A), line("B ="), mx(B))}
<p>A is 2×3 and B is 3×2, so the product exists and is 2×2. Let's compute the entries one at a time.</p>
{entries}
{box(line("AB ="), mx(AB))}

<h2>Changing the order changes the result</h2>
<p>With the same two matrices, BA is a 3×3 matrix because B is 3×2 and A is 2×3. The sizes alone are different, so AB and BA cannot even be compared.</p>
{box(line("BA ="), mx(BA))}
<p>Even when both matrices are square, so that both products exist, usually AB ≠ BA.</p>
{box(mx(C), op("×"), mx(D), op("="), mx(CD), line("but"), mx(D), op("×"), mx(C), op("="), mx(DC))}
<p>Multiplying on the left and multiplying on the right are different operations. That is why, when you say "multiply A by B", it matters which side B goes on.</p>

<h2>Useful properties</h2>
<ul>
<li>Associative: (AB)C = A(BC)</li>
<li>Distributive: A(B + C) = AB + AC, (A + B)C = AC + BC</li>
<li>Scalars: (kA)B = k(AB) = A(kB)</li>
<li>Identity: AI = IA = A. The identity matrix plays the role of the number 1 in multiplication.</li>
<li>Transpose: (AB)ᵀ = BᵀAᵀ. Note that the order flips.</li>
</ul>

<h2>Where matrices behave differently from numbers</h2>
<ul>
<li><strong>No commutative law.</strong> In general AB ≠ BA.</li>
<li><strong>AB = 0 does not force A = 0 or B = 0.</strong> Neither matrix below is the zero matrix, yet their product is.</li>
</ul>
{box(mx(P), op("×"), mx(Q), op("="), mx(matmul(P, Q)))}
<ul>
<li><strong>No cancellation.</strong> AB = AC does not imply B = C. Only when A is invertible can you multiply both sides by A⁻¹ to get B = C.</li>
</ul>

<h2>Common mistakes</h2>
<ul>
<li>Multiplying entries in the same position. That is a different operation called the Hadamard product, not matrix multiplication.</li>
<li>Starting to compute without checking sizes. Before multiplying, check that the two inner numbers match.</li>
<li>Pairing rows and columns the wrong way round. Take rows from A and columns from B.</li>
<li>Writing (AB)ᵀ as AᵀBᵀ. The order flips: BᵀAᵀ is correct.</li>
</ul>

{faq(("Can AB exist while BA does not?", "Yes. If A is 2×3 and B is 3×3, then AB is a 2×3 matrix, but BA is undefined because B has 3 columns and A has 2 rows."),
     ("When multiplying several matrices, does it matter which product I compute first?", "No. Multiplication is associative, so any grouping gives the same result. What you cannot do is change the order. Starting with the pair whose sizes fit best often saves intermediate work."),
     ("What about multiplying a square matrix by itself several times?", "AA is written A². A² is defined only when A is square. Diagonal matrices are easy: just raise each diagonal entry to the power."))}
"""
    return dict(
        slug="matrix-multiplication", title="Matrix Multiplication: Rules, Worked Examples and Why AB ≠ BA",
        h1="Matrix Multiplication: Rules, Worked Examples and Why AB ≠ BA",
        meta="When two matrices can be multiplied and how to compute each entry, shown step by step with 2×3 and 3×2 examples. Why AB ≠ BA, plus common mistakes.",
        desc="The size condition, how to compute each entry, and why AB and BA differ, with worked examples.",
        min=6, calc=("Matrix multiplication calculator", "/multiplication/"), body=body,
        related=["matrix-add-subtract-scalar", "matrix-transpose-properties"],
    )


# =====================================================================
# 6. Addition, subtraction, scalar multiplication
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
<p class="lead">Matrix addition, subtraction and scalar multiplication work entry by entry, which makes them the easiest matrix operations. Even so, people lose marks on the size condition and on sign slips, so here are the rules and examples in one place.</p>

<h2>Addition and subtraction</h2>
<p>Two matrices can be added or subtracted <strong>only when they have the same size</strong>. The entry in row i, column j of the result is the sum or difference of the entries in row i, column j of the two matrices.</p>
{box(line("(A ± B)ᵢⱼ = aᵢⱼ ± bᵢⱼ"))}
<p>Let's work through two 2×2 matrices.</p>
{box(line("A ="), mx(A), line("B ="), mx(B))}
<h3>A + B</h3>
{cells(S, "+")}
{box(line("A + B ="), mx(S))}
<h3>A − B</h3>
{cells(Df, "−")}
{box(line("A − B ="), mx(Df))}
<p>Matrices of different sizes have entries with no partner, so addition and subtraction are not defined. You cannot add a 2×3 matrix to a 2×2 matrix.</p>

<h2>Scalar multiplication</h2>
<p>Multiplying a matrix by a number k multiplies every entry by k. The whole matrix is scaled, not just the first entry.</p>
{box(line("3A ="), mx(K))}

<h2>Combining the operations</h2>
<p>When scalar multiplication and subtraction appear together, as in 2A − B, do the scalar multiplication first and then subtract entry by entry.</p>
{box(line("2A ="), mx([[2 * A[i][j] for j in range(2)] for i in range(2)]), line("2A − B ="), mx(L))}

<h2>Properties</h2>
<ul>
<li>Commutative: A + B = B + A</li>
<li>Associative: (A + B) + C = A + (B + C)</li>
<li>Zero matrix: A + O = A, A − A = O</li>
<li>Distributive: k(A + B) = kA + kB, (k + l)A = kA + lA</li>
<li>Scalars combine: k(lA) = (kl)A</li>
</ul>
<p>Unlike multiplication, addition is commutative. In the example above, computing B + A gives the same matrix as A + B.</p>

<h2>Common mistakes</h2>
<ul>
<li>Trying to add matrices of different sizes. Check the sizes first.</li>
<li>Sign errors when subtracting negative entries. Use parentheses, as in 5 − (−2) = 7.</li>
<li>Applying the scalar to only one row or only the first entry. Multiply every entry.</li>
<li>Treating −A as "flip one sign". Every entry changes sign.</li>
</ul>

{faq(("Can I add a number to a matrix?", "Adding a number to a matrix is not defined. If you mean something like A + 3, write it as adding 3I (three times the identity matrix)."),
     ("What is the zero matrix?", "A matrix whose entries are all 0. It behaves like the number 0 in addition, so A + O = A."),
     ("Do the same rules apply with decimals or fractions?", "Yes. Add fractions with a common denominator and line up decimal places. The calculator works with exact fractions."))}
"""
    return dict(
        slug="matrix-add-subtract-scalar", title="Matrix Addition, Subtraction and Scalar Multiplication: Rules and Examples",
        h1="Matrix Addition, Subtraction and Scalar Multiplication: Rules and Examples",
        meta="Why matrices must be the same size to add or subtract, how scalar multiplication works, and mixed expressions like 2A − B, with examples and common mistakes.",
        desc="The size condition, entry-by-entry computation, scalar multiplication and mixed expressions, with examples.",
        min=5, calc=("Matrix addition calculator", "/addition/"), body=body,
        related=["matrix-multiplication", "matrix-transpose-properties"],
    )


# =====================================================================
# 7. Transpose
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
<p class="lead">The transpose of a matrix swaps its rows and columns. The idea is simple, but it comes with a cluster of exam favorites: the transpose of a product, symmetric matrices and skew-symmetric matrices. This guide collects them in one place.</p>

<h2>Definition of the transpose</h2>
<p>The transpose Aᵀ of an m×n matrix A is an n×m matrix. The entry in row i, column j of A becomes the entry in row j, column i of Aᵀ.</p>
{box(line("(Aᵀ)ⱼᵢ = aᵢⱼ"))}
<p>Transposing a 2×3 matrix gives a 3×2 matrix. Picture the first row tipping over to become the first column.</p>
{box(line("A ="), mx(A), op("→"), line("Aᵀ ="), mx(At))}
<p>Transposing twice brings you back to where you started: (Aᵀ)ᵀ = A.</p>

<h2>Basic properties</h2>
<ul>
<li>(A + B)ᵀ = Aᵀ + Bᵀ</li>
<li>(kA)ᵀ = kAᵀ</li>
<li>(AB)ᵀ = BᵀAᵀ <strong>(the order flips)</strong></li>
<li>(A⁻¹)ᵀ = (Aᵀ)⁻¹</li>
<li>det(Aᵀ) = det(A)</li>
<li>rank(Aᵀ) = rank(A)</li>
</ul>

<h2>Transpose of a product: (AB)ᵀ = BᵀAᵀ</h2>
<p>This is the property people get wrong most often. Let's check it by multiplying two matrices directly.</p>
{box(line("C ="), mx(C), line("D ="), mx(D))}
{box(line("(CD)ᵀ ="), mx(lhs))}
{box(line("DᵀCᵀ ="), mx(T(D)), op("×"), mx(T(C)), op("="), mx(rhs))}
<p>The two results agree. By contrast, keeping the original order, CᵀDᵀ, gives a different matrix.</p>
{box(line("CᵀDᵀ ="), mx(wrong))}
<p>The sizes explain why. If A is m×n and B is n×p, then AB is m×p and (AB)ᵀ is p×m. BᵀAᵀ is (p×n)·(n×m) = p×m, so the sizes fit, but AᵀBᵀ is (n×m)·(p×n), which cannot even be multiplied when m ≠ p.</p>

<h2>Symmetric and skew-symmetric matrices</h2>
<p>A matrix that is unchanged by transposing is called a <strong>symmetric matrix</strong>. It satisfies Aᵀ = A, so the entries mirror each other across the main diagonal.</p>
{box(line("S ="), mx(S), line("Sᵀ = S"))}
<p>A matrix whose transpose flips the sign, Aᵀ = −A, is a <strong>skew-symmetric matrix</strong>. Each diagonal entry must equal its own negative, so the diagonal is all zeros.</p>
{box(line("K ="), mx(K), line("Kᵀ = −K"))}

<h2>Making any square matrix symmetric</h2>
<p>For any square matrix N, the matrix N + Nᵀ is always symmetric.</p>
{box(line("N ="), mx(N), line("N + Nᵀ ="), mx(Sym))}
<p>N − Nᵀ is skew-symmetric. So every square matrix can be written as the sum of a symmetric and a skew-symmetric matrix: N = (N + Nᵀ)/2 + (N − Nᵀ)/2.</p>

<h2>Common mistakes</h2>
<ul>
<li>Writing (AB)ᵀ as AᵀBᵀ. The order flips: BᵀAᵀ is correct.</li>
<li>Getting the size wrong after transposing a rectangular matrix. The transpose of a 2×3 matrix is 3×2.</li>
<li>Forgetting that a symmetric matrix must be square. A rectangular matrix can never satisfy Aᵀ = A.</li>
<li>Putting nonzero entries on the diagonal of a skew-symmetric matrix.</li>
</ul>

{faq(("Are the transpose and the inverse the same thing?", "No. The transpose exists for every matrix and just swaps rows and columns. The inverse is the matrix that multiplies to give the identity, and only invertible matrices have one. The two coincide only for orthogonal matrices."),
     ("Why doesn't transposing change the determinant?", "Because the determinant has the same value whether you expand along rows or along columns. That is also why every row property of determinants holds for columns too."),
     ("What is the transpose of a vector?", "Transposing a column vector gives a row vector. That is why the dot product of two column vectors u and v is written uᵀv."))}
"""
    return dict(
        slug="matrix-transpose-properties", title="Transpose of a Matrix: Properties, (AB)ᵀ = BᵀAᵀ and Symmetric Matrices",
        h1="Transpose of a Matrix: Properties, (AB)ᵀ = BᵀAᵀ and Symmetric Matrices",
        meta="Definition and basic properties of the transpose, a worked check of why (AB)ᵀ = BᵀAᵀ, and the ideas of symmetric and skew-symmetric matrices.",
        desc="The definition of the transpose, the transpose of a product, and symmetric and skew-symmetric matrices, with examples.",
        min=6, calc=("Transpose calculator", "/transpose/"), body=body,
        related=["matrix-multiplication", "special-matrices"],
    )


# =====================================================================
# 8. Cramer's rule
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
<p class="lead">Cramer's rule writes down the solution of a linear system using nothing but determinants. For two or three equations it is quick and tidy, which is why it shows up so often on exams. This guide shows how the formula is used and when it cannot be used.</p>

<h2>What is Cramer's rule?</h2>
<p>For a system Ax = b with as many equations as unknowns, if the determinant det(A) of the coefficient matrix is nonzero, the solution is given by</p>
{box(line("xⱼ = det(Aⱼ) / det(A)"))}
<p>where Aⱼ is the matrix A with its j-th column replaced by b. In other words, you compute one extra determinant per variable.</p>

<h2>Example 1: a 2×2 system</h2>
{box(line("3x + 2y = 7"))}
{box(line("x − y = 4"))}
<p>First find the determinant of the coefficient matrix. If it is 0, Cramer's rule cannot be used.</p>
{box(mx(A2), line(f"det(A) = 3·(−1) − 2·1 = {num(d2)}"))}
<p>For x, replace the first column by b; for y, replace the second column.</p>
{box(line("A₁ (column 1 replaced by b) ="), mx(parts2[0][0]), line(f"det = 7·(−1) − 2·4 = {num(parts2[0][1])}"))}
{box(line("A₂ (column 2 replaced by b) ="), mx(parts2[1][0]), line(f"det = 3·4 − 7·1 = {num(parts2[1][1])}"))}
{box(line(f"x = {num(parts2[0][1])} / ({num(d2)}) = {num(x2[0])}"), line(f"y = {num(parts2[1][1])} / ({num(d2)}) = {num(x2[1])}"))}
<p>Check by substituting: 3·3 + 2·(−1) = 7 and 3 − (−1) = 4, so both equations hold.</p>

<h2>Example 2: a 3×3 system</h2>
{box(line("2x + y − z = 8"))}
{box(line("−3x − y + 2z = −11"))}
{box(line("−2x + y + 2z = −3"))}
<p>The determinant of the coefficient matrix is {num(d3)}. It is nonzero, so the system has exactly one solution. The determinants of the matrices with each column replaced by b are shown below.</p>
{dets3}
{box(line(f"x = {num(parts3[0][1])} / ({num(d3)}) = {num(x3[0])}"), line(f"y = {num(parts3[1][1])} / ({num(d3)}) = {num(x3[1])}"), line(f"z = {num(parts3[2][1])} / ({num(d3)}) = {num(x3[2])}"))}
<p>The solution is (x, y, z) = (2, 3, −1). Solving the same system by <a href="/en/guide/linear-system-solutions/">Gauss-Jordan elimination</a> gives the same answer.</p>

<h2>When Cramer's rule cannot be used</h2>
<ul>
<li><strong>When det(A) = 0</strong>: you cannot divide by zero. The system then has either no solution or infinitely many, and Cramer's rule cannot tell you which; you need elimination for that.</li>
<li><strong>When the number of equations differs from the number of unknowns</strong>: the coefficient matrix is not square, so it has no determinant.</li>
</ul>

<h2>Why Cramer's rule is rarely used in practice</h2>
<p>Solving for n variables requires n + 1 determinants of n×n matrices. Determinants are already expensive, so the work grows quickly as n increases. On exams it is best kept to two or three variables; beyond that, elimination is far faster. If you only need a single variable, however, Cramer's rule can be the better choice.</p>

<h2>Common mistakes</h2>
<ul>
<li>Replacing the wrong column with b. x uses column 1, y column 2, z column 3.</li>
<li>Dividing without first checking whether det(A) is 0.</li>
<li>Sign errors in the determinants. In a 3×3 expansion, double-check the + − + pattern.</li>
<li>Replacing a row instead of a column with b. It is the column that gets replaced.</li>
</ul>

{faq(("Does det(A) = 0 mean there is no solution?", "No. There may be no solution or infinitely many. You have to row-reduce the augmented matrix with elimination to decide which."),
     ("Can Cramer's rule be used to find an inverse?", "The inverse formula using the adjugate rests on the same principle as Cramer's rule. It is covered in <a href='/en/guide/inverse-adjugate-cofactor/'>Inverse by cofactors and the adjugate</a>."),
     ("Can I check this with the calculator?", "Yes. Enter the coefficients and constants in the linear system solver and you will get the same solution."))}
"""
    return dict(
        slug="cramer-rule", title="Cramer's Rule: Solving Linear Systems with Determinants (2×2 and 3×3 Examples)",
        h1="Cramer's Rule: Solving Linear Systems with Determinants (2×2 and 3×3 Examples)",
        meta="Cramer's rule xⱼ = det(Aⱼ)/det(A) explained with worked 2×2 and 3×3 systems, when it cannot be used, and why elimination is usually faster.",
        desc="Cramer's rule for solving systems with determinants, with worked examples and pitfalls.",
        min=7, calc=("Linear system solver", "/linear-system/"), body=body,
        related=["determinant-3x3", "linear-system-solutions"],
    )


# =====================================================================
# 9. Inverse by cofactors and the adjugate
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
<p class="lead">Elimination is not the only way to find an inverse. There is also the adjugate formula, built from the determinant and the cofactors. For 2×2 matrices it is the fastest method, and for 3×3 it is a regular exam question.</p>

<h2>The adjugate and the inverse formula</h2>
<p>For a square matrix A, the <strong>cofactor</strong> Cᵢⱼ in row i, column j is the determinant of the minor obtained by deleting row i and column j, multiplied by (−1)^(i+j). The matrix of all the cofactors is the cofactor matrix, and its transpose is the <strong>adjugate</strong> adj(A).</p>
{box(line("A⁻¹ = (1 / det(A)) · adj(A)"), line("adj(A) = (cofactor matrix)ᵀ"))}
<p>If det(A) = 0, then 1/det(A) does not exist, so there is no inverse.</p>

<h2>For 2×2, one formula does it all</h2>
<p>If A = [[a, b], [c, d]], the cofactor matrix is [[d, −c], [−b, a]], and transposing gives the adjugate [[d, −b], [−c, a]]. Swap the diagonal entries and change the sign of the other two.</p>
{box(line("A ="), mx(A), line(f"det(A) = 1·4 − 2·3 = {num(dA)}"))}
{box(line("adj(A) ="), mx(adj2), line("A⁻¹ = −½ ·"), mx(adj2), line("="), mx(inv2))}
<p>To check, confirm that AA⁻¹ = I.</p>
{box(mx(A), op("×"), mx(inv2), op("="), mx(matmul(A, inv2)))}

<h2>Example: a 3×3 matrix</h2>
{box(line("B ="), mx(B))}
<p>First find the determinant. Expanding along row 1: 2·(3·2 − 1·1) − 1·(1·2 − 1·0) + 0 = 10 − 2 = {num(dB)}. It is nonzero, so the inverse exists.</p>
<p>Now compute the nine cofactors. For each position, take the determinant of the 2×2 minor left after deleting that row and column, and attach the sign from the pattern (+ − + / − + − / + − +).</p>
{cofs}
<p>Here is the cofactor matrix and its transpose, the adjugate. This particular matrix is symmetric, so transposing leaves it unchanged.</p>
{box(line("C ="), mx(CB), line("adj(B) = Cᵀ ="), mx(adjB))}
<p>Finally, multiply the adjugate by 1/det(B) = 1/{num(dB)}.</p>
{box(line("B⁻¹ ="), mx(invB))}
{box(mx(B), op("×"), mx(invB), op("="), mx(matmul(B, invB)))}

<h2>Adjugate or elimination: which is better?</h2>
<ul>
<li>2×2: the formula wins by a wide margin.</li>
<li>3×3: nine cofactors make it long. To reduce arithmetic slips, <a href="/en/guide/inverse-gauss-jordan/">Gauss-Jordan elimination</a> is more reliable, although some exams ask for the formula method for partial credit.</li>
<li>4×4 and larger: elimination is practically essential.</li>
</ul>

<h2>Common mistakes</h2>
<ul>
<li>Using the cofactor matrix without transposing it. You must use the transposed matrix, the adjugate.</li>
<li>Dropping the (−1)^(i+j) sign. Apply it like a checkerboard: + − + / − + − / + − +.</li>
<li>Forgetting to multiply by 1/det(A). The adjugate is not the inverse.</li>
<li>Carrying on when det(A) = 0. Check the determinant first.</li>
</ul>

{faq(("What else is the adjugate called?", "It is also known as the classical adjoint. Textbooks write it adj(A)."),
     ("What is A·adj(A)?", "A·adj(A) = det(A)·I. Dividing this identity by det(A) gives the inverse formula."),
     ("Is the inverse of an integer matrix always an integer matrix?", "No. That is guaranteed only when det(A) is 1 or −1. When the determinant is 8, as in the example above, fractions appear."))}
"""
    return dict(
        slug="inverse-adjugate-cofactor", title="Inverse of a Matrix by Cofactors and the Adjugate (2×2 and 3×3)",
        h1="Inverse of a Matrix by Cofactors and the Adjugate (2×2 and 3×3)",
        meta="The formula A⁻¹ = adj(A)/det(A) with the 2×2 shortcut and a full 3×3 cofactor example: build the cofactor matrix, transpose to the adjugate, avoid mistakes.",
        desc="The cofactor matrix, the adjugate and the inverse formula, with 2×2 and 3×3 examples.",
        min=8, calc=("Inverse calculator", "/inverse/"), body=body,
        related=["inverse-gauss-jordan", "determinant-properties"],
    )


# =====================================================================
# 10. Properties of the determinant
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
<p class="lead">Computing a determinant straight from the definition gets long fast. That is why exam problems usually expect you to simplify the rows using the properties first. This guide checks each of the commonly used properties with an example.</p>

<h2>How row operations affect the determinant</h2>
<p>The three row operations used in elimination each change the determinant in a different way. Knowing just these three settles most problems.</p>
<div class="tbl"><table class="gtable">
<thead><tr><th>Row operation</th><th>Effect on the determinant</th></tr></thead>
<tbody>
<tr><td>Swap two rows</td><td>The sign flips (multiplied by −1)</td></tr>
<tr><td>Multiply a row by k</td><td>Multiplied by k</td></tr>
<tr><td>Add a multiple of one row to another</td><td>Unchanged</td></tr>
</tbody></table></div>
<p>Let's verify all three with a 2×2 matrix. The starting point is det(A) = 1·4 − 2·3 = {num(dA)}.</p>
{box(line("A ="), mx(A))}
{box(line("R₁ ↔ R₂"), op("→"), mx(sw), line(f"det = {num(det2(sw))}"))}
{box(line("R₁ ← 3R₁"), op("→"), mx(sc), line(f"det = {num(det2(sc))} = 3 × ({num(dA)})"))}
{box(line("R₂ ← R₂ − 3R₁"), op("→"), mx(ad), line(f"det = {num(det2(ad))}"))}
<p>The first flipped the sign, the second tripled the value, and the third left it unchanged. That third property is what lets you row-reduce to a triangular matrix without losing the determinant.</p>

<h2>Determinant of a triangular matrix</h2>
<p>The determinant of an upper or lower triangular matrix is the product of its diagonal entries.</p>
{box(mx(Tri), line("det = 2·3·4 = 24"))}
<p>So computing a determinant boils down to "row-reduce to a triangular matrix, then multiply the diagonal". Just remember to fix the sign once for every row swap you made.</p>

<h2>When the determinant is zero</h2>
<ul>
<li>Two rows (or two columns) are equal.</li>
<li>One row is a multiple of another.</li>
<li>There is a row (or column) of all zeros.</li>
</ul>
<p>In short, if the rows are not linearly independent, the determinant is 0. Both matrices below have determinant 0.</p>
{box(mx(Dup), line("row 1 = row 3"), mx(Pm), line("row 2 = 2 × row 1"))}

<h2>Products, transposes and scalar multiples</h2>
<ul>
<li>det(AB) = det(A)·det(B)</li>
<li>det(Aᵀ) = det(A)</li>
<li>det(A⁻¹) = 1/det(A)</li>
<li>For an n×n matrix, det(kA) = kⁿ·det(A)</li>
</ul>
<p>Let's check the product rule. Here det(B) = −1 and det(A) = −2.</p>
{box(mx(A), op("×"), mx(Bm), op("="), mx(matmul(A, Bm)), line(f"det = {num(det2(matmul(A, Bm)))} = ({num(dA)})·({num(det2(Bm))})"))}
<p>det(kA) = kⁿ·det(A) is a particularly common slip. Multiplying the whole matrix by k multiplies each of the n rows by k, so k appears n times. Doubling the 3×3 matrix with det = 24 from earlier gives a determinant of 2³·24 = 192, not 2·24.</p>
<p>Also, det(A + B) is not equal to det(A) + det(B). There is a rule for products but none for sums.</p>

<h2>Using the properties in a calculation</h2>
<p>If A is a 2×2 matrix with det(A) = −2, then det(3A²) = 3²·det(A)² = 9·4 = 36. You never need to compute 3A² itself.</p>

<h2>Common mistakes</h2>
<ul>
<li>Writing det(A + B) = det(A) + det(B). It is false.</li>
<li>Writing det(kA) = k·det(A). For a square matrix of size n it is kⁿ.</li>
<li>Losing count of row swaps and getting the sign wrong.</li>
<li>Multiplying a row by k and forgetting to compensate the determinant by a factor of k.</li>
</ul>

{faq(("What does a zero determinant mean?", "The matrix has no inverse, and its rows (or columns) are not linearly independent. Geometrically, area or volume is squashed down to zero."),
     ("Do column operations have the same properties?", "Yes. Since det(Aᵀ) = det(A), every property for rows holds for columns too."),
     ("Can a determinant be negative?", "Yes. The sign tells you whether orientation is reversed, and the magnitude is the scaling factor for area or volume."))}
"""
    return dict(
        slug="determinant-properties", title="Properties of Determinants: Row Operations, Products and det(kA)",
        h1="Properties of Determinants: Row Operations, Products and det(kA)",
        meta="How row swaps, scaling and row addition change the determinant, plus det(AB), det(Aᵀ) and det(kA) = kⁿdet(A), each verified with a worked example.",
        desc="How each row operation changes the determinant, plus the product, transpose and scalar rules, with examples.",
        min=7, calc=("Determinant calculator", "/determinant/"), body=body,
        related=["determinant-3x3", "inverse-adjugate-cofactor"],
    )


ARTICLES = [art_mul(), art_add(), art_transpose(), art_cramer(), art_adj(), art_detprop()]
