#!/bin/sh
# ai-footprint eval: does the report math reproduce the hand-computed numbers
# from the fixture transcript? Also smoke-tests the statusline mode.
# Zero dependencies beyond node (which the scripts themselves require anyway).
set -eu

DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$DIR/../scripts/footprint.js"
FIXTURE="$DIR/fixture-transcript.jsonl"
EXPECTED="$DIR/expected.json"

node - "$SCRIPT" "$FIXTURE" "$EXPECTED" <<'EOF'
const { execFileSync } = require('child_process');
const fs = require('fs');
const [script, fixture, expectedPath] = process.argv.slice(2);

const got = JSON.parse(execFileSync(process.execPath, [script, 'json', fixture], { encoding: 'utf8' }));
const exp = JSON.parse(fs.readFileSync(expectedPath, 'utf8'));

let fails = 0;
const close = (a, b) => Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b));
const check = (name, gotV, expV) => {
  const ok = Array.isArray(expV) ? expV.every((v, i) => close(gotV[i], v)) : close(gotV, expV);
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  expected=${JSON.stringify(expV)} got=${JSON.stringify(gotV)}`);
  if (!ok) fails++;
};

check('kwh_central', got.kwh_central, exp.kwh_central);
check('kwh_range', got.kwh_range, exp.kwh_range);
check('co2_g_range', got.co2_g_range, exp.co2_g_range);
check('water_onsite_l_range', got.water_onsite_l_range, exp.water_onsite_l_range);
check('water_offsite_l_range', got.water_offsite_l_range, exp.water_offsite_l_range);
check('paper_by_co2_range', got.paper_by_co2_range, exp.paper_by_co2_range);
check('paper_by_water_range', got.paper_by_water_range, exp.paper_by_water_range);
check('model_count (dedupe + synthetic/no-usage filtering)', got.models.length, exp.model_count);
for (const [model, kwh] of Object.entries(exp.per_model_kwh)) {
  const row = got.models.find((m) => m.model === model);
  if (!row) { console.log(`FAIL  per-model ${model}: missing`); fails++; continue; }
  check(`per-model kwh ${model}`, row.kwh, kwh);
}

// Statusline smoke test: feed it a statusline-style stdin JSON pointing at the fixture.
const stdin = JSON.stringify({ session_id: 'fixture', transcript_path: fixture, model: { display_name: 'Test' } });
const line = execFileSync(process.execPath, [script, 'statusline'], { input: stdin, encoding: 'utf8' });
const slOk = /CO2e ~.+\|.*water ~/.test(line) && line.length < 120;
console.log(`${slOk ? 'PASS' : 'FAIL'}  statusline output: "${line}"`);
if (!slOk) fails++;

if (fails) { console.error(`\n${fails} check(s) failed`); process.exit(1); }
console.log('\nAll checks passed.');
EOF
