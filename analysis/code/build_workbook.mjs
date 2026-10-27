// Run from a private OS tmp directory with node_modules symlinked to
// $CODEX_PRIMARY_RUNTIME_NODE_MODULES, using $CODEX_PRIMARY_RUNTIME_NODE.
// Copy this builder there; pass NEXORA_ROOT=/absolute/package/path.
import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.NEXORA_ROOT || path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const data=JSON.parse(await fs.readFile(path.join(root,'results/workbook_inputs.json'),'utf8'));
const out=path.join(root,'outputs/nexora_v1');await fs.mkdir(out,{recursive:true});
const wb=Workbook.create();
const names=['Summary','Finance','Policy Lab','Heatmap','Capacity','Geography','Risk','Case Facts','Assumptions','Sources','Ops Import','Audit','ReadMe'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const navy='#193C5A',blue='#315F83',amber='#F4D9A6',ink='#253645',grey='#EEF2F5',red='#9D3030',green='#17743C';
const num='#,##0.000;(#,##0.000);"–"';const pct='0.0%;(0.0%);"–"';
function cell(s,a,v){sheets[s].getRange(a).values=[[v]];}
function formula(s,a,v){sheets[s].getRange(a).formulas=[[v]];sheets[s].getRange(a).format.font.color=v.includes("'!")||v.includes("'!")?'#17743C':'#000000';}
function write(s,a,rows){sheets[s].getRange(a).write(rows);}
function head(s,r,c,labels){const sh=sheets[s];const rg=sh.getRangeByIndexes(r-1,c-1,1,labels.length);rg.values=[labels];rg.format={fill:navy,font:{name:'Arial',bold:true,color:'#FFFFFF',size:10},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,rowHeight:32};}
function title(s,t){cell(s,'C2',t);sheets[s].getRange('C2').format.font={name:'Arial',size:15,bold:true,color:navy};sheets[s].getRange('C3:K3').format.borders={bottom:{style:'thin',color:blue}};}
function input(s,a,v,fmt){cell(s,a,v);const rg=sheets[s].getRange(a);rg.format={fill:'#FFF3D8',font:{color:'#0000FF'},horizontalAlignment:'right'};if(fmt)rg.setNumberFormat(fmt);}
function note(s,a,v){cell(s,a,v);sheets[s].getRange(a).format.font={name:'Arial',size:10,color:'#596775',italic:true};}
for(const n of names){const sh=sheets[n];sh.showGridLines=false;sh.getRange('A1:V170').format.font={name:'Arial',size:10,color:ink};sh.getRange('A1:B170').format.columnWidth=2.2;sh.getRange('C1:C170').format.columnWidth=36;sh.getRange('D1:V170').format.columnWidth=16;sh.getRange('C1:V170').format.rowHeight=22;sh.getRange('D4:V170').setNumberFormat(num);sh.getRange('C1:V170').format.verticalAlignment='center';}
sheets.Summary.tabColor=navy;sheets.Finance.tabColor=blue;sheets.ReadMe.tabColor='#8A939B';

// CASE FACTS AND BASELINE BUILD
title('Case Facts','Case facts and baseline reconciliation');head('Case Facts',4,3,['2025 fact','Value','Unit / source']);
write('Case Facts','C5',[
 ['GMV',600,'Rp tn, handoff p.7'],['Platform revenue',60,'Rp tn, p.7'],['Marketing',24,'Rp tn, p.7'],['Annual parcels',2,'bn parcels, p.10'],['Internal share',.5,'fraction, p.10'],['Internal cost',8000,'IDR/parcel, p.10'],['External cost',12000,'IDR/parcel, p.10'],['Group operating profit',5,'Rp tn, p.7'],['Small-seller churn',.12,'annual, p.10'],['Repeat-buyer rate 2024',.62,'fraction, p.10'],['Repeat-buyer rate 2025',.57,'fraction, p.10']]);
sheets['Case Facts'].getRange('D9').setNumberFormat(pct);sheets['Case Facts'].getRange('D13:D15').setNumberFormat(pct);sheets['Case Facts'].getRange('D10:D11').setNumberFormat('#,##0');sheets['Case Facts'].getRange('E1:E35').format.columnWidth=32;
head('Case Facts',17,3,['Derived identity','Value','Interpretation']);
const facts=[['Blended cost','=D9*D10+(1-D9)*D11','IDR/parcel'],['Delivery spending','=D8*D18/1000','Rp tn; conditional aligned scopes'],['Internal delivery spending','=D8*D9*D10/1000','Rp tn'],['External delivery spending','=D8*(1-D9)*D11/1000','Rp tn'],['GMV per parcel','=D5*1000/D8','IDR; not proven order value'],['Revenue per parcel','=D6*1000/D8','IDR; not marginal contribution'],['Other operating costs','=D6-D7-D12','Rp tn including logistics'],['Conditional residual','=D24-D19','Rp tn; not identified fixed overhead'],['10pp mechanical switch saving','=D8*0.1*(D11-D10)/1000','Rp tn; reference, not forecast'],['Rp1,000/parcel sanity check','=D8','Rp tn per 1,000 IDR/parcel']];
facts.forEach((r,i)=>{cell('Case Facts',`C${18+i}`,r[0]);formula('Case Facts',`D${18+i}`,r[1]);cell('Case Facts',`E${18+i}`,r[2]);});
note('Case Facts','G5','Source access: supplied Markdown extract. Original casebook PDF not inspected.');
head('Case Facts',8,7,['2024 fact','Value','Source']);write('Case Facts','G9',[['GMV',560,'Rp tn,p.7'],['Revenue',45,'Rp tn,p.7'],['Marketing',28,'Rp tn,p.7'],['Delivery cost/parcel',12000,'IDR,p.7'],['Operating loss',-3,'Rp tn,p.7'],['Reported take rate',.08,'rounded,p.7']]);cell('Case Facts','G16','Exact implied 2024 take rate');formula('Case Facts','H16','=H10/H9');sheets['Case Facts'].getRange('H14:H16').setNumberFormat(pct);sheets['Case Facts'].getRange('G1:G35').format.columnWidth=28;

// IMPORTED POLICY OPERATING RESULTS: explicit refresh boundary.
title('Ops Import','Imported operating results for deterministic finance');cell('Ops Import','C3','Reference operating inflation');cell('Ops Import','D3',.025);sheets['Ops Import'].getRange('D3').setNumberFormat(pct);
const ops=data.central7;
head('Ops Import',4,3,['Policy ID','Package','Share ceiling','Buffer','Software capex','Physical capex','Transition','Y1 real benefit','Y2 real benefit','Y3 real benefit','Y4 real benefit','Y5 real benefit','Y6 real benefit','Y7 real benefit','Mean NPV','p10 NPV','p90 NPV','Service violation']);
write('Ops Import','C5',ops.map(o=>{const s=data.policies.finalists.find(x=>x.policy_id===o.policy_id);return[o.policy_id,o.package,o.target,o.buffer,o.soft_capex,o.physical_capex,o.transition,...o.benefit_2025_tn,s.expected_npv_tn,s.p10_npv_tn,s.p90_npv_tn,s.service_violation_world_fraction];}));
sheets['Ops Import'].getRange('C1:C30').format.columnWidth=32;sheets['Ops Import'].getRange('E5:F18').setNumberFormat(pct);sheets['Ops Import'].getRange('T5:T18').setNumberFormat(pct);sheets['Ops Import'].freezePanes.unfreeze();note('Ops Import','C22','Imported real benefits include recurring package costs. Changing dispatch/capacity assumptions requires script refresh.');note('Ops Import','C24','All monetary inputs here are Rp tn. Benefits are 2025-price net operating cost reductions, before transition/D&A.');

// ONE EDITABLE DETERMINISTIC FINANCIAL BUILD.
title('Finance','Incremental project cash flow and annual profit gate');
const selected=ops.findIndex(o=>o.policy_id===data.analysis.recommended.policy_id)+1;
const controls=[['Policy selector',selected,'0'],['Nominal IDR discount rate',.14,pct],['Evaluation horizon',5,'0'],['Tax rate',.22,pct],['Nominal logistics inflation',.025,pct],['Other net OP increase per year',0,num],['Implementation cost multiplier',1,'0.00x'],['Operating benefit multiplier',1,'0.00x'],['Physical book-value recovery',.35,pct]];
controls.forEach((r,i)=>{cell('Finance',`C${i+4}`,r[0]);input('Finance',`D${i+4}`,r[1],r[2]);});
sheets.Finance.getRange('D4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:ops.length}};
sheets.Finance.getRange('D6').dataValidation={rule:{type:'list',values:['3','5','7']}};
formula('Finance','F4',`=INDEX('Ops Import'!$C$5:$C$${4+ops.length},$D$4)`);sheets.Finance.getRange('F4').format.font.color=green;sheets.Finance.getRange('F4:I4').format.borders={bottom:{style:'dotted',color:blue}};
const end=4+ops.length;
[['G5','Software initial capex'],['G6','Physical initial capex'],['G7','Transition expense'],['G8','Initial working capital'],['G9','Import reference inflation'],['G10','Starting group OP'],['G11','Software economic life'],['G12','Vehicle life'],['G13','Sortation life'],['G14','Leasehold life']].forEach(([a,v])=>cell('Finance',a,v));sheets.Finance.getRange('G1:G15').format.columnWidth=29;
formula('Finance','H5',`=INDEX('Ops Import'!$G$5:$G$${end},$D$4)*$D$10`);formula('Finance','H6',`=INDEX('Ops Import'!$H$5:$H$${end},$D$4)*$D$10`);formula('Finance','H7',`=INDEX('Ops Import'!$I$5:$I$${end},$D$4)*$D$10`);formula('Finance','H8','=H5*0.01+H6*0.02');formula('Finance','H9',"='Ops Import'!D3");formula('Finance','H10',"='Case Facts'!D12");input('Finance','H11',4,'0');input('Finance','H12',5,'0');input('Finance','H13',8,'0');input('Finance','H14',10,'0');
note('Finance','J7','Blue / amber cells are editable.');note('Finance','J9','Operating allocations remain imported.');note('Finance','J11','Cash flows are unlevered, Rp tn.');note('Finance','J13','Positive NPV does not override failed annual OP growth.');
head('Finance',16,3,['Model year',0,1,2,3,4,5,6,7]);
sheets.Finance.getRange('D16:K16').setNumberFormat('0');
const labels={18:'National annual workload, bn',19:'Matched current logistics cost',20:'Net operating cost reduction',21:'Transition cash expense',22:'Software depreciation',23:'Physical depreciation',24:'Total depreciation',25:'Incremental operating profit',26:'Matched current group OP',27:'Policy group operating profit',28:'Annual group OP change',29:'Annual group OP growth',30:'Annual positive-growth test',31:'Incremental EBITDA',32:'Incremental cash tax',33:'Initial capital expenditure',34:'Replacement expenditure',35:'Working-capital cash flow',36:'Physical salvage proceeds',37:'Unlevered project cash flow',38:'Discount factor',39:'Present value',40:'Cumulative cash flow',41:'Cumulative present value'};
for(const[r,l]of Object.entries(labels))cell('Finance',`C${r}`,l);
for(let c=4;c<=11;c++){
 const L=String.fromCharCode(64+c),prev=String.fromCharCode(63+c),year=c-4;
 for(const rr of Object.keys(labels))cell('Finance',`${L}${rr}`,0);
 if(year===0){formula('Finance',`${L}33`,'=-SUM($H$5:$H$6)');formula('Finance',`${L}35`,'=-$H$8');}
 else{
  const y=`${L}$16`,active=`${y}<=$D$6`;
  const factor=(start,life)=>`MAX(MIN(${y}-${start}+0.5,${life})-MAX(MIN(${y}-${start}-0.5,${life}),0),0)/${life}`;
  formula('Finance',`${L}18`,`=IF(${active},'Case Facts'!$D$8,0)`);
  formula('Finance',`${L}19`,`=IF(${active},'Case Facts'!$D$19*(1+$D$8)^${y},0)`);
  formula('Finance',`${L}20`,`=IF(${active},INDEX('Ops Import'!$J$5:$P$${end},$D$4,${y})*(1+$D$8)^${y}*$D$11,0)`);
  formula('Finance',`${L}21`,`=IF(AND(${active},${y}=1),$H$7,0)`);
  formula('Finance',`${L}22`,`=IF(${active},$H$5*(${factor(1,'$H$11')})+$H$5*0.5*(${factor(5,'$H$11')}),0)`);
  formula('Finance',`${L}23`,`=IF(${active},$H$6*(0.3*(${factor(1,'$H$12')})+0.4*(${factor(1,'$H$13')})+0.3*(${factor(1,'$H$14')}))+$H$6*0.3*(${factor(6,'$H$12')}),0)`);
  formula('Finance',`${L}24`,`=SUM(${L}22:${L}23)`);formula('Finance',`${L}25`,`=${L}20-${L}21-${L}24`);
  formula('Finance',`${L}26`,`=IF(${active},$H$10-(${L}19-'Case Facts'!$D$19)+${y}*$D$9,"")`);
  formula('Finance',`${L}27`,`=IF(${active},${L}26+${L}25,"")`);
  formula('Finance',`${L}28`,`=IF(${active},${L}27-${year===1?'$H$10':prev+'27'},"")`);
  formula('Finance',`${L}29`,`=IF(${active},IF(${year===1?'$H$10':prev+'27'}=0,"n.a.",${L}28/${year===1?'$H$10':prev+'27'}),"")`);
  formula('Finance',`${L}30`,`=IF(${active},IF(${L}28>0,"PASS","FAIL"),"")`);
  formula('Finance',`${L}31`,`=${L}20-${L}21`);formula('Finance',`${L}32`,`=MAX(${L}25,0)*$D$7`);
  formula('Finance',`${L}34`,`=IF(${active},IF(${y}=5,-$H$5*0.5,0)+IF(${y}=6,-$H$6*0.3,0),0)`);
  formula('Finance',`${L}35`,`=IF(${y}=$D$6,$H$8,0)`);
  formula('Finance',`${L}36`,`=IF(${y}=$D$6,MAX($H$6+IF(${y}>=6,$H$6*0.3,0)-SUM($E$23:${L}23),0)*$D$12,0)`);
 }
 formula('Finance',`${L}37`,`=${L}31-${L}32+SUM(${L}33:${L}36)`);formula('Finance',`${L}38`,`=1/(1+$D$5)^${L}$16`);formula('Finance',`${L}39`,`=${L}37*${L}38`);formula('Finance',`${L}40`,`=SUM($D$37:${L}37)`);formula('Finance',`${L}41`,`=SUM($D$39:${L}39)`);
}
[['C43','Project NPV'],['C44','Project IRR'],['C45','Payback, years'],['C46','Discounted payback, years'],['C47','Peak funding need'],['C48','All annual profit growth positive'],['C49','IRR above selected discount']].forEach(([a,v])=>cell('Finance',a,v));
formula('Finance','D43','=SUM(D39:K39)');formula('Finance','D44','=IF(SUM($H$5:$H$6)=0,"n.a.",IRR(D37:K37))');sheets.Finance.getRange('D44').setNumberFormat(pct);
function pb(cum,cash){let f='"not reached"';for(let y=7;y>=1;y--){const l=String.fromCharCode(68+y),pr=String.fromCharCode(67+y);f=`IF(${l}${cum}>=0,${y-1}-${pr}${cum}/${l}${cash},${f})`;}return`=IF(D${cum}>=0,0,${f})`;}
formula('Finance','D45',pb(40,37));formula('Finance','D46',pb(41,39));formula('Finance','D47','=-MIN(D40:K40)');formula('Finance','D48','=IF(AND(COUNT(E28:K28)=$D$6,MIN(E28:K28)>0),"PASS","FAIL")');formula('Finance','D49','=IF(SUM(H5:H6)=0,"n.a.",IF(D44>D5,"PASS","FAIL"))');sheets.Finance.getRange('E29:K29').setNumberFormat(pct);sheets.Finance.getRange('D38:K38').setNumberFormat('0.000');
for(const row of [25,27,37,43]){sheets.Finance.getRange(`C${row}:K${row}`).format={fill:grey,font:{bold:true},borders:{top:{style:'thin',color:'#AFBCC6'}}};}
sheets.Finance.getRange('D48').conditionalFormats.add('containsText',{text:'FAIL',format:{fill:'#FCE7E7',font:{color:red,bold:true}}});sheets.Finance.getRange('E30:K30').conditionalFormats.add('containsText',{text:'FAIL',format:{fill:'#FCE7E7',font:{color:red,bold:true}}});
cell('Finance','N14','NPV sensitivity: capex multiple vs discount');cell('Finance','N15','Native two-input Excel data table');formula('Finance','N17','=D43');write('Finance','O17',[[.11,.14,.18]]);write('Finance','N18',[[.8],[1],[1.6]]);sheets.Finance.dataTables.add('N17:Q20',{rowInput:'D5',columnInput:'D10'});sheets.Finance.getRange('O17:Q17').setNumberFormat(pct);sheets.Finance.getRange('N18:N20').setNumberFormat('0.00x');sheets.Finance.getRange('O18:Q20').conditionalFormats.add('colorScale',{colors:['#F1D5D5','#FFFFFF','#BCD9C8'],thresholds:['min','50%','max']});
sheets.Finance.freezePanes.unfreeze();

// SUMMARY
title('Summary','Nexora logistics investment assessment');
cell('Summary','C5','Conditional investment candidate');formula('Summary','D5',"='Finance'!F4");sheets.Summary.getRange('D5').format.font.color=green;
const summaryRows=[['Central project NPV',"='Finance'!D43"],['Held-out mean NPV',`=INDEX('Ops Import'!$Q$5:$Q$${end},'Finance'!D4)`],['Held-out p10 NPV',`=INDEX('Ops Import'!$R$5:$R$${end},'Finance'!D4)`],['Central project IRR',"='Finance'!D44"],['Year1 group operating profit',"='Finance'!E27"],['Annual group-profit growth gate',"='Finance'!D48"]];
summaryRows.forEach((r,i)=>{cell('Summary',`C${7+i}`,r[0]);formula('Summary',`D${7+i}`,r[1]);sheets.Summary.getRange(`D${7+i}`).format.font.color=ink;});sheets.Summary.getRange('D10').setNumberFormat(pct);sheets.Summary.getRange('D12').conditionalFormats.add('containsText',{text:'FAIL',format:{fill:'#FCE7E7',font:{color:red,bold:true}}});
cell('Summary','C14','No national rollout passes the central annual-profit-growth requirement.');cell('Summary','C15','Detailed street GIS acquisition remains partial; regional layers are a labelled corridor fallback.');cell('Summary','C16','Rules are a close challenger. Software and targeted upgrades require operating evidence before commitment.');
const displayIds=['P_CURRENT','P_RULES_70_88',data.analysis.recommended.policy_id,data.analysis.maxreturn.policy_id,'P_TARGETED_75_100','P_LARGE_85_100'];
const shortNames=['Current','Rules 88%','Software 88%','Software 100%','Targeted','Large'];
head('Summary',18,3,['Policy','Mean NPV','p10 NPV','p90 NPV','Violation worlds','Realised internal','Mean capex']);write('Summary','C19',displayIds.map((id,i)=>{const s=data.policies.finalists.find(a=>a.policy_id===id);return[shortNames[i],s.expected_npv_tn,s.p10_npv_tn,s.p90_npv_tn,s.service_violation_world_fraction,s.realised_internal_share,s.initial_capex_tn];}));sheets.Summary.getRange('G19:H24').setNumberFormat(pct);note('Summary','C26','Rp tn unless stated. Percentages in policy labels are capacity-buffer settings.');note('Summary','C28','Year 1 savings do not prove positive group-profit growth. Percentiles reflect authored distributions.');
const chart=sheets.Summary.charts.add('bar',sheets.Summary.getRange('C18:D24'));chart.title='Expected five-year NPV';chart.setPosition('L4','U21');chart.hasLegend=false;chart.yAxis={numberFormatCode:'0.0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:11}};chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};chart.series.items[0].fill=blue;

// POLICY LAB and all evaluated candidates
title('Policy Lab','Policy search and held-out evaluation');note('Policy Lab','C3','Imported simulation results. All shortlisted central annual-growth gates fail. No global optimality claim.');
note('Policy Lab','C4','Money is Rp tn. Share ceilings differ from realised shares. Service violations are planning-model outcomes.');
const ph=['Policy ID','Package','Share ceiling','Buffer','Mean NPV','Median NPV','p10 NPV','Positive NPV','Y1 ΔEBIT','Y5 ΔEBIT','Internal share','Violation worlds','Growth-pass worlds','Mean capex'];
head('Policy Lab',5,3,ph);write('Policy Lab','C6',data.policies.finalists.map(s=>[s.policy_id,s.package,s.target,s.buffer,s.expected_npv_tn,s.median_npv_tn,s.p10_npv_tn,s.prob_positive_npv,s.expected_y1_ebit_tn,s.expected_y5_ebit_tn,s.realised_internal_share,s.service_violation_world_fraction,s.prob_positive_growth_all_years,s.initial_capex_tn]));
for(const a of ['E6:F19','J6:J19','M6:O19'])sheets['Policy Lab'].getRange(a).setNumberFormat(pct);head('Policy Lab',23,3,['Screened policy','Package','Ceiling','Buffer','Mean NPV','p10 NPV','Violation worlds','Realised share']);write('Policy Lab','C24',data.policies.screening.map(s=>[s.policy_id,s.package,s.target,s.buffer,s.expected_npv_tn,s.p10_npv_tn,s.service_violation_world_fraction,s.realised_internal_share]));for(const a of ['E24:F156','I24:J156'])sheets['Policy Lab'].getRange(a).setNumberFormat(pct);sheets['Policy Lab'].freezePanes.unfreeze();

// NUMERIC HEATMAP
title('Heatmap','Year5 incremental operating profit heatmap');note('Heatmap','C4','Rp tn. Same-demand counterfactual per cell. Requested ceiling may not be reached.');
const targets=[...new Set(data.heatmap.cells.map(c=>c.target_share))].sort((a,b)=>a-b),demands=[...new Set(data.heatmap.cells.map(c=>c.demand_axis))].sort((a,b)=>a-b);
head('Heatmap',6,3,['Internal-share ceiling',...demands]);
targets.forEach((t,i)=>write('Heatmap',`C${7+i}`,[[t,...demands.map(d=>data.heatmap.cells.find(c=>c.target_share===t&&c.demand_axis===d).expected_y5_ebit_tn)]]));sheets.Heatmap.getRange('C7:C17').setNumberFormat(pct);sheets.Heatmap.getRange('D6:I6').setNumberFormat(pct);sheets.Heatmap.getRange('D7:I17').conditionalFormats.add('colorScale',{colors:['#EFC3C3','#FFFFFF','#B8D5C3'],thresholds:['min','50%','max']});
targets.forEach((t,i)=>demands.forEach((d,j)=>{const c=data.heatmap.cells.find(c=>c.target_share===t&&c.demand_axis===d);if(!c.feasible)sheets.Heatmap.getRangeByIndexes(6+i,3+j,1,1).setNumberFormat('0.000" *";(0.000)" *";"– *"');}));
note('Heatmap','C19','* Requested share not attained or service-risk limit failed. Actual fallback outcome shown; reasons below.');
head('Heatmap',21,3,['Cell ID','Ceiling','Demand axis','Realised share','ΔEBIT Y5','NPV','Feasible requested point','Reason']);write('Heatmap','C22',data.heatmap.cells.map(c=>[c.cell_id,c.target_share,c.demand_axis,c.realised_internal_share,c.expected_y5_ebit_tn,c.expected_npv_tn,c.feasible,c.reasons.join('; ')||'Within model limits']));sheets.Heatmap.getRange('D22:F87').setNumberFormat(pct);sheets.Heatmap.getRange('J1:J90').format.columnWidth=62;sheets.Heatmap.getRange('J22:J87').format.wrapText=true;sheets.Heatmap.getRange('C22:J87').format.rowHeight=33;sheets.Heatmap.freezePanes.unfreeze();

// CAPACITY / EDITABLE CALIBRATION
title('Capacity','Marginal cost, committed costs and capacity');
head('Capacity',5,3,['Market type','Weight','Historical share','Type demand bn','Internal q0 bn','Capacity bn','Avg internal IDR','External IDR','Fixed fraction','Fixed cost tn','Variable IDR','Utilisation']);
data.config.national_market_types.forEach((t,i)=>{const r=6+i;write('Capacity',`C${r}`,[[t,data.config.weights[i],data.config.baseline_internal_shares[i],null,null,data.config.capacity_bn[i],data.config.internal_costs[i],data.config.external_costs[i],.25]]);formula('Capacity',`F${r}`,`=D${r}*'Case Facts'!$D$8`);formula('Capacity',`G${r}`,`=F${r}*E${r}`);formula('Capacity',`L${r}`,`=G${r}*I${r}*K${r}/1000`);formula('Capacity',`M${r}`,`=I${r}*(1-K${r})-IF(G${r}=0,0,${[3500,4500,6500,8000][i]}*MAX(G${r}-0.85*H${r},0)^2/(0.30*H${r})/G${r})`);formula('Capacity',`N${r}`,`=G${r}/H${r}`);});sheets.Capacity.getRange('D6:E9').setNumberFormat(pct);sheets.Capacity.getRange('K6:K9').setNumberFormat(pct);sheets.Capacity.getRange('N6:N9').setNumberFormat(pct);sheets.Capacity.getRange('I6:J9').setNumberFormat('#,##0');
head('Capacity',12,3,['Capacity interpretation','Parcel capacity bn','Truck equivalents','Courier equivalents','Sort parcels/hour']);
data.config.national_market_types.forEach((t,i)=>{const r=13+i;cell('Capacity',`C${r}`,t);formula('Capacity',`D${r}`,`=H${6+i}`);formula('Capacity',`E${r}`,`=ROUNDUP(D${r}*1000000000/365/2400,0)`);formula('Capacity',`F${r}`,`=ROUNDUP(D${r}*1000000000/365/80,0)`);formula('Capacity',`G${r}`,`=D${r}*1000000000/365/8`);});sheets.Capacity.getRange('E13:G16').setNumberFormat('#,##0');note('Capacity','C18','Hypothetical equivalents: 2,400 parcels/truck-day; 80/courier-day; 8 sort hours. Not an observed fleet count.');note('Capacity','C20','Effective capacity is the minimum of hub, linehaul and courier ceilings; upgrades must deliver all three.');
head('Capacity',23,3,['Market type','Capacity use','Internal q bn','Average IDR','Marginal IDR','External IDR','Within capacity']);write('Capacity','C24',data.curves.map(c=>[c.market_type,c.capacity_fraction,c.internal_bn,c.average_cost_idr,c.marginal_cost_idr,c.external_price_idr,c.feasible]));sheets.Capacity.getRange('D24:D123').setNumberFormat(pct);sheets.Capacity.getRange('F24:H123').setNumberFormat('#,##0');sheets.Capacity.freezePanes.unfreeze();

// GEOGRAPHY: explicit synthetic and fallback labels
title('Geography','Greater Jakarta corridor fallback');note('Geography','C4','PARTIAL GIS gate. Schematic geometry and some corridor weights are authored. No downloaded street/building extract.');
head('Geography',6,3,['Regional assumption','Value','Unit / meaning']);write('Geography','C7',[['National-volume allocation',.20,'assumed fraction'],['Regional parcels annually',400000000,'parcels/year'],['Regional parcels daily',400000000/365,'parcels/day'],['Corridor nodes / edges','16 / 17','34 directed arcs'],['Analytical zones / facilities','9 / 4','all facilities hypothetical'],['CRS','OGC:CRS84','longitude, latitude'],['Road acquisition','PARTIAL','coarse corridor attributes only']]);sheets.Geography.getRange('E1:E80').format.columnWidth=29;sheets.Geography.getRange('D7').setNumberFormat(pct);sheets.Geography.getRange('D8:D9').setNumberFormat('#,##0');
head('Geography',17,3,['Zone','Name','Daily synthetic parcels','Internal fraction','Advantage IDR','Capacity pressure','Switching fraction']);const zones=data.geo.features.filter(x=>x.properties.policy_id==='P_RULES_70_88').map(x=>x.properties);write('Geography','C18',zones.map(z=>[z.zone_id,z.name,z.daily_parcels,z.internal_fraction,z.marginal_advantage_idr,z.max_shared_hub_pressure,z.internal_majority_fraction_of_200_worlds]));sheets.Geography.getRange('D18:D26').setNumberFormat('@');sheets.Geography.getRange('D1:D80').format.columnWidth=31;sheets.Geography.getRange('F18:F26').setNumberFormat(pct);sheets.Geography.getRange('H18:I26').setNumberFormat(pct);sheets.Geography.getRange('E18:E26').setNumberFormat('#,##0');sheets.Geography.getRange('G18:G26').setNumberFormat('#,##0');
head('Geography',30,3,['Lane ID','Hub ID','Zone ID','Corridor km','Estimated minutes','Reachable','Local access km']);write('Geography','C31',data.routes.lanes.map(l=>[l.lane_id,l.hub_id,l.zone_id,l.corridor_network_km,l.estimated_one_way_minutes,l.reachable,l.local_access_distance_km]));sheets.Geography.getRange('F31:G66').setNumberFormat('0.0');sheets.Geography.freezePanes.unfreeze();

// UNCERTAINTY AND STRESS, all preserved.
title('Risk','Monte Carlo, structural reversals and stress');write('Risk','C5',[['Screen candidates',data.analysis.screening_candidates],['Screen worlds each',1000],['Fresh finalists',data.analysis.finalists],['Fresh worlds each',10000],['Screen seed',data.analysis.screen_seed],['Fresh seed',data.analysis.heldout_seed],['National analysis seconds',data.analysis.runtime_seconds],['Required annual other OP increase',data.analysis.minimum_annual_nonlogistics_ebit_increase_tn],['Break-even initial candidate capex',data.analysis.break_even_initial_capex_tn]]);sheets.Risk.getRange('D5:D10').setNumberFormat('#,##0');
head('Risk',16,3,['Sensitivity driver','Low','High','NPV at low','NPV at high']);write('Risk','C17',data.analysis.sensitivity.map(s=>[s.driver,s.low,s.high,s.npv_at_low,s.npv_at_high]));
head('Risk',25,3,['Structural variant','Policy ID','Mean NPV','p10 NPV','Baseline internal share']);write('Risk','C26',data.analysis.structural.map(s=>[s.variant,s.policy_id,s.expected_npv_tn,s.p10_npv_tn,s.baseline_internal_share]));sheets.Risk.getRange('D1:D145').format.columnWidth=31;sheets.Risk.getRange('G26:G137').setNumberFormat(pct);
head('Risk',142,3,['Stress scenario','Policy ID','NPV','Y1 ΔEBIT','Y5 ΔEBIT','Min planning feasibility','Growth gate']);write('Risk','C143',data.analysis.stresses.map(s=>[s.scenario_id,s.policy_id,s.npv_tn,s.y1_ebit_tn,s.y5_ebit_tn,s.service_min,s.growth_pass]));sheets.Risk.getRange('C143:I268').format.rowHeight=23;sheets.Risk.getRange('C143:I268').format.font={name:'Arial',size:10};sheets.Risk.getRange('H143:H268').setNumberFormat(pct);sheets.Risk.freezePanes.unfreeze();

// SOURCE AND ASSUMPTION REGISTERS
title('Assumptions','Authored assumptions and sensitivity ranges');head('Assumptions',5,3,['ID','Input','Central / array','Unit','Low','High','Reason and scope','Source / confidence']);
const str=x=>x===null?'n.a.':Array.isArray(x)?x.join(' / '):x;
write('Assumptions','C6',data.assumptions.map(a=>[a.id,a.name,str(a.value),a.unit,str(a.low),str(a.high),a.reason,(a.source||'Analyst assumption')+'; '+a.confidence]));sheets.Assumptions.getRange('C1:C60').format.columnWidth=9;sheets.Assumptions.getRange('D1:D60').format.columnWidth=32;sheets.Assumptions.getRange('E1:E60').format.columnWidth=27;sheets.Assumptions.getRange('F1:F60').format.columnWidth=26;sheets.Assumptions.getRange('I1:I60').format.columnWidth=90;sheets.Assumptions.getRange('J1:J60').format.columnWidth=55;sheets.Assumptions.getRange('D6:J53').format.wrapText=true;sheets.Assumptions.getRange('C6:J53').format.rowHeight=50;sheets.Assumptions.freezePanes.unfreeze();
title('Sources','Primary-source and acquisition register');head('Sources',5,3,['Source ID','Title','Date / scope','Access route and status','URL','Observation / license']);write('Sources','C6',data.sources.map(s=>[s.id,s.title,s.date+'; '+s.scope,s.access,s.url||'Supplied extract',s.observation+' '+s.license]));sheets.Sources.getRange('C1:C30').format.columnWidth=21;sheets.Sources.getRange('D1:D30').format.columnWidth=57;sheets.Sources.getRange('E1:E30').format.columnWidth=48;sheets.Sources.getRange('F1:F30').format.columnWidth=76;sheets.Sources.getRange('G1:G30').format.columnWidth=85;sheets.Sources.getRange('H1:H30').format.columnWidth=80;sheets.Sources.getRange('C6:H18').format.wrapText=true;sheets.Sources.getRange('C6:H18').format.rowHeight=68;sheets.Sources.freezePanes.unfreeze();

// TERMINAL AUDIT. No other worksheet reads this area.
title('Audit','Validation results and remaining gate');head('Audit',5,3,['Check','Status / difference','Detail']);write('Audit','C6',data.validation.checks.map(c=>[c.check_id,c.status,c.detail]));sheets.Audit.getRange('E1:E40').format.columnWidth=95;sheets.Audit.getRange('E6:E20').format.wrapText=true;sheets.Audit.getRange('C6:E20').format.rowHeight=34;
cell('Audit','C23','Blend versus case');formula('Audit','D23',"='Case Facts'!D18-10000");cell('Audit','C24','Delivery spending versus case-derived');formula('Audit','D24',"='Case Facts'!D19-20");cell('Audit','C25','Finance NPV versus sum PV');formula('Audit','D25',"='Finance'!D43-SUM('Finance'!D39:K39)");cell('Audit','C26','Annual growth detection');formula('Audit','D26',"='Finance'!D48");sheets.Audit.getRange('D23:D25').setNumberFormat('0.00');

title('ReadMe','Model scope and refresh');
const help=[['Scope','National incremental logistics economics, with a separate Greater Jakarta corridor prototype model. No website build or commercial growth benefits.'],['Original source','The original PDF was not inspected here. Historical case facts come from the supplied handoff extract.'],['Decision','No central national rollout meets positive group-profit growth in every year. A positive project NPV does not change this gate.'],['Finance controls','Finance is the single editable deterministic build. Select a policy number and adjust the amber inputs. The imported dispatch allocation does not re-optimise.'],['Simulation refresh','Rerun model.py, geography.py, prepare_deliverables.py and build_workbook.mjs after changing operating assumptions. Imported tables are snapshots.'],['Money / volume','National amounts Rp tn, volume bn parcels/year. Regional data use IDR/day and parcels/day; incident data use IDR/4h.'],['Counterfactual','Every policy shares the same demand, cost and traffic world as its current-policy comparison. No higher-volume commercial benefit is credited.'],['Annual profit bridge','5tn minus change in matched logistics cost, plus explicit other net OP drift, plus incremental policy EBIT. The residual is not assumed wholly fixed overhead.'],['Geography limitation','No downloaded detailed road/building source layer. Schematic corridor geometry and authored subsections are marked; actual access and last-mile routing remain unresolved.'],['Uncertainty','World percentiles and simulated service fractions are conditional on authored distributions. They are not empirical confidence about Nexora.'],['Project returns','Unlevered annual cash flows, no invented financing. Rules/current have no initial capital outlay; IRR is n.a.'],['Horizon','Primary5years;3/7alternatives include refresh and replacement. No perpetuity value.'],['Files','Master Context Pack preserves decisions, original brief, limitations and continuation prompt. JSON, GeoJSON, code, draws and fixtures are in the ZIP.']];
write('ReadMe','C5',help);sheets.ReadMe.getRange('D1:D25').format.columnWidth=118;sheets.ReadMe.getRange('D5:D17').format.wrapText=true;sheets.ReadMe.getRange('C5:D17').format.rowHeight=43;

// One recalc before applicable checks; verify input changes and restore before final export.
wb.recalculate();
const base=sheets.Finance.getRange('D43:D49').values;
const parity=[];
for(const years of [3,5,7]){cell('Finance','D6',years);wb.recalculate();parity.push({horizon:years,npv:sheets.Finance.getRange('D43').values[0][0],irr:sheets.Finance.getRange('D44').values[0][0]});}
cell('Finance','D6',5);cell('Finance','D5',.18);wb.recalculate();const changedRate=sheets.Finance.getRange('D43').values[0][0];cell('Finance','D5',.14);
cell('Finance','D4',ops.findIndex(x=>x.package==='large')+1);wb.recalculate();const largeNpv=sheets.Finance.getRange('D43').values[0][0];cell('Finance','D4',selected);wb.recalculate();
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:80},maxChars:5000});
const inspection=await wb.inspect({kind:'table',range:'Finance!C43:D49',include:'values,formulas',tableMaxRows:8,tableMaxCols:3,maxChars:4000});
await fs.writeFile(path.join(root,'results/workbook_artifact_checks.json'),JSON.stringify({base,parity,changedRate,largeNpv,scan:scan.ndjson,inspection:inspection.ndjson,dataTable:sheets.Finance.getRange('O18:Q20').values},null,2));
await fs.mkdir(path.join(out,'previews'),{recursive:true});
for(const n of names){const ranges={Summary:'C2:U28',Finance:'C16:K49','Policy Lab':'C2:P20',Heatmap:'C2:I17',Capacity:'C2:N20',Geography:'C2:I26',Risk:'C2:G22','Case Facts':'C2:I27',Assumptions:'C2:J13',Sources:'C2:H12','Ops Import':'C2:T18',Audit:'C2:E26',ReadMe:'C2:D17'};try{const blob=await wb.render({sheetName:n,range:ranges[n],scale:1.3,format:'png'});await fs.writeFile(path.join(out,'previews',n.replaceAll(' ','_')+'.png'),new Uint8Array(await blob.arrayBuffer()));}catch(e){await fs.appendFile(path.join(root,'results/workbook_render_errors.txt'),n+':'+String(e)+'\n');}}
const controlsPreview=await wb.render({sheetName:'Finance',range:'C2:Q20',scale:1.3,format:'png'});await fs.writeFile(path.join(out,'previews','Finance_controls.png'),new Uint8Array(await controlsPreview.arrayBuffer()));
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(out,'Nexora_Logistics_Analysis.xlsx'));
console.log(JSON.stringify({workbook:path.join(out,'Nexora_Logistics_Analysis.xlsx'),sheets:names,base,parity,changedRate,largeNpv,errorScan:scan.ndjson}));
