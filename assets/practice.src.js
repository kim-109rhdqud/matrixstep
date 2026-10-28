/* ---------- 연습 문제 (build.py가 app.js 핵심부 뒤에 이어 붙여 practice.js로 만들어요) ---------- */
const PS={ko:{
  topics:{mix:'종합',det:'행렬식',inverse:'역행렬',mul:'곱셈',addsub:'덧셈·뺄셈',power:'거듭제곱',rref:'RREF',solve:'연립방정식',rank:'계수(rank)',eigen:'고윳값'},
  sizes:{2:'2×2',3:'3×3',mix:'섞어서'},
  q:{det:'다음 행렬의 행렬식 det(A)를 구하세요.',inverse:'다음 행렬의 역행렬 A⁻¹을 구하세요.',mul:'두 행렬의 곱 AB를 구하세요.',add:'두 행렬의 합 A + B를 구하세요.',sub:'두 행렬의 차 A − B를 구하세요.',
     power:k=>'다음 행렬의 거듭제곱 A'+SUP[k]+'을 구하세요.',rref:'다음 행렬의 기약 행사다리꼴(RREF)을 구하세요.',solve:'다음 연립방정식을 푸세요.',rank:'다음 행렬의 계수(rank)를 구하세요.',eigen:'다음 행렬의 고윳값을 모두 구하세요.'},
  sheetTitle:(tp,n)=>'행렬 연습 문제 · '+tp+' '+n+'문제', nameLine:'이름: ____________    날짜: ____________',
  answers:'정답', check:'확인', checkAll:'전체 채점', score:(a,b)=>a+' / '+b+' 정답', correct:'정답이에요', wrong:'아쉬워요. 정답은 아래에 있어요.',
  answerIs:'정답', seeSteps:'계산기에서 풀이 보기', eigenHint:'쉼표로 구분 · 예: 2, 5', solveHint:'x, y, z 순서로 입력',
  newSet:'새 문제', print:'인쇄 · PDF 저장', docx:'워드(.docx) 내려받기', withAns:'정답지 포함', share:'문제 링크 복사', shared:'이 문제 세트의 링크를 복사했어요',
  showAns:'정답 보기', hideAns:'정답 숨기기', vars:['x','y','z','w'], docName:'행렬_연습문제', generating:'파일을 만들고 있어요…', made:'내려받기를 시작했어요',
  inputEmpty:'답을 입력해 주세요', generating2:'문제를 만드는 중…'
},en:{
  topics:{mix:'Mixed',det:'Determinant',inverse:'Inverse',mul:'Multiplication',addsub:'Add & subtract',power:'Powers',rref:'RREF',solve:'Linear systems',rank:'Rank',eigen:'Eigenvalues'},
  sizes:{2:'2×2',3:'3×3',mix:'Mixed'},
  q:{det:'Find the determinant det(A).',inverse:'Find the inverse A⁻¹.',mul:'Compute the product AB.',add:'Compute the sum A + B.',sub:'Compute the difference A − B.',
     power:k=>'Compute A'+SUP[k]+'.',rref:'Find the reduced row echelon form (RREF).',solve:'Solve the linear system.',rank:'Find the rank.',eigen:'Find all eigenvalues.'},
  sheetTitle:(tp,n)=>'Matrix practice · '+tp+' · '+n+' problems', nameLine:'Name: ____________    Date: ____________',
  answers:'Answers', check:'Check', checkAll:'Grade all', score:(a,b)=>a+' / '+b+' correct', correct:'Correct', wrong:'Not quite. The answer is below.',
  answerIs:'Answer', seeSteps:'See the steps in the calculator', eigenHint:'Comma-separated, e.g. 2, 5', solveHint:'Enter x, y, z in order',
  newSet:'New set', print:'Print · Save as PDF', docx:'Download Word (.docx)', withAns:'Include answer key', share:'Copy link to this set', shared:'Link to this problem set copied',
  showAns:'Show answers', hideAns:'Hide answers', vars:['x','y','z','w'], docName:'matrix_practice', generating:'Preparing the file…', made:'Download started',
  inputEmpty:'Enter an answer', generating2:'Generating…'
}};
const SUP={2:'²',3:'³'};
const ps=(k,...a)=>{const v=PS[LANG][k];return typeof v==='function'?v(...a):v};
const Fi=n=>new F(BigInt(n));
const Fm=M=>M.map(r=>r.map(Fi));

