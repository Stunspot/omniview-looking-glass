// Bounded application-logic checks with DOM stubs; this is not browser or visual evidence.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const workspace = path.join(root, 'plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace');
const source = fs.readFileSync(path.join(workspace, 'app.js'), 'utf8').replace(/\nload\(\);\s*$/, '\n');
const domain = JSON.parse(fs.readFileSync(path.join(workspace, 'domain.json'), 'utf8'));
const nodes = new Map();
function node(selector) {
  if (!nodes.has(selector)) nodes.set(selector, {
    value: '', textContent: '', innerHTML: '', hidden: false, open: false, children: [],
    querySelectorAll() { return this.children; }, setAttribute() {}, focus() {},
    showModal() { this.open = true; }, close() { this.open = false; }, addEventListener() {},
  });
  return nodes.get(selector);
}
function storage() { const data = new Map(); return {setItem(k,v) {data.set(k,String(v));}, getItem(k) {return data.get(k) ?? null;}, removeItem(k) {data.delete(k);}}; }
const ctx = {
  document: {querySelector: node, querySelectorAll: () => [], addEventListener() {}, body: {dataset: {}}},
  window: {addEventListener() {}, matchMedia() { return {matches: false, addEventListener() {}}; }}, localStorage: storage(), sessionStorage: storage(),
  structuredClone, console, confirm: () => true, domain,
};
vm.createContext(ctx);
vm.runInContext(source, ctx);
vm.runInContext('config=domain;', ctx);
function run(code) { return vm.runInContext(code, ctx); }
function plain(value) { return JSON.parse(JSON.stringify(value)); }
let passed = 0;
function check(name, test) { test(); passed++; console.log('PASS: ' + name); }

check('source notes and returned-image attributes escape supplied text', () => {
  run(`current={title:'<img src=x onerror=bad()>', evidence:'<script>bad()</script> & source', inference:'"quoted"', scenario:"<open>"}; renderGrounding();`);
  const markup = node('#evidence-content').innerHTML;
  assert.ok(markup.includes('&lt;script&gt;bad()&lt;/script&gt; &amp; source'));
  assert.ok(!markup.includes('<script>'));
  assert.ok(!markup.includes('<open>'));
  const image = run(`imageMarkup({title:'" onerror="bad()',render_state:'host-rendered',output_reference:'https://example.invalid/a.png?x="&y=1'})`);
  assert.ok(image.includes('&quot; onerror=&quot;bad()'));
  assert.ok(image.includes('?x=&quot;&amp;y=1'));
});

check('image URLs require a returned state and preserve safe HTTPS references', () => {
  for (const state of ['prompt-only', 'render-failed', 'source-unavailable', '']) {
    ctx.input = {render_state:state, output_reference:'https://example.invalid/old.png'};
    assert.equal(run('imageUrl(input)'), '');
  }
  assert.equal(run("imageUrl({render_state:'host-rendered',output_reference:'https://example.invalid/result.png'})"), 'https://example.invalid/result.png');
});

check('local preview binds a saved identity to its exact returned reference', () => {
  ctx.saved = {_id:'a'.repeat(24), _revision:1, render_state:'host-rendered', output_reference:'E:/actual/returned.png'};
  run('records=[structuredClone(saved)];');
  assert.equal(run('imageUrl(saved)'), '/api/image/'+'a'.repeat(24));
  assert.equal(run("imageUrl({...saved,output_reference:'E:/different/returned.png'})"), '');
  assert.equal(run("imageUrl({...saved,_id:'b'.repeat(24)})"), '');
  assert.equal(run('imageUrl({...saved,_id:undefined})'), '');
  run("records[0].render_state='prompt-only';");
  assert.equal(run('imageUrl(saved)'), '');
  run("records=[{render_state:'host-rendered',output_reference:'E:/actual/returned.png'}];");
  assert.equal(run('imageUrl(records[0])'), '', 'A missing saved identity must not produce /api/image/undefined');
});

check('chronology sorts explicit BCE, year and ISO dates while keeping ambiguous slots', () => {
  ctx.chronology = [
    {_id:'late',time:'2001'}, {_id:'period',time:'Late Bronze Age'}, {_id:'bce',time:'500 BCE'},
    {_id:'iso-later',time:'1900-12-31'}, {_id:'unknown',time:'around 600'}, {_id:'iso-earlier',time:'1900-01-01'},
    {_id:'year',time:'1900'}, {_id:'ad',time:'44 AD'}, {_id:'bc',time:'20 BC'},
  ];
  run('records=structuredClone(chronology);');
  assert.deepEqual(plain(run('orderedRecords().map(r=>r._id)')), ['bce','period','bc','ad','unknown','year','iso-earlier','iso-later','late']);
  assert.deepEqual(plain(run('records')), ctx.chronology, 'Ordering must not mutate the archive');
});

