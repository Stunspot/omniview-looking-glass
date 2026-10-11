'use strict';
const $ = s => document.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let pendingImages = [];
let collectionGeneration=0, loadGeneration=0;
let config, records = [], current = {}, group = 'Aperture', dirty = false, locked = null, mode = 'aperture', saving = false, rendering = false, renderReady = false, renderModel = '';
const hints = {
  Aperture: 'Locate the physical ground and carry only the precision your date earns.',
  Witness: 'One optic, one material event. Describe what occupies foreground, middle distance, and horizon.',
  Grounding: 'Keep source-backed conditions, visual inference, and unresolved choices distinct.',
  'Render handoff': 'Use the complete seed with your agent’s image tool. Register the returned image and observed host here.'
};
const cameraThemes = {
  chronoscope: ['An improbable instrument. An entire world.', 'THE CHRONOSCOPE', 'Anywhere.<br>Anywhen.', 'A little brass.<br>A rather large universe.'],
  pocket: ['Big adventures. Pocket-sized impossible.', 'POCKET UNIVERSE', 'Oh, the places.<br>Oh, the whens.', 'Point your curiosity.<br>Keep what makes you wonder.'],
  cinema: ['Tonight, the world is your picture palace.', 'MIDNIGHT CINEMA', 'Every place<br>has a thousand stories.', 'Choose a moment.<br>Give it the whole screen.']
};
function applySkin(skin) {
  if (!cameraThemes[skin]) skin='chronoscope';
  document.body.dataset.skin=skin;
  const [motto,kicker,title,tagline]=cameraThemes[skin];
  $('#theme-motto').textContent=motto;$('#lens-kicker').textContent=kicker;
  $('#lens-title').innerHTML=title;$('#lens-tagline').innerHTML=tagline;
  previewDestination();
}
function previewDestination() {
  const place=$('#start-place').value.trim(),time=$('#start-time').value.trim();
  const copy=$('#welcome .portal-copy');
  copy.classList.toggle('tuned',!!(place||time));
  if(place||time){$('#lens-kicker').textContent='DESTINATION IN SIGHT';$('#lens-title').textContent=time||'Anywhen';$('#lens-tagline').textContent=place||'Choose a place';}
  else {const t=cameraThemes[document.body.dataset.skin]||cameraThemes.chronoscope;$('#lens-kicker').textContent=t[1];$('#lens-title').innerHTML=t[2];$('#lens-tagline').innerHTML=t[3];}
}
function status(text, error = false) { $('#status').textContent = text; $('#status').className = error ? 'error' : ''; }
async function api(path, body) {
  const response = await fetch(path, body ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)} : {});
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error || 'The workspace did not respond. Try reloading.');
    error.result = result; error.httpStatus = response.status; throw error;
  }
  return result;
}
function download(name, content, type) {
  const url = URL.createObjectURL(new Blob([content], {type}));
  const a = document.createElement('a'); a.href = url; a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function basename() { return (current.title || 'OmniView').replace(/[^a-z0-9_-]+/gi, '-').slice(0,80); }
function mark() { dirty = true; $('#dirty').textContent = 'Unsaved changes'; $('#save-note').textContent = 'Draft changes stay here until saved.'; }
function meaningful(r) { return !!(r.place || r.time || r.title); }
function precisionFor(time) {
  const era=String(time).match(/^(\d{1,6})\s*(BCE?|CE|AD)$/i);
  if(era)return /^BC/i.test(era[2])?'year':Number(era[1])>new Date().getFullYear()?'declared future scenario':'year';
  if (/^-?\d{1,6}$/.test(time)) return Number(time)>new Date().getFullYear()?'declared future scenario':'year';
  if (/^\d{4}-\d{2}-\d{2}$/.test(time)) return time>new Date().toISOString().slice(0,10)?'declared future scenario':'full date';
  return 'period';
}
function canLeave() { return !dirty || confirm('Leave this draft and discard its unsaved changes?'); }
function choose(record, options = {}) {
  if (!options.force && !canLeave()) return false;
  current = structuredClone(record); dirty = !!options.draft;
  $('#active-render-feedback').textContent='';
  if (current._id && config) localStorage.setItem(config.product+'-last-view',current._id);
  $('#dirty').textContent = dirty ? 'Unsaved draft' : current._revision ? 'Saved · revision '+current._revision : 'New view';
  group = 'Aperture';
  render(); return true;
}
function orderedRecords() {
  function point(r) {
    const v = String(r.time || '').trim();
    const year = v.match(/^(-?\d{1,6})(?:\s*(BCE?|CE|AD))?$/i);
    if (year) return Number(year[1]) * (/^BC/i.test(year[2] || '') ? -1 : 1);
    if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return Number(v.slice(0,4)) + (Number(v.slice(5,7))-1)/12 + Number(v.slice(8,10))/372;
    return null;
  }
  // Only reorder dates we can interpret; leave ambiguous period slots in archive order.
  const dated = records.filter(r=>point(r)!==null).sort((a,b)=>point(a)-point(b));
  let i=0; return records.map(r=>point(r)===null?r:dated[i++]);
}
function list() {
  const query = $('#search').value.trim().toLowerCase();
  const items = orderedRecords().filter(r=>[r.title,r.place,r.time,r.view].join(' ').toLowerCase().includes(query));
  $('#count').textContent = records.length;
  $('#records').innerHTML = items.length ? items.map(r=>`<button class="record ${r._id===current._id?'active':''}" data-record="${esc(r._id)}" aria-current="${r._id===current._id?'true':'false'}"><span class="record-thumb">${imageUrl(r)?`<img src="${esc(imageUrl(r))}" alt="" loading="lazy"><span class="record-thumb-empty" hidden>◎<small>Image unavailable</small></span>`:'<span class="record-thumb-empty">◎<small>APERTURE PLANNED</small></span>'}</span><span class="record-time">${esc(r.time || 'Time unresolved')}</span><strong class="record-title">${esc(r.title)}</strong><span class="record-meta">${esc(r.place)} · ${esc(renderLabel(r))}</span></button>`).join('') : `<div class="collection-empty"><span class="empty-number" aria-hidden="true">◫</span><div><p>${query?'No matching moments. Try another place or date.':'Your adventures will collect here.'}</p><p class="micro">${query?'':'Keep a view. Revisit it. See what a century changes.'}</p></div></div>`;
  $('#records').querySelectorAll('img').forEach(img=>img.onerror=()=>{img.hidden=true;img.nextElementSibling.hidden=false;});
  bindRecords($('#records'));
}
function bindRecords(parent) { parent.querySelectorAll('[data-record]').forEach(b=>b.onclick=()=>{const id=b.dataset.record;if(choose(records.find(r=>r._id===id))){Array.from(parent.querySelectorAll('[data-record]')).find(x=>x.dataset.record===id)?.focus({preventScroll:true});}}); }
function renderLabel(r) { return {'host-rendered':'Returned image','render-failed':'Render failed','source-unavailable':'Grounding blocked','prompt-only':'Prompt only'}[r.render_state] || 'Prompt only'; }
function imageUrl(r) {
  if (r.render_state !== 'host-rendered' || !r.output_reference) return '';
  if (/^https:\/\//i.test(r.output_reference)) return r.output_reference;
  if (!/^[a-f0-9]{24}$/.test(r._id || "")) return "";
  const saved = records.find(x=>x._id===r._id);
  return saved && saved.output_reference === r.output_reference && saved.render_state === 'host-rendered' ? '/api/image/'+r._id : '';
}
function imageMarkup(r, cls='scene-image') {
  const url = imageUrl(r);
  return url ? `<div class="image-holder"><img class="${cls}" src="${esc(url)}" alt="Returned reconstruction: ${esc(r.title || r.place)}" loading="lazy"><p class="image-failure" hidden>Image unavailable. The saved reference is retained. Check the file or URL in Render handoff.</p></div>` : '';
}
function bindImages() { document.querySelectorAll('.image-holder img').forEach(img=>{img.onerror=()=>{img.hidden=true;img.nextElementSibling.hidden=false;};}); }
function fieldHtml(f) {
  const raw = current[f.key] ?? ''; const value = typeof raw === 'object' ? JSON.stringify(raw,null,2) : raw;
  const id='field-'+f.key; let control;
  if (f.options) control=`<select id="${id}" name="${f.key}"><option value="">Unresolved</option>${f.options.map(o=>`<option value="${esc(o)}" ${o===value?'selected':''}>${esc(o)}</option>`).join('')}</select>`;
  else if (f.type==='textarea') control=`<textarea id="${id}" name="${f.key}" rows="5">${esc(value)}</textarea>`;
  else control=`<input id="${id}" name="${f.key}" value="${esc(value)}" ${f.required?'aria-required="true"':''}>`;
  return `<label class="${f.type==='textarea'?'wide':''}" for="${id}">${esc(f.label)}${control}</label>`;
}
function renderEditor() {
  $('#editor [name=title]').value=current.title || '';
  $('#tabs').innerHTML=config.groups.map(g=>`<button type="button" data-group="${esc(g)}" aria-pressed="${g===group}">${esc(g)}</button>`).join('');
  $('#group-hint').textContent=hints[group] || '';
  $('#fields').innerHTML=config.fields.filter(f=>f.group===group).map(fieldHtml).join('');
  $('#tabs').querySelectorAll('button').forEach(b=>b.onclick=()=>{group=b.dataset.group;renderEditor();$('#tabs [aria-pressed=true]').focus();});
  $('#fields').querySelectorAll('input,textarea,select').forEach(input=>input.oninput=()=>{current[input.name]=input.value;if(input.name==='time'){current.precision=input.value.trim()?precisionFor(input.value.trim()):'';const precision=$("#field-precision");if(precision)precision.value=current.precision;}mark();});
}
function openEditor(next='Aperture', focusKey) {
  if (!config) return;
  group=next; renderEditor();
  if (!$('#editor-dialog').open) $('#editor-dialog').showModal();
  if (focusKey) $('#editor [name="'+focusKey+'"]').focus();
}
function closeEditor() { $('#editor-dialog').close();render(); }
function render() {
  const active=meaningful(current);
  $('#welcome').hidden=active; $('#active-view').hidden=!active;
  $('#mode').textContent=active ? 'LOOKING THROUGH TIME / '+(current._id?'SAVED MOMENT':'APERTURE FRAMED') : 'THE WORLD IS WAITING';
  $('#record-title').textContent=current.title || 'UNTITLED VIEW';
  $('#place-title').textContent=current.place || 'Place unresolved';
  $('#time-title').textContent=current.time || 'Time unresolved';
  $('#precision-label').textContent=current.precision ? current.precision+' precision' : 'precision unresolved';
  const context=[current.hour,current.support?current.support+' viewpoint':'',current.habitation].filter(Boolean);$('#context-line').innerHTML=context.map(x=>`<span class="context-chip">${esc(x)}</span>`).join('');$('#context-line').hidden=!context.length;
  $('#save-note').textContent=dirty?'Draft changes stay here until saved.':current._revision?'Saved in your local collection.':'This aperture has not been saved.';
  list(); renderScene(); renderGrounding(); renderRibbon(); setMode(mode); bindImages();
}
function renderScene() {
  const picture=imageMarkup(current);
  const next = current.render_state==='source-unavailable' ? 'Resolve the load-bearing source before composing the scene.' : current.render_state==='render-failed' ? 'The render failed. The seed is retained for a new attempt with your agent.' : current.render_state==='host-rendered' && current.output_reference ? 'Save this view to display its local image. The returned reference is retained.' : current.render_seed ? 'The seed is ready to hand to your agent. Register the returned image when it arrives.' : 'Ground this place and moment with your agent, then compose the view and render seed.';
  $('#scene').innerHTML=picture ? `<figure class="scene-frame">${picture}<figcaption class="scene-caption"><p class="eyebrow">${esc(renderLabel(current))}${current.render_host?' · '+esc(current.render_host):''} · RECONSTRUCTION</p><p class="witness-text">${esc(current.view || (String(current.scenario||'').startsWith('Quick image')?'Quick visual interpretation from place and time. Source grounding has not been supplied.':'Add a witnessed view in the notebook.'))}</p>${current.material_change?`<p class="material-event">${esc(current.material_change)}</p>`:''}</figcaption></figure>` : `<div class="unexposed"><div class="camera-stage"><div class="portal-art" aria-hidden="true"></div><div class="destination-copy"><p class="micro">APERTURE FRAMED</p><strong>${esc(current.time||'Anywhen')}</strong><span>${esc(current.place||'Anywhere')}</span><p class="micro">${esc(renderLabel(current))} · no image displayed</p></div></div><div class="next-step"><p>${esc(next)}</p><button class="text-button" id="scene-next">${current.render_seed?'Bring back the image ↗':'Shape the scene ↗'}</button></div>${current.view?`<details class="scene-notes" open><summary>The scene taking shape</summary><p class="witness-text">${esc(current.view)}</p>${current.material_change?`<p class="material-event">${esc(current.material_change)}</p>`:''}</details>`:''}</div>`;
  const nextButton=$('#scene-next'); if(nextButton)nextButton.onclick=()=>openEditor(current.render_seed?'Render handoff':'Witness');
  $('#seed').disabled=false;
  $('#seed').textContent=current.render_seed?'Copy render seed':'Copy aperture brief';
  $('#seed').title=current.render_seed?'Copy the complete render seed':'Copy this place, time, and scene brief for your agent';
  $('#lock').textContent=locked && sameIdentity(locked,current)?'Update pinned reference':'Pin as reference';
  $('#optic').innerHTML=[['THE OPTIC',current.camera||'Choose the camera relation, height, and framing.'],['SPATIAL ANCHOR',current.coordinate_meaning||'Describe the physical place that persists across views.'],['WHAT STAYS FIXED',current.invariant||'Pin a view and name the geometry to hold through time.']].map(([label,value])=>`<div class="optic-cell"><p class="eyebrow">${label}</p><p>${esc(value)}</p></div>`).join('');
}
function isSavedSnapshot(record) {
  const saved=records.find(r=>r._id && r._id===record._id);
  const ordered=value=>JSON.stringify(value,(_key,item)=>item && typeof item==='object' && !Array.isArray(item)?Object.fromEntries(Object.entries(item).sort(([a],[b])=>a<b?-1:a>b?1:0)):item);
  return !!saved && ordered(saved)===ordered(record);
}
function sameIdentity(a,b) { return a._id && a._id===b._id || !a._id && !b._id && a.title===b.title && a.time===b.time; }
function sourceMarkup(value) {
  return String(value || '').split(/(https?:\/\/[^\s<>"']+)/g).map(part=>/^https?:\/\//.test(part)?`<a href="${esc(part)}" target="_blank" rel="noopener noreferrer">${esc(part)}</a>`:esc(part)).join('');
}
function renderGrounding() {
  const items=[['evidence','01','Source-backed','What conditions can the sources actually establish?'],['inference','02','Visual inference','Which ordinary details complete the scene?'],['scenario','03','Open variables','What is unresolved, or deliberately composed?']];
  $('#evidence-content').innerHTML=items.map(([key,n,title,hint])=>`<details class="evidence-register" ${current[key]?'open':''}><summary><span class="register-number">${n}</span><strong>${title}</strong><span class="register-state">${current[key]?'Notes':'Unspecified'}</span></summary><p class="register-content">${key==="evidence"?sourceMarkup(current[key]||hint):esc(current[key]||hint)}</p><button class="text-button" data-evidence="${key}">${current[key]?'Edit notes':'Add notes'} ↗</button></details>`).join('')+`<div class="precision-note"><p class="eyebrow">TEMPORAL HONESTY</p><p>${esc(current.precision==='year'?'A year does not select a season, exact weather, or a particular day. Keep those choices explicit.':current.precision==='declared future scenario'?'A future view is a composed possibility. Name the causal scenario and carry it through the image.':'Let the supplied date and evidence set the resolution of the scene.')}</p></div>`;
  $('#evidence-content').querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>openEditor('Grounding',b.dataset.evidence));
  $('#reference-pin').hidden=!locked;
  if(locked) {
    $('#reference-pin').innerHTML=`<p class="eyebrow">PINNED REFERENCE</p><strong>${esc(locked.time || 'Time unresolved')}</strong><p>${esc(locked.title || locked.place)}</p><button id="open-compare" class="text-button">Compare with this moment ↗</button><button id="unpin" class="text-button">Unpin</button>`;
    $('#open-compare').onclick=()=>{if(!meaningful(current))return status('Open a moment to compare with the reference.',true);setMode('compare');};
    $('#unpin').onclick=()=>{locked=null;sessionStorage.removeItem(config.product+'-reference');render();$('#grounding > summary').focus();status('Reference unpinned.');};
  }
}
function renderRibbon() {
  const ordered=orderedRecords();
  $('#aperture-strip').innerHTML=ordered.length ? ordered.map(r=>`<button class="strip-stop ${r._id===current._id?'active':''}" data-record="${esc(r._id)}" aria-current="${r._id===current._id?'true':'false'}"><strong>${esc(r.time||'Unresolved')}</strong><span>${esc(r.title)}</span><small>${esc(r.place)}</small></button>`).join('') : '<p class="micro">Save a moment, then continue through time. Each stop keeps its own evidence.</p>';
  bindRecords($('#aperture-strip'));
}
function setMode(next) {
  mode=next;
  document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.mode===mode));
  $('#aperture-panel').hidden=mode!=='aperture'; $('#comparison').hidden=mode!=='compare'; $('#journey').hidden=mode!=='journey';
  if(mode==='compare')renderComparison(); if(mode==='journey')renderJourney(); bindImages();
}
function comparePane(r,label) { return `<article class="compare-pane"><header><p class="eyebrow">${label} · ${esc(renderLabel(r))}</p><h3>${esc(r.time||'Time unresolved')}</h3><p>${esc(r.title||r.place)}</p></header><div class="compare-media">${imageMarkup(r)||`<p class="compare-text">${esc(r.view||'Scene not yet composed.')}</p>`}</div>${imageUrl(r)?`<p class="compare-text">${esc(r.view)}</p>`:''}<p class="micro">${esc(r.material_change || 'Material event unspecified')}</p></article>`; }
function renderComparison() {
  if(!locked) {
    $('#comparison').innerHTML='<div class="compare-empty"><p class="eyebrow">ONE OPTIC / TWO MOMENTS</p><h3>Give time a point of reference.</h3><p>Pin this moment, then open another from your collection. Compare the images and check what the camera actually holds fixed.</p><button class="primary" id="pin-from-compare">Pin this view</button></div>';
    $('#pin-from-compare').onclick=pin; return;
  }
  const keys=[['coordinate_meaning','Spatial anchor'],['camera','Camera & framing'],['hour','Local light'],['support','Physical support'],['invariant','Declared invariant']];
  const audit=keys.map(([key,label])=>{const a=locked[key],b=current[key];const state=!a||!b?'missing':a===b?'same':'different';return `<div class="audit-row"><div class="audit-key"><strong>${label}</strong><span class="audit-state" data-state="${state}">${state==='same'?'Same recorded value':state==='different'?'Changed · review':'Unresolved'}</span></div><div class="audit-values"><p>${esc(a||'Not specified')}</p><p>${esc(b||'Not specified')}</p></div></div>`;}).join('');
  $('#comparison').innerHTML=`<div class="comparison-toolbar"><div><p class="eyebrow">TWO WINDOWS THROUGH TIME</p><p>${sameIdentity(locked,current)?'Reference pinned. Choose another saved moment to reveal the change.':'Read the change. Check the continuity.'}</p></div><label class="comparison-target">Compare to<select id="compare-target"><option value="">Choose a saved moment…</option>${orderedRecords().map(r=>`<option value="${esc(r._id)}" ${r._id===current._id?'selected':''}>${esc(r.time)} · ${esc(r.title)}</option>`).join('')}</select></label><button id="swap-comparison">Swap reference & current</button></div><div class="compare-grid">${comparePane(locked,'PINNED REFERENCE')}${comparePane(current,'CURRENT MOMENT')}</div><details class="invariant-audit"><summary>What holds between these views?</summary><p class="micro">Matching text records an intended invariant; it does not prove pixel alignment or source validity.</p>${audit}</details>`;
  $('#compare-target').onchange=e=>{const target=records.find(r=>r._id===e.target.value);if(target){if(!choose(target))renderComparison();$('#compare-target').focus();}};
  $('#swap-comparison').onclick=()=>{if(!canLeave())return;const old=structuredClone(current);const next=structuredClone(locked);locked=old;sessionStorage.setItem(config.product+'-reference',JSON.stringify(locked));choose(next,{force:true,draft:!isSavedSnapshot(next)});$('#swap-comparison').focus();status('Reference and current moment exchanged.'+(dirty?' This restored view has unsaved changes.':''));};
}
function renderJourney() {
  const stops=String(current.traversal||'').split('\n').map(s=>s.trim()).filter(Boolean);
  $('#journey').innerHTML=`<div class="journey-heading"><p class="eyebrow">A WORLD IN SEQUENCE</p><h3>One camera. A thousand lifetimes.</h3><p>Planned stops are a route, not completed images. Each moment earns its own world.</p><button id="edit-route">Edit planned stops ↗</button></div>${stops.length?`<ol class="journey-stops">${stops.map((s,i)=>`<li class="journey-stop"><span class="stop-index">${String(i+1).padStart(2,'0')}</span><div class="stop-copy"><h4>${esc(s)}</h4><p>Planned · grounding and render status belong to its saved view.</p></div><button data-stop="${i}">Frame this stop</button></li>`).join('')}</ol>`:'<div class="journey-empty"><p>No route has been named yet. Add one place-time stop per line, or continue from this moment.</p><button id="journey-next" class="primary">Continue through time →</button></div>'}<div class="journey-footnote"><p class="eyebrow">THE CONTINUITY THREAD</p><p>${esc(current.invariant||'Name the spatial anchor, framing, support, and light that should remain comparable.')}</p><p class="micro">Journey plans do not dispatch images. Create image requests one image at a time; agree the render count before a multi-image run.</p></div>`;
  $('#edit-route').onclick=()=>openEditor('Grounding','traversal');
  if($('#journey-next'))$('#journey-next').onclick=()=>continueView();
  $('#journey').querySelectorAll('[data-stop]').forEach(b=>b.onclick=()=>continueView(stops[Number(b.dataset.stop)]));
}
function pin() {
  locked=structuredClone(current); sessionStorage.setItem(config.product+'-reference',JSON.stringify(locked));render();
  if(mode==='compare')$('#compare-target').focus();
  status('Reference pinned. Open another saved moment to compare; your draft remains unchanged.');
}
function continueView(stop='') {
  if(!canLeave())return;
  const copy={};
  for(const key of ['place','coordinate_meaning','precision','hour','support','camera','invariant','traversal']) copy[key]=current[key]||'';
  copy.title=(current.place||'View')+' — '+(stop||'next moment'); copy.time=stop.split(/\s[—–]\s/)[0]; copy.operation='traverse';copy.render_state='prompt-only';if(copy.time)copy.precision=precisionFor(copy.time);
  if(!locked){locked=structuredClone(current);sessionStorage.setItem(config.product+'-reference',JSON.stringify(locked));}
  choose(copy,{force:true,draft:true}); mode='aperture';setMode(mode);openEditor('Aperture','time');
  status('Optic carried forward. Ground the new date independently; the previous scene and sources were not copied.');
}
async function save() {
  if(saving)return;
  if(!String(current.title||'').trim()) {openEditor('Aperture','title');status('Give this view a title before saving.',true);return;}
  const missing=config.fields.find(f=>f.required&&!String(current[f.key]||'').trim());
  if(missing){openEditor(missing.group,missing.key);status('Set '+missing.label.toLowerCase()+' before saving.',true);return;}
  const viewUnchanged=activeViewSnapshot();
  saving=true; $("#workspace").inert=true; $("#editor").inert=true; document.querySelectorAll('#save-view,#editor button[type=submit]').forEach(b=>b.disabled=true);status('Saving this moment…');
  try {let saved=await api('/api/record',{record:current,revision:current._revision||0});saved=rememberRecord(saved);if(viewUnchanged()){choose(saved,{force:true});$('#editor-dialog').close();status('Saved · revision '+saved._revision+'.');}else{list();status('Submitted moment saved. Your newer active work remains here; save or export it before opening that result.');}}
  catch(e){status(e.message+' Your draft is still here. Export it before reloading if needed.',true);}
  finally {saving=false;$("#workspace").inert=false;$("#editor").inert=false;document.querySelectorAll('#save-view,#editor button[type=submit]').forEach(b=>b.disabled=false);}
}
function markdown() { return '# '+(current.title||'OmniView')+'\n\n'+config.fields.map(f=>'## '+f.label+'\n\n'+(typeof current[f.key]==='object'?JSON.stringify(current[f.key],null,2):current[f.key]||'Unspecified')).join('\n\n')+'\n\n---\nRecord '+(current._id||'unsaved')+'; revision '+(current._revision||0)+'.\n'; }
async function load() {
  const viewUnchanged=activeViewSnapshot();
  const readId=++loadGeneration, submittedCollection=collectionGeneration;
  $("#workspace").inert=true;
  $('#workspace').setAttribute('aria-busy','true');$('#load-error').hidden=true;
  try {
    const state=await api('/api/state');if(readId!==loadGeneration)return;config=state.config;const newerWrites=collectionGeneration!==submittedCollection;if(!newerWrites){records=state.records;collectionGeneration++;}renderReady=!!state.render_ready;renderModel=state.render_model||'';$('#version').textContent='v'+config.version;$('#home').textContent=state.data_home;$('#render-availability').textContent=renderReady?'Sends place and time to OpenAI · API charges apply. No source research.':'Rendering needs OPENAI_API_KEY in the local host environment. Set it, restart OmniView, then press Create image. You can still plan with your agent.';
    const stored=localStorage.getItem(config.product+'-skin'); const skin=Object.hasOwn(cameraThemes,stored)?stored:'chronoscope';$('#skin').value=skin;applySkin(skin);
    if(!locked){try{locked=JSON.parse(sessionStorage.getItem(config.product+'-reference')||'null');}catch{locked=null;}}
    const id=current._id || localStorage.getItem(config.product+'-last-view');
    const latest=[...records].sort((a,b)=>String(b._updated||'').localeCompare(String(a._updated||'')))[0];
    if(viewUnchanged())choose(records.find(r=>r._id===id)||latest||{},{force:true});else{render();list();}
    $('#workspace').setAttribute('aria-busy','false');$("#workspace").inert=false;status('Ready · '+records.length+' collected moment'+(records.length===1?'':'s')+'.'+(newerWrites?' A later saved result was retained; reload again to fetch other external changes.':''));
  } catch(e){if(readId!==loadGeneration)return;$('#load-error').hidden=false;$('#load-error-text').textContent=e.message;$('#workspace').setAttribute('aria-busy','false');status(e.message,true);}
  finally {if(readId===loadGeneration)$("#workspace").inert=false;}
}
function startRecord() {const form=new FormData($('#start-form'));const place=String(form.get('place')||'').trim(),time=String(form.get('time')||'').trim();return {title:place+' · '+time,place,time,hour:String(form.get('hour')||'').trim(),precision:precisionFor(time),render_state:'prompt-only',operation:'render'};}
function planOnly() {if(!config||!$('#start-form').reportValidity())return;const record=startRecord();record.operation='prompt';choose(record,{draft:true});mode='aperture';setMode(mode);status('Destination framed. Copy the aperture brief for your agent, or shape the scene in the camera notebook.');}
function activeViewSnapshot(fromStart=false, submittedStart=null) {
  const view=JSON.stringify(current), wasDirty=dirty;
  const trackDestination=fromStart || !(current.place || current.time || current.title);
  const destination=trackDestination?JSON.stringify(submittedStart || startRecord()):null;
  return ()=>JSON.stringify(current)===view && dirty===wasDirty && (!trackDestination || JSON.stringify(startRecord())===destination);
}
function rememberRecord(record) {
  const index=records.findIndex(r=>r._id===record._id);
  if(index>=0 && Number(records[index]._revision)>Number(record._revision))return records[index];
  if(index<0)records.push(record);else records[index]=record;
  collectionGeneration++;
  return record;
}
function pendingImageList() {
  const panel=$('#pending-images'); panel.hidden=pendingImages.length===0;
  const items=$('#pending-image-items'); items.replaceChildren();
  pendingImages.forEach((draft,index)=>{
    const row=document.createElement('div');
    const label=document.createElement('p');label.textContent=draft.title+' — '+draft.output_reference;row.append(label);
    const open=document.createElement('button');open.textContent='Open retained image draft';
    open.onclick=()=>{if(choose(draft,{draft:true})){pendingImages.splice(index,1);pendingImageList();mode='aperture';setMode(mode);status('Retained image draft opened. Save or export it; no new generation is needed.');}};row.append(open);
    const exportButton=document.createElement('button');exportButton.textContent='Export retained image draft';
    exportButton.onclick=()=>{download('OmniView-recovered-image.json',JSON.stringify(draft,null,2),'application/json');status('Retained image draft exported, including its path, seed and observed host.');};row.append(exportButton);items.append(row);
  });
}
async function createImage(fromStart=false) {
  if(rendering||!config)return;
  const record=fromStart?startRecord():structuredClone(current);
  const viewUnchanged=activeViewSnapshot(fromStart,record);
  if(!record.place||!record.time){status('Enter a place and time to create an image.',true);return;}
  const feedback=$(fromStart?'#render-feedback':'#active-render-feedback');
  if(!renderReady){feedback.textContent='Rendering needs OPENAI_API_KEY in the local host environment. Set it and restart OmniView, or plan with your agent.';status(feedback.textContent,true);return;}
  rendering=true;const button=$(fromStart?'#start-form .shutter':'#render-image');const original=button.innerHTML;button.disabled=true;button.innerHTML='Creating image…';feedback.textContent='Creating one image. This may take a minute; the result will be saved in your collection.';status('Creating one image for '+record.place+' · '+record.time+'…');
  try {
    let saved=await api('/api/render',{record,revision:record._revision||0});
    saved=rememberRecord(saved);
    if(!viewUnchanged()){
      list();status('Image created and saved in your time reel. Your newer draft or destination remains active; export or save it before opening the returned moment.');
      return;
    }
    choose(saved,{force:true});mode='aperture';setMode(mode);
    $('#active-render-feedback').textContent='Image created and saved. This is a reconstruction; inspect source grounding before relying on historical details.';
    status('Image ready and saved · '+saved.place+' · '+saved.time+'.');
    $('#active-view').scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
  } catch(error){
    const result=error.result;
    if(result && result.collection_saved===false && result.render_state==='host-rendered' && result.output_reference){
      const draft=structuredClone(record);
      draft.render_recovery={source_record_id:record._id||null,submitted_revision:record._revision||0,reason:'collection-save-failed'};
      delete draft._id; delete draft._revision; delete draft._updated;
      draft.title=(record.title||record.place||'View')+' (recovered image)';
      draft.operation='render'; draft.render_state=result.render_state;
      draft.output_reference=result.output_reference; draft.render_seed=result.render_seed; draft.render_host=result.render_host;
      if(!draft.evidence && !draft.scenario)draft.scenario='Quick image from place and time; no source research was performed by this workspace.';
      if(!viewUnchanged()){
        pendingImages.push(draft);pendingImageList();
        status('Image retained separately; your newer draft remains active. Export the retained image draft below, or open it after saving or exporting your current work. No new generation is needed. '+error.message,true);
        return;
      }
      choose(draft,{force:true,draft:true});mode='aperture';setMode(mode);
      const message='Image retained; collection saving failed. Its path, seed and observed host are kept in this unsaved draft. Save or export this moment after storage recovers; no new generation is needed. '+error.message;
      $('#active-render-feedback').textContent=message;status(message,true);
    } else {
      feedback.textContent=error.message+' Your place and time are still here.';status(feedback.textContent,true);
    }
  }
  finally {rendering=false;button.disabled=false;button.innerHTML=original;}
}
$('#start-form').onsubmit=e=>{e.preventDefault();createImage(true);};
$('#plan-only').onclick=planOnly;
$('#render-image').onclick=()=>createImage();
$('#new').onclick=()=>{if(choose({})){mode='aperture';$('#start-form').reset();previewDestination();$('#start-place').focus();}};
$('#example').onclick=()=>{if(config&&choose(config.example,{draft:true})){mode='aperture';setMode(mode);status('Labeled example loaded as an unsaved draft; its historical conditions remain unresearched.');}};
$('#editor').onsubmit=e=>{e.preventDefault();save();};
$('#editor [name=title]').oninput=e=>{current.title=e.target.value;mark();};
$('#close-editor').onclick=closeEditor;$('#keep-draft').onclick=closeEditor;
$('#editor-dialog').addEventListener('cancel',()=>render());
$('#edit-view').onclick=()=>openEditor();$('#save-view').onclick=save;
$('#lock').onclick=pin;$('#duplicate').onclick=()=>continueView();
$('#seed').onclick=async()=>{const text=current.render_seed||markdown();try{await navigator.clipboard.writeText(text);status(current.render_seed?'Render seed copied. Your agent can bring this view to life.':'Aperture brief copied. Give it to your agent to ground and render this view.');}catch{download(basename()+(current.render_seed?'-render-seed.txt':'-aperture-brief.md'),text,'text/plain');status('Clipboard unavailable; aperture brief downloaded.');}};
$('#skin').onchange=e=>{applySkin(e.target.value);if(config)localStorage.setItem(config.product+'-skin',e.target.value);};
$('#search').oninput=list;$('#refresh').onclick=()=>{if(canLeave())load();};$('#retry').onclick=load;
$('#export').onclick=()=>{download(basename()+'.json',JSON.stringify(current,null,2),'application/json');status('View exported, including unsaved changes and original imported fields.');};
$('#handoff').onclick=()=>{download(basename()+'.md',markdown(),'text/markdown');status('Agent handoff downloaded with scene, evidence, uncertainty, and seed.');};
$('#export-all').onclick=()=>download('omniview-records.json',JSON.stringify({product:config.product,records},null,2),'application/json');
$('#import').onchange=async e=>{
  const file=e.target.files[0];if(!file)return;
  const viewUnchanged=activeViewSnapshot();
  let completed=0;
  try {
    if(!canLeave())return;if(file.size>2_000_000)throw new Error('Import is larger than 2 MB.');
    const parsed=JSON.parse(await file.text());const incoming=parsed.records||[parsed];
    if(!Array.isArray(incoming)||incoming.length>500)throw new Error('Import a record or a bundle of up to 500 records.');
    if(!confirm('Import '+incoming.length+' moments as new copies? Original JSON will be retained.'))return;
    let last;
    for(const original of incoming){const copy=structuredClone(original);delete copy._id;delete copy._revision;copy._import_original=JSON.stringify(original);last=await api('/api/record',{record:copy,revision:0});last=rememberRecord(last);completed++;}
    const unchanged=viewUnchanged();if(last && unchanged)choose(last,{force:true});else list();status('Imported '+completed+' moments. Original JSON retained.'+(!unchanged?' Your newer active work remains here; save or export it before opening an imported moment.':''));
  }catch(error){list();status(error.message+(completed?' '+completed+' moments were already imported; do not repeat those entries.':''),true);}
  finally{e.target.value='';}
};
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
window.addEventListener('beforeunload',e=>{if(dirty || pendingImages.length){e.preventDefault();e.returnValue='';}});
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'&&config&&meaningful(current)){e.preventDefault();save();}});

const destinations=[['Alexandria harbor','300 BCE'],['Venice, the Grand Canal','1500'],['Kyoto, Kamo River','1700'],['Manhattan, Lower Broadway','1900'],['Istanbul, the Golden Horn','1600'],['The Thames at Westminster','2100']];
let lastDestination=-1;
$('#surprise').onclick=()=>{let i;do{i=Math.floor(Math.random()*destinations.length);}while(i===lastDestination);lastDestination=i;$('#start-place').value=destinations[i][0];$('#start-time').value=destinations[i][1];previewDestination();$('#destination-note').textContent='A starting idea, ready for your agent to ground. Change anything you like.';status('Destination dealt: '+destinations[i].join(' · ')+'. No image has been generated.');};
function nudgeYear(value,delta) {
  const match=String(value).trim().match(/^(-?\d{1,6})(?:\s*(BCE?|CE|AD))?$/i);
  if(!match)return null;
  const era=/^BC/i.test(match[2]||'');const before=Number(match[1])*(era?-1:1);
  if(before===0||(era&&Number(match[1])<1))return null;
  let after=before+delta;if(before<0&&after>=0)after++;if(before>0&&after<=0)after--;
  if(Math.abs(after)>999999)return null;
  return after<0?Math.abs(after)+' BCE':String(after);
}
document.querySelectorAll('[data-year-nudge]').forEach(button=>button.onclick=()=>{const input=$('#start-time');const result=nudgeYear(input.value||String(new Date().getFullYear()),Number(button.dataset.yearNudge));if(result===null){status('The century dial works with a year. Type a full date or era directly.',true);input.focus();return;}input.value=result;previewDestination();status('Time dial set to '+result+'.');});

$('#start-place').oninput=previewDestination;$('#start-time').oninput=previewDestination;
load();










