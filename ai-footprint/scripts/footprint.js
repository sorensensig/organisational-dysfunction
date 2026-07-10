#!/usr/bin/env node
/*
 * ai-footprint — order-of-magnitude environmental footprint estimates for
 * Claude Code sessions. Zero dependencies (Node stdlib only), zero network calls.
 *
 * Usage:
 *   footprint.js statusline                 # reads Claude Code statusline JSON on stdin
 *   footprint.js report [transcript.jsonl]  # full markdown report (auto-locates newest
 *                                           # transcript for the cwd if no path given)
 *   footprint.js json [transcript.jsonl]    # machine-readable numbers (used by evals)
 *
 * Methodology & coefficient attribution: see the release README ("Methodology").
 * Per-token energy coefficients from the claude-carbon project (MIT,
 * https://github.com/gwittebolle/claude-carbon), which fit measurements from
 * Jegham et al. 2025, "How Hungry is AI?" (arXiv:2505.09598).
 *
 * DISCLAIMER: Order-of-magnitude estimate, not a measurement. Anthropic
 * publishes no per-token energy data; coefficients are third-party benchmarks
 * fit to Claude Sonnet on assumed AWS hardware. Published per-query figures
 * span two orders of magnitude.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

/* ---------------------------------------------------------------- constants */

// kWh per million tokens, by model family (claude-carbon, fit to Jegham et al. 2025).
// Opus is a 2x extrapolation from the Sonnet fit; Haiku a 0.5x one.
const COEFF = {
  haiku:  { in: 0.07, out: 1.44 },
  sonnet: { in: 0.14, out: 2.88 },
  opus:   { in: 0.27, out: 5.76 },
};
const DEFAULT_FAMILY = 'sonnet';       // unknown model ids assume Sonnet coefficients
const CACHE_READ_FACTOR = 0.08;        // cache reads: 8% of the input coefficient
const CO2_G_PER_KWH = 287;             // AWS US, location-based grid intensity (g CO2e/kWh)
const WATER_ONSITE_L_PER_KWH = 0.18;   // AWS on-site WUE (datacenter cooling)
const WATER_OFFSITE_L_PER_KWH = [2, 3];// off-site water: electricity generation, ~2-3 L/kWh
const UNCERT = 3;                      // display band: central /3 .. central x3
const PAPER_CO2_G = 5;                 // one A4 sheet, lifecycle CO2e midpoint (~2-10 g)
const PAPER_WATER_L = 10;              // one A4 sheet, lifecycle water midpoint (~2-20 L)

const DISCLAIMER =
  'Order-of-magnitude estimate, not a measurement. Anthropic publishes no ' +
  'per-token energy data; coefficients are third-party benchmarks fit to ' +
  'Claude Sonnet on assumed AWS hardware. Published per-query figures span ' +
  'two orders of magnitude.';

/* ------------------------------------------------------------- aggregation */

function familyOf(modelId) {
  const m = String(modelId || '').toLowerCase();
  if (m.includes('haiku')) return 'haiku';
  if (m.includes('opus')) return 'opus';
  if (m.includes('sonnet')) return 'sonnet';
  return null; // unknown -> DEFAULT_FAMILY, flagged as assumed
}

// Parse a Claude Code transcript JSONL and aggregate token usage per model id.
// Transcripts write one line per content block, repeating the same message
// (same message.id) with identical usage — so we dedupe by message id.
function aggregate(transcriptPath) {
  const byModel = {}; // modelId -> { input, cacheCreate, cacheRead, output, requests }
  const seen = new Set();
  let text;
  try {
    text = fs.readFileSync(transcriptPath, 'utf8');
  } catch (e) {
    return { byModel, error: `could not read transcript: ${e.message}` };
  }
  for (const line of text.split('\n')) {
    if (!line) continue;
    let o;
    try { o = JSON.parse(line); } catch { continue; }
    if (o.type !== 'assistant' || !o.message || !o.message.usage) continue;
    const msg = o.message;
    const model = msg.model || 'unknown';
    if (model === '<synthetic>') continue; // client-generated notices, no inference
    const key = msg.id || o.uuid;
    if (key && seen.has(key)) continue;
    if (key) seen.add(key);
    const u = msg.usage;
    const row = byModel[model] || (byModel[model] = {
      input: 0, cacheCreate: 0, cacheRead: 0, output: 0, requests: 0,
    });
    row.input += u.input_tokens || 0;
    row.cacheCreate += u.cache_creation_input_tokens || 0;
    row.cacheRead += u.cache_read_input_tokens || 0;
    row.output += u.output_tokens || 0;
    row.requests += 1;
  }
  return { byModel };
}

