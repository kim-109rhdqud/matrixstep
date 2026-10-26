(function(){
'use strict';
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SUBD='₀₁₂₃₄₅₆₇₈₉', SUPD='⁰¹²³⁴⁵⁶⁷⁸⁹';
const sub=n=>String(n).split('').map(d=>SUBD[+d]).join('');
const sup=n=>String(n).split('').map(d=>SUPD[+d]).join('');
const ij=(i,j)=>sub(i+1)+sub(j+1);
const MAX=6;

/* ---------- 문구 (한국어 / 영어) ---------- */
const LANG=/^en/i.test((document.documentElement&&document.documentElement.lang)||'')?'en':'ko';
const STR={
ko:{
  swap:(c,r)=>c+'열에서 피벗으로 쓸 0이 아닌 성분을 '+r+'행으로 올려요.',
  scale:r=>'피벗을 1로 만들기 위해 '+r+'행 전체를 피벗 값으로 나눠요.',
  elim:c=>c+'열에서 피벗을 제외한 나머지 성분을 0으로 만들어요.',
  uNoPivot:c=>c+'열의 대각선 아래가 모두 0이라 피벗을 잡을 수 없어요. 따라서 행렬식은 0이에요.',
  uSwap:'두 행을 바꾸면 행렬식의 부호가 바뀌어요.',
  uElim:c=>c+'열의 피벗 아래를 0으로 만들어요. 이 연산은 행렬식을 바꾸지 않아요.',
  uDone:neg=>'상삼각행렬의 행렬식은 대각 성분의 곱이에요.'+(neg?' 행을 홀수 번 바꿨으니 부호를 바꿔요.':''),
  invFormula:'2×2 행렬은 공식으로 바로 구할 수 있어요. 아래 소거법 풀이와 결과가 같아요.',
  invAug:'오른쪽에 단위행렬 I를 붙여 [A | I]를 만들어요.',
  invSingular:'왼쪽 부분에 영행이 생겨 단위행렬을 만들 수 없어요. 그래서 A는 역행렬이 없어요.',
  invNoneHead:'<strong>역행렬이 없어요</strong><span>det(A) = 0이라서 A는 가역행렬이 아니에요.</span>',
  chipSingular:'비가역 행렬',
  invDone:'왼쪽이 단위행렬이 되었어요. 오른쪽 부분이 A⁻¹이에요.',
  det1:'1×1 행렬의 행렬식은 그 성분 자체예요.',
  det2:'2×2 행렬식은 주대각선의 곱에서 반대 대각선의 곱을 빼요.',
  det3Intro:'1행을 따라 여인수 전개를 해요. 부호는 + − + 순서로 붙어요.',
  det3Minor:j=>'1행과 '+j+'열을 지우고 남은 2×2 행렬의 행렬식이 M₁'+sub(j)+'이에요.',
  det3Sum:'각 성분과 소행렬식을 곱하고 부호를 붙여 더해요.',
  detNIntro:'행 소거로 상삼각행렬을 만든 뒤 대각 성분을 곱해요.',
  chipNoInv:'역행렬 없음', chipInv:'역행렬 있음',
  mulOk:(n,m,q)=>'A의 열 수와 B의 행 수가 '+n+'로 같아서 곱할 수 있어요. 결과는 '+m+'×'+q+' 행렬이에요.',
  mulEntry:(i,j)=>'A의 '+i+'행과 B의 '+j+'열을 차례로 곱해 더해요.',
  addIntro:'두 행렬의 크기가 같아서 같은 위치의 성분끼리 더해요.',
  subIntro:'두 행렬의 크기가 같아서 같은 위치의 성분끼리 빼요.',
  scalarIntro:k=>'모든 성분에 k = '+k+' 를 곱해요.',
  trRow:i=>'A의 '+i+'행을 Aᵀ의 '+i+'열로 옮겨요.',
  rrefStart:'주어진 행렬에서 시작해요.',
  rrefAlready:'이미 기약 행사다리꼴이에요.',
  rrefPiv:list=>'피벗은 '+list+'열에 있어요. 피벗의 개수가 랭크예요.',
  rrefZero:'모든 성분이 0이라 피벗이 없어요.',
  chipPivCols:list=>'피벗 열 '+list,
  solAug:'계수행렬 A 옆에 b를 붙여 첨가행렬 [A | b]를 만들어요.',
  solContra:(row,v)=>row+'행이 0 = '+v+' 꼴이 되어 모순이에요. 따라서 해가 없어요.',
  solNoneHead:v=>'<strong>해가 없어요</strong><span>소거 과정에서 0 = '+v+' 같은 모순인 식이 생겨요.</span>',
  chipNone:'해 없음',
  solUnique:'모든 변수 열에 피벗이 있어서 해가 하나로 정해져요.',
  chipUnique:'유일한 해',
  solFree:(vars,n)=>'피벗이 없는 '+vars+' 는 자유변수예요. 매개변수 t로 두고 나머지 변수를 나타내요.',
  solInfHead:'<strong>해가 무수히 많아요</strong>',
  chipFree:n=>'자유변수 '+n+'개',
  dec:l=>l+' 줄이기', inc:l=>l+' 늘리기',
  cell:(l,i,j)=>l+' '+i+'행 '+j+'열',
  size:'크기', rows:'행', cols:'열',
  bCell:i=>'b '+i+'행',
  sys:(r,c)=>'식 '+r+'개 · 미지수 '+c+'개 · Ax = b',
  errInput:'빨간 칸의 값을 확인해 주세요. 정수, 분수(1/3), 소수(0.25)만 입력할 수 있어요.',
  errFail:'계산하지 못했어요. 입력값을 확인해 주세요.',
  stepsEmpty:'값을 입력하면 풀이가 여기에 나와요.',
  stepsLess:'풀이 접기', stepsMore:n=>'나머지 '+n+'단계 보기', stepsCount:n=>n+'단계',
  copied:'LaTeX를 복사했어요. Overleaf, 노션 수식 블록, 워드 수식 편집기에 붙여넣으세요.', copyFail:'복사하지 못했어요. 브라우저 설정을 확인해 주세요',
  pow0:'어떤 정사각행렬이든 0제곱은 단위행렬 I로 정해요.',
  pow1:'A¹ = A 에서 시작해요.',
  powStep:i=>'A'+sup(i-1)+'에 A를 한 번 더 곱해 A'+sup(i)+'을 구해요.',
  powNote:'n은 0부터 12까지의 정수예요.',
  errPow:'지수 n은 0부터 12까지의 정수만 입력할 수 있어요.',
  rankDone:r=>'피벗의 개수가 랭크예요. rank(A) = '+r+'이에요.',
  rankZero:'모든 성분이 0이라 피벗이 없어요. rank(A) = 0이에요.',
  rankNullity:(c,r)=>'nullity(A) = (열 수) − rank(A) = '+c+' − '+r+' = '+(c-r)+'. 피벗이 없는 열의 개수와 같아요.',
  rankPiv:list=>'피벗 열: '+list, rankBasis:list=>'열공간 기저: A의 '+list+'열',
  chipFull:'최대 랭크', chipDeficient:'랭크 부족',
  adj1:'1×1 행렬의 수반행렬은 [1]로 정해요.',
  adjMinor:(i,j,sg)=>i+'행과 '+j+'열을 지우고 남은 행렬의 행렬식이 소행렬식 M'+ij(i-1,j-1)+'이에요. 부호 '+sg+'를 붙이면 여인수 C'+ij(i-1,j-1)+'예요.',
  adjCof:'여인수를 같은 위치에 모으면 여인수행렬 C예요.',
  adjT:'여인수행렬을 전치하면 수반행렬 adj(A) = Cᵀ예요.',
  adjInv:'det(A) ≠ 0 이므로 A⁻¹ = adj(A) / det(A) 로 역행렬도 바로 구할 수 있어요.',
  adjNoInv:'det(A) = 0 이라서 역행렬은 없지만 수반행렬은 항상 존재해요. 이때 A·adj(A) = det(A)·I = O 예요.',
  eigPoly:'특성다항식 p(λ) = det(λI − A)를 구해요. 이 다항식의 근이 고윳값이에요.',
  eigPoly2:(tr,d)=>'2×2에서는 p(λ) = λ² − (대각합)λ + (행렬식) = λ² − ('+tr+')λ + ('+d+') 이에요.',
  eigRational:list=>'유리수 근을 찾았어요: '+list+'. 특성다항식을 이 근으로 나눠 차수를 낮춰요.',
  eigNoRational:'유리수 근이 없어요.',
  eigQuad:q=>'남은 이차식 '+q+' = 0 을 근의 공식으로 풀어요.',
  eigQuadD:D=>'판별식 D = b² − 4c = '+D,
  eigComplex:'D < 0 이라서 실수 고윳값이 없어요. 고윳값은 켤레복소수 쌍이에요.',
  eigNumeric:q=>'남은 다항식 '+q+' = 0 은 유리수 근이 없어서 수치적으로 근사해요.',
  eigVec:l=>'λ = '+l+' 에 대해 (A − λI)v = 0 을 풀어요. 영공간의 기저가 고유벡터예요.',
  eigVecRes:(l,g)=>'λ = '+l+' 의 고유벡터예요. 자유변수가 '+g+'개라서 기하적 중복도는 '+g+'이에요.',
  eigMult:m=>'중복 '+m, chipDiag:'대각화 가능', chipNotDiag:'대각화 불가능', chipComplex:'복소 고윳값',
  eigLabelExact:'고윳값', eigLabelApprox:'근사 고윳값'
},
en:{
  swap:(c,r)=>'Move a nonzero entry of column '+c+' up to row '+r+' to use as the pivot.',
  scale:r=>'Divide row '+r+' by the pivot so the pivot becomes 1.',
  elim:c=>'Make every other entry of column '+c+' zero.',
  uNoPivot:c=>'Column '+c+' has no nonzero entry on or below the diagonal, so there is no pivot. The determinant is 0.',
  uSwap:'Swapping two rows changes the sign of the determinant.',
  uElim:c=>'Clear the entries below the pivot in column '+c+'. This does not change the determinant.',
  uDone:neg=>'The determinant of an upper triangular matrix is the product of its diagonal entries.'+(neg?' Rows were swapped an odd number of times, so flip the sign.':''),
  invFormula:'A 2×2 matrix can be inverted directly with the formula. It gives the same result as the elimination below.',
  invAug:'Append the identity matrix I on the right to form [A | I].',
  invSingular:'A zero row appeared on the left side, so it cannot become the identity. A has no inverse.',
  invNoneHead:'<strong>No inverse</strong><span>det(A) = 0, so A is not invertible.</span>',
  chipSingular:'Singular matrix',
  invDone:'The left side is now the identity. The right side is A⁻¹.',
  det1:'The determinant of a 1×1 matrix is its single entry.',
  det2:'For a 2×2 matrix, multiply along the main diagonal and subtract the product of the other diagonal.',
  det3Intro:'Expand by cofactors along row 1. The signs alternate + − +.',
  det3Minor:j=>'Delete row 1 and column '+j+'. The determinant of the remaining 2×2 matrix is M₁'+sub(j)+'.',
  det3Sum:'Multiply each entry by its minor, attach the sign, and add.',
  detNIntro:'Row-reduce to an upper triangular matrix, then multiply the diagonal entries.',
  chipNoInv:'Not invertible', chipInv:'Invertible',
  mulOk:(n,m,q)=>'A has '+n+' columns and B has '+n+' rows, so the product is defined. The result is '+m+'×'+q+'.',
  mulEntry:(i,j)=>'Multiply row '+i+' of A by column '+j+' of B entry by entry and add.',
  addIntro:'The matrices have the same size, so add the corresponding entries.',
  subIntro:'The matrices have the same size, so subtract the corresponding entries.',
  scalarIntro:k=>'Multiply every entry by k = '+k+'.',
  trRow:i=>'Row '+i+' of A becomes column '+i+' of Aᵀ.',
  rrefStart:'Start from the given matrix.',
  rrefAlready:'The matrix is already in reduced row echelon form.',
  rrefPiv:list=>'The pivots are in column '+list+'. The number of pivots is the rank.',
  rrefZero:'Every entry is 0, so there are no pivots.',
  chipPivCols:list=>'Pivot columns '+list,
  solAug:'Append b to the coefficient matrix A to form the augmented matrix [A | b].',
  solContra:(row,v)=>'Row '+row+' reads 0 = '+v+', which is a contradiction. The system has no solution.',
  solNoneHead:v=>'<strong>No solution</strong><span>Elimination produces the contradiction 0 = '+v+'.</span>',
  chipNone:'No solution',
  solUnique:'Every variable column has a pivot, so the solution is unique.',
  chipUnique:'Unique solution',
  solFree:(vars,n)=>vars+(n>1?' have no pivots and are free variables. Set them to parameters t and express the other variables.':' has no pivot and is a free variable. Set it to a parameter t and express the other variables.'),
  solInfHead:'<strong>Infinitely many solutions</strong>',
  chipFree:n=>n+' free variable'+(n>1?'s':''),
  dec:l=>'Decrease '+l, inc:l=>'Increase '+l,
  cell:(l,i,j)=>l+' row '+i+', column '+j,
  size:'Size', rows:'Rows', cols:'Cols',
  bCell:i=>'b row '+i,
  sys:(r,c)=>r+(r>1?' equations':' equation')+' · '+c+(c>1?' unknowns':' unknown')+' · Ax = b',
  errInput:'Check the highlighted cells. Only integers, fractions (1/3) and decimals (0.25) are allowed.',
  errFail:'The calculation failed. Please check the input.',
  stepsEmpty:'Enter values and the steps will appear here.',
  stepsLess:'Show fewer steps', stepsMore:n=>'Show '+n+' more step'+(n>1?'s':''), stepsCount:n=>n+' step'+(n>1?'s':''),
  copied:'LaTeX copied. Paste it into Overleaf, a Notion equation block or Word\'s equation editor.', copyFail:'Could not copy. Check your browser settings.',
  pow0:'Any square matrix to the power 0 is defined as the identity matrix I.',
  pow1:'Start with A¹ = A.',
  powStep:i=>'Multiply A'+sup(i-1)+' by A once more to get A'+sup(i)+'.',
  powNote:'n is an integer from 0 to 12.',
  errPow:'The exponent n must be an integer from 0 to 12.',
  rankDone:r=>'The number of pivots is the rank: rank(A) = '+r+'.',
  rankZero:'Every entry is 0, so there are no pivots and rank(A) = 0.',
  rankNullity:(c,r)=>'nullity(A) = (number of columns) − rank(A) = '+c+' − '+r+' = '+(c-r)+', the number of columns without a pivot.',
  rankPiv:list=>'Pivot columns: '+list, rankBasis:list=>'Column space basis: columns '+list+' of A',
  chipFull:'Full rank', chipDeficient:'Rank deficient',
  adj1:'The adjugate of a 1×1 matrix is defined as [1].',
  adjMinor:(i,j,sg)=>'Delete row '+i+' and column '+j+'; the determinant of what remains is the minor M'+ij(i-1,j-1)+'. Attach the sign '+sg+' to get the cofactor C'+ij(i-1,j-1)+'.',
  adjCof:'Collect the cofactors in their positions to form the cofactor matrix C.',
  adjT:'Transpose the cofactor matrix to get the adjugate adj(A) = Cᵀ.',
  adjInv:'Since det(A) ≠ 0, the inverse follows directly: A⁻¹ = adj(A) / det(A).',
  adjNoInv:'det(A) = 0, so there is no inverse, but the adjugate always exists. Here A·adj(A) = det(A)·I = O.',
  eigPoly:'Find the characteristic polynomial p(λ) = det(λI − A). Its roots are the eigenvalues.',
  eigPoly2:(tr,d)=>'For a 2×2 matrix, p(λ) = λ² − (trace)λ + (determinant) = λ² − ('+tr+')λ + ('+d+').',
  eigRational:list=>'Rational roots found: '+list+'. Divide the polynomial by these roots to lower its degree.',
  eigNoRational:'There are no rational roots.',
  eigQuad:q=>'Solve the remaining quadratic '+q+' = 0 with the quadratic formula.',
  eigQuadD:D=>'Discriminant D = b² − 4c = '+D,
  eigComplex:'D < 0, so there are no real eigenvalues. The eigenvalues are a complex conjugate pair.',
  eigNumeric:q=>'The remaining polynomial '+q+' = 0 has no rational roots, so its roots are approximated numerically.',
  eigVec:l=>'For λ = '+l+', solve (A − λI)v = 0. A basis of the null space gives the eigenvectors.',
  eigVecRes:(l,g)=>'Eigenvectors for λ = '+l+'. There '+(g>1?'are '+g+' free variables':'is 1 free variable')+', so the geometric multiplicity is '+g+'.',
  eigMult:m=>'multiplicity '+m, chipDiag:'Diagonalizable', chipNotDiag:'Not diagonalizable', chipComplex:'Complex eigenvalues',
  eigLabelExact:'Eigenvalues', eigLabelApprox:'Approximate eigenvalues'
}};
const t=(k,...a)=>{const v=STR[LANG][k];return typeof v==='function'?v(...a):v};

/* ---------- 분수 ---------- */
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a}
class F{
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}const g=gcd(n,d)||1n;this.n=n/g;this.d=d/g}
  add(o){return new F(this.n*o.d+o.n*this.d,this.d*o.d)}
  sub(o){return new F(this.n*o.d-o.n*this.d,this.d*o.d)}
  mul(o){return new F(this.n*o.n,this.d*o.d)}
  div(o){return new F(this.n*o.d,this.d*o.n)}
  neg(){return new F(-this.n,this.d)}
  abs(){return new F(this.n<0n?-this.n:this.n,this.d)}
  isZero(){return this.n===0n}
  isOne(){return this.n===1n&&this.d===1n}
  isNeg(){return this.n<0n}
}
const Z=new F(0n), ONE=new F(1n);

