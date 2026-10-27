/* NexoraOps 1.0 — float64 port of analysis/code/model.py. Volume bn/year; money Rp tn. */
export const W=[.35,.30,.25,.10],S=[.8,.6,.16,0],A=[7000,8500,12750,18000],E=[10000,11000,12000,14600],K=[.64,.43,.13,.02],OT=[3500,4500,6500,8000],MIX=[3500,6000,10000,14000];
export const packages={current:{soft:0,physical:0,add:[0,0,0,0],fixed:0,recurring:0,transition:0,ramp:[1,1,1,1,1,1,1]},rules:{soft:0,physical:0,add:[0,0,0,0],fixed:0,recurring:.008,transition:.015,ramp:[.85,1,1,1,1,1,1]},software:{soft:.18,physical:0,add:[0,0,0,0],fixed:0,recurring:.045,transition:.06,ramp:[.55,.9,1,1,1,1,1],eff:true},targeted:{soft:.18,physical:.85,add:[.08,.08,.03,0],fixed:.15,recurring:.0705,transition:.10,ramp:[.35,.8,1,1,1,1,1],eff:true},large:{soft:.18,physical:3.6,add:[.22,.22,.12,.04],fixed:.55,recurring:.153,transition:.20,ramp:[.15,.6,.9,1,1,1,1],eff:true}};
const sum=a=>a.reduce((s,x)=>s+x,0),clip=(x,l,h)=>Math.max(l,Math.min(h,x));
const q0=W.map((w,i)=>2*w*S[i]),fixed=q0.map((q,i)=>q*A[i]*.25/1000);
const pen=(q,k,i)=>OT[i]/2*Math.max(q-.85*k,0)**2/(.15*k)/1000;
const variable=A.map((a,i)=>a*.75-(q0[i]?pen(q0[i],K[i],i)*1000/q0[i]:0));
export function central(years=5){return {demand:Array(years).fill(1),travel:Array(years).fill(1),input_cost:Array(years).fill(1),external:Array(years).fill(1),capacity:Array(years).fill(1),eff:[.03],adoption:[1],inflation:[.025],overrun:[1],daily_surge:Array(years).fill(1)}}
export function operating(w,policy,{axis=1,capacityMult=1,travelMult=1,inflation=null}={}){
 const p=packages[policy.package],out=[];
 for(let y=0;y<w.demand.length;y++){
  const d=W.map(v=>2*axis*w.demand[y]*v),travel=w.travel[y]*travelMult,idx=(1+(inflation??w.inflation[0]))**(y+1),v=variable.map(x=>x*w.input_cost[y]*(.55+.45*travel)),ext=E.map(x=>x*w.external[y]),k0=K.map(x=>x*w.capacity[y]*capacityMult),qc=d.map((x,i)=>Math.min(x*S[i],k0[i]));
  let q=qc.slice(),k=k0.slice(),ve=v.slice(),ramp=1;
  if(policy.package!=='current'){
   ramp=p.ramp[y]*Math.min(w.adoption[0],1);const eff=p.eff?clip(w.eff[0],0,.15):0;
   k=k0.map((x,i)=>(x+p.add[i]*ramp)*(1+.02*eff/.03*ramp));ve=v.map(x=>x*(1-.65*eff*ramp));
   let tranches=[];
   for(let i=0;i<4;i++)for(let t=0;t<24;t++){
    const max=Math.min(d[i],k[i]*policy.buffer),mid=max*(t+.5)/24,mc=ve[i]+OT[i]*Math.max(mid-.85*k[i],0)/(.15*k[i])+MIX[i]*Math.max(mid-q0[i],0)/Math.max(d[i]-q0[i],1e-6);
    tranches.push({i,t,chunk:max/24,saving:ext[i]-mc});
   }
   tranches.sort((a,b)=>b.saving-a.saving||a.i-b.i||a.t-b.t);
   let budget=sum(d)*policy.target,qo=[0,0,0,0];
   for(const t of tranches){if(t.saving<=0||budget<=0)break;const take=Math.min(t.chunk,budget);qo[t.i]+=take;budget-=take}
   q=qc.map((x,i)=>Math.min(x+ramp*(qo[i]-x),k[i],d[i]));
  }
  const ec=W.map((x,i)=>(2*x*(1-S[i])*1.65+[.04,.04,.03,.015][i])*clip(1-.1*Math.max(travel-1,0),.7,1)),e=d.map((x,i)=>Math.min(Math.max(x-q[i],0),ec[i])),u=d.map((x,i)=>Math.max(x-q[i]-e[i],0)),util=q.map((x,i)=>x/k[i]);
  let cost=sum(fixed)+sum(q.map((x,i)=>ve[i]*x/1000+pen(x,k[i],i)+MIX[i]/2*Math.max(x-q0[i],0)**2/Math.max(d[i]-q0[i],1e-6)/1000+ext[i]*e[i]/1000))+sum(u)*18;
  cost*=idx;if(policy.package!=='current')cost+=(p.fixed*ramp+p.recurring)*idx;
  const peak=sum(q.map((x,i)=>Math.max(x*w.daily_surge[y]-k[i],0)+Math.max(e[i]*w.daily_surge[y]-ec[i],0))),late=sum(q.map((x,i)=>Math.max(util[i]-.90,0)/.10*.06*x)),service=clip(1-(sum(u)+peak+late)/sum(d),0,1);
  out.push({cost,q,e,d,k,u,util,share:sum(q)/sum(d),service,violation:sum(u)/sum(d)>.005||service<.95,unused:k.map((x,i)=>x-q[i])});
 }
 return out;
}
function factor(y,start,life){return Math.max(Math.min(y-start+.5,life)-Math.max(Math.min(y-start-.5,life),0),0)/life}
export function finance(op,cf,pkg,w,{discount=.14,otherDrift=0,tax=.22,salvageFactor=.35}={}){
 const p=packages[pkg],soft=p.soft*w.overrun[0],phys=p.physical*w.overrun[0],wc=.01*soft+.02*phys,rows=[],flows=[-soft-phys-wc];
 for(let i=0;i<op.length;i++){
  const y=i+1,dep=soft*factor(y,1,4)+(op.length>=5?.5*soft*factor(y,5,4):0)+phys*(.30*factor(y,1,5)+.40*factor(y,1,8)+.30*factor(y,1,10))+(op.length>=6?.30*phys*factor(y,6,5):0);
  const benefit=cf[i].cost-op[i].cost,transition=y===1?p.transition*w.overrun[0]:0,ebitda=benefit-transition,ebit=ebitda-dep,taxes=Math.max(ebit,0)*tax,replacement=(y===5?.5*soft:0)+(y===6?.3*phys:0);
  let salvage=0;if(y===op.length){salvage=phys*(.3*(1-Math.min(y-.5,5)/5)+.4*(1-Math.min(y-.5,8)/8)+.3*(1-Math.min(y-.5,10)/10));if(y>=6)salvage+=.3*phys*(1-Math.min(y-5.5,5)/5);salvage*=salvageFactor}
  const flow=ebitda-taxes-replacement+(y===op.length?salvage+wc:0),cfprofit=5-(cf[i].cost-20)+y*otherDrift,profit=cfprofit+ebit,prev=i?rows[i-1].profit:5;
  flows.push(flow);rows.push({year:y,benefit,transition,ebitda,dep,ebit,taxes,replacement,flow,cfprofit,profit,growth:profit-prev,growthRate:(profit-prev)/prev,salvage});
 }
 const npv=sum(flows.map((f,i)=>f/(1+discount)**i)),growthPass=rows.every(x=>x.growth>1e-10);
 const pb=rate=>{let c=flows[0];if(c>=0)return 0;for(let i=1;i<flows.length;i++){const f=flows[i]/(1+rate)**i;if(c+f>=0&&f>0)return i-1-c/f;c+=f}return null};
 let cum=0,peak=0;for(const f of flows){cum+=f;peak=Math.max(peak,-cum)}
 return {rows,flows,npv,irr:irr(flows),payback:pb(0),discountedPayback:pb(discount),peakFunding:peak,growthPass,capex:soft+phys};
}
export function irr(flows){if(!flows.some(x=>x<0)||!flows.some(x=>x>0))return null;const fun=r=>sum(flows.map((f,i)=>f/(1+r)**i));let l=-.95,h=100;if(fun(l)*fun(h)>0)return null;for(let i=0;i<120;i++){const m=(l+h)/2;if(fun(l)*fun(m)<=0)h=m;else l=m}return(l+h)/2}
export function evaluate(world,policy,opts={}){const op=operating(world,policy,opts),cf=operating(world,{package:'current',target:.5,buffer:1},opts);return {op,cf,financial:finance(op,cf,policy.package,world,opts)}}
export function quantile(a,p){const x=a.slice().sort((a,b)=>a-b),k=(x.length-1)*p,i=Math.floor(k);return x[i]+(x[Math.min(i+1,x.length-1)]-x[i])*(k-i)}
export function summarise(results){const vals=results.map(x=>x.financial.npv);return {n:vals.length,mean:sum(vals)/vals.length,p10:quantile(vals,.1),p50:quantile(vals,.5),p90:quantile(vals,.9),positive:vals.filter(x=>x>0).length/vals.length,violations:results.filter(x=>x.op.some(r=>r.violation)).length/results.length,values:vals}}

