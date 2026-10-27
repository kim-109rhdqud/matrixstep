"""English guides 11-15 (/en/guide/). Every example value is checked with assert."""
from fractions import Fraction as Fr

from guides import (M_, box, det2, gj, ident, line, matmul, mx, num, op, par, steps_html, sub)
from guides_a import T, tr_det3
from guides_en import NOTES_EN


def faq(*items):
    return ('<h2>FAQ</h2><div class="faq">'
            + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>")


def vec(v):
    return mx([[x] for x in v])


# =====================================================================
# 11. Special matrices
# =====================================================================
def art_special():
    I3 = ident(3)
    Dg = M_([[2, 0, 0], [0, -1, 0], [0, 0, 3]])
    Dg2 = matmul(Dg, Dg)
    assert Dg2 == M_([[4, 0, 0], [0, 1, 0], [0, 0, 9]])
    assert tr_det3(Dg) == -6
    U = M_([[1, 2, 3], [0, 4, 5], [0, 0, 6]])
    assert tr_det3(U) == 24
    S = M_([[1, 2], [2, 5]])
    assert T(S) == S
    Q = M_([[0, -1], [1, 0]])
    assert matmul(T(Q), Q) == ident(2) and det2(Q) == 1
    Rf = M_([[1, 0], [0, -1]])
    assert matmul(T(Rf), Rf) == ident(2) and det2(Rf) == -1
    P = M_([[1, 0], [0, 0]])
    assert matmul(P, P) == P
    Nl = M_([[0, 1], [0, 0]])
    assert matmul(Nl, Nl) == M_([[0, 0], [0, 0]])
    Iv = M_([[1, 0], [0, -1]])
    assert matmul(Iv, Iv) == ident(2)

    body = f"""
<p class="lead">Some matrices have names because of their shape or their properties. Knowing the names and what they imply makes calculations much faster, and when a problem says "A is symmetric" or "Q is orthogonal" you will immediately know what you can use.</p>

<h2>The zero matrix and the identity matrix</h2>
<p>The <strong>zero matrix</strong> O has every entry equal to 0. It behaves like the number 0 under addition: A + O = A.</p>
<p>The <strong>identity matrix</strong> I is the square matrix with 1s on the diagonal and 0s everywhere else. It behaves like the number 1 under multiplication: AI = IA = A.</p>
{box(line("I₃ ="), mx(I3))}

<h2>Diagonal matrices</h2>
<p>A square matrix whose entries off the diagonal are all 0. These are the easiest matrices to work with, so much so that there is a whole technique (diagonalization) for turning other matrices into diagonal ones.</p>
{box(line("D ="), mx(Dg))}
<ul>
<li>The determinant is the product of the diagonal entries. Here it is 2·(−1)·3 = −6.</li>
<li>To take a power, raise each diagonal entry to that power.</li>
<li>The inverse replaces each diagonal entry by its reciprocal (as long as no diagonal entry is 0).</li>
</ul>
{box(line("D² ="), mx(Dg2))}

<h2>Triangular matrices</h2>
<p>If everything below the diagonal is 0, the matrix is <strong>upper triangular</strong>; if everything above the diagonal is 0, it is <strong>lower triangular</strong>. Elimination produces exactly an upper triangular matrix.</p>
{box(line("U ="), mx(U), line("det(U) = 1·4·6 = 24"))}
<p>The determinant of a triangular matrix is also the product of its diagonal entries. The product of two triangular matrices of the same kind is again triangular of that kind.</p>

<h2>Symmetric and skew-symmetric matrices</h2>
<p>If Aᵀ = A, the matrix is <strong>symmetric</strong>: the entries mirror each other across the diagonal.</p>
{box(line("S ="), mx(S))}
<p>If Aᵀ = −A, the matrix is <strong>skew-symmetric</strong>, and its diagonal entries are all 0. See the <a href="/en/guide/matrix-transpose-properties/">transpose guide</a> for more properties.</p>

<h2>Orthogonal matrices</h2>
<p>A square matrix with QᵀQ = I. This means the columns are mutually perpendicular and each has length 1. The inverse is simply the transpose, Q⁻¹ = Qᵀ, and the determinant is 1 or −1.</p>
{box(line("Rotation Q ="), mx(Q), line("QᵀQ ="), mx(matmul(T(Q), Q)), line("det = 1"))}
{box(line("Reflection R ="), mx(Rf), line("RᵀR ="), mx(matmul(T(Rf), Rf)), line("det = −1"))}
<p>Orthogonal matrices preserve lengths and angles, so they represent transformations such as rotations and reflections.</p>

<h2>Idempotent, nilpotent and involutory matrices</h2>
<ul>
<li><strong>Idempotent</strong>: A² = A. The matrix below is the projection that keeps only the first component.</li>
<li><strong>Nilpotent</strong>: some power of the matrix is the zero matrix.</li>
<li><strong>Involutory</strong>: A² = I. The matrix is its own inverse.</li>
</ul>
{box(line("Idempotent"), mx(P), op("×"), mx(P), op("="), mx(matmul(P, P)))}
{box(line("Nilpotent"), mx(Nl), op("×"), mx(Nl), op("="), mx(matmul(Nl, Nl)))}
{box(line("Involutory"), mx(Iv), op("×"), mx(Iv), op("="), mx(matmul(Iv, Iv)))}

<h2>Summary table</h2>
<div class="tbl"><table class="gtable">
<thead><tr><th>Name</th><th>Condition</th><th>Why it matters</th></tr></thead>
<tbody>
<tr><td>Symmetric</td><td>Aᵀ = A</td><td>Real eigenvalues, easy to diagonalize</td></tr>
<tr><td>Skew-symmetric</td><td>Aᵀ = −A</td><td>All diagonal entries are 0</td></tr>
<tr><td>Orthogonal</td><td>QᵀQ = I</td><td>Inverse is the transpose, preserves length</td></tr>
<tr><td>Diagonal</td><td>Off-diagonal entries are 0</td><td>Powers and inverses are easy</td></tr>
<tr><td>Triangular</td><td>One side of the diagonal is all 0</td><td>Determinant is the product of the diagonal</td></tr>
<tr><td>Idempotent</td><td>A² = A</td><td>Projections</td></tr>
</tbody></table></div>

<h2>Common mistakes</h2>
<ul>
<li>Thinking "orthogonal" means "entries are 0 or 1". The condition is that the columns are perpendicular and have length 1.</li>
<li>Forgetting the case of a 0 on the diagonal when inverting a diagonal matrix. If any diagonal entry is 0, there is no inverse.</li>
<li>Multiplying every entry of a triangular matrix to get the determinant. Only the diagonal entries are multiplied.</li>
</ul>

{faq(("Is the identity matrix a diagonal matrix?", "Yes, it is the diagonal matrix whose diagonal entries are all 1. It is also symmetric and orthogonal."),
     ("Is the determinant of an orthogonal matrix always 1?", "No. It is 1 or −1. Rotations have determinant 1 and reflections have determinant −1."),
     ("Is the product of two symmetric matrices symmetric?", "Not always. For symmetric matrices A and B, the product AB is symmetric only when AB = BA."))}
"""
    return dict(
        slug="special-matrices", title="Special Matrices: Identity, Diagonal, Triangular, Symmetric and Orthogonal",
        h1="Special Matrices: Identity, Diagonal, Triangular, Symmetric and Orthogonal",
        meta="Definitions and properties of identity, diagonal, triangular, symmetric, orthogonal and idempotent matrices, with examples and a summary table for exam review.",
        desc="Definitions and properties of the named matrices, with examples and a summary table.",
        min=7, calc=("Transpose calculator", "/transpose/"), body=body,
        related=["matrix-transpose-properties", "determinant-properties"],
    )


# =====================================================================
# 12. Null space and column space
# =====================================================================
def art_spaces():
    A = M_([[1, 2, 0, -1], [2, 4, 1, 1], [3, 6, 1, 0]])
    Mf, st, piv, rk = gj(A, 4, NOTES_EN)
    assert Mf == M_([[1, 2, 0, -1], [0, 0, 1, 3], [0, 0, 0, 0]]) and piv == [0, 2] and rk == 2
    v1, v2 = [Fr(-2), Fr(1), Fr(0), Fr(0)], [Fr(1), Fr(0), Fr(-3), Fr(1)]
    for v in (v1, v2):
        assert all(sum(A[i][j] * v[j] for j in range(4)) == 0 for i in range(3))
    col1, col3 = [A[i][0] for i in range(3)], [A[i][2] for i in range(3)]
    assert col1 == [1, 2, 3] and col3 == [0, 1, 1]
    assert 4 - rk == 2
    ex = steps_html("Start from the given matrix.", A, st)

    body = f"""
<p class="lead">The null space and the column space are two of the most important spaces attached to a matrix. For both, one RREF is enough to read off a basis. Let's find a basis and the dimension of each space for a single matrix.</p>

<h2>Definitions</h2>
<ul>
<li><strong>Null space N(A)</strong>: the set of all vectors x with Ax = 0. It always contains the zero vector.</li>
<li><strong>Column space C(A)</strong>: the set of all vectors that can be written as linear combinations of the columns of A. Equivalently, it is the set of all b for which Ax = b has a solution.</li>
</ul>

<h2>Example matrix</h2>
{box(line("A ="), mx(A))}
<p>This is a 3×4 matrix. First we compute its RREF.</p>
{ex}
{box(line("RREF(A) ="), mx(Mf))}
<p>The pivots are in columns 1 and 3, so rank(A) = 2. Columns 2 and 4 have no pivot, so there are two free variables.</p>

<h2>Finding a basis for the null space</h2>
<p>Read the equations from the RREF: x₁ + 2x₂ − x₄ = 0 and x₃ + 3x₄ = 0. Setting the free variables x₂ = s and x₄ = t gives the following.</p>
{box(line("x₁ = −2s + t"), line("x₂ = s"), line("x₃ = −3t"), line("x₄ = t"))}
<p>Collecting the s terms and the t terms into vectors, every solution is a linear combination of two vectors.</p>
{box(line("x = s"), vec(v1), line("+ t"), vec(v2))}
<p>So these two vectors form a basis for the null space. Multiply each by A to check that the result is the zero vector.</p>
{box(mx(A), op("×"), vec(v1), op("="), vec([sum(A[i][j] * v1[j] for j in range(4)) for i in range(3)]), mx(A), op("×"), vec(v2), op("="), vec([sum(A[i][j] * v2[j] for j in range(4)) for i in range(3)]))}

<h2>Finding a basis for the column space</h2>
<p>The pivot columns of the RREF are columns 1 and 3. A basis for the column space is <strong>columns 1 and 3 of the original matrix A</strong>, not the columns of the RREF. This matters because row operations change the column space.</p>
{box(line("Basis:"), vec(col1), vec(col3))}
<p>The remaining columns 2 and 4 are linear combinations of these two. For example, column 2 is twice column 1.</p>

<h2>The relationship between the dimensions</h2>
<p>There are 4 columns and the rank is 2, so the dimension of the null space (the nullity) is 4 − 2 = 2, which matches the number of basis vectors we just found. This relationship is the <strong>rank-nullity theorem</strong>.</p>
{box(line("rank(A) + nullity(A) = number of columns"), line("2 + 2 = 4"))}

<h2>Common mistakes</h2>
<ul>
<li>Using the columns of the RREF as a basis for the column space. You must use the columns of the original A.</li>
<li>Choosing a non-free variable as a parameter for the null space. The free variables are the ones in columns without a pivot.</li>
<li>Missing the case where the null space basis is empty. With no free variables, the null space is just the zero vector.</li>
<li>Mixing up the row space and the column space. A basis for the row space is the set of nonzero rows of the RREF.</li>
</ul>

{faq(("Do the null space and the column space live in the same space?", "No. For an m×n matrix, the column space is a subspace of ℝᵐ and the null space is a subspace of ℝⁿ."),
     ("How do I find a basis for the row space?", "The nonzero rows of the RREF form a basis for the row space. Row operations do not change the row space, so the rows of the RREF can be used directly."),
     ("What does it mean if the null space has dimension 0?", "It means the only solution of Ax = 0 is the zero vector. Equivalently, every column has a pivot, and the columns are linearly independent."))}
"""
    return dict(
        slug="null-space-column-space", title="How to Find a Basis for the Null Space and Column Space (RREF Example)",
        h1="How to Find a Basis for the Null Space and Column Space (RREF Example)",
        meta="Find bases and dimensions of the null space and column space from a single RREF, worked on a 3×4 matrix. Includes the rank-nullity theorem and common mistakes.",
        desc="How to read bases for the null space and column space off the RREF, with a worked example.",
        min=8, calc=("RREF calculator", "/rref/"), body=body,
        related=["rank-and-rref", "linear-independence"],
    )


# =====================================================================
# 13. Linear independence
# =====================================================================
def art_indep():
    v1, v2, v3 = [1, 2, 3], [2, 1, 0], [1, -1, -3]
    Ad = M_([[v1[i], v2[i], v3[i]] for i in range(3)])
    Mf, st, piv, rk = gj(Ad, 3, NOTES_EN)
    assert rk == 2 and tr_det3(Ad) == 0
    assert [v1[i] - v2[i] + v3[i] for i in range(3)] == [0, 0, 0]
    ex_dep = steps_html("The matrix whose columns are the three vectors.", Ad, st)
    w1, w2, w3 = [1, 0, 1], [0, 1, 1], [1, 1, 0]
    Ai = M_([[w1[i], w2[i], w3[i]] for i in range(3)])
    assert tr_det3(Ai) == -2
    Mi, sti, _, ri = gj(Ai, 3, NOTES_EN)
    assert ri == 3 and Mi == ident(3)

    body = f"""
<p class="lead">Deciding whether a set of vectors is linearly independent is one of the most common problems in linear algebra. There is really only one method: put the vectors in the columns of a matrix and look at its rank. Let's compare an independent example and a dependent one.</p>

<h2>Definition of linear independence</h2>
<p>Vectors v₁, v₂, …, vₖ are <strong>linearly independent</strong> if the only coefficients satisfying c₁v₁ + c₂v₂ + … + cₖvₖ = 0 are c₁ = c₂ = … = cₖ = 0. If the zero vector can be produced with coefficients that are not all zero, the vectors are <strong>linearly dependent</strong>. When they are dependent, at least one vector can be written as a linear combination of the others.</p>

<h2>Testing with a matrix</h2>
<p>If we form the matrix A = [v₁ v₂ … vₖ] with the vectors as columns, the equation above becomes Ax = 0. Therefore <strong>linearly independent ⟺ Ax = 0 has only the solution x = 0 ⟺ rank(A) = number of vectors</strong>.</p>
<div class="tbl"><table class="gtable">
<thead><tr><th>Situation</th><th>Conclusion</th></tr></thead>
<tbody>
<tr><td>rank(A) = number of vectors</td><td>Linearly independent</td></tr>
<tr><td>rank(A) &lt; number of vectors</td><td>Linearly dependent</td></tr>
<tr><td>A is square and det(A) ≠ 0</td><td>Linearly independent</td></tr>
<tr><td>Number of vectors &gt; dimension of the vectors</td><td>Always linearly dependent</td></tr>
</tbody></table></div>

<h2>Example 1: a linearly dependent set</h2>
<p>Put the three vectors v₁ = (1, 2, 3), v₂ = (2, 1, 0), v₃ = (1, −1, −3) in the columns.</p>
{box(line("A ="), mx(Ad))}
{ex_dep}
<p>The RREF has only two pivots, so rank(A) = 2, while there are three vectors. The set is <strong>linearly dependent</strong>. Column 3, which has no pivot, can be expressed in terms of the other columns; indeed v₁ − v₂ + v₃ = 0.</p>
{box(vec(v1), line("−"), vec(v2), line("+"), vec(v3), op("="), vec([0, 0, 0]))}
<p>Since the matrix is square, the determinant also settles it: det(A) = 0.</p>

<h2>Example 2: a linearly independent set</h2>
<p>This time take w₁ = (1, 0, 1), w₂ = (0, 1, 1), w₃ = (1, 1, 0).</p>
{box(line("A ="), mx(Ai), line("det(A) = −2 ≠ 0"))}
<p>The determinant is nonzero, and the RREF is the identity matrix, so the rank is 3.</p>
{box(line("RREF(A) ="), mx(Mi))}
<p>Every column has a pivot, so the vectors are <strong>linearly independent</strong>. The three vectors form a basis for ℝ³.</p>

<h2>Useful facts</h2>
<ul>
<li>Any set that contains the zero vector is linearly dependent.</li>
<li>More than n vectors in ℝⁿ are always linearly dependent.</li>
<li>Any n linearly independent vectors in ℝⁿ form a basis.</li>
<li>A single vector is linearly independent as long as it is not the zero vector.</li>
<li>Two vectors are linearly dependent only when one is a scalar multiple of the other.</li>
</ul>

<h2>Common mistakes</h2>
<ul>
<li>Putting the vectors in rows works too, but mixing rows and columns gets confusing. Pick one convention; we recommend columns.</li>
<li>Concluding that the whole set is independent because some pairs are. In Example 1 any two of the vectors are independent, yet all three are dependent.</li>
<li>Using the determinant on a non-square matrix. The determinant only applies to square matrices; for rectangular ones, use the rank.</li>
</ul>

{faq(("Are linear independence and orthogonality the same thing?", "No. Nonzero orthogonal vectors are linearly independent, but linearly independent vectors need not be orthogonal."),
     ("How are a basis and linear independence related?", "A basis is a set of vectors that is linearly independent and spans the whole space. In ℝⁿ, any n linearly independent vectors automatically form a basis."),
     ("Can functions or polynomials be linearly independent?", "Yes. Convert them to coefficient vectors and use the same method. For example, the coefficient vectors of 1, x, x² form the identity matrix, so they are linearly independent."))}
"""
    return dict(
        slug="linear-independence", title="How to Test Vectors for Linear Independence (Using Rank)",
        h1="How to Test Vectors for Linear Independence (Using Rank)",
        meta="Test whether vectors are linearly independent by putting them in a matrix and finding its rank. Two worked examples, the determinant link and common mistakes.",
        desc="Test linear independence by putting the vectors in columns and finding the rank, with worked examples.",
        min=7, calc=("RREF calculator", "/rref/"), body=body,
        related=["rank-and-rref", "null-space-column-space"],
    )


# =====================================================================
# 14. Elementary matrices
# =====================================================================
def art_elem():
    A = M_([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    E1 = M_([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    E2 = M_([[1, 0, 0], [0, 1, 0], [0, 0, 2]])
    E3 = M_([[1, 0, 0], [0, 1, 0], [-7, 0, 1]])
    r1 = matmul(E1, A)
    assert r1 == M_([[4, 5, 6], [1, 2, 3], [7, 8, 10]])
    r2 = matmul(E2, A)
    assert r2 == M_([[1, 2, 3], [4, 5, 6], [14, 16, 20]])
    r3 = matmul(E3, A)
    assert r3 == M_([[1, 2, 3], [4, 5, 6], [0, -6, -11]])
    E3i = M_([[1, 0, 0], [0, 1, 0], [7, 0, 1]])
    assert matmul(E3, E3i) == ident(3)
    E2i = M_([[1, 0, 0], [0, 1, 0], [0, 0, Fr(1, 2)]])
    assert matmul(E2, E2i) == ident(3)
    assert matmul(E1, E1) == ident(3)
    assert tr_det3(E1) == -1 and tr_det3(E2) == 2 and tr_det3(E3) == 1

    body = f"""
<p class="lead">A row operation can also be written as "multiply the matrix on the left". The matrix you multiply by is an elementary matrix. This idea is essential for understanding why elimination gives you inverses and determinants.</p>

<h2>What is an elementary matrix?</h2>
<p>An <strong>elementary matrix</strong> is what you get by applying a single row operation to the identity matrix I. Since there are three kinds of row operation, there are three kinds of elementary matrix.</p>
<ul>
<li>Swap two rows</li>
<li>Multiply a row by a nonzero number</li>
<li>Add a multiple of one row to another row</li>
</ul>
<p>The key fact is one line. Applying a row operation to a matrix A gives the same result as multiplying A on the <strong>left</strong> by the elementary matrix E built from that row operation: the result is EA.</p>

<h2>Example matrix</h2>
{box(line("A ="), mx(A))}

<h2>1. Swapping two rows</h2>
<p>Multiply by E₁, the identity with rows 1 and 2 swapped.</p>
{box(line("E₁ ="), mx(E1), op("×"), mx(A), op("="), mx(r1))}
<p>Rows 1 and 2 of A have been swapped. Multiplying by the same matrix again restores the original, so E₁² = I.</p>

<h2>2. Multiplying a row by a constant</h2>
<p>E₂ is the identity with row 3 multiplied by 2.</p>
{box(line("E₂ ="), mx(E2), op("×"), mx(A), op("="), mx(r2))}
<p>Only row 3 of A has been doubled. To undo this, use the elementary matrix that multiplies row 3 by 1/2.</p>

<h2>3. Adding a multiple of one row to another</h2>
<p>R₃ ← R₃ − 7R₁ corresponds to E₃, the identity with −7 placed in row 3, column 1.</p>
{box(line("E₃ ="), mx(E3), op("×"), mx(A), op("="), mx(r3))}
<p>The first entry of row 3 is now 0. This is exactly the step in elimination that clears the entries below a pivot.</p>

<h2>Inverses of elementary matrices</h2>
<p>Every elementary matrix is invertible, and its inverse is also an elementary matrix: the one for the row operation that undoes the original.</p>
{box(line("E₃⁻¹ ="), mx(E3i), line("(R₃ ← R₃ + 7R₁)"))}
{box(mx(E3), op("×"), mx(E3i), op("="), mx(matmul(E3, E3i)))}

<h2>Determinants of elementary matrices</h2>
<ul>
<li>Row swap: det = −1 (E₁ above)</li>
<li>Multiply a row by k: det = k (E₂ above has 2)</li>
<li>Add a multiple of another row: det = 1 (E₃ above)</li>
</ul>
<p>This matches exactly how row operations change the determinant, as seen in <a href="/en/guide/determinant-properties/">properties of the determinant</a>, because det(EA) = det(E)·det(A).</p>

<h2>Why elimination gives the inverse</h2>
<p>Let E₁, E₂, …, Eₖ be the elementary matrices for the row operations that turn A into the identity, in order. Then Eₖ…E₂E₁A = I, so Eₖ…E₂E₁ is precisely A⁻¹. Applying the same row operations to [A | I] accumulates this product on the I side, which is where A⁻¹ appears. Turning the equation around, A is a product of inverses of elementary matrices. This is the theory behind <a href="/en/guide/inverse-gauss-jordan/">Gauss-Jordan elimination</a>.</p>

<h2>Common mistakes</h2>
<ul>
<li>Multiplying on the right of A to do a row operation. Row operations multiply on the left; multiplying on the right gives a column operation.</li>
<li>Writing several elementary matrices in the wrong order. The operation performed first goes furthest to the right (next to A).</li>
<li>Building an elementary matrix by multiplying a row by 0. Only nonzero numbers are allowed.</li>
</ul>

{faq(("How do column operations work?", "Multiplying A on the right by the same elementary matrix performs the corresponding column operation. For example, AE₁ swaps columns 1 and 2 of A."),
     ("Can every invertible matrix be written as a product of elementary matrices?", "Yes. An invertible matrix reduces to the identity by elimination, so it can be written as a product of elementary matrices."),
     ("Are elementary matrices a tool for actual computation?", "Mostly they are used in proofs and theory. For real calculations it is easier to perform the row operations directly."))}
"""
    return dict(
        slug="elementary-matrices", title="Elementary Matrices and Row Operations: Why Elimination Finds the Inverse",
        h1="Elementary Matrices and Row Operations: Why Elimination Finds the Inverse",
        meta="How row operations become left-multiplication by elementary matrices, with three 3×3 examples. Why elimination gives the inverse, plus their determinants.",
        desc="Express row operations as products of elementary matrices and see why elimination gives the inverse.",
        min=7, calc=("Matrix multiplication calculator", "/multiplication/"), body=body,
        related=["inverse-gauss-jordan", "determinant-properties"],
    )


# =====================================================================
# 15. Eigenvalues and eigenvectors (2×2)
# =====================================================================
def art_eigen():
    A = M_([[4, 1], [2, 3]])
    tr = A[0][0] + A[1][1]
    dt = det2(A)
    assert (tr, dt) == (7, 10)
    lam = [Fr(5), Fr(2)]
    assert lam[0] + lam[1] == tr and lam[0] * lam[1] == dt
    for l in lam:
        assert l * l - tr * l + dt == 0
    vs = {Fr(5): [Fr(1), Fr(1)], Fr(2): [Fr(1), Fr(-2)]}
    for l, v in vs.items():
        Av = [sum(A[i][j] * v[j] for j in range(2)) for i in range(2)]
        assert Av == [l * x for x in v]
    A5 = M_([[A[0][0] - 5, A[0][1]], [A[1][0], A[1][1] - 5]])
    A2 = M_([[A[0][0] - 2, A[0][1]], [A[1][0], A[1][1] - 2]])
    assert A5 == M_([[-1, 1], [2, -2]]) and A2 == M_([[2, 1], [2, 1]])
    assert det2(A5) == 0 and det2(A2) == 0
    Tg = M_([[3, 1, 4], [0, 5, 9], [0, 0, 2]])
    assert tr_det3(Tg) == 30
    Rot = M_([[0, -1], [1, 0]])
    assert Rot[0][0] + Rot[1][1] == 0 and det2(Rot) == 1

    body = f"""
<p class="lead">Eigenvalues and eigenvectors tell you which directions a matrix merely stretches. The calculation starts with solving the characteristic equation and ends with finding a null space. Let's follow one 2×2 matrix from start to finish.</p>

<h2>Definition</h2>
<p>For a square matrix A, a nonzero vector v with Av = λv is called an <strong>eigenvector</strong>, and the number λ is the corresponding <strong>eigenvalue</strong>. In other words, multiplying by A leaves the direction of v unchanged and only scales its length by λ.</p>

<h2>The procedure</h2>
<ol>
<li>Solve the characteristic equation det(A − λI) = 0 to find the eigenvalues λ.</li>
<li>For each eigenvalue, find a nonzero solution of (A − λI)v = 0. That solution is an eigenvector.</li>
</ol>
<p>For (A − λI)v = 0 to have a nonzero solution, A − λI must not be invertible, so its determinant must be 0. That is why step 1 is a determinant equation.</p>

<h2>Example</h2>
{box(line("A ="), mx(A))}
<h3>Step 1: the characteristic equation</h3>
<p>For a 2×2 matrix the characteristic equation is λ² − (trace)λ + (determinant) = 0. Here the trace is 4 + 3 = {num(tr)} and the determinant is 4·3 − 1·2 = {num(dt)}.</p>
{box(line("λ² − 7λ + 10 = 0"), line("(λ − 5)(λ − 2) = 0"), line("λ = 5, 2"))}
<p>Here is a quick check. The sum of the eigenvalues equals the trace (7) and their product equals the determinant (10). Since 5 + 2 = 7 and 5·2 = 10, everything is consistent.</p>

<h3>Step 2: the eigenvector for λ = 5</h3>
{box(line("A − 5I ="), mx(A5))}
<p>The second row is −2 times the first, so there is only one equation: −x + y = 0. Hence y = x, and choosing x = 1 gives the eigenvector below.</p>
{box(line("v₁ ="), vec(vs[Fr(5)]))}
<h3>Step 3: the eigenvector for λ = 2</h3>
{box(line("A − 2I ="), mx(A2))}
<p>The equation is 2x + y = 0. Since y = −2x, choosing x = 1 gives this eigenvector.</p>
{box(line("v₂ ="), vec(vs[Fr(2)]))}

<h2>Checking the answer</h2>
<p>Multiply out Av and confirm that it equals λv.</p>
{box(mx(A), op("×"), vec(vs[Fr(5)]), op("="), vec([5, 5]), line("= 5 ·"), vec(vs[Fr(5)]))}
{box(mx(A), op("×"), vec(vs[Fr(2)]), op("="), vec([2, -4]), line("= 2 ·"), vec(vs[Fr(2)]))}

<h2>Useful properties</h2>
<ul>
<li>Any scalar multiple of an eigenvector is also an eigenvector. All vectors in the same direction belong to the same eigenspace.</li>
<li>An n×n matrix has n eigenvalues counted with multiplicity (including complex ones).</li>
<li>The sum of the eigenvalues is the trace and their product is the determinant.</li>
<li>The eigenvalues of a triangular matrix are its diagonal entries. For example, the matrix below has eigenvalues 3, 5, 2.</li>
<li>A matrix with eigenvalue 0 is not invertible (its determinant is 0).</li>
</ul>
{box(mx(Tg), line("Eigenvalues: 3, 5, 2"), line("det = 30"))}

<h2>When there are no real eigenvalues</h2>
<p>A 90° rotation changes the direction of every vector, so no vector keeps its direction. The characteristic equation is λ² + 1 = 0, and the eigenvalues are the complex numbers i and −i.</p>
{box(line("Rotation ="), mx(Rot), line("λ² + 1 = 0"))}

<h2>Common mistakes</h2>
<ul>
<li>Computing det(A − λI) as if it were A − λ. Subtract λ only from the diagonal entries.</li>
<li>Giving the zero vector as an eigenvector. The zero vector is never an eigenvector.</li>
<li>Expecting the two equations from one eigenvalue to be independent. If you have worked correctly, the rows of A − λI are dependent.</li>
<li>Sign errors are easy to make, so always finish by checking Av = λv.</li>
</ul>

{faq(("Is an eigenvector unique?", "No. Any scalar multiple is also an eigenvector, so only the direction is determined. Normalize to length 1 only when the problem asks for it."),
     ("What if an eigenvalue is repeated?", "Check how many independent eigenvectors that eigenvalue has. If there are as many as its multiplicity, the matrix can be diagonalized; if fewer, it cannot."),
     ("Where are eigenvalues used?", "Diagonalization, matrix powers, differential equations, principal component analysis (PCA) and Google's PageRank, among many others."))}
"""
    return dict(
        slug="eigenvalues-2x2", title="How to Find Eigenvalues and Eigenvectors (2×2 Matrix Example)",
        h1="How to Find Eigenvalues and Eigenvectors (2×2 Matrix Example)",
        meta="Find eigenvalues from det(A − λI) = 0 and eigenvectors from the null space, worked on a 2×2 example. Includes a quick check and the complex-eigenvalue case.",
        desc="Follow a worked example: eigenvalues from the characteristic equation, eigenvectors from (A − λI)v = 0.",
        min=8, calc=("Determinant calculator", "/determinant/"), body=body,
        related=["determinant-properties", "special-matrices"],
    )


ARTICLES = [art_special(), art_spaces(), art_indep(), art_elem(), art_eigen()]