function parseF(raw){
  const s=String(raw).trim().replace(/[−–]/g,'-').replace(/\s+/g,'');
  if(s==='') return Z;
  let m=s.match(/^([+-]?)(\d+)\/(\d+)$/);
  if(m){ if(/^0+$/.test(m[3])) return null; return new F(BigInt((m[1]==='-'?'-':'')+m[2]),BigInt(m[3])); }
  m=s.match(/^([+-]?)(\d+)?(?:\.(\d*))?$/);
  if(!m||(!m[2]&&!m[3])) return null;
  const fr=m[3]||'';
  return new F(BigInt((m[1]==='-'?'-':'')+(m[2]||'0')+fr),10n**BigInt(fr.length));
}

/* ---------- 표시 ---------- */
let MODE='frac';
function decStr(f){const v=Number(f.n)/Number(f.d);let s=String(Math.round(v*1e4)/1e4);if(s==='-0')s='0';return s.replace('-','−')}
function txt(f){
  if(MODE==='dec'&&f.d!==1n) return decStr(f);
  const s=f.isNeg()?'−':'', a=f.isNeg()?-f.n:f.n;
  return f.d===1n? s+a : s+a+'/'+f.d;
}
function html(f){
  if(MODE==='dec'||f.d===1n) return esc(txt(f));
  const s=f.isNeg()?'−':'', a=f.isNeg()?-f.n:f.n;
  return s+'<span class="fr"><span>'+a+'</span><span>'+f.d+'</span></span>';
}
function tex(f){
  if(MODE==='dec'&&f.d!==1n) return decStr(f).replace('−','-');
  if(f.d===1n) return f.n.toString();
  const a=f.isNeg()?-f.n:f.n;
  return (f.isNeg()?'-':'')+'\\frac{'+a+'}{'+f.d+'}';
}
const p=f=>f.isNeg()?'('+txt(f)+')':txt(f);
const coef=f=>(f.d!==1n||f.isNeg())?'('+txt(f)+')':txt(f);
const coefAbs=f=>{const a=f.abs();return a.isOne()?'':(a.d===1n?txt(a):'('+txt(a)+')')};
const bm=M=>'\\begin{bmatrix} '+M.map(r=>r.map(tex).join(' & ')).join(' \\\\ ')+' \\end{bmatrix}';
function mx(M,o){
  o=o||{};const c=M[0].length,sep=o.sep==null?-1:o.sep;
  let h='<span class="mx '+(o.cls||'')+'"><span class="mx-g" style="grid-template-columns:repeat('+c+',auto)">';
  M.forEach(r=>r.forEach((v,j)=>{h+='<span class="mx-c'+(j===sep?' sep':'')+'">'+html(v)+'</span>'}));
  return h+'</span></span>';
}
const eq=s=>'<span class="eq">'+s+'</span>';
const snap=M=>M.map(r=>r.slice());