/* Small continuous min-cost-flow solver: regional transport graph, not vehicle routing. */
export function minCostFlow(demand,cost,capacity,external,extCap,emergency=0){
 const h=capacity.length,z=demand.length,source=0,hub=1,ext=hub+h,em=ext+1,back=ext+2,zone=back+1,sink=zone+z,N=sink+1,g=Array.from({length:N},()=>[]);
 const add=(a,b,cap,cost)=>{const e={to:b,rev:g[b].length,cap,cost,original:cap};g[a].push(e);g[b].push({to:a,rev:g[a].length-1,cap:0,cost:-cost,original:0});return e};
 const he=Array.from({length:h},()=>[]),ex=[],ee=[],uu=[];
 capacity.forEach((c,i)=>add(source,hub+i,c,0));add(source,ext,extCap,0);add(source,em,emergency,0);add(source,back,sum(demand),0);
 for(let j=0;j<z;j++){for(let i=0;i<h;i++)he[i][j]=add(hub+i,zone+j,sum(demand),cost[i][j]);ex[j]=add(ext,zone+j,sum(demand),external[j]);ee[j]=add(em,zone+j,sum(demand),14000);uu[j]=add(back,zone+j,sum(demand),18000);add(zone+j,sink,demand[j],0)}
 let remain=sum(demand),total=0,iterations=0;
 while(remain>1e-5&&iterations++<1000){const dist=Array(N).fill(Infinity),pn=Array(N),pe=Array(N),queued=Array(N).fill(false),queue=[source];dist[source]=0;queued[source]=true;
  for(let pos=0;pos<queue.length;pos++){const n=queue[pos];queued[n]=false;g[n].forEach((e,k)=>{if(e.cap>1e-7&&dist[e.to]>dist[n]+e.cost+1e-8){dist[e.to]=dist[n]+e.cost;pn[e.to]=n;pe[e.to]=k;if(!queued[e.to]){queue.push(e.to);queued[e.to]=true}}})}
  if(!Number.isFinite(dist[sink]))throw Error('Alokasi tidak terhubung');let f=remain;for(let n=sink;n!==source;n=pn[n])f=Math.min(f,g[pn[n]][pe[n]].cap);for(let n=sink;n!==source;n=pn[n]){const e=g[pn[n]][pe[n]];e.cap-=f;g[n][e.rev].cap+=f}remain-=f;total+=f*dist[sink];
 }
 const used=e=>e.original-e.cap;return{internal:he.map(a=>a.map(used)),external:ex.map(used),emergency:ee.map(used),deferred:uu.map(used),cost_idr:total};
}