/* 난수 (seed 고정 → 같은 링크면 같은 문제) */
function rng(seed){let a=seed>>>0;return()=>{a+=0x6D2B79F5;let x=a;x=Math.imul(x^(x>>>15),x|1);x^=x+Math.imul(x^(x>>>7),x|61);return((x^(x>>>14))>>>0)/4294967296}}
let R=Math.random;
const ri=(lo,hi)=>lo+Math.floor(R()*(hi-lo+1));
const pick=a=>a[Math.floor(R()*a.length)];
const imat=(r,c,lo,hi)=>Array.from({length:r},()=>Array.from({length:c},()=>ri(lo,hi)));
const imul=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,a,k)=>s+a*B[k][j],0)));
function unimod(n){ // det = ±1 인 정수 행렬 (작은 성분)
  const L=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1:j<i?ri(-1,1):0));
  const U=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?pick([1,-1]):j>i?ri(-1,1):0));
  return imul(L,U);
}
const idet=A=>{const n=A.length;if(n===1)return A[0][0];let s=0;for(let j=0;j<n;j++){if(!A[0][j])continue;s+=(j%2?-1:1)*A[0][j]*idet(A.slice(1).map(r=>r.filter((_,c)=>c!==j)))}return s};

/* 문제 생성 */
const KINDS=['det','inverse','mul','addsub','power','rref','solve','rank','eigen'];
function gen(kind,n){
  if(kind==='mix')kind=pick(KINDS);
  if(n==='mix')n=pick([2,3]);
  n=+n;
  const p={kind,n};
  if(kind==='det'){p.A=imat(n,n,-5,5);p.ans={kind:'scalar',v:Fi(idet(p.A))};p.op='det'}
  else if(kind==='inverse'){
    if(R()<0.7){p.A=unimod(n);if(n===2&&R()<0.5)p.A=imul(p.A,unimod(n))}
    else{do{p.A=imat(n,n,-4,4)}while(idet(p.A)===0||Math.abs(idet(p.A))>6)}
    const A=Fm(p.A),g=gj(A.map((r,i)=>[...r,...r.map((_,j)=>i===j?ONE:Z)]),n);
    p.ans={kind:'matrix',v:g.M.map(r=>r.slice(n))};p.op='inverse';
  }
  else if(kind==='mul'){const k=pick([2,3]),q=pick([2,3]);p.A=imat(n,k,-4,4);p.B=imat(k,q,-4,4);p.ans={kind:'matrix',v:Fm(imul(p.A,p.B))};p.op='mul'}
  else if(kind==='addsub'){const c=pick([2,3]);p.A=imat(n,c,-6,6);p.B=imat(n,c,-6,6);p.sub=R()<0.5;p.ans={kind:'matrix',v:Fm(p.A.map((r,i)=>r.map((x,j)=>p.sub?x-p.B[i][j]:x+p.B[i][j])))};p.op=p.sub?'sub':'add'}
  else if(kind==='power'){p.A=imat(2,2,-3,3);p.k=n===3?3:pick([2,3]);let M=p.A;for(let i=1;i<p.k;i++)M=imul(M,p.A);p.ans={kind:'matrix',v:Fm(M)};p.op='power';p.n=2}
  else if(kind==='rref'){const c=n+1;p.A=imat(n,c,-4,4);if(R()<0.4&&n>1){const i=ri(1,n-1),m=pick([-2,-1,2]);p.A[i]=p.A[0].map(x=>x*m)}
    p.ans={kind:'matrix',v:gj(Fm(p.A),c).M};p.op='rref'}
  else if(kind==='solve'){const x=Array.from({length:n},()=>ri(-4,4));do{p.A=imat(n,n,-4,4)}while(idet(p.A)===0);p.b=imul(p.A,x.map(v=>[v])).map(r=>r[0]);
    p.ans={kind:'vector',v:x.map(Fi)};p.op='solve'}
  else if(kind==='rank'){const c=n+1,r=R()<0.5?n:ri(1,n-1);p.A=imul(imat(n,r,-2,2),imat(r,c,-2,2));if(p.A.every(row=>row.every(x=>!x)))p.A[0][0]=1;
    p.ans={kind:'scalar',v:Fi(gj(Fm(p.A),c).rank)};p.op='rank'}
  else if(kind==='eigen'){const d=Array.from({length:n},()=>ri(-3,4));const P=unimod(n),Pi=gj(Fm(P).map((r,i)=>[...r,...r.map((_,j)=>i===j?ONE:Z)]),n).M.map(r=>r.slice(n).map(x=>Number(x.n)));
    const D=d.map((v,i)=>d.map((_,j)=>i===j?v:0));p.A=imul(imul(P,D),Pi);p.ans={kind:'list',v:d.slice().sort((a,b)=>a-b).map(Fi)};p.op='eigen'}
  return p;
}
function makeSet(topic,size,count,seed){R=rng(seed);const out=[];for(let i=0;i<count;i++)out.push(gen(topic,size));R=Math.random;return out}