/* ---------- 소거 ---------- */
function gj(M0,split){
  const M=snap(M0),R=M.length,C=M[0].length,steps=[],piv=[];let r=0;
  for(let c=0;c<split&&r<R;c++){
    let pr=-1;
    for(let i=r;i<R;i++){ if(!M[i][c].isZero()){ if(pr<0)pr=i; if(M[i][c].isOne()){pr=i;break} } }
    if(pr<0) continue;
    if(pr!==r){ [M[pr],M[r]]=[M[r],M[pr]]; steps.push({ops:['R'+sub(r+1)+' ↔ R'+sub(pr+1)],t:t('swap',c+1,r+1),M:snap(M)}); }
    const pv=M[r][c];
    if(!pv.isOne()){ const iv=ONE.div(pv); M[r]=M[r].map(x=>x.mul(iv)); steps.push({ops:['R'+sub(r+1)+' ← '+coef(iv)+'R'+sub(r+1)],t:t('scale',r+1),M:snap(M)}); }
    const ops=[];
    for(let i=0;i<R;i++){
      if(i===r) continue; const f=M[i][c]; if(f.isZero()) continue;
      M[i]=M[i].map((x,j)=>x.sub(f.mul(M[r][j])));
      ops.push('R'+sub(i+1)+' ← R'+sub(i+1)+' '+(f.isNeg()?'+':'−')+' '+coefAbs(f)+'R'+sub(r+1));
    }
    if(ops.length) steps.push({ops,t:t('elim',c+1),M:snap(M)});
    piv.push(c); r++;
  }
  return {M,steps,piv,rank:r};
}
function upper(A0){
  const M=snap(A0),n=M.length,steps=[];let sign=1;
  for(let c=0;c<n;c++){
    let pr=-1; for(let i=c;i<n;i++) if(!M[i][c].isZero()){pr=i;break}
    if(pr<0){ steps.push({t:t('uNoPivot',c+1),m:mx(M)}); return {det:Z,steps}; }
    if(pr!==c){ [M[pr],M[c]]=[M[c],M[pr]]; sign=-sign; steps.push({ops:['R'+sub(c+1)+' ↔ R'+sub(pr+1)],t:t('uSwap'),m:mx(M)}); }
    const ops=[];
    for(let i=c+1;i<n;i++){ const f=M[i][c].div(M[c][c]); if(f.isZero()) continue; M[i]=M[i].map((x,j)=>x.sub(f.mul(M[c][j]))); ops.push('R'+sub(i+1)+' ← R'+sub(i+1)+' '+(f.isNeg()?'+':'−')+' '+coefAbs(f)+'R'+sub(c+1)); }
    if(ops.length) steps.push({ops,t:t('uElim',c+1),m:mx(M)});
  }
  let d=sign<0?ONE.neg():ONE; M.forEach((r,i)=>{d=d.mul(r[i])});
  steps.push({t:t('uDone',sign<0),m:eq('det(A) = '+(sign<0?'−':'')+M.map((r,i)=>p(r[i])).join('·')+' = '+txt(d))});
  return {det:d,steps};
}
const det2=m=>m[0][0].mul(m[1][1]).sub(m[0][1].mul(m[1][0]));
function lin(c0,terms){
  let s=c0.isZero()?'':txt(c0);
  terms.forEach(([f,name])=>{ if(f.isZero())return; const co=coefAbs(f);
    s = s==='' ? (f.isNeg()?'−':'')+co+name : s+' '+(f.isNeg()?'−':'+')+' '+co+name; });
  return s||'0';
}
function entrySteps(R,C,fn){const out=[];for(let i=0;i<R;i++)for(let j=0;j<C;j++)out.push(fn(i,j));return out}

