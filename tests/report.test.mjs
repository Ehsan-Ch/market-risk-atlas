import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import{selectRows,score,csv}from '../core.mjs';
const report=JSON.parse(fs.readFileSync(new URL('../report.json',import.meta.url)));
test('browser scoring matches Python for every model and level',()=>{for(const s of report.summary){const r=score(report.rows,s.model,s.level);assert.equal(r.breaches,s.breaches);assert.ok(Math.abs(r.pinball-s.pinball_bps)<1e-9);assert.ok(Math.abs(r.mean-s.mean_var_bps)<1e-9);assert.equal(r.longest,s.longest_breach_run);}});
test('date filters partition all evaluated observations',()=>{let n=0;for(const d of report.daily){const rows=selectRows(report,d.date);assert.equal(rows.length,d.n);n+=rows.length;}assert.equal(n,report.evaluated);});
test('CSV preserves selected dates and thresholds',()=>{const rows=selectRows(report,'2024-01-10'),lines=csv(rows,'ewma','99').trim().split('\n');assert.equal(lines.length,rows.length+1);assert.equal(Number(lines[1].split(',')[3]),rows[0].ewma['99']);});
test('invalid empty scoring fails explicitly',()=>assert.throws(()=>score([],'ewma',99)));
