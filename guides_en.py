"""English guides (/en/guide/). Same verified examples as the Korean articles.

Every number in the text is recomputed with Fraction and checked with assert,
so a wrong figure stops the build.
"""
from fractions import Fraction as Fr
from guides import (M_, ident, matmul, det2, minor, mx, mx_text, op, line, box, steps_html,
                    gj, upper, lin, num, par, sub)

NOTES_EN = dict(
    swap="Move a nonzero entry of column {c} up to row {r} to use as the pivot.",
    scale="Divide row {r} by the pivot so the pivot becomes 1.",
    elim="Make every other entry of column {c} zero.",
    uswap="Swapping two rows changes the sign of the determinant.",
    uelim="Clear the entries below the pivot in column {c}. This does not change the determinant.",
)


# =====================================================================
# 1. Inverse by Gauss-Jordan
# =====================================================================
def art_inverse():
    A = M_([[2, 1], [5, 3]])
    aug = [A[i] + ident(2)[i] for i in range(2)]
    Mf, st, piv, rk = gj(aug, 2, NOTES_EN)
    inv = [r[2:] for r in Mf]
    assert inv == M_([[3, -1], [-5, 2]]) and rk == 2
    assert matmul(A, inv) == ident(2)
    assert A[0][0] * A[1][1] - A[0][1] * A[1][0] == 1
    ex1 = steps_html("Append the identity matrix I to the right of A to form [A | I].", aug, st, sep=2)

    B = M_([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
    augB = [B[i] + ident(3)[i] for i in range(3)]
    Mb, stb, _, rkb = gj(augB, 3, NOTES_EN)
    invB = [r[3:] for r in Mb]
    assert invB == M_([[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]) and rkb == 3
    assert matmul(B, invB) == ident(3)
    ex2 = steps_html("Form [B | I].", augB, stb, sep=3)

    C = M_([[1, 2], [2, 4]])
    augC = [C[i] + ident(2)[i] for i in range(2)]
    Mc, stc, _, rkc = gj(augC, 2, NOTES_EN)
    assert rkc == 1 and all(x == 0 for x in Mc[1][:2])
    ex3 = steps_html("Form [C | I].", augC, stc, sep=2)

    body = f"""
<p class="lead">The inverse of a matrix plays the role that division plays for numbers. This guide walks through Gauss-Jordan elimination on a 2×2 and a 3×3 example, one row operation at a time, and shows what happens when no inverse exists.</p>

<h2>What is an inverse matrix?</h2>
<p>For a square matrix A, a matrix B with AB = BA = I is called the inverse of A and written A⁻¹. Here I is the identity matrix: ones on the diagonal, zeros everywhere else.</p>
<p>Not every matrix has an inverse. It exists <strong>only when A is square and its determinant is not zero</strong>. A matrix with an inverse is called invertible (or nonsingular).</p>

<h2>Gauss-Jordan elimination at a glance</h2>
<p>Write the identity matrix next to A to form [A | I]. Apply row operations until the left half becomes I. The right half is then A⁻¹.</p>
{box(line("[ A | I ]"), op("→"), line("row operations"), op("→"), line("[ I | A⁻¹ ]"))}
<p>Three row operations are allowed.</p>
<ul>
<li>Swap two rows: R₁ ↔ R₂</li>
<li>Multiply a row by a nonzero number: R₁ ← 2R₁</li>
<li>Add a multiple of one row to another: R₂ ← R₂ − 5R₁</li>
</ul>
<p>Why does this work? Each row operation is the same as multiplying on the left by an invertible matrix. The product of all the operations that turn A into I is exactly A⁻¹, and applying the same operations to I accumulates that product on the right.</p>

<h2>Example 1: a 2×2 matrix</h2>
<p>Let's invert the matrix below.</p>
{box(line("A ="), mx(A))}
{ex1}
<p>The left half is now the identity, so the right half is the inverse.</p>
{box(line("A⁻¹ ="), mx(inv))}
<p>For 2×2 matrices there is also a formula. If A = [[a, b], [c, d]], then A⁻¹ = 1/(ad − bc) · [[d, −b], [−c, a]]. Here ad − bc = 2·3 − 1·5 = 1, which gives [[3, −1], [−5, 2]], the same as elimination.</p>

<h3>Checking the answer</h3>
<p>Multiply AA⁻¹. If you get the identity matrix, the inverse is correct.</p>
{box(mx(A), op("×"), mx(inv), op("="), mx(matmul(A, inv)))}

<h2>Example 2: a 3×3 matrix</h2>
<p>Now a 3×3 matrix. The method is identical; there is just one more pivot.</p>
{box(line("B ="), mx(B))}
{ex2}
<p>The left half is I, so B⁻¹ is the matrix below. Because det(B) = 1, every entry of the inverse is an integer.</p>
{box(line("B⁻¹ ="), mx(invB))}

<h2>When there is no inverse</h2>
<p>If a row of zeros appears on the left half during elimination, the left half can never become the identity. The matrix has no inverse.</p>
{box(line("C ="), mx(C))}
{ex3}
<p>Row 2 of the left half became all zeros, so C is not invertible. Indeed det(C) = 1·4 − 2·2 = 0: the second row is twice the first.</p>

<h2>Common mistakes</h2>
<ul>
<li>Applying an operation to the left half only. Every row operation applies to the whole row, including the I part.</li>
<li>Skipping a zero pivot. If a lower row has a nonzero entry in that column, swap it up.</li>
<li>Sign errors in fraction arithmetic. Always finish by checking AA⁻¹ = I.</li>
<li>Pushing on when the determinant is zero. Computing the determinant first can save a lot of work.</li>
</ul>

<h2>FAQ</h2>
<div class="faq">
<details><summary>Can I tell in advance whether the inverse exists?</summary><p>Yes: the inverse exists exactly when the determinant is nonzero. For 3×3 determinants see the <a href="/en/guide/determinant-3x3/">cofactor expansion guide</a>.</p></details>
<details><summary>What about 4×4 and larger?</summary><p>The method is the same, but the arithmetic gets long and error-prone by hand. Use the calculator to check your work.</p></details>
<details><summary>Should I use elimination for 2×2 too?</summary><p>For 2×2 the formula is faster. From 3×3 up, elimination is usually easier to organize.</p></details>
</div>
"""
    return dict(
        slug="inverse-gauss-jordan",
        title="How to Find the Inverse of a Matrix by Gauss-Jordan Elimination",
        h1="How to Find the Inverse of a Matrix by Gauss-Jordan Elimination",
        meta="Step-by-step Gauss-Jordan elimination on [A | I] with 2×2 and 3×3 examples, the 2×2 shortcut formula, how to check the answer, and what a singular matrix looks like.",
        desc="Row-reduce [A | I] to [I | A⁻¹], with worked 2×2 and 3×3 examples.",
        min=6, calc=("Inverse calculator", "/inverse/"), body=body,
        related=["determinant-3x3", "linear-system-solutions"],
    )


# =====================================================================
# 2. 3×3 determinant
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
    a = A
    dr = a[0][0] * a[1][1] * a[2][2] + a[0][1] * a[1][2] * a[2][0] + a[0][2] * a[1][0] * a[2][1]
    dl = a[0][2] * a[1][1] * a[2][0] + a[0][0] * a[1][2] * a[2][1] + a[0][1] * a[1][0] * a[2][2]
    assert (dr, dl, dr - dl) == (24, 0, 24)
    du, Mu, stu = upper(A, NOTES_EN)
    assert du == 24

    def m2(m):
        return f"{par(m[0][0])}·{par(m[1][1])} − {par(m[0][1])}·{par(m[1][0])} = {num(det2(m))}"

    minors_html = ""
    for j in range(3):
        minors_html += box(line(f"M₁{sub(j + 1)} ="), mx(mins[j]), line(m2(mins[j])))
    elim = steps_html("Row-reduce to an upper triangular matrix.", A, stu)

    body = f"""
<p class="lead">A 3×3 determinant can be broken into three 2×2 determinants by cofactor expansion. This guide computes the same determinant three ways: cofactor expansion, the rule of Sarrus, and row reduction.</p>

<h2>What is a determinant?</h2>
<p>The determinant assigns a single number to a square matrix. Geometrically it tells how much the matrix scales area (2×2) or volume (3×3). If the determinant is 0, the matrix has no inverse.</p>
<p>Keep the 2×2 determinant in mind; it is used over and over in the 3×3 computation.</p>
{box(line("det [[a, b], [c, d]] = ad − bc"))}

<h2>The cofactor expansion rule</h2>
<p>Pick a row (or column). Multiply each entry of that row by its <strong>minor</strong> and add the results with alternating signs. The minor Mᵢⱼ of the entry aᵢⱼ is the determinant of the matrix left after deleting row i and column j.</p>
<p>The signs follow a checkerboard pattern. The top-left is +, and the sign flips with every step.</p>
{box(mx_text([["+", "−", "+"], ["−", "+", "−"], ["+", "−", "+"]]))}
<p>Expanding along row 1 gives:</p>
{box(line("det(A) = a₁₁M₁₁ − a₁₂M₁₂ + a₁₃M₁₃"))}

<h2>Example: expanding along row 1</h2>
{box(line("A ="), mx(A))}
<p>The entries of row 1 are 2, −1, 0. First find the minor for each.</p>
{minors_html}
<p>Now attach the signs and add.</p>
{box(line(f"det(A) = {par(A[0][0])}·{num(mv[0])} − {par(A[0][1])}·{num(mv[1])} + {par(A[0][2])}·{num(mv[2])} = {num(d)}"))}
<p>The third entry of row 1 is 0, so the third term is 0 without computing its minor. <strong>Expanding along a row or column with many zeros saves work.</strong></p>

<h3>Any row or column gives the same answer</h3>
<p>Column 1 has a zero at the bottom. Expanding along column 1 makes a₃₁M₃₁ vanish, leaving two terms with signs +, −, +.</p>
{box(line(f"det(A) = 2·10 − 1·M₂₁ + 0·M₃₁,  M₂₁ = {m2(m21)}"))}
{box(line("det(A) = 2·10 − 1·(−4) = 24"))}
<p>Same value as the row-1 expansion. Every row and column gives the same result, so choose whichever is easiest.</p>

<h2>The rule of Sarrus</h2>
<p>This shortcut works only for 3×3 matrices. Add the products of the three diagonals running down to the right, and subtract the products of the three diagonals running down to the left.</p>
{box(line(f"Down-right: 2·3·4 + (−1)·2·0 + 0·1·1 = {num(dr)}"))}
{box(line(f"Down-left: 0·3·0 + 2·2·1 + (−1)·1·4 = {num(dl)}"))}
{box(line(f"det(A) = {num(dr)} − {num(dl)} = {num(dr - dl)}"))}
<p>Sarrus does not extend to 4×4 or larger. Cofactor expansion works for any size, so it is worth knowing both.</p>

<h2>Row reduction</h2>
<p>For 4×4 and larger, row-reducing to an upper triangular matrix is usually the most practical method. Once everything below the diagonal is 0, the determinant is the product of the diagonal entries. Here is the same matrix again.</p>
{elim}
<p>The diagonal product is 2 · 7/2 · 24/7 = 24. No rows were swapped, so the sign is unchanged. All three methods agree.</p>

<h2>Properties of the determinant</h2>
<ul>
<li>Swapping two rows (or columns) flips the sign.</li>
<li>Multiplying a row by k multiplies the determinant by k.</li>
<li>Adding a multiple of one row to another leaves the determinant unchanged.</li>
<li>det(Aᵀ) = det(A) and det(AB) = det(A)·det(B).</li>
<li>For an n×n matrix, det(kA) = kⁿ·det(A).</li>
<li>The determinant of a triangular matrix is the product of its diagonal entries.</li>
<li>If det(A) = 0, A has no inverse and its rows are linearly dependent.</li>
</ul>

<h2>Common mistakes</h2>
<ul>
<li>Deleting the wrong row and column for a minor. Delete the row and the column that contain the entry.</li>
<li>Forgetting the checkerboard sign. The middle entry of row 1, a₁₂, gets a minus.</li>
<li>Using Sarrus on a 4×4 matrix. Sarrus is for 3×3 only.</li>
<li>Swapping rows during reduction and forgetting to flip the sign.</li>
</ul>

<h2>FAQ</h2>
<div class="faq">
<details><summary>What does a negative determinant mean?</summary><p>The transformation reverses orientation. The absolute value still tells how much area or volume is scaled.</p></details>
<details><summary>Do rectangular matrices have a determinant?</summary><p>No. The determinant is defined only for square matrices.</p></details>
<details><summary>I have the determinant. How do I get the inverse?</summary><p>See the <a href="/en/guide/inverse-gauss-jordan/">Gauss-Jordan elimination guide</a> for a step-by-step method.</p></details>
</div>
"""
    return dict(
        slug="determinant-3x3",
        title="How to Compute a 3×3 Determinant (Cofactor Expansion and Sarrus)",
        h1="How to Compute a 3×3 Determinant: Cofactor Expansion and the Rule of Sarrus",
        meta="Three ways to compute the same 3×3 determinant: cofactor expansion, the rule of Sarrus, and row reduction, plus the key properties and common mistakes.",
        desc="Cofactor expansion, the rule of Sarrus, and row reduction on one 3×3 example.",
        min=6, calc=("Determinant calculator", "/determinant/"), body=body,
        related=["inverse-gauss-jordan", "rank-and-rref"],
    )


# =====================================================================
# 3. Rank and RREF
# =====================================================================
def art_rank():
    A = M_([[1, 2, -1, 3], [2, 4, 1, 0], [-1, -2, 2, 1]])
    Mf, st, piv, rk = gj(A, 4, NOTES_EN)
    assert Mf == M_([[1, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert piv == [0, 2, 3] and rk == 3
    ex = steps_html("Start from the given matrix.", A, st)

    body = f"""
<p class="lead">Reduced row echelon form (RREF) is the simplest shape a matrix can be reduced to. Once you have it, the rank, the pivot columns and the solutions of a linear system can all be read off at a glance.</p>

<h2>The four conditions for RREF</h2>
<p>A matrix is in reduced row echelon form when all of the following hold.</p>
<ol>
<li>Rows consisting entirely of zeros are at the bottom.</li>
<li>The first nonzero entry of each row (the <strong>pivot</strong>, or leading 1) is 1.</li>
<li>Each pivot lies to the right of the pivot in the row above, giving a staircase shape.</li>
<li>Every other entry in a pivot column is 0.</li>
</ol>
<p>Conditions 1–3 alone define row echelon form (REF); some textbooks do not even require the pivot to be 1. A matrix has many possible REFs, but <strong>exactly one RREF</strong>. Whatever order of row operations you use, you end at the same RREF.</p>

<h2>Example: reducing to RREF</h2>
<p>Let's reduce a 3×4 matrix.</p>
{box(line("A ="), mx(A))}
{ex}
<p>The final result:</p>
{box(line("RREF(A) ="), mx(Mf))}

<h2>Reading the result</h2>
<ul>
<li>The <strong>pivot columns</strong> are columns 1, 3 and 4.</li>
<li>The <strong>rank</strong> is the number of pivots: 3.</li>
<li>Column 2 has no pivot, so it is a <strong>free variable</strong> column. In a linear system, that variable can take any value.</li>
</ul>
<p>In column 2 every entry below the first row was already 0, so no pivot could be chosen there. In that case skip the column and look for a pivot in the next one.</p>

<h2>What the rank tells you</h2>
<p>The rank is the number of linearly independent rows (equivalently, columns) of the matrix.</p>
<ul>
<li>The rank of an m×n matrix is at most min(m, n).</li>
<li>Row rank equals column rank: rank(A) = rank(Aᵀ).</li>
<li>An n×n matrix with rank n is invertible and has a nonzero determinant.</li>
<li><strong>Rank-nullity theorem</strong>: rank(A) + nullity(A) = number of columns. Here 3 + 1 = 4, so the solution space of Ax = 0 (the null space) is one-dimensional.</li>
</ul>
<p>One caution when finding a basis of the column space: take the pivot column <em>numbers</em> from the RREF, but use the columns of the <strong>original matrix A</strong>. Here columns 1, 3 and 4 of A form a basis of the column space. The columns of the RREF itself span a different space.</p>

<h2>Common mistakes</h2>
<ul>
<li>Stopping before scaling the pivots to 1. That is REF, not RREF.</li>
<li>Forgetting to clear the entries above each pivot. RREF needs zeros above and below.</li>
<li>Giving up at a zero column. Move on to the next column and look for a pivot there.</li>
<li>Using the RREF's columns as a basis of the column space. Use the columns of the original A.</li>
</ul>

<h2>FAQ</h2>
<div class="faq">
<details><summary>Can a matrix have rank 0?</summary><p>Only the zero matrix. It has no pivots at all.</p></details>
<details><summary>What is RREF used for?</summary><p>Solving linear systems, computing rank, finding bases of the null space and column space, and inverting matrices are all RREF computations.</p></details>
<details><summary>How does this relate to solving linear systems?</summary><p>Reduce the augmented matrix to RREF and read off the solution. The <a href="/en/guide/linear-system-solutions/">linear systems guide</a> continues from here.</p></details>
</div>
"""
    return dict(
        slug="rank-and-rref",
        title="Rank and Reduced Row Echelon Form (RREF) Explained",
        h1="Rank and Reduced Row Echelon Form (RREF) Explained",
        meta="The four conditions for RREF, a worked reduction of a 3×4 matrix, and how to read the pivot columns, rank, free variables and null space dimension from the result.",
        desc="Reduce a matrix to RREF and read off pivot columns, rank and free variables.",
        min=6, calc=("RREF calculator", "/rref/"), body=body,
        related=["linear-system-solutions", "inverse-gauss-jordan"],
    )


# =====================================================================
# 4. Solutions of linear systems
# =====================================================================
def art_system():
    A1 = M_([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    M1, _, p1, r1 = gj(A1, 3, NOTES_EN)
    assert [row[3] for row in M1] == [2, 3, -1] and r1 == 3
    x = [row[3] for row in M1]
    for row in A1:
        assert sum(row[j] * x[j] for j in range(3)) == row[3]

    A2 = M_([[1, 1, 1, 3], [2, 2, 2, 5], [1, -1, 0, 1]])
    M2, st2, p2, r2 = gj(A2, 3, NOTES_EN)
    assert r2 == 2 and M2[2][:3] == [0, 0, 0] and M2[2][3] != 0
    ex2 = steps_html("Form the augmented matrix [A | b].", A2, st2, sep=3)

    A3 = M_([[1, 2, 1, 4], [2, 4, 2, 8], [1, 1, 0, 3]])
    M3, st3, p3, r3 = gj(A3, 3, NOTES_EN)
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
    ex3 = steps_html("Form the augmented matrix [A | b].", A3, st3, sep=3)

    body = f"""
<p class="lead">A system of linear equations has exactly one solution, no solution, or infinitely many. Reducing the augmented matrix tells you which case you are in. Three examples make the difference clear.</p>

<h2>The augmented matrix</h2>
<p>For a system Ax = b, the matrix [A | b] obtained by writing b to the right of the coefficient matrix A is called the augmented matrix. Reduce it to RREF with row operations and the solution can be read off.</p>

<h2>How to tell the three cases apart</h2>
<p>Let n be the number of unknowns. After reduction, compare ranks.</p>
<div class="tbl"><table class="gtable">
<thead><tr><th>Condition</th><th>Number of solutions</th><th>What the reduced matrix looks like</th></tr></thead>
<tbody>
<tr><td>rank(A) &lt; rank([A | b])</td><td>None</td><td>A row of the form 0 = (nonzero) appears</td></tr>
<tr><td>rank(A) = rank([A | b]) = n</td><td>Exactly one</td><td>Every variable column has a pivot</td></tr>
<tr><td>rank(A) = rank([A | b]) &lt; n</td><td>Infinitely many</td><td>Some variable column has no pivot (a free variable)</td></tr>
</tbody></table></div>

<h2>Case 1: exactly one solution</h2>
<p>Solve the system below.</p>
{box(line("2x + y − z = 8"))}
{box(line("−3x − y + 2z = −11"))}
{box(line("−2x + y + 2z = −3"))}
<p>Reducing the augmented matrix to RREF gives the matrix on the right. The calculator shows every intermediate step.</p>
{box(mx(A1, sep=3), op("→"), mx(M1, sep=3))}
<p>All three variable columns have pivots. Since rank(A) = rank([A | b]) = 3 = n, the solution is unique and the last column is the solution.</p>
{box(line("(x, y, z) = (2, 3, −1)"))}
<p>Check by substituting: 2·2 + 3 − (−1) = 8, −3·2 − 3 + 2·(−1) = −11, and −2·2 + 3 + 2·(−1) = −3 all hold.</p>

<h2>Case 2: no solution</h2>
{box(line("x + y + z = 3"))}
{box(line("2x + 2y + 2z = 5"))}
{box(line("x − y = 1"))}
<p>Doubling the first equation gives 2x + 2y + 2z = 6, but the second equation says 5. The equations contradict each other. Elimination makes this visible.</p>
{ex2}
<p>Row 3 became [0, 0, 0 | −1], which says 0 = −1. That is impossible, so there is no solution. rank(A) = 2 while rank([A | b]) = 3, so rank(A) &lt; rank([A | b]).</p>

<h2>Case 3: infinitely many solutions</h2>
{box(line("x + 2y + z = 4"))}
{box(line("2x + 4y + 2z = 8"))}
{box(line("x + y = 3"))}
<p>The second equation is twice the first, so there are really only two equations.</p>
{ex3}
<p>Row 3 is all zeros and column 3 has no pivot. rank(A) = rank([A | b]) = 2 with n = 3, so there are infinitely many solutions. The variable of the pivot-free column, z, is a <strong>free variable</strong>. Set z = t and the other variables follow.</p>
{box('<div class="sol">' + "".join(f"<div>{s}</div>" for s in sol) + "</div>")}
<p>Any value of t satisfies all three equations: t = 0 gives (2, 1, 0) and t = 1 gives (3, 0, 1). The number of free variables is n − rank = 3 − 2 = 1, so the solutions form a line.</p>

<h2>Common mistakes</h2>
<ul>
<li>Deciding by counting equations and unknowns. Extra equations may be redundant, and fewer equations usually means infinitely many solutions, not none.</li>
<li>Reading a row 0 = 0 as "no solution". 0 = 0 is harmless. Only 0 = (nonzero) rules out solutions.</li>
<li>Taking only one free variable when there are several. Every pivot-free column is a free variable.</li>
<li>Sign errors in the general solution. Substitute back into the original equations to check.</li>
</ul>

<h2>FAQ</h2>
<div class="faq">
<details><summary>If there are more equations than unknowns, is there never a solution?</summary><p>Not necessarily. If some equations repeat others, a solution can exist. Decide by rank.</p></details>
<details><summary>Can I choose which variable is free?</summary><p>The free variables are those in pivot-free columns of the RREF. A different elimination order may make the solution look different, but the solution set is the same.</p></details>
<details><summary>What about Ax = 0?</summary><p>x = 0 is always a solution, so a homogeneous system is never inconsistent. If there is a free variable, there are infinitely many nonzero solutions too.</p></details>
</div>
"""
    return dict(
        slug="linear-system-solutions",
        title="One Solution, No Solution, or Infinitely Many? How to Tell",
        h1="One Solution, No Solution, or Infinitely Many? How to Tell",
        meta="Use the ranks of A and [A | b] to decide whether a linear system has one solution, none, or infinitely many. Three worked examples and how to write the general solution.",
        desc="Decide the number of solutions by rank and write the general solution with free variables.",
        min=7, calc=("Linear system solver", "/linear-system/"), body=body,
        related=["rank-and-rref", "inverse-gauss-jordan"],
    )


ARTICLES = [art_inverse(), art_det(), art_rank(), art_system()]
for _a in ARTICLES:
    _a["published"] = "2026-10-26"

# The remaining guides live in separate modules (imported after NOTES_EN exists).
import guides_en_a  # noqa: E402
import guides_en_b  # noqa: E402
import guides_en_c  # noqa: E402
for _a in guides_en_a.ARTICLES + guides_en_b.ARTICLES + guides_en_c.ARTICLES:
    _a["published"] = "2026-10-27"
ARTICLES += guides_en_a.ARTICLES + guides_en_b.ARTICLES + guides_en_c.ARTICLES
BY_SLUG = {a["slug"]: a for a in ARTICLES}