/* ---------- 연산 ---------- */
const OPS={
  inverse:{square:true,
    run({A}){
      const n=A.length,steps=[];
      const aug=A.map((r,i)=>[...r,...r.map((_,j)=>i===j?ONE:Z)]);
      if(n===2){const d=det2(A); if(!d.isZero()){const adj=[[A[1][1],A[0][1].neg()],[A[1][0].neg(),A[0][0]]];
        steps.push({t:t('invFormula'),m:eq('ad − bc = '+p(A[0][0])+'·'+p(A[1][1])+' − '+p(A[0][1])+'·'+p(A[1][0])+' = '+txt(d))+'<span class="eq">A⁻¹ = '+html(ONE.div(d))+' ·</span>'+mx(adj)});}}
      steps.push({t:t('invAug'),m:mx(aug,{sep:n})});
      const g=gj(aug,n);
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M,{sep:n})}));
      if(g.rank<n){
        steps.push({t:t('invSingular')});
        return {head:'<div class="none">'+t('invNoneHead')+'</div>',chips:[['bad',t('chipSingular')]],steps};
      }
      const inv=g.M.map(r=>r.slice(n));
      steps.push({t:t('invDone')});
      return {head:'<div class="eqline"><span class="lhs">A⁻¹ =</span>'+mx(inv,{cls:'big'})+'</div>',chips:[['','det(A) = '+txt(upper(A).det)],['ok',t('chipInv')]],latex:bm(inv),steps};
    }},
  det:{square:true,
    run({A}){
      const n=A.length;let steps=[],d;
      if(n===1){d=A[0][0];steps.push({t:t('det1')});}
      else if(n===2){d=det2(A);steps.push({t:t('det2'),m:eq('det(A) = ad − bc = '+p(A[0][0])+'·'+p(A[1][1])+' − '+p(A[0][1])+'·'+p(A[1][0])+' = '+txt(d))});}
      else if(n===3){
        const a=A[0],mins=[0,1,2].map(j=>A.slice(1).map(r=>r.filter((_,k)=>k!==j))),mv=mins.map(det2);
        steps.push({t:t('det3Intro'),m:eq('det(A) = a₁₁M₁₁ − a₁₂M₁₂ + a₁₃M₁₃')});
        mins.forEach((m,j)=>steps.push({t:t('det3Minor',j+1),m:mx(m)+eq('M₁'+sub(j+1)+' = '+p(m[0][0])+'·'+p(m[1][1])+' − '+p(m[0][1])+'·'+p(m[1][0])+' = '+txt(mv[j]))}));
        d=a[0].mul(mv[0]).sub(a[1].mul(mv[1])).add(a[2].mul(mv[2]));
        steps.push({t:t('det3Sum'),m:eq('det(A) = '+p(a[0])+'·'+p(mv[0])+' − '+p(a[1])+'·'+p(mv[1])+' + '+p(a[2])+'·'+p(mv[2])+' = '+txt(d))});
      } else {
        steps.push({t:t('detNIntro'),m:mx(A)});
        const u=upper(A);d=u.det;steps=steps.concat(u.steps);
      }
      return {head:'<div class="eqline"><span class="lhs">det(A) =</span><span class="scalar">'+html(d)+'</span></div>',chips:[d.isZero()?['bad',t('chipNoInv')]:['ok',t('chipInv')]],latex:tex(d),steps};
    }},
  mul:{B:'mul',sym:'×',
    run({A,B}){
      const m=A.length,n=B.length,q=B[0].length;
      const C=A.map((r,i)=>B[0].map((_,j)=>r.reduce((s,a,k)=>s.add(a.mul(B[k][j])),Z)));
      const steps=[{t:t('mulOk',n,m,q)}].concat(
        entrySteps(m,q,(i,j)=>({ops:['c'+ij(i,j)],t:t('mulEntry',i+1,j+1),m:eq(A[i].map((a,k)=>p(a)+'·'+p(B[k][j])).join(' + ')+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">AB =</span>'+mx(C,{cls:'big'})+'</div>',chips:[['',m+'×'+n+' · '+n+'×'+q+' → '+m+'×'+q]],latex:bm(C),steps};
    }},
  add:{B:'same',sym:'+',
    run({A,B}){
      const C=A.map((r,i)=>r.map((a,j)=>a.add(B[i][j])));
      const steps=[{t:t('addIntro')}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(A[i][j])+' + '+p(B[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">A + B =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  sub:{B:'same',sym:'−',
    run({A,B}){
      const C=A.map((r,i)=>r.map((a,j)=>a.sub(B[i][j])));
      const steps=[{t:t('subIntro')}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(A[i][j])+' − '+p(B[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">A − B =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  scalar:{k:true,
    run({A,k}){
      const C=A.map(r=>r.map(a=>a.mul(k)));
      const steps=[{t:t('scalarIntro',txt(k))}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(k)+'·'+p(A[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">kA =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  transpose:{
    run({A}){
      const T=A[0].map((_,j)=>A.map(r=>r[j]));
      const steps=A.map((r,i)=>({t:t('trRow',i+1),m:mx([r])+'<span class="eq">→</span>'+mx(r.map(x=>[x]))}));
      return {head:'<div class="eqline"><span class="lhs">Aᵀ =</span>'+mx(T,{cls:'big'})+'</div>',chips:[['',A.length+'×'+A[0].length+' → '+A[0].length+'×'+A.length]],latex:bm(T),steps};
    }},
  rref:{
    run({A}){
      const g=gj(A,A[0].length),steps=[{t:t('rrefStart'),m:mx(A)}];
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M)}));
      if(!g.steps.length) steps.push({t:t('rrefAlready')});
      steps.push({t:g.rank?t('rrefPiv',g.piv.map(c=>c+1).join(', ')):t('rrefZero')});
      return {head:'<div class="eqline"><span class="lhs">RREF(A) =</span>'+mx(g.M,{cls:'big'})+'</div>',chips:[['','rank = '+g.rank]].concat(g.rank?[['',t('chipPivCols',g.piv.map(c=>c+1).join(', '))]]:[]),latex:bm(g.M),steps};
    }},
  solve:{vec:true,
    run({A,b}){
      const n=A[0].length,aug=A.map((r,i)=>[...r,b[i]]),xs=Array.from({length:n},(_,j)=>'x'+sub(j+1));
      const steps=[{t:t('solAug'),m:mx(aug,{sep:n})}];
      const g=gj(aug,n);
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M,{sep:n})}));
      const bad=g.M.findIndex(r=>r.slice(0,n).every(x=>x.isZero())&&!r[n].isZero());
      if(bad>=0){
        steps.push({t:t('solContra',bad+1,txt(g.M[bad][n]))});
        return {head:'<div class="none">'+t('solNoneHead',esc(txt(g.M[bad][n])))+'</div>',chips:[['bad',t('chipNone')]],steps};
      }
      if(g.rank===n){
        const x=xs.map((_,j)=>g.M[g.piv.indexOf(j)][n]);
        const lines=xs.map((nm,j)=>nm+' = '+txt(x[j]));
        steps.push({t:t('solUnique'),m:'<div class="sol">'+lines.map(esc).join('<br>')+'</div>'});
        return {head:'<div class="eqline"><span class="lhs">x =</span>'+mx(x.map(v=>[v]),{cls:'big'})+'</div><div class="sol">'+lines.map(l=>'<div>'+esc(l)+'</div>').join('')+'</div>',chips:[['ok',t('chipUnique')]],latex:bm(x.map(v=>[v])),steps};
      }
      const free=xs.map((_,j)=>j).filter(j=>!g.piv.includes(j)),tn=j=>'t'+sub(free.indexOf(j)+1);
      const lines=xs.map((nm,j)=>{
        if(free.includes(j)) return nm+' = '+tn(j);
        const r=g.M[g.piv.indexOf(j)];
        return nm+' = '+lin(r[n],free.map(f=>[r[f].neg(),tn(f)]));
      });
      steps.push({t:t('solFree',free.map(f=>xs[f]).join(', '),free.length),m:'<div class="sol">'+lines.map(esc).join('<br>')+'</div>'});
      return {head:'<div class="none">'+t('solInfHead')+'</div><div class="sol">'+lines.map(l=>'<div>'+esc(l)+'</div>').join('')+'</div>',chips:[['warn',t('chipFree',free.length)],['','rank = '+g.rank]],steps};
    }}
};

/* ---------- 거듭제곱 · 랭크 · 수반행렬 · 고윳값 ---------- */
const ident=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?ONE:Z));
const mmul=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,a,k)=>s.add(a.mul(B[k][j])),Z)));
const trace=A=>A.reduce((s,r,i)=>s.add(r[i]),Z);
const detF=A=>upper(A).det;
const minorOf=(A,i,j)=>A.filter((_,r)=>r!==i).map(r=>r.filter((_,c)=>c!==j));
const col=v=>mx(v.map(x=>[x]));
const eqline=(lhs,inner)=>'<div class="eqline"><span class="lhs">'+lhs+'</span>'+inner+'</div>';
function charPoly(A){ // Faddeev–LeVerrier: p(λ)=λⁿ+c[n-1]λⁿ⁻¹+…+c[0], 정확한 분수
  const n=A.length,c=Array(n+1).fill(Z);c[n]=ONE;let M=A.map(r=>r.map(()=>Z));
  for(let k=1;k<=n;k++){const AM=mmul(A,M);M=AM.map((r,i)=>r.map((x,j)=>i===j?x.add(c[n-k+1]):x));c[n-k]=trace(mmul(A,M)).div(new F(BigInt(k))).neg();}
  return c;
}
const peval=(c,x)=>{let r=Z;for(let i=c.length-1;i>=0;i--)r=r.mul(x).add(c[i]);return r};
function deflate(c,r){const n=c.length-1,q=Array(n).fill(Z);q[n-1]=c[n];for(let i=n-1;i>=1;i--)q[i-1]=c[i].add(r.mul(q[i]));return q;}
function polyStr(c,latex){
  const n=c.length-1;let s='';
  for(let k=n;k>=0;k--){const a=c[k];if(a.isZero())continue;const m=a.abs();
    let co=(k>0&&m.isOne())?'':(latex?tex(m):(m.d===1n?txt(m):'('+txt(m)+')'));
    const v=k===0?'':(latex?('\\lambda'+(k>1?'^{'+k+'}':'')):('λ'+(k>1?sup(k):'')));
    const term=co+v;
    if(s==='')s=(a.isNeg()?(latex?'-':'−'):'')+term;else s+=' '+(a.isNeg()?(latex?'-':'−'):'+')+' '+term;}
  return s||'0';
}
function isqrt(n){if(n<2n)return n;let x=BigInt(Math.floor(Math.sqrt(Number(n))));while(x*x>n)x--;while((x+1n)*(x+1n)<=n)x++;return x;}
function sqrtSimp(D){ // D>0: √D = k·√m (k 분수, m 정수)
  let m=D.n*D.d,s=1n;
  for(let f=2n;f*f<=m&&f<100000n;f++){const ff=f*f;while(m%ff===0n){m/=ff;s*=f}}
  const r=isqrt(m);if(r*r===m){s*=r;m=1n}
  return {k:new F(s,D.d),m};
}
function divisorsOf(L){ // L의 약수 (작은 소인수 기준, 최대 400개)
  const fac=[];let m=L;for(let f=2n;f*f<=m&&f<100000n;f++){let e=0;while(m%f===0n){m/=f;e++}if(e)fac.push([f,e])}
  if(m>1n)fac.push([m,1]);
  let ds=[1n];for(const [f,e] of fac){const nd=[];for(const d of ds){let x=d;for(let i=0;i<=e;i++){nd.push(x);x*=f}}ds=nd;if(ds.length>400)break}
  return ds.sort((a,b)=>(a<b?-1:a>b?1:0));
}
function dkRoots(a){ // Durand–Kerner, a: 실수 계수(낮은 차수부터, 최고차 1)
  const m=a.length-1;if(m<1)return[];
  const cm=(x,y)=>[x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]],cs=(x,y)=>[x[0]-y[0],x[1]-y[1]],ca=(x,y)=>[x[0]+y[0],x[1]+y[1]];
  const cd=(x,y)=>{const d=y[0]*y[0]+y[1]*y[1]||1e-300;return[(x[0]*y[0]+x[1]*y[1])/d,(x[1]*y[0]-x[0]*y[1])/d]};
  const pe=z=>{let r=[1,0];for(let i=m-1;i>=0;i--)r=ca(cm(r,z),[a[i],0]);return r};
  let z=Array.from({length:m},(_,k)=>{let p=[1,0];for(let i=0;i<=k;i++)p=cm(p,[0.4,0.9]);return p});
  for(let it=0;it<2000;it++){let mx=0;const nz=z.map((zi,i)=>{let den=[1,0];z.forEach((zj,j)=>{if(j!==i)den=cm(den,cs(zi,zj))});const d=cd(pe(zi),den);mx=Math.max(mx,Math.hypot(d[0],d[1]));return cs(zi,d)});z=nz;if(mx<1e-15)break}
  return z.map(r=>Math.abs(r[1])<1e-7*(1+Math.abs(r[0]))?[r[0],0]:r);
}
function pmStr(re,k,m,sg,im){ // re ± k√m 을 (a ± b√m)/d 꼴로. im이면 허수 단위 i를 붙여요
  const D=re.d*k.d/gcd(re.d,k.d),a=re.n*(D/re.d),b=k.n*(D/k.d),rad=m===1n?'':'√'+m;
  let bs=(b===1n&&(rad||im))?'':String(b);
  let tail=bs+rad+(im?((rad?' ':'')+'i'):'');
  const core=(a===0n?'':a+' ')+sg+' '+tail;
  return D===1n?core:'('+core+')/'+D;
}
const dec4=x=>{let s=String(Math.round(x*1e4)/1e4);if(s==='-0')s='0';return s.replace('-','−')};
function nullBasis(M){ // Mv=0 의 기저 (정확)
  const n=M[0].length,g=gj(M,n),free=[];for(let j=0;j<n;j++)if(!g.piv.includes(j))free.push(j);
  return {g,vecs:free.map(f=>{const v=Array(n).fill(Z);v[f]=ONE;g.piv.forEach((pc,r)=>{v[pc]=g.M[r][f].neg()});
    let L=1n;v.forEach(x=>{L=L*x.d/gcd(L,x.d)});let G=0n;v.forEach(x=>{G=gcd(G,x.n*L/x.d)});const sc=new F(L,G||1n); // 분모를 없애고 최대공약수로 나눠 정수 벡터로
    return v.map(x=>x.mul(sc))})};
}
const OPS2={
  power:{square:true,k:true,kint:true,
    run({A,k}){
      const n=Number(k.n),N=A.length,steps=[];
      if(n===0){const I=ident(N);steps.push({t:t('pow0'),m:mx(I)});return {head:eqline('A⁰ =',mx(I,{cls:'big'})),chips:[['','n = 0']],latex:bm(I),steps};}
      let P=A;steps.push({t:t('pow1'),m:mx(A)});
      for(let i=2;i<=n;i++){P=mmul(P,A);steps.push({t:t('powStep',i),ops:['A'+sup(i)+' = A'+sup(i-1)+'·A'],m:mx(P)});}
      return {head:eqline('A'+sup(n)+' =',mx(P,{cls:'big'})),chips:[['','n = '+n]],latex:bm(P),steps,data:{n}};
    }},
  rank:{
    run({A}){
      const m=A.length,n=A[0].length,g=gj(A,n),r=g.rank,steps=[{t:t('rrefStart'),m:mx(A)}];
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M)}));
      const pl=g.piv.map(c=>c+1).join(', ');
      steps.push({t:r?t('rankDone',r):t('rankZero'),m:mx(g.M)});
      steps.push({t:t('rankNullity',n,r)});
      const sol='<div class="sol"><div>nullity(A) = '+(n-r)+'</div>'+(r?'<div>'+esc(t('rankPiv',pl))+'</div><div>'+esc(t('rankBasis',pl))+'</div>':'')+'</div>';
      const full=r===Math.min(m,n);
      return {head:eqline('rank(A) =','<span class="scalar">'+r+'</span>')+sol,chips:[['',m+'×'+n],full?['ok',t('chipFull')]:['warn',t('chipDeficient')]],latex:String(r),steps,data:{rank:r,nullity:n-r,piv:g.piv}};
    }},
  adj:{square:true,
    run({A}){
      const n=A.length,steps=[];
      if(n===1){const adj=[[ONE]],d=A[0][0];steps.push({t:t('adj1')});steps.push({t:d.isZero()?t('adjNoInv'):t('adjInv')});return {head:eqline('adj(A) =',mx(adj,{cls:'big'})),chips:[['','det(A) = '+txt(d)],d.isZero()?['bad',t('chipNoInv')]:['ok',t('chipInv')]],latex:bm(adj),steps,data:{adj:[['1/1']],det:d.n+'/'+d.d}};}
      const C=A.map((r,i)=>r.map((_,j)=>{const mn=detF(minorOf(A,i,j));return (i+j)%2?mn.neg():mn}));
      A.forEach((r,i)=>r.forEach((_,j)=>{const mn=minorOf(A,i,j),md=detF(mn),sg=(i+j)%2?'−':'+';
        steps.push({ops:['C'+ij(i,j)],t:t('adjMinor',i+1,j+1,sg),m:mx(mn)+eq('M'+ij(i,j)+' = '+txt(md)+',  C'+ij(i,j)+' = '+sg+p(md)+' = '+txt(C[i][j]))});}));
      steps.push({t:t('adjCof'),m:mx(C)});
      const adj=C[0].map((_,j)=>C.map(r=>r[j]));
      steps.push({t:t('adjT'),m:mx(adj)});
      const d=detF(A);
      if(!d.isZero()){const inv=adj.map(r=>r.map(x=>x.div(d)));steps.push({t:t('adjInv'),m:eq('A⁻¹ = '+html(ONE.div(d))+' ·')+mx(adj)+eq('=')+mx(inv)});}
      else steps.push({t:t('adjNoInv')});
      return {head:eqline('adj(A) =',mx(adj,{cls:'big'})),chips:[['','det(A) = '+txt(d)],d.isZero()?['bad',t('chipNoInv')]:['ok',t('chipInv')]],latex:bm(adj),steps,data:{adj:adj.map(r=>r.map(x=>x.n+'/'+x.d)),det:d.n+'/'+d.d}};
    }},
  eigen:{square:true,
    run({A}){
      const n=A.length,steps=[],c=charPoly(A);
      const data={poly:c.map(x=>x.n+'/'+x.d),rational:[],quad:null,numeric:[],vecs:[]};
      steps.push({t:t('eigPoly'),m:eq('p(λ) = '+polyStr(c))});
      if(n===2)steps.push({t:t('eigPoly2',txt(trace(A)),txt(detF(A)))});
      // 유리수 근: 수치 근을 유리수로 맞춰 보고 정확히 검산
      let q=c.slice(),found=[];
      let L=1n;c.forEach(x=>{L=L*x.d/gcd(L,x.d)});const ds=divisorsOf(L);
      for(let guard=0;guard<n&&q.length>1;guard++){
        let hit=null;
        if(q[0].isZero())hit=Z;
        else{const num=dkRoots(q.map(x=>Number(x.n)/Number(x.d)));
          outer:for(const z of num){if(Math.abs(z[1])>1e-3*(1+Math.abs(z[0])))continue;for(const d of ds){const r=new F(BigInt(Math.round(z[0]*Number(d))),d);if(peval(q,r).isZero()){hit=r;break outer}}}}
        if(hit===null)break;
        const f=found.find(x=>x[0].sub(hit).isZero());if(f)f[1]++;else found.push([hit,1]);
        q=deflate(q,hit);
      }
      const vals=[];let complex=false,approx=false;
      if(q.length===3){ // 남은 이차식 λ²+bλ+c
        const b=q[1],cc=q[0],D=b.mul(b).sub(cc.mul(new F(4n))),re=b.neg().div(new F(2n));
        steps.push({t:t('eigQuad',polyStr(q)),m:eq(t('eigQuadD',txt(D)))});
        const S_=D.isZero()?{k:Z,m:1n}:sqrtSimp(D.abs()),k=S_.k.div(new F(2n));
        if(!D.isNeg()&&S_.m===1n){ // 사실은 유리수 근 (중근 포함)
          for(const r of [re.add(k),re.sub(k)]){const f=found.find(x=>x[0].sub(r).isZero());if(f)f[1]++;else found.push([r,1]);}
          q=[ONE];
          steps.push({m:eq('λ = '+txt(re)+' ± '+txt(k)+' = '+txt(re.add(k))+', '+txt(re.sub(k)))});
        } else {
          const num=Number(re.n)/Number(re.d),kn=Number(k.n)/Number(k.d)*Math.sqrt(Number(S_.m));
          data.quad={D:D.n+'/'+D.d,re:re.n+'/'+re.d,k:k.n+'/'+k.d,m:String(S_.m)};
          if(D.isNeg()){complex=true;steps.push({t:t('eigComplex')});
            const basei=pmStr(re,k,S_.m,'±',true);
            vals.push({s:basei,pair:true,approx:dec4(num)+' ± '+dec4(kn)+'i'});
            steps.push({m:eq('λ = '+(re.isZero()?'':txt(re)+' ')+'± '+(k.isOne()?'':coef(k))+'√(−'+txt(D.abs())+') = '+basei)});}
          else{const pl=pmStr(re,k,S_.m,'+'),mi=pmStr(re,k,S_.m,'−');
            vals.push({s:pl,approx:dec4(num+kn),irr:true},{s:mi,approx:dec4(num-kn),irr:true});
            steps.push({m:eq('λ = '+pmStr(re,k,S_.m,'±')+'  ≈ '+dec4(num+kn)+', '+dec4(num-kn))});}
        }
      } else if(q.length>3){
        approx=true;steps.push({t:t('eigNumeric',polyStr(q))});
        dkRoots(q.map(x=>Number(x.n)/Number(x.d))).forEach(z=>{if(z[1]!==0)complex=true;vals.push({s:'≈ '+(z[1]===0?dec4(z[0]):dec4(z[0])+(z[1]<0?' − ':' + ')+dec4(Math.abs(z[1]))+'i'),approx:true});data.numeric.push([z[0],z[1]])});
      }
      found.sort((x,y)=>{const d=x[0].sub(y[0]);return d.isNeg()?-1:d.isZero()?0:1});
      data.rational=found.map(([r,m])=>[r.n+'/'+r.d,m]);
      const fstr=found.map(([r,m])=>'λ = '+txt(r)+(m>1?' ('+t('eigMult',m)+')':'')).join(', ');
      steps.push({t:found.length?t('eigRational',fstr):t('eigNoRational')});
      found.slice().reverse().forEach(([r,m])=>{for(let i=0;i<m;i++)vals.unshift({exact:r,s:txt(r)})});
      // 고유벡터 (정확한 유리수 고윳값만)
      let geoSum=0;const vecHtml=[];
      found.forEach(([r,m])=>{const Ml=A.map((row,i)=>row.map((x,j)=>i===j?x.sub(r):x));const nb=nullBasis(Ml);
        steps.push({t:t('eigVec',txt(r)),m:eq('A − ('+txt(r)+')I =')+mx(Ml)+eq('→')+mx(nb.g.M)});
        steps.push({t:t('eigVecRes',txt(r),nb.vecs.length),m:nb.vecs.map((v,i)=>eq('v'+sub(i+1)+' =')+col(v)).join('')});
        geoSum+=nb.vecs.length;vecHtml.push('<div>λ = '+esc(txt(r))+': '+nb.vecs.map(v=>col(v)).join(' ')+'</div>');
        data.vecs.push([r.n+'/'+r.d,nb.vecs.map(v=>v.map(x=>x.n+'/'+x.d))]);});
      const allExact=vals.every(v=>v.exact);
      const label=approx?t('eigLabelApprox'):t('eigLabelExact');
      let list=vals.map(v=>v.s).join(', ');
      let head='<div class="eqline"><span class="lhs">λ =</span><span class="scalar sm">'+esc(list)+'</span></div>';
      const ap=vals.filter(v=>v.approx&&!approx).map(v=>v.approx).filter((x,i,a)=>a.indexOf(x)===i);
      if(ap.length)head+='<div class="sol"><div>≈ '+esc(ap.join(', '))+'</div></div>';
      if(vecHtml.length)head+='<div class="sol">'+vecHtml.join('')+'</div>';
      const chips=[['','tr(A) = '+txt(trace(A))],['','det(A) = '+txt(detF(A))]];
      if(complex)chips.push(['warn',t('chipComplex')]);
      else if(allExact)chips.push(geoSum===n?['ok',t('chipDiag')]:['bad',t('chipNotDiag')]);
      else if(!approx&&new Set(vals.map(v=>v.s)).size===n)chips.push(['ok',t('chipDiag')]);
      return {head,chips,latex:polyStr(c,true),steps,data};
    }}
};
Object.assign(OPS,OPS2);
const ORDER=['inverse','det','mul','add','sub','scalar','transpose','rref','solve','rank','power','adj','eigen'];