// Central energy estimate for one model row, in kWh.
// Cache-creation tokens are processed like fresh input -> full input coefficient.
function kwhOf(modelId, row) {
  const fam = familyOf(modelId) || DEFAULT_FAMILY;
  const c = COEFF[fam];
  return (
    (row.input + row.cacheCreate) * c.in +
    row.cacheRead * c.in * CACHE_READ_FACTOR +
    row.output * c.out
  ) / 1e6;
}

function compute(byModel) {
  const models = [];
  let kwh = 0;
  for (const [modelId, row] of Object.entries(byModel)) {
    const fam = familyOf(modelId);
    const k = kwhOf(modelId, row);
    kwh += k;
    models.push({
      model: modelId,
      family: fam || DEFAULT_FAMILY,
      familyAssumed: !fam,
      ...row,
      kwh: k,
      co2_g: k * CO2_G_PER_KWH,
      water_onsite_l: k * WATER_ONSITE_L_PER_KWH,
    });
  }
  models.sort((a, b) => b.kwh - a.kwh);
  const lo = kwh / UNCERT, hi = kwh * UNCERT;
  return {
    models,
    kwh_central: kwh,
    kwh_range: [lo, hi],
    co2_g_range: [lo * CO2_G_PER_KWH, hi * CO2_G_PER_KWH],
    water_onsite_l_range: [lo * WATER_ONSITE_L_PER_KWH, hi * WATER_ONSITE_L_PER_KWH],
    water_offsite_l_range: [lo * WATER_OFFSITE_L_PER_KWH[0], hi * WATER_OFFSITE_L_PER_KWH[1]],
    paper_by_co2_range: [
      (lo * CO2_G_PER_KWH) / PAPER_CO2_G,
      (hi * CO2_G_PER_KWH) / PAPER_CO2_G,
    ],
    paper_by_water_range: [
      (lo * WATER_OFFSITE_L_PER_KWH[0]) / PAPER_WATER_L,
      (hi * WATER_OFFSITE_L_PER_KWH[1]) / PAPER_WATER_L,
    ],
  };
}

/* -------------------------------------------------------------- formatting */

function sig2(x) {
  if (x === 0) return '0';
  const s = Number(x.toPrecision(2));
  return String(s >= 1e6 || (s < 1e-4 && s > 0) ? s.toExponential(1) : s);
}

function fmtMass(g) { // grams -> mg / g / kg
  if (g >= 1000) return `${sig2(g / 1000)} kg`;
  if (g < 0.1) return `${sig2(g * 1000)} mg`;
  return `${sig2(g)} g`;
}

function fmtVol(l) { // litres -> mL / L
  if (l < 0.1) return `${sig2(l * 1000)} mL`;
  return `${sig2(l)} L`;
}

function fmtRange([lo, hi], fmt) { return `${fmt(lo)} – ${fmt(hi)}`; }

function fmtTok(n) {
  if (n >= 1e6) return `${sig2(n / 1e6)}M`;
  if (n >= 1e3) return `${Math.round(n / 1e3)}k`;
  return String(n);
}

/* ------------------------------------------------------ transcript locating */

// Claude Code stores transcripts under ~/.claude/projects/<munged-cwd>/<session>.jsonl
// where the munge replaces every non-alphanumeric character with '-'.
function projectDirFor(cwd) {
  return path.join(os.homedir(), '.claude', 'projects', cwd.replace(/[^a-zA-Z0-9]/g, '-'));
}

function newestTranscript(cwd) {
  const dir = projectDirFor(cwd);
  let entries;
  try { entries = fs.readdirSync(dir); } catch { return null; }
  let best = null, bestM = 0;
  for (const f of entries) {
    if (!f.endsWith('.jsonl')) continue;
    const p = path.join(dir, f);
    const m = fs.statSync(p).mtimeMs;
    if (m > bestM) { bestM = m; best = p; }
  }
  return best;
}

/* ------------------------------------------------------------------- modes */

function runStatusline() {
  let input = '';
  process.stdin.on('data', (d) => { input += d; });
  process.stdin.on('end', () => {
    let transcript = null;
    try { transcript = JSON.parse(input).transcript_path || null; } catch { /* ignore */ }
    if (!transcript || !fs.existsSync(transcript)) {
      process.stdout.write('CO2e ~0 (no transcript)');
      return;
    }
    const { byModel } = aggregate(transcript);
    const r = compute(byModel);
    // Compact: CO2e range + on-site (datacenter) water range. Full story: /footprint.
    process.stdout.write(
      `CO2e ~${fmtRange(r.co2_g_range, fmtMass)} | water ~${fmtRange(r.water_onsite_l_range, fmtVol)} (est)`
    );
  });
}

