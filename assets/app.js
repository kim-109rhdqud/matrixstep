(function(){
'use strict';
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SUBD='₀₁₂₃₄₅₆₇₈₉';
const sub=n=>String(n).split('').map(d=>SUBD[+d]).join('');
const ij=(i,j)=>sub(i+1)+sub(j+1);
const MAX=6;

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
    if(pr!==r){ [M[pr],M[r]]=[M[r],M[pr]]; steps.push({ops:['R'+sub(r+1)+' ↔ R'+sub(pr+1)],t:(c+1)+'열에서 피벗으로 쓸 0이 아닌 성분을 '+(r+1)+'행으로 올려요.',M:snap(M)}); }
    const pv=M[r][c];
    if(!pv.isOne()){ const iv=ONE.div(pv); M[r]=M[r].map(x=>x.mul(iv)); steps.push({ops:['R'+sub(r+1)+' ← '+coef(iv)+'R'+sub(r+1)],t:'피벗을 1로 만들기 위해 '+(r+1)+'행 전체를 피벗 값으로 나눠요.',M:snap(M)}); }
    const ops=[];
    for(let i=0;i<R;i++){
      if(i===r) continue; const f=M[i][c]; if(f.isZero()) continue;
      M[i]=M[i].map((x,j)=>x.sub(f.mul(M[r][j])));
      ops.push('R'+sub(i+1)+' ← R'+sub(i+1)+' '+(f.isNeg()?'+':'−')+' '+coefAbs(f)+'R'+sub(r+1));
    }
    if(ops.length) steps.push({ops,t:(c+1)+'열에서 피벗을 제외한 나머지 성분을 0으로 만들어요.',M:snap(M)});
    piv.push(c); r++;
  }
  return {M,steps,piv,rank:r};
}
function upper(A0){
  const M=snap(A0),n=M.length,steps=[];let sign=1;
  for(let c=0;c<n;c++){
    let pr=-1; for(let i=c;i<n;i++) if(!M[i][c].isZero()){pr=i;break}
    if(pr<0){ steps.push({t:(c+1)+'열의 대각선 아래가 모두 0이라 피벗을 잡을 수 없어요. 따라서 행렬식은 0이에요.',m:mx(M)}); return {det:Z,steps}; }
    if(pr!==c){ [M[pr],M[c]]=[M[c],M[pr]]; sign=-sign; steps.push({ops:['R'+sub(c+1)+' ↔ R'+sub(pr+1)],t:'두 행을 바꾸면 행렬식의 부호가 바뀌어요.',m:mx(M)}); }
    const ops=[];
    for(let i=c+1;i<n;i++){ const f=M[i][c].div(M[c][c]); if(f.isZero()) continue; M[i]=M[i].map((x,j)=>x.sub(f.mul(M[c][j]))); ops.push('R'+sub(i+1)+' ← R'+sub(i+1)+' '+(f.isNeg()?'+':'−')+' '+coefAbs(f)+'R'+sub(c+1)); }
    if(ops.length) steps.push({ops,t:(c+1)+'열의 피벗 아래를 0으로 만들어요. 이 연산은 행렬식을 바꾸지 않아요.',m:mx(M)});
  }
  let d=sign<0?ONE.neg():ONE; M.forEach((r,i)=>{d=d.mul(r[i])});
  steps.push({t:'상삼각행렬의 행렬식은 대각 성분의 곱이에요.'+(sign<0?' 행을 홀수 번 바꿨으니 부호를 바꿔요.':''),m:eq('det(A) = '+(sign<0?'−':'')+M.map((r,i)=>p(r[i])).join('·')+' = '+txt(d))});
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
  inverse:{label:'역행렬',title:'역행렬 구하기',desc:'가우스-조던 소거법으로 A⁻¹을 구하고, 행 연산을 하나씩 보여드려요.',square:true,
    run({A}){
      const n=A.length,steps=[];
      const aug=A.map((r,i)=>[...r,...r.map((_,j)=>i===j?ONE:Z)]);
      if(n===2){const d=det2(A); if(!d.isZero()){const adj=[[A[1][1],A[0][1].neg()],[A[1][0].neg(),A[0][0]]];
        steps.push({t:'2×2 행렬은 공식으로 바로 구할 수 있어요. 아래 소거법 풀이와 결과가 같아요.',m:eq('ad − bc = '+p(A[0][0])+'·'+p(A[1][1])+' − '+p(A[0][1])+'·'+p(A[1][0])+' = '+txt(d))+'<span class="eq">A⁻¹ = '+html(ONE.div(d))+' ·</span>'+mx(adj)});}}
      steps.push({t:'오른쪽에 단위행렬 I를 붙여 [A | I]를 만들어요.',m:mx(aug,{sep:n})});
      const g=gj(aug,n);
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M,{sep:n})}));
      if(g.rank<n){
        steps.push({t:'왼쪽 부분에 영행이 생겨 단위행렬을 만들 수 없어요. 그래서 A는 역행렬이 없어요.'});
        return {head:'<div class="none"><strong>역행렬이 없어요</strong><span>det(A) = 0이라서 A는 가역행렬이 아니에요.</span></div>',chips:[['bad','비가역 행렬']],steps};
      }
      const inv=g.M.map(r=>r.slice(n));
      steps.push({t:'왼쪽이 단위행렬이 되었어요. 오른쪽 부분이 A⁻¹이에요.'});
      return {head:'<div class="eqline"><span class="lhs">A⁻¹ =</span>'+mx(inv,{cls:'big'})+'</div>',chips:[['','det(A) = '+txt(upper(A).det)]],latex:bm(inv),steps};
    }},
  det:{label:'행렬식',title:'행렬식 계산',desc:'2×2는 공식으로, 3×3은 여인수 전개로, 4×4 이상은 행 소거로 풀어요.',square:true,
    run({A}){
      const n=A.length;let steps=[],d;
      if(n===1){d=A[0][0];steps.push({t:'1×1 행렬의 행렬식은 그 성분 자체예요.'});}
      else if(n===2){d=det2(A);steps.push({t:'2×2 행렬식은 주대각선의 곱에서 반대 대각선의 곱을 빼요.',m:eq('det(A) = ad − bc = '+p(A[0][0])+'·'+p(A[1][1])+' − '+p(A[0][1])+'·'+p(A[1][0])+' = '+txt(d))});}
      else if(n===3){
        const a=A[0],mins=[0,1,2].map(j=>A.slice(1).map(r=>r.filter((_,k)=>k!==j))),mv=mins.map(det2);
        steps.push({t:'1행을 따라 여인수 전개를 해요. 부호는 + − + 순서로 붙어요.',m:eq('det(A) = a₁₁M₁₁ − a₁₂M₁₂ + a₁₃M₁₃')});
        mins.forEach((m,j)=>steps.push({t:'1행과 '+(j+1)+'열을 지우고 남은 2×2 행렬의 행렬식이 M₁'+sub(j+1)+'이에요.',m:mx(m)+eq('M₁'+sub(j+1)+' = '+p(m[0][0])+'·'+p(m[1][1])+' − '+p(m[0][1])+'·'+p(m[1][0])+' = '+txt(mv[j]))}));
        d=a[0].mul(mv[0]).sub(a[1].mul(mv[1])).add(a[2].mul(mv[2]));
        steps.push({t:'각 성분과 소행렬식을 곱하고 부호를 붙여 더해요.',m:eq('det(A) = '+p(a[0])+'·'+p(mv[0])+' − '+p(a[1])+'·'+p(mv[1])+' + '+p(a[2])+'·'+p(mv[2])+' = '+txt(d))});
      } else {
        steps.push({t:'행 소거로 상삼각행렬을 만든 뒤 대각 성분을 곱해요.',m:mx(A)});
        const u=upper(A);d=u.det;steps=steps.concat(u.steps);
      }
      return {head:'<div class="eqline"><span class="lhs">det(A) =</span><span class="scalar">'+html(d)+'</span></div>',chips:[d.isZero()?['bad','역행렬 없음']:['ok','역행렬 있음']],latex:tex(d),steps};
    }},
  mul:{label:'곱셈',title:'행렬 곱셈',desc:'AB의 각 성분을 A의 행과 B의 열로 어떻게 계산하는지 하나씩 보여드려요.',B:'mul',sym:'×',
    run({A,B}){
      const m=A.length,n=B.length,q=B[0].length;
      const C=A.map((r,i)=>B[0].map((_,j)=>r.reduce((s,a,k)=>s.add(a.mul(B[k][j])),Z)));
      const steps=[{t:'A의 열 수와 B의 행 수가 '+n+'로 같아서 곱할 수 있어요. 결과는 '+m+'×'+q+' 행렬이에요.'}].concat(
        entrySteps(m,q,(i,j)=>({ops:['c'+ij(i,j)],t:'A의 '+(i+1)+'행과 B의 '+(j+1)+'열을 차례로 곱해 더해요.',m:eq(A[i].map((a,k)=>p(a)+'·'+p(B[k][j])).join(' + ')+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">AB =</span>'+mx(C,{cls:'big'})+'</div>',chips:[['',m+'×'+n+' · '+n+'×'+q+' → '+m+'×'+q]],latex:bm(C),steps};
    }},
  add:{label:'덧셈',title:'행렬 덧셈',desc:'크기가 같은 두 행렬을 같은 위치의 성분끼리 더해요.',B:'same',sym:'+',
    run({A,B}){
      const C=A.map((r,i)=>r.map((a,j)=>a.add(B[i][j])));
      const steps=[{t:'두 행렬의 크기가 같아서 같은 위치의 성분끼리 더해요.'}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(A[i][j])+' + '+p(B[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">A + B =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  sub:{label:'뺄셈',title:'행렬 뺄셈',desc:'크기가 같은 두 행렬을 같은 위치의 성분끼리 빼요.',B:'same',sym:'−',
    run({A,B}){
      const C=A.map((r,i)=>r.map((a,j)=>a.sub(B[i][j])));
      const steps=[{t:'두 행렬의 크기가 같아서 같은 위치의 성분끼리 빼요.'}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(A[i][j])+' − '+p(B[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">A − B =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  scalar:{label:'스칼라배',title:'스칼라배',desc:'행렬의 모든 성분에 같은 수 k를 곱해요.',k:true,
    run({A,k}){
      const C=A.map(r=>r.map(a=>a.mul(k)));
      const steps=[{t:'모든 성분에 k = '+txt(k)+' 를 곱해요.'}].concat(entrySteps(A.length,A[0].length,(i,j)=>({ops:['c'+ij(i,j)],m:eq(p(k)+'·'+p(A[i][j])+' = '+txt(C[i][j]))})));
      return {head:'<div class="eqline"><span class="lhs">kA =</span>'+mx(C,{cls:'big'})+'</div>',latex:bm(C),steps};
    }},
  transpose:{label:'전치',title:'전치행렬',desc:'행과 열을 맞바꿔 Aᵀ를 만들어요.',
    run({A}){
      const T=A[0].map((_,j)=>A.map(r=>r[j]));
      const steps=A.map((r,i)=>({t:'A의 '+(i+1)+'행을 Aᵀ의 '+(i+1)+'열로 옮겨요.',m:mx([r])+'<span class="eq">→</span>'+mx(r.map(x=>[x]))}));
      return {head:'<div class="eqline"><span class="lhs">Aᵀ =</span>'+mx(T,{cls:'big'})+'</div>',chips:[['',A.length+'×'+A[0].length+' → '+A[0].length+'×'+A.length]],latex:bm(T),steps};
    }},
  rref:{label:'RREF',title:'기약 행사다리꼴 (RREF)',desc:'행 연산으로 기약 행사다리꼴을 만들고 랭크와 피벗 열을 알려드려요.',
    run({A}){
      const g=gj(A,A[0].length),steps=[{t:'주어진 행렬에서 시작해요.',m:mx(A)}];
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M)}));
      if(!g.steps.length) steps.push({t:'이미 기약 행사다리꼴이에요.'});
      steps.push({t:g.rank?'피벗은 '+g.piv.map(c=>c+1).join(', ')+'열에 있어요. 피벗의 개수가 랭크예요.':'모든 성분이 0이라 피벗이 없어요.'});
      return {head:'<div class="eqline"><span class="lhs">RREF(A) =</span>'+mx(g.M,{cls:'big'})+'</div>',chips:[['','rank = '+g.rank]].concat(g.rank?[['','피벗 열 '+g.piv.map(c=>c+1).join(', ')]]:[]),latex:bm(g.M),steps};
    }},
  solve:{label:'연립방정식',title:'연립방정식 풀이',desc:'Ax = b를 첨가행렬로 바꿔 소거하고, 해가 하나인지·없는지·무수히 많은지 판단해요.',vec:true,
    run({A,b}){
      const n=A[0].length,aug=A.map((r,i)=>[...r,b[i]]),xs=Array.from({length:n},(_,j)=>'x'+sub(j+1));
      const steps=[{t:'계수행렬 A 옆에 b를 붙여 첨가행렬 [A | b]를 만들어요.',m:mx(aug,{sep:n})}];
      const g=gj(aug,n);
      g.steps.forEach(s=>steps.push({t:s.t,ops:s.ops,m:mx(s.M,{sep:n})}));
      const bad=g.M.findIndex(r=>r.slice(0,n).every(x=>x.isZero())&&!r[n].isZero());
      if(bad>=0){
        steps.push({t:(bad+1)+'행이 0 = '+txt(g.M[bad][n])+' 꼴이 되어 모순이에요. 따라서 해가 없어요.'});
        return {head:'<div class="none"><strong>해가 없어요</strong><span>소거 과정에서 0 = '+esc(txt(g.M[bad][n]))+' 같은 모순인 식이 생겨요.</span></div>',chips:[['bad','해 없음']],steps};
      }
      if(g.rank===n){
        const x=xs.map((_,j)=>g.M[g.piv.indexOf(j)][n]);
        const lines=xs.map((nm,j)=>nm+' = '+txt(x[j]));
        steps.push({t:'모든 변수 열에 피벗이 있어서 해가 하나로 정해져요.',m:'<div class="sol">'+lines.map(esc).join('<br>')+'</div>'});
        return {head:'<div class="eqline"><span class="lhs">x =</span>'+mx(x.map(v=>[v]),{cls:'big'})+'</div><div class="sol">'+lines.map(l=>'<div>'+esc(l)+'</div>').join('')+'</div>',chips:[['ok','유일한 해']],latex:bm(x.map(v=>[v])),steps};
      }
      const free=xs.map((_,j)=>j).filter(j=>!g.piv.includes(j)),tn=j=>'t'+sub(free.indexOf(j)+1);
      const lines=xs.map((nm,j)=>{
        if(free.includes(j)) return nm+' = '+tn(j);
        const r=g.M[g.piv.indexOf(j)];
        return nm+' = '+lin(r[n],free.map(f=>[r[f].neg(),tn(f)]));
      });
      steps.push({t:'피벗이 없는 '+free.map(f=>xs[f]).join(', ')+' 는 자유변수예요. 매개변수 t로 두고 나머지 변수를 나타내요.',m:'<div class="sol">'+lines.map(esc).join('<br>')+'</div>'});
      return {head:'<div class="none"><strong>해가 무수히 많아요</strong></div><div class="sol">'+lines.map(l=>'<div>'+esc(l)+'</div>').join('')+'</div>',chips:[['warn','자유변수 '+free.length+'개'],['','rank = '+g.rank]],steps};
    }}
};
const ORDER=['inverse','det','mul','add','sub','scalar','transpose','rref','solve'];

const EX={
  inverse:{A:[[2,1,1],[1,3,2],[1,0,0]]},
  det:{A:[[2,-1,0],[1,3,2],[0,1,4]]},
  mul:{A:[[1,2,0],[3,-1,4]],B:[[2,1],[0,3],[1,-2]]},
  add:{A:[[1,2],[3,4]],B:[[5,-1],[0,'1/2']]},
  sub:{A:[[1,2],[3,4]],B:[[5,-1],[0,'1/2']]},
  scalar:{A:[[2,-1],[4,'1/3']],k:'3/2'},
  transpose:{A:[[1,2,3],[4,5,6]]},
  rref:{A:[[1,2,-1,3],[2,4,1,0],[-1,-2,2,1]]},
  solve:{A:[[2,1,-1],[-3,-1,2],[-2,1,2]],b:[8,-11,-3]}
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
    '<button type="button" data-act="dec" data-m="'+m+'" data-d="'+d+'" aria-label="'+label+' 줄이기"'+(val<=1?' disabled':'')+'>−</button>'+
    '<output>'+val+'</output>'+
    '<button type="button" data-act="inc" data-m="'+m+'" data-d="'+d+'" aria-label="'+label+' 늘리기"'+(val>=MAX?' disabled':'')+'>+</button></span>';
}
function editor(m,T,ctrl,label){
  let cells='';
  for(let i=0;i<T.r;i++)for(let j=0;j<T.c;j++)
    cells+='<input id="'+m+'-'+i+'-'+j+'" data-m="'+m+'" data-i="'+i+'" data-j="'+j+'" autocomplete="off" spellcheck="false" placeholder="0" value="'+esc(T.v[i][j])+'" aria-label="'+label+' '+(i+1)+'행 '+(j+1)+'열">';
  return '<div class="ed"><div class="ed-head"><span class="ed-name">'+label+'<span class="dim">'+T.r+' × '+T.c+'</span></span><span class="ctrls">'+ctrl+'</span></div>'+
    '<div class="ed-scroll"><div class="brk"><div class="cells" style="grid-template-columns:repeat('+T.c+',var(--cell))">'+cells+'</div></div></div></div>';
}
function renderInputs(){
  const o=OPS[S.op];let h='<div class="eqrow">';
  const aCtrl=o.square?stepper('A','n','크기',S.A.r):stepper('A','r','행',S.A.r)+stepper('A','c','열',S.A.c);
  if(o.k) h+='<div class="ed"><div class="ed-head"><label class="ed-name" for="k">k</label></div><input id="k" class="kin" data-m="k" autocomplete="off" spellcheck="false" value="'+esc(S.k)+'"></div><span class="opsym" aria-hidden="true">·</span>';
  h+=editor('A',S.A,aCtrl,'A');
  if(o.B){ h+='<span class="opsym" aria-hidden="true">'+o.sym+'</span>'+editor('B',S.B,o.B==='mul'?stepper('B','c','열',S.B.c):'','B'); }
  if(o.vec){
    let cells='';for(let i=0;i<S.A.r;i++) cells+='<input id="b-'+i+'" data-m="b" data-i="'+i+'" autocomplete="off" spellcheck="false" placeholder="0" value="'+esc(S.b[i])+'" aria-label="b '+(i+1)+'행">';
    h+='<span class="opsym" aria-hidden="true">|</span><div class="ed"><div class="ed-head"><span class="ed-name">b<span class="dim">'+S.A.r+' × 1</span></span></div><div class="ed-scroll"><div class="brk"><div class="cells" style="grid-template-columns:var(--cell)">'+cells+'</div></div></div></div>';
  }
  h+='</div>';
  if(o.vec) h+='<p class="sys">식 '+S.A.r+'개 · 미지수 '+S.A.c+'개 · Ax = b</p>';
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
  if(o.k){const f=parseF(S.k);const el=$('#k');if(el)el.classList.toggle('bad',!f);if(!f||String(S.k).trim()==='')ok=false;args.k=f||Z}
  let res;
  if(!ok) res={head:'<p class="err">빨간 칸의 값을 확인해 주세요. 정수, 분수(1/3), 소수(0.25)만 입력할 수 있어요.</p>',steps:[]};
  else { try{res=o.run(args)}catch(e){res={head:'<p class="err">계산하지 못했어요. 입력값을 확인해 주세요.</p>',steps:[]}} }
  renderResult(res);
}
function renderResult(res){
  let h=res.head;
  if(res.chips&&res.chips.length) h+='<div class="chips">'+res.chips.map(c=>'<span class="chip '+c[0]+'">'+esc(c[1])+'</span>').join('')+'</div>';
  $('#resMain').innerHTML=h;
  S.latex=res.latex||null; $('#copyTex').disabled=!S.latex;
  const steps=res.steps||[],LIM=8,show=S.showAll?steps:steps.slice(0,LIM);
  $('#steps').innerHTML=show.length?show.map((s,i)=>'<li class="step"><span class="no">'+(i+1)+'</span><div class="sb"><div class="st">'+esc(s.t||'')+'</div>'+
    (s.ops?'<div class="rop">'+s.ops.map(x=>'<code>'+esc(x)+'</code>').join('')+'</div>':'')+(s.m?'<div class="sm">'+s.m+'</div>':'')+'</div></li>').join(''):'<li class="st">값을 입력하면 풀이가 여기에 나와요.</li>';
  const more=$('#moreBtn');
  if(steps.length>LIM){more.hidden=false;more.textContent=S.showAll?'풀이 접기':'나머지 '+(steps.length-LIM)+'단계 보기';}else more.hidden=true;
}

/* ---------- 페이지 시작 ---------- */
function save(){try{sessionStorage.setItem('mx-state',JSON.stringify({A:S.A,B:S.B,b:S.b,k:S.k,touched:S.touched}))}catch(e){}}
function init(){
  const op=document.body.dataset.op;S.op=OPS[op]?op:'inverse';
  let st=null;try{st=JSON.parse(sessionStorage.getItem('mx-state')||'null')}catch(e){}
  if(st&&st.touched&&st.A&&st.B){S.A=st.A;S.B=st.B;S.b=st.b||S.b;S.k=st.k||S.k;S.touched=true}else loadExample(S.op);
  try{const m=localStorage.getItem('mx-mode');if(m==='dec'||m==='frac'){MODE=m;document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.mode===m)))}}catch(e){}
  fitDims();renderInputs();compute();
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
let toastT;
function toast(msg){const t=$('#toast');t.textContent=msg;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{t.hidden=true},1800)}
$('#copyTex').addEventListener('click',()=>{
  if(!S.latex)return;const v=S.latex;
  const fallback=()=>{const ta=document.createElement('textarea');ta.value=v;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}ta.remove();toast(ok?'LaTeX를 복사했어요':'복사하지 못했어요. 브라우저 설정을 확인해 주세요')};
  try{navigator.clipboard.writeText(v).then(()=>toast('LaTeX를 복사했어요'),fallback)}catch(e){fallback()}
});
init();
})();
