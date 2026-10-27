// assets/app.js의 계산 부분만 떼어 Node에서 실행하고, 무작위 입력에 대한 결과를 JSON으로 출력해요.
// 검증은 tests/check_app.py가 Python fractions로 독립적으로 해요.
'use strict';
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'assets', 'app.js'), 'utf8');
const cut = src.indexOf('const ORDER=');
if (cut < 0) throw new Error('app.js에서 const ORDER= 를 찾지 못했어요');
let core = src.slice(0, cut).replace(/^\(function\(\)\{\s*'use strict';/, '');
const LANG = process.argv[3] || 'ko';
const lib = new Function('document', core + '\nreturn {F,parseF,OPS,gj,upper,det2,tex,bm};')({ querySelector: () => null, documentElement: { lang: LANG } });

// 사용: node tests/run_app.js [seed] [ko|en]
// 재현 가능한 난수
let seed = Number(process.argv[2] || 20261013);
const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const pick = a => a[Math.floor(rnd() * a.length)];
function entry() {
  const r = rnd();
  if (r < 0.45) return String(Math.floor(rnd() * 13) - 6);            // 정수 -6..6
  if (r < 0.65) return String(Math.floor(rnd() * 9) - 4) + '/' + (Math.floor(rnd() * 6) + 2); // 분수
  if (r < 0.80) return (Math.floor(rnd() * 41) - 20) / 10 + '';         // 소수 한 자리
  if (r < 0.90) return '0';
  return String(Math.floor(rnd() * 2001) - 1000);                       // 큰 정수
}
const mat = (r, c) => Array.from({ length: r }, () => Array.from({ length: c }, entry));
const F = s => lib.parseF(s);
const toF = M => M.map(r => r.map(F));

function latexOf(res) { return res.latex == null ? null : res.latex; }
const out = [];
function push(op, inp, res, extra) { out.push(Object.assign({ op, inp, latex: latexOf(res), chips: (res.chips || []).map(c => c[1]), steps: res.steps.length, data: res.data || null }, extra || {})); }

for (let n = 1; n <= 6; n++) for (let k = 0; k < 40; k++) {
  let A = mat(n, n);
  if (k % 5 === 0 && n > 1) A[n - 1] = A[0].slice();                  // 특이행렬 섞기
  if (k % 7 === 0 && n > 1) A[1] = A[0].map(x => '0');                 // 영행
  const fA = toF(A);
  push('inverse', { A }, lib.OPS.inverse.run({ A: fA }));
  push('det', { A }, lib.OPS.det.run({ A: fA }));
  if (n <= 4) { push('inverse', { A, method: 'adj' }, lib.OPS.inverse.run({ A: fA, method: 'adj' })); }
  for (const method of ['cof', 'sarrus', 'elim']) push('det', { A, method }, lib.OPS.det.run({ A: fA, method }));
  push('transpose', { A }, lib.OPS.transpose.run({ A: fA }));
  const kv = entry();
  push('scalar', { A, k: kv }, lib.OPS.scalar.run({ A: fA, k: F(kv) }));
  push('adj', { A }, lib.OPS.adj.run({ A: fA }));
  push('rank', { A }, lib.OPS.rank.run({ A: fA }));
  if (n <= 4 || k % 4 === 0) { const ne = k % 13; push('power', { A, k: String(ne) }, lib.OPS.power.run({ A: fA, k: F(String(ne)) })); }
}
// 고윳값: 작은 정수·분수 행렬, 삼각행렬, 닮은 행렬(P D P⁻¹)
const small = () => String(Math.floor(rnd() * 13) - 6);
const smallFrac = () => (rnd() < 0.8 ? small() : String(Math.floor(rnd() * 9) - 4) + '/' + (Math.floor(rnd() * 3) + 2));
for (let n = 1; n <= 5; n++) for (let k = 0; k < 24; k++) {
  let A;
  const kind = k % 4;
  if (kind === 0) A = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => j < i ? '0' : small()));            // 상삼각
  else if (kind === 1 && n >= 2) {                                                                                               // P D P⁻¹ (P 단위모듈러 → 고윳값 = d)
    const Fn = x => new lib.F(BigInt(x)), ONE = Fn(1), ZERO = Fn(0);
    const d = Array.from({ length: n }, () => Math.floor(rnd() * 7) - 3);
    const U = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => Fn(i === j ? 1 : (j > i ? Math.floor(rnd() * 3) - 1 : 0))));
    const Lo = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => Fn(i === j ? 1 : (j < i ? Math.floor(rnd() * 3) - 1 : 0))));
    const M = (X, Y) => X.map(r => Y[0].map((_, j) => r.reduce((s, a, t) => s.add(a.mul(Y[t][j])), ZERO)));
    const P = M(U, Lo);                                                                                                          // det = 1
    const inv = lib.gj(P.map((r, i) => [...r, ...r.map((_, j) => i === j ? ONE : ZERO)]), n).M.map(r => r.slice(n));
    const D = P.map((r, i) => r.map((_, j) => Fn(i === j ? d[i] : 0)));
    A = M(M(P, D), inv).map(r => r.map(x => x.n + (x.d === 1n ? '' : '/' + x.d)));
  } else if (kind === 2) A = Array.from({ length: n }, () => Array.from({ length: n }, smallFrac));
  else A = Array.from({ length: n }, () => Array.from({ length: n }, small));
  push('eigen', { A }, lib.OPS.eigen.run({ A: toF(A) }));
  push('diag', { A }, lib.OPS.diag.run({ A: toF(A) }));
  push('lu', { A }, lib.OPS.lu.run({ A: toF(A) }));
}
for (let k = 0; k < 150; k++) {
  const m = 1 + Math.floor(rnd() * 6), n = 1 + Math.floor(rnd() * 6), q = 1 + Math.floor(rnd() * 6);
  const A = mat(m, n), B = mat(n, q), C = mat(m, n);
  push('mul', { A, B }, lib.OPS.mul.run({ A: toF(A), B: toF(B) }));
  push('add', { A, B: C }, lib.OPS.add.run({ A: toF(A), B: toF(C) }));
  push('sub', { A, B: C }, lib.OPS.sub.run({ A: toF(A), B: toF(C) }));
  let R = mat(m, n);
  if (k % 4 === 0 && m > 1) R[m - 1] = R[0].map((x, j) => x);          // 종속 행
  push('rref', { A: R }, lib.OPS.rref.run({ A: toF(R) }));
  let S = mat(m, n), b = Array.from({ length: m }, entry);
  if (k % 3 === 0 && m > 1) S[m - 1] = S[0].slice();                   // 종속 행 → 해 없음/무수히 많음
  push('solve', { A: S, b }, lib.OPS.solve.run({ A: toF(S), b: b.map(F) }));
  // AX = B (정방 A), 그람-슈미트, LU
  let Q = mat(n, n), Bq = mat(n, q);
  if (k % 3 === 0 && n > 1) Q[n - 1] = Q[0].slice();
  if (k % 6 === 0 && n > 1) { Bq[n - 1] = Bq[0].slice(); }                 // 종속 A에 모순 없는 B가 되도록 섞기
  push('axb', { A: Q, B: Bq }, lib.OPS.axb.run({ A: toF(Q), B: toF(Bq) }));
  let G = mat(m, n);
  if (k % 4 === 0 && n > 1) G = G.map(r => { r[n - 1] = r[0]; return r; });  // 종속 열
  push('gs', { A: G }, lib.OPS.gs.run({ A: toF(G) }));
  let Lm = mat(n, n);
  if (k % 5 === 0) Lm[0][0] = '0';                                             // 행 교환 유도
  if (k % 7 === 0 && n > 1) Lm[n - 1] = Lm[0].slice();
  push('lu', { A: Lm }, lib.OPS.lu.run({ A: toF(Lm) }));
}
// 입력 파서 경계값
const parse = ['', '  ', '3', '-3', '+3', '1/2', '-1/2', '0.25', '-.5', '2.', '1/0', 'abc', '1/2/3', '−3', '1 / 2', '007', '1e3'].map(s => { const f = lib.parseF(s); return [s, f === null ? null : f.n + '/' + f.d]; });
process.stdout.write(JSON.stringify({ lang: LANG, cases: out, parse }));