const EX={
  inverse:{A:[[2,1,1],[1,3,2],[1,0,0]]},
  det:{A:[[2,-1,0],[1,3,2],[0,1,4]]},
  mul:{A:[[1,2,0],[3,-1,4]],B:[[2,1],[0,3],[1,-2]]},
  add:{A:[[1,2],[3,4]],B:[[5,-1],[0,'1/2']]},
  sub:{A:[[1,2],[3,4]],B:[[5,-1],[0,'1/2']]},
  scalar:{A:[[2,-1],[4,'1/3']],k:'3/2'},
  transpose:{A:[[1,2,3],[4,5,6]]},
  rref:{A:[[1,2,-1,3],[2,4,1,0],[-1,-2,2,1]]},
  solve:{A:[[2,1,-1],[-3,-1,2],[-2,1,2]],b:[8,-11,-3]},
  rank:{A:[[1,2,-1,3],[2,4,1,0],[-1,-2,2,1]]},
  power:{A:[[1,1],[1,0]],k:'5'},
  adj:{A:[[2,-1,0],[1,3,2],[0,1,4]]},
  eigen:{A:[[4,1],[2,3]]}
};

/* ---------- 상태 ---------- */
const blank=()=>Array.from({length:MAX},()=>Array(MAX).fill(''));
const S={op:'inverse',A:{r:3,c:3,v:blank()},B:{r:3,c:3,v:blank()},b:Array(MAX).fill(''),k:'2',touched:false,showAll:false,latex:null};