function resolveTranscript(arg) {
  if (arg) return { file: arg, autoLocated: false };
  const f = newestTranscript(process.cwd());
  return { file: f, autoLocated: true };
}

function runReport(arg) {
  const { file, autoLocated } = resolveTranscript(arg);
  if (!file || !fs.existsSync(file)) {
    console.log('No transcript found. Pass a path: footprint.js report <transcript.jsonl>');
    process.exitCode = 1;
    return;
  }
  const { byModel, error } = aggregate(file);
  if (error) { console.log(error); process.exitCode = 1; return; }
  const r = compute(byModel);
  const L = [];
  L.push('# Session environmental footprint (estimate)');
  L.push('');
  L.push(`Transcript: \`${file}\`${autoLocated ? ' _(newest for this project — a concurrent session may be newer than yours; pass a path to pin it)_' : ''}`);
  L.push('');
  L.push('## Totals');
  L.push('');
  L.push('| | estimated range |');
  L.push('|---|---|');
  L.push(`| Energy | ${fmtRange(r.kwh_range, (x) => `${sig2(x * 1000)} Wh`)} |`);
  L.push(`| CO2e (AWS US grid, 287 g/kWh) | ${fmtRange(r.co2_g_range, fmtMass)} |`);
  L.push(`| Water, on-site cooling (0.18 L/kWh) | ${fmtRange(r.water_onsite_l_range, fmtVol)} |`);
  L.push(`| Water, off-site generation (2–3 L/kWh) | ${fmtRange(r.water_offsite_l_range, fmtVol)} |`);
  L.push('');
  L.push('_On-site and off-site water are different things (datacenter cooling vs. power-plant water use) — they are listed separately, not summed._');
  L.push('');
  L.push('## Per model');
  L.push('');
  L.push('| model | requests | input | cache write | cache read | output | energy (central) | CO2e (central) |');
  L.push('|---|---|---|---|---|---|---|---|');
  for (const m of r.models) {
    const fam = m.familyAssumed ? `${m.family} coeffs assumed` : m.family;
    L.push(`| ${m.model} (${fam}) | ${m.requests} | ${fmtTok(m.input)} | ${fmtTok(m.cacheCreate)} | ${fmtTok(m.cacheRead)} | ${fmtTok(m.output)} | ${sig2(m.kwh * 1000)} Wh | ${fmtMass(m.co2_g)} |`);
  }
  if (!r.models.length) L.push('| _no API usage found in transcript_ | | | | | | | |');
  L.push('');
  L.push('_Central values shown per model for arithmetic transparency; treat every number as ±3x._');
  L.push('');
  L.push('## In A4 paper sheets');
  L.push('');
  L.push(`- **By CO2e:** roughly **${fmtRange(r.paper_by_co2_range, sig2)} sheets** (one sheet ≈ 5 g CO2e lifecycle, midpoint of ~2–10 g)`);
  L.push(`- **By water:** roughly **${fmtRange(r.paper_by_water_range, sig2)} sheets** (one sheet ≈ 10 L lifecycle water, midpoint of published estimates; compared against off-site generation water)`);
  L.push('');
  L.push(`> ${DISCLAIMER}`);
  L.push('');
  L.push('Coefficients: [claude-carbon](https://github.com/gwittebolle/claude-carbon) (MIT), fit to [Jegham et al. 2025](https://arxiv.org/abs/2505.09598). Full methodology: the ai-footprint README.');
  console.log(L.join('\n'));
}

function runJson(arg) {
  const { file } = resolveTranscript(arg);
  if (!file || !fs.existsSync(file)) {
    console.error('No transcript found.');
    process.exitCode = 1;
    return;
  }
  const { byModel, error } = aggregate(file);
  if (error) { console.error(error); process.exitCode = 1; return; }
  console.log(JSON.stringify({ transcript: file, ...compute(byModel) }, null, 2));
}

/* -------------------------------------------------------------------- main */

const [, , mode, arg] = process.argv;
if (mode === 'statusline') runStatusline();
else if (mode === 'report') runReport(arg);
else if (mode === 'json') runJson(arg);
else {
  console.error('usage: footprint.js statusline | report [transcript.jsonl] | json [transcript.jsonl]');
  process.exitCode = 2;
}