/* 표시 */
const enc=M=>M.map(r=>r.join(',')).join(';');
function calcLink(p){
  const slug={det:'determinant',inverse:'inverse',mul:'multiplication',add:'addition',sub:'subtraction',power:'power',rref:'rref',solve:'linear-system',rank:'rank',eigen:'eigenvalues'}[p.op];
  let h='#A='+enc(p.A);if(p.B)h+='&B='+enc(p.B);if(p.b)h+='&b='+p.b.join(',');if(p.k)h+='&k='+p.k;
  return (LANG==='en'?'/en/':'/')+slug+'/'+h;
}
const V=ps('vars');
function sysText(p){ // 연립방정식 문장
  return p.A.map((r,i)=>{let s='';r.forEach((a,j)=>{if(!a)return;const sg=a<0?'−':'+';const ab=Math.abs(a);s+=(s?' '+sg+' ':(a<0?'−':''))+(ab===1?'':ab)+V[j]});return (s||'0')+' = '+p.b[i]});
}
function stmt(p){return p.kind==='power'?ps('q').power(p.k):ps('q')[p.op==='add'||p.op==='sub'?p.op:p.kind]}
function given(p){
  if(p.kind==='solve')return '<div class="psys">'+sysText(p).map(l=>'<div>'+esc(l)+'</div>').join('')+'</div>';
  let h='<div class="eqline"><span class="lhs">A =</span>'+mx(Fm(p.A))+'</div>';
  if(p.B)h+='<div class="eqline"><span class="lhs">B =</span>'+mx(Fm(p.B))+'</div>';
  return h;
}
function ansHtml(a){
  if(a.kind==='scalar')return '<span class="ansv">'+html(a.v)+'</span>';
  if(a.kind==='list')return '<span class="ansv">λ = '+a.v.map(html).join(', ')+'</span>';
  if(a.kind==='vector')return '<span class="ansv">'+a.v.map((x,i)=>V[i]+' = '+html(x)).join(', ')+'</span>';
  return mx(a.v);
}
function inputHtml(p,i){
  const a=p.ans;
  if(a.kind==='matrix'){const r=a.v.length,c=a.v[0].length;let h='<div class="pin-m" style="grid-template-columns:repeat('+c+',minmax(0,56px))">';
    for(let x=0;x<r*c;x++)h+='<input class="pin" inputmode="text" autocomplete="off" aria-label="'+(Math.floor(x/c)+1)+','+(x%c+1)+'">';return h+'</div>'}
  if(a.kind==='vector')return '<div class="pin-v">'+a.v.map((_,j)=>'<label>'+V[j]+' = <input class="pin" autocomplete="off"></label>').join('')+'</div>';
  if(a.kind==='list')return '<input class="pin wide" autocomplete="off" placeholder="'+esc(ps('eigenHint'))+'">';
  return '<input class="pin" autocomplete="off">';
}
let SET=[],CFG={topic:'mix',size:'mix',count:10,seed:1},SHOW=false;
function render(){
  const list=$('#plist');let h='';
  SET.forEach((p,i)=>{
    h+='<article class="prob" data-i="'+i+'"><div class="prob-h"><span class="pno">'+String(i+1).padStart(2,'0')+'</span><p>'+esc(stmt(p))+'</p></div><div class="pgiven">'+given(p)+'</div>'
      +'<div class="pans"><div class="pans-in">'+inputHtml(p,i)+'</div><button type="button" class="ghost chk">'+ps('check')+'</button></div>'
      +'<div class="verdict" hidden></div><div class="key"'+(SHOW?'':' hidden')+'><span class="lbl">'+ps('answerIs')+'</span>'+ansHtml(p.ans)+' <a href="'+calcLink(p)+'">'+ps('seeSteps')+' →</a></div></article>';
  });
  list.innerHTML=h;$('#score').textContent='';
  $('#sheetT').textContent=ps('sheetTitle',ps('topics')[CFG.topic]+(CFG.size==='mix'?'':' '+ps('sizes')[CFG.size]),SET.length);
  $('#sheetL').textContent='WORKSHEET · #'+CFG.seed;
  $('#showAns').textContent=SHOW?ps('hideAns'):ps('showAns');
  renderKey();
}
function renderKey(){ // 인쇄용 정답지
  $('#keylist').innerHTML=SET.map((p,i)=>'<div class="krow"><span class="pno">'+String(i+1).padStart(2,'0')+'</span>'+ansHtml(p.ans)+'</div>').join('');
}
function parseAns(p,el){
  const a=p.ans,ins=[...el.querySelectorAll('.pin')];
  if(a.kind==='list'){const v=ins[0].value.split(/[,\s]+/).filter(Boolean).map(parseF);if(!v.length||v.some(x=>!x))return null;return v.sort((x,y)=>x.sub(y).isNeg()?-1:1)}
  const v=ins.map(x=>parseF(x.value));if(v.some(x=>!x)||ins.every(x=>!x.value.trim()))return null;
  if(a.kind==='scalar')return v[0];
  if(a.kind==='vector')return v;
  const c=a.v[0].length;return a.v.map((_,i)=>v.slice(i*c,i*c+c));
}
function check(i,quiet){
  const p=SET[i],el=$('.prob[data-i="'+i+'"]'),got=parseAns(p,el),vd=el.querySelector('.verdict'),a=p.ans;
  el.querySelectorAll('.pin').forEach(x=>x.classList.remove('bad'));
  if(got===null){if(quiet){vd.hidden=true;return null}vd.hidden=false;vd.className='verdict warn';vd.textContent=ps('inputEmpty');return null}
  let ok;
  if(a.kind==='scalar')ok=got.eq(a.v);
  else if(a.kind==='list'||a.kind==='vector'){ok=got.length===a.v.length&&got.every((x,j)=>x.eq(a.v[j]));if(a.kind==='vector')el.querySelectorAll('.pin').forEach((x,j)=>{if(!got[j].eq(a.v[j]))x.classList.add('bad')})}
  else{ok=true;const c=a.v[0].length;el.querySelectorAll('.pin').forEach((x,k)=>{const i2=Math.floor(k/c),j=k%c;if(!got[i2][j].eq(a.v[i2][j])){ok=false;x.classList.add('bad')}})}
  vd.hidden=false;vd.className='verdict '+(ok?'ok':'bad');vd.textContent=ok?ps('correct'):ps('wrong');
  el.querySelector('.key').hidden=ok&&!SHOW;el.dataset.ok=ok?'1':'0';
  return ok;
}
function checkAll(){let n=0,c=0;SET.forEach((_,i)=>{const r=check(i,true);if(r!==null){n++;if(r)c++}});$('#score').textContent=ps('score',c,SET.length)}