check('date precision distinguishes historical dates, periods and future scenarios', () => {
  assert.equal(run("precisionFor('1900')"), 'year');
  assert.equal(run("precisionFor('1900-06-15')"), 'full date');
  assert.equal(run("precisionFor('Late Bronze Age')"), 'period');
  const future = String(new Date().getFullYear() + 5);
  ctx.futureYear = future;
  assert.equal(run('precisionFor(futureYear)'), 'declared future scenario');
  assert.equal(run("precisionFor(futureYear+'-06-15')"), 'declared future scenario');
});

check('editing a date updates stale future, year and blank precision', () => {
  run("current={title:'Date edit',place:'Harbor',time:futureYear,precision:'declared future scenario'};group='Aperture';");
  const timeInput={name:'time',value:'1900'};
  node('#fields').children=[timeInput];
  run('renderEditor();');
  timeInput.oninput();
  assert.equal(run('current.precision'), 'year');
  timeInput.value='1900-06-15';timeInput.oninput();
  assert.equal(run('current.precision'), 'full date');
  timeInput.value='';timeInput.oninput();
  assert.equal(run('current.precision'), '');
  node('#fields').children=[];
});

check('continueView retains optic and route but clears time-bound truth and render receipt', () => {
  ctx.original = {
    _id:'c'.repeat(24), _revision:3, title:'Original', place:'River bend', time:'1900', precision:'year', hour:'midday',
    coordinate_meaning:'Bank anchor', support:'physical', camera:'1.65m, north', invariant:'One optic', traversal:'1900\n2000 — return',
    view:'Old scene', material_change:'Old action', habitation:'settled', evidence:'Old sources', inference:'Old inference',
    scenario:'Old uncertainty', render_seed:'Old prompt', render_host:'Old model', output_reference:'E:/old.png', render_state:'host-rendered',
  };
  run('records=[]; locked=null; dirty=false; current=structuredClone(original); continueView();');
  const next = plain(run('current'));
  for (const key of ['place','coordinate_meaning','precision','hour','support','camera','invariant','traversal']) assert.equal(next[key], ctx.original[key]);
  for (const key of ['_id','_revision','view','material_change','habitation','evidence','inference','scenario','render_seed','render_host','output_reference']) assert.ok(!next[key], key+' must not retain earlier-stop truth');
  assert.equal(next.time, '');
  assert.equal(next.render_state, 'prompt-only');
  assert.equal(next.operation, 'traverse');
  assert.equal(run('dirty'), true);
  assert.deepEqual(plain(run('locked')), ctx.original, 'The previous moment becomes a stable comparison reference');
  run("dirty=false;current=structuredClone(original);continueView('2000 — return');");
  assert.equal(run('current.time'), '2000');
  run("dirty=false;current=structuredClone(original);continueView(futureYear+' — scenario');");
  assert.equal(run('current.precision'), 'declared future scenario');
  assert.equal(run('current.time'), ctx.futureYear);
});

check('choosing and editing preserve unknown imported fields and the source record', () => {
  ctx.imported = {_id:'d'.repeat(24),_revision:2,title:'Imported',place:'Harbor',time:'1900',evidence:'Old note',custom_extension:{tags:['one'],nested:{keep:true}},_import_original:'{"exact":"original"}'};
  run('records=[structuredClone(imported)];locked=null;dirty=false;choose(records[0]);');
  node('#editor [name=title]').oninput({target:{value:'Renamed'}});
  const evidenceInput = {name:'evidence',value:'New note'};
  node('#fields').children = [evidenceInput];
  run("group='Grounding';renderEditor();");
  evidenceInput.oninput();
  assert.equal(run('current.title'), 'Renamed');
  assert.equal(run('current.evidence'), 'New note');
  assert.deepEqual(plain(run('current.custom_extension')), ctx.imported.custom_extension);
  assert.equal(run('current._import_original'), ctx.imported._import_original);
  assert.deepEqual(plain(run('records[0]')), ctx.imported);
  assert.equal(run('dirty'), true);
  node('#fields').children = [];
});

check('century controls preserve era boundaries and leave dates and periods alone',()=>{
  assert.equal(run("nudgeYear('100 BCE',100)"),'1');
  assert.equal(run("nudgeYear('1',-100)"),'100 BCE');
  assert.equal(run("nudgeYear('1900',100)"),'2000');
  assert.equal(run("nudgeYear('1900-06-01',100)"),null);
  assert.equal(run("nudgeYear('Classical era',100)"),null);
  assert.equal(run("nudgeYear('-100 BCE',100)"),null);
  assert.equal(run("precisionFor('300 BCE')"),'year');
  assert.equal(run("precisionFor('9999 CE')"),'declared future scenario');
});

console.log(`All ${passed} bounded application-logic checks passed. No browser/render claim.`);