function loadExample(op){
  const e=EX[op];
  S.A.v=blank(); S.A.r=e.A.length; S.A.c=e.A[0].length; e.A.forEach((r,i)=>r.forEach((x,j)=>{S.A.v[i][j]=String(x)}));
  if(e.B){S.B.v=blank();S.B.r=e.B.length;S.B.c=e.B[0].length;e.B.forEach((r,i)=>r.forEach((x,j)=>{S.B.v[i][j]=String(x)}));}
  if(e.b){S.b=Array(MAX).fill('');e.b.forEach((x,i)=>{S.b[i]=String(x)});}
  if(e.k) S.k=e.k;
  S.touched=false;
}
const clamp=v=>Math.max(1,Math.min(MAX,v));
function fitDims(){
  const o=OPS[S.op];
  if(o.square) S.A.c=S.A.r;
  if(o.B==='mul') S.B.r=S.A.c;
  if(o.B==='same'){S.B.r=S.A.r;S.B.c=S.A.c;}
}

/* ---------- 입력 화면 ---------- */
function stepper(m,d,label,val){
  return '<span class="stp"><span class="stp-l">'+label+'</span>'+
    '<button type="button" data-act="dec" data-m="'+m+'" data-d="'+d+'" aria-label="'+esc(t('dec',label))+'"'+(val<=1?' disabled':'')+'>−</button>'+
    '<output>'+val+'</output>'+
    '<button type="button" data-act="inc" data-m="'+m+'" data-d="'+d+'" aria-label="'+esc(t('inc',label))+'"'+(val>=MAX?' disabled':'')+'>+</button></span>';
}
function editor(m,T,ctrl,label){
  let cells='';
  for(let i=0;i<T.r;i++)for(let j=0;j<T.c;j++)
    cells+='<input id="'+m+'-'+i+'-'+j+'" data-m="'+m+'" data-i="'+i+'" data-j="'+j+'" autocomplete="off" spellcheck="false" placeholder="0" value="'+esc(T.v[i][j])+'" aria-label="'+esc(t('cell',label,i+1,j+1))+'">';
  return '<div class="ed"><div class="ed-head"><span class="ed-name">'+label+'<span class="dim">'+T.r+' × '+T.c+'</span></span><span class="ctrls">'+ctrl+'</span></div>'+
    '<div class="ed-scroll"><div class="brk"><div class="cells" style="grid-template-columns:repeat('+T.c+',var(--cell))">'+cells+'</div></div></div></div>';
}
function renderInputs(){
  const o=OPS[S.op];let h='<div class="eqrow">';
  const aCtrl=o.square?stepper('A','n',t('size'),S.A.r):stepper('A','r',t('rows'),S.A.r)+stepper('A','c',t('cols'),S.A.c);
  if(o.k&&!o.kint) h+='<div class="ed"><div class="ed-head"><label class="ed-name" for="k">k</label></div><input id="k" class="kin" data-m="k" autocomplete="off" spellcheck="false" value="'+esc(S.k)+'"></div><span class="opsym" aria-hidden="true">·</span>';
  h+=editor('A',S.A,aCtrl,'A');
  if(o.kint) h+='<span class="opsym" aria-hidden="true">^</span><div class="ed"><div class="ed-head"><label class="ed-name" for="k">n</label></div><input id="k" class="kin" data-m="k" inputmode="numeric" autocomplete="off" spellcheck="false" value="'+esc(S.k)+'"></div>';
  if(o.B){ h+='<span class="opsym" aria-hidden="true">'+o.sym+'</span>'+editor('B',S.B,o.B==='mul'?stepper('B','c',t('cols'),S.B.c):'','B'); }
  if(o.vec){
    let cells='';for(let i=0;i<S.A.r;i++) cells+='<input id="b-'+i+'" data-m="b" data-i="'+i+'" autocomplete="off" spellcheck="false" placeholder="0" value="'+esc(S.b[i])+'" aria-label="'+esc(t('bCell',i+1))+'">';
    h+='<span class="opsym" aria-hidden="true">|</span><div class="ed"><div class="ed-head"><span class="ed-name">b<span class="dim">'+S.A.r+' × 1</span></span></div><div class="ed-scroll"><div class="brk"><div class="cells" style="grid-template-columns:var(--cell)">'+cells+'</div></div></div></div>';
  }
  h+='</div>';
  if(o.vec) h+='<p class="sys">'+esc(t('sys',S.A.r,S.A.c))+'</p>';
  if(o.kint) h+='<p class="sys">A'+sup(String(S.k).trim()||'n')+' · '+esc(t('powNote'))+'</p>';
  $('#inputs').innerHTML=h;
}