/* 설정 ↔ 해시 */
function readHash(){
  const q=new URLSearchParams(location.hash.slice(1));
  const tp=q.get('t'),sz=q.get('n'),ct=q.get('c'),sd=q.get('s');
  if(tp&&(tp==='mix'||KINDS.includes(tp)))CFG.topic=tp;
  if(sz&&['2','3','mix'].includes(sz))CFG.size=sz;
  if(ct&&[5,10,20].includes(+ct))CFG.count=+ct;
  CFG.seed=sd&&/^\d+$/.test(sd)?+sd:Math.floor(Math.random()*1e9);
}
function writeHash(){history.replaceState(null,'','#t='+CFG.topic+'&n='+CFG.size+'&c='+CFG.count+'&s='+CFG.seed)}
let genT=0;
function skeleton(n){
  const list=$('#plist');let h='';
  for(let i=0;i<n;i++)h+='<div class="prob skel" style="animation-delay:'+(i*60)+'ms"><div class="sk sk-t"></div><div class="sk sk-m"></div><div class="sk sk-b"></div></div>';
  list.innerHTML=h;$('#score').textContent='';
  const sh=$('.sheet');sh.classList.add('busy');$('#sheetL').textContent=ps('generating2');
}
function build(newSeed,delay){
  if(newSeed)CFG.seed=Math.floor(Math.random()*1e9);
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wait=reduce?0:(delay==null?650:delay);
  clearTimeout(genT);skeleton(CFG.count);
  const go=()=>{SET=makeSet(CFG.topic,CFG.size,CFG.count,CFG.seed);writeHash();render();$('.sheet').classList.remove('busy');
    if(!reduce)document.querySelectorAll('#plist .prob').forEach((el,i)=>{el.style.animationDelay=(i*45)+'ms';el.classList.add('in')})};
  if(wait)genT=setTimeout(go,wait);else go();
}

