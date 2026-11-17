export function selectRows(report,date){return report.rows.filter(r=>date==='all'||r.date===date);}
export function score(rows,model,level){
 if(!rows.length)throw Error('No rows');const l=Number(level)/100,key=String(level);let breaches=0,pinball=0,mean=0,streak=0,longest=0;
 for(const r of rows){const v=r[model][key],diff=-r.return_bps-v;mean+=v;pinball+=Math.max(l*diff,(l-1)*diff);if(diff>0){breaches++;streak++;longest=Math.max(longest,streak);}else streak=0;}
 return {n:rows.length,breaches,rate:breaches/rows.length,pinball:pinball/rows.length,mean:mean/rows.length,longest};
}
export function csv(rows,model,level){return 'prediction_time,target_end,return_bps,var_bps,breach\n'+rows.map(r=>[r.prediction_time,r.target_end,r.return_bps,r[model][level],-r.return_bps>r[model][level]].join(',')).join('\n')+'\n';}