/* ---------- 계산 ---------- */
function readM(m,T){
  let ok=true;const M=[];
  for(let i=0;i<T.r;i++){const row=[];for(let j=0;j<T.c;j++){const f=parseF(T.v[i][j]);const el=document.getElementById(m+'-'+i+'-'+j);if(el)el.classList.toggle('bad',!f);if(!f){ok=false;row.push(Z)}else row.push(f)}M.push(row)}
  return {M,ok};
}
function compute(){
  save();
  const o=OPS[S.op];let ok=true;const args={};
  const a=readM('A',S.A);args.A=a.M;ok=ok&&a.ok;
  if(o.B){const b=readM('B',S.B);args.B=b.M;ok=ok&&b.ok;}
  if(o.vec){args.b=[];for(let i=0;i<S.A.r;i++){const f=parseF(S.b[i]);const el=document.getElementById('b-'+i);if(el)el.classList.toggle('bad',!f);if(!f)ok=false;args.b.push(f||Z)}}
  let kbad=false;
  if(o.k){const f=parseF(S.k);let good=!!f&&String(S.k).trim()!=='';if(good&&o.kint&&!(f.d===1n&&f.n>=0n&&f.n<=12n))good=false;const el=$('#k');if(el)el.classList.toggle('bad',!good);if(!good){ok=false;kbad=true}args.k=f||Z}
  let res;
  if(!ok) res={head:'<p class="err">'+esc(kbad&&o.kint&&a.ok?t('errPow'):t('errInput'))+'</p>',steps:[]};
  else { try{res=o.run(args)}catch(e){res={head:'<p class="err">'+esc(t('errFail'))+'</p>',steps:[]}} }
  renderResult(res);
}
function renderResult(res){
  let h=res.head;
  if(res.chips&&res.chips.length) h+='<div class="chips">'+res.chips.map(c=>'<span class="chip '+c[0]+'">'+esc(c[1])+'</span>').join('')+'</div>';
  $('#resMain').innerHTML=h;
  S.latex=res.latex||null; $('#copyTex').disabled=!S.latex;
  const steps=res.steps||[],LIM=8,show=S.showAll?steps:steps.slice(0,LIM);
  $('#steps').innerHTML=show.length?show.map((s,i)=>'<li class="step"><span class="no">'+String(i+1).padStart(2,'0')+'</span><div class="sb"><div class="st">'+esc(s.t||'')+'</div>'+
    (s.ops?'<div class="rop">'+s.ops.map(x=>'<code>'+esc(x)+'</code>').join('')+'</div>':'')+(s.m?'<div class="sm">'+s.m+'</div>':'')+'</div></li>').join(''):'<li class="st">'+esc(t('stepsEmpty'))+'</li>';
  const more=$('#moreBtn');
  if(steps.length>LIM){more.hidden=false;more.textContent=S.showAll?t('stepsLess'):t('stepsMore',steps.length-LIM);}else more.hidden=true;
  $('#stepsD').hidden=!steps.length;
  $('#stepCount').textContent=steps.length?t('stepsCount',steps.length):'';
}