/* ---------- .docx 만들기 (압축 없는 zip + OMML 수식) ---------- */
const CRC=(()=>{const T=new Int32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?(0xEDB88320^(c>>>1)):(c>>>1);T[n]=c}return b=>{let c=-1;for(let i=0;i<b.length;i++)c=T[(c^b[i])&255]^(c>>>8);return(c^-1)>>>0}})();
function zip(files){ // files: [{name,data:Uint8Array}]
  const enc=new TextEncoder(),parts=[],cd=[];let off=0;
  const u16=v=>[v&255,v>>8&255],u32=v=>[v&255,v>>8&255,v>>16&255,v>>>24&255];
  files.forEach(f=>{const nm=enc.encode(f.name),crc=CRC(f.data),n=f.data.length;
    const loc=new Uint8Array([0x50,0x4b,3,4,20,0,0,0,0,0,0,0,0,0,...u32(crc),...u32(n),...u32(n),...u16(nm.length),0,0,...nm]);
    parts.push(loc,f.data);
    cd.push(new Uint8Array([0x50,0x4b,1,2,20,0,20,0,0,0,0,0,0,0,0,0,...u32(crc),...u32(n),...u32(n),...u16(nm.length),0,0,0,0,0,0,0,0,0,0,0,0,...u32(off),...nm]));
    off+=loc.length+n});
  const cdLen=cd.reduce((s,x)=>s+x.length,0);
  const end=new Uint8Array([0x50,0x4b,5,6,0,0,0,0,...u16(files.length),...u16(files.length),...u32(cdLen),...u32(off),0,0]);
  return new Blob([...parts,...cd,end],{type:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
}
const X=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const mt=s=>'<m:r><m:t xml:space="preserve">'+X(s)+'</m:t></m:r>';
function mnum(f){ // 분수는 m:f
  if(f.d===1n)return mt(f.n.toString().replace('-','−'));
  const s=f.isNeg()?mt('−'):'',a=f.isNeg()?-f.n:f.n;
  return s+'<m:f><m:num>'+mt(a)+'</m:num><m:den>'+mt(f.d)+'</m:den></m:f>';
}
function mmat(M){
  const c=M[0].length;
  return '<m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e><m:m><m:mPr><m:mcs><m:mc><m:mcPr><m:count m:val="'+c+'"/><m:mcJc m:val="center"/></m:mcPr></m:mc></m:mcs></m:mPr>'
    +M.map(r=>'<m:mr>'+r.map(x=>'<m:e>'+mnum(x)+'</m:e>').join('')+'</m:mr>').join('')+'</m:m></m:e></m:d>';
}
const wp=(inner,pr)=>'<w:p>'+(pr||'')+inner+'</w:p>';
const wr=(s,b)=>'<w:r>'+(b?'<w:rPr><w:b/></w:rPr>':'')+'<w:t xml:space="preserve">'+X(s)+'</w:t></w:r>';
const wmath=parts=>'<m:oMathPara><m:oMathParaPr><m:jc m:val="left"/></m:oMathParaPr><m:oMath>'+parts+'</m:oMath></m:oMathPara>';
const winl=parts=>'<m:oMath>'+parts+'</m:oMath>';
function docxBlob(withKey){
  const topic=ps('topics')[CFG.topic]+(CFG.size==='mix'?'':' '+ps('sizes')[CFG.size]);
  let b=wp(wr(ps('sheetTitle',topic,SET.length)),'<w:pPr><w:pStyle w:val="Title"/></w:pPr>')+wp(wr(ps('nameLine')),'<w:pPr><w:spacing w:after="360"/></w:pPr>');
  SET.forEach((p,i)=>{
    b+=wp(wr((i+1)+'. ',true)+wr(stmt(p)),'<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/></w:pPr>');
    if(p.kind==='solve')sysText(p).forEach(l=>{b+=wp(wmath(mt(l)),'<w:pPr><w:ind w:left="567"/></w:pPr>')});
    else{let m=mt('A = ')+mmat(Fm(p.A));if(p.B)m+=mt(',   B = ')+mmat(Fm(p.B));b+=wp(wmath(m),'<w:pPr><w:ind w:left="567"/><w:spacing w:after="240"/></w:pPr>')}
  });
  if(withKey){
    b+=wp('<w:r><w:br w:type="page"/></w:r>')+wp(wr(ps('answers')),'<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>');
    SET.forEach((p,i)=>{const a=p.ans;let m;
      if(a.kind==='scalar')m=mnum(a.v);else if(a.kind==='list')m=mt('λ = ')+a.v.map((x,j)=>(j?mt(', '):'')+mnum(x)).join('');
      else if(a.kind==='vector')m=a.v.map((x,j)=>(j?mt(',  '):'')+mt(V[j]+' = ')+mnum(x)).join('');else m=mmat(a.v);
      b+=wp(wr((i+1)+'. ',true)+winl(m),'<w:pPr><w:spacing w:after="120"/></w:pPr>')});
  }
  const NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
  const doc='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+NS+'><w:body>'+b+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr></w:body></w:document>';
  const styles='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles '+NS+'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Malgun Gothic" w:cs="Calibri"/><w:sz w:val="22"/><w:lang w:val="'+(LANG==='en'?'en-US':'ko-KR')+'" w:eastAsia="ko-KR"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
    +'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    +'<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>'
    +'<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style></w:styles>';
  const ct='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>';
  const rels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>';
  const drels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>';
  const E=s=>new TextEncoder().encode(s);
  return zip([{name:'[Content_Types].xml',data:E(ct)},{name:'_rels/.rels',data:E(rels)},{name:'word/_rels/document.xml.rels',data:E(drels)},{name:'word/document.xml',data:E(doc)},{name:'word/styles.xml',data:E(styles)}]);
}
function download(){
  toast(ps('generating'));
  const blob=docxBlob($('#withAns').checked),u=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=u;a.download=ps('docName')+'_'+CFG.topic+'_'+CFG.seed+'.docx';a.hidden=true;document.body.appendChild(a);a.click();setTimeout(()=>{a.remove();URL.revokeObjectURL(u)},4000);toast(ps('made'));
}

/* ---------- 시작 ---------- */
function toast(msg){const el=$('#toast');el.textContent=msg;el.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(()=>{el.hidden=true},1800)}
function copyText(v,okMsg){const fb=()=>{const ta=document.createElement('textarea');ta.value=v;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}ta.remove();toast(okMsg)};try{navigator.clipboard.writeText(v).then(()=>toast(okMsg),fb)}catch(e){fb()}}
readHash();
function paintCfg(){[['#topic',CFG.topic],['#size',CFG.size],['#count',String(CFG.count)]].forEach(([id,v])=>$(id).querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===v))))}
paintCfg();build(false,350);
[['#topic','topic'],['#size','size'],['#count','count']].forEach(([id,k])=>$(id).addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;CFG[k]=k==='count'?+b.dataset.v:b.dataset.v;paintCfg();build(true)}));
$('#newBtn').addEventListener('click',()=>build(true));
$('#printBtn').addEventListener('click',()=>{document.body.classList.toggle('print-key',$('#withAns').checked);window.print()});
$('#docxBtn').addEventListener('click',download);
$('#shareBtn').addEventListener('click',()=>copyText(location.href,ps('shared')));
$('#showAns').addEventListener('click',()=>{SHOW=!SHOW;document.querySelectorAll('.prob .key').forEach(k=>{k.hidden=!SHOW});$('#showAns').textContent=SHOW?ps('hideAns'):ps('showAns')});
$('#gradeBtn').addEventListener('click',checkAll);
$('#plist').addEventListener('click',e=>{const b=e.target.closest('.chk');if(b)check(+b.closest('.prob').dataset.i)});
$('#plist').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.classList.contains('pin')){e.preventDefault();check(+e.target.closest('.prob').dataset.i)}});
$('#withAns').addEventListener('change',()=>{try{localStorage.setItem('mx-pr-key',$('#withAns').checked?'1':'0')}catch(e){}});
try{if(localStorage.getItem('mx-pr-key')==='1')$('#withAns').checked=true}catch(e){}
