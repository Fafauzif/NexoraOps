import{evaluate,summarise}from'./engine.js';
let worlds;
const stress=(w,s)=>s==='weak'?{...w,eff:[0],adoption:[.5]}:s==='overrun'?{...w,overrun:[1.6],adoption:[.65]}:w;
onmessage=async({data:m})=>{try{worlds??=await(await fetch('./data/worlds.json')).json();const start=performance.now();
 if(m.type==='heatmap'){let cells=[];for(let t=.45;t<.951;t+=.05)for(const axis of [.8,.9,1,1.1,1.2,1.4]){const policy={...m.policy,target:Math.round(t*100)/100};let rr=[];for(let i=0;i<100;i++)rr.push(evaluate(stress(worlds[i],m.opts.scenario),policy,{...m.opts,axis:axis*(m.opts.scenario==='campaign'?1.35:1)}));const s=summarise(rr);cells.push({target:policy.target,axis,mean:s.mean,p10:s.p10,violation:s.violations,share:rr.reduce((v,r)=>v+r.op[4].share,0)/rr.length});postMessage({type:'progress',progress:cells.length/66});await new Promise(r=>setTimeout(r,0))}postMessage({type:'heatmap',cells,runtime:performance.now()-start,n:100});
 }else{let rr=[];const count=Math.min(m.n,worlds.length);for(let i=0;i<count;i++){rr.push(evaluate(stress(worlds[i],m.opts.scenario),m.policy,m.opts));if(i%100===0){postMessage({type:'progress',progress:i/count});await new Promise(r=>setTimeout(r,0))}}postMessage({type:'result',result:summarise(rr),runtime:performance.now()-start,seed:20261101})}
 }catch(e){postMessage({type:'error',message:e.message})}};