/* ---------- 페이지 시작 ---------- */
function save(){try{sessionStorage.setItem('mx-state',JSON.stringify({A:S.A,B:S.B,b:S.b,k:S.k,touched:S.touched}))}catch(e){}}
function init(){
  const op=document.body.dataset.op;S.op=OPS[op]?op:'inverse';
  let st=null;try{st=JSON.parse(sessionStorage.getItem('mx-state')||'null')}catch(e){}
  if(st&&st.touched&&st.A&&st.B){S.A=st.A;S.B=st.B;S.b=st.b||S.b;S.k=st.k||S.k;S.touched=true}else loadExample(S.op);
  if(OPS[S.op].kint&&!/^\s*\d{1,2}\s*$/.test(String(S.k)))S.k=EX[S.op].k;
  try{const m=localStorage.getItem('mx-mode');if(m==='dec'||m==='frac'){MODE=m;document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.mode===m)))}}catch(e){}
  fitDims();renderInputs();compute();
  try{if(sessionStorage.getItem('mx-steps')==='1')$('#stepsD').open=true}catch(e){}
  const cur=document.querySelector('.ops [aria-current],.ops .on');
  if(cur){const bar=cur.parentElement;if(bar.scrollWidth>bar.clientWidth)bar.scrollLeft=cur.offsetLeft-(bar.clientWidth-cur.offsetWidth)/2}
}

/* ---------- 이벤트 ---------- */
const inputs=$('#inputs');
inputs.addEventListener('input',e=>{
  const t=e.target,d=t.dataset;if(!d.m)return;
  if(d.m==='k')S.k=t.value;else if(d.m==='b')S.b[+d.i]=t.value;else S[d.m].v[+d.i][+d.j]=t.value;
  S.touched=true;compute();
});
inputs.addEventListener('keydown',e=>{
  const t=e.target;if(t.tagName!=='INPUT')return;const d=t.dataset;
  if(e.key==='Enter'){e.preventDefault();const all=[...inputs.querySelectorAll('input')];const nx=all[all.indexOf(t)+1];if(nx){nx.focus();nx.select()}return}
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){
    const di=e.key==='ArrowDown'?1:-1;let id=null;
    if(d.m==='A'||d.m==='B')id=d.m+'-'+(+d.i+di)+'-'+d.j;else if(d.m==='b')id='b-'+(+d.i+di);
    const el=id&&document.getElementById(id);if(el){e.preventDefault();el.focus();el.select()}
  }
});
inputs.addEventListener('focusin',e=>{if(e.target.tagName==='INPUT')e.target.select()});
inputs.addEventListener('click',e=>{
  const b=e.target.closest('[data-act]');if(!b)return;
  const m=b.dataset.m,d=b.dataset.d,act=b.dataset.act,dl=act==='inc'?1:-1,T=S[m];
  if(d==='n'){T.r=clamp(T.r+dl);T.c=T.r}else T[d]=clamp(T[d]+dl);
  S.touched=true;fitDims();renderInputs();compute();
  const again=inputs.querySelector('[data-act="'+act+'"][data-m="'+m+'"][data-d="'+d+'"]');
  if(again&&!again.disabled)again.focus();
});
$('#exBtn').addEventListener('click',()=>{loadExample(S.op);fitDims();renderInputs();compute()});
$('#clrBtn').addEventListener('click',()=>{S.A.v=blank();S.B.v=blank();S.b=Array(MAX).fill('');S.touched=true;renderInputs();compute();const f=document.getElementById('A-0-0');if(f)f.focus()});
document.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>{
  MODE=b.dataset.mode;try{localStorage.setItem('mx-mode',MODE)}catch(e){}document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));compute();
}));
$('#moreBtn').addEventListener('click',()=>{S.showAll=!S.showAll;compute()});
$('#stepsD').addEventListener('toggle',e=>{try{sessionStorage.setItem('mx-steps',e.target.open?'1':'0')}catch(x){}});
let toastT;
function toast(msg){const t=$('#toast');t.textContent=msg;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{t.hidden=true},1800)}
$('#copyTex').addEventListener('click',()=>{
  if(!S.latex)return;const v=S.latex;
  const fallback=()=>{const ta=document.createElement('textarea');ta.value=v;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}ta.remove();toast(ok?t('copied'):t('copyFail'))};
  try{navigator.clipboard.writeText(v).then(()=>toast(t('copied')),fallback)}catch(e){fallback()}
});
init();
})();
