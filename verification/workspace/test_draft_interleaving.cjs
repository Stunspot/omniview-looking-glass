const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const source=fs.readFileSync(path.resolve(__dirname,'../../plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace/app.js'),'utf8');
const choose=source.slice(source.indexOf('function choose('),source.indexOf('function orderedRecords('));
const mark=source.slice(source.indexOf('function mark('),source.indexOf('function meaningful('));
const actual=source.slice(source.indexOf('function activeViewSnapshot('),source.indexOf("$('#start-form').onsubmit"));
class Element {constructor(){this.hidden=false;this.children=[];this.innerHTML='Create image';this.textContent='';}append(x){this.children.push(x)}replaceChildren(){this.children=[]}scrollIntoView(){}}
async function run(outcome,change){
 const elements=new Map();const get=s=>{if(!elements.has(s))elements.set(s,new Element());return elements.get(s)};
 let release,calls=0,confirmations=0,allow=false,exports=[];const deferred=new Promise((resolve,reject)=>{release={resolve,reject}});
 const c=vm.createContext({structuredClone,JSON,document:{createElement:()=>new Element()},$:get,localStorage:{setItem(){}},window:{matchMedia:()=>({matches:true})},confirm:()=>{confirmations++;return allow},render(){},list(){},setMode(){},status(text){get('#status').textContent=text},download(name,data){exports.push(JSON.parse(data))},api(){calls++;return deferred}});
 vm.runInContext("let collectionGeneration=0,loadGeneration=0;let config={product:'qa'},records=[],current={_id:'owner',_revision:1,title:'Submitted original',place:'Estuary',time:'1500'},dirty=false,rendering=false,renderReady=true,mode='aperture',group='',pendingImages=[];let start={title:'Start',place:'Delta',time:'1600'};function startRecord(){return structuredClone(start)};function canLeave(){return !dirty||confirm('Discard?')};",c);
 vm.runInContext(mark+choose+actual,c);
 const fromStart=change==='start-edit';const task=vm.runInContext('createImage('+fromStart+')',c);
 if(change==='title')vm.runInContext("current.title='Newer unsaved owner edit';mark();",c);
 if(change==='destination')vm.runInContext("current={place:'Other',time:'1700',title:'Different destination'};mark();",c);
 if(change==='new-empty')vm.runInContext("current={};dirty=false;",c);
 if(fromStart)vm.runInContext("start.place='Changed start destination';",c);
 const result={_id:'owner',_revision:2,title:'Submitted original',place:'Estuary',time:'1500',render_state:'host-rendered',output_reference:'E:/QA/retained.png',render_seed:'Exact submitted seed',render_host:'Mock host'};
 if(outcome==='success')release.resolve(result);else{const e=new Error('Image retained. Do not regenerate.');e.result={...result,collection_saved:false};release.reject(e)}
 await task;assert.equal(calls,1);assert.equal(confirmations,0);
 const state=()=>vm.runInContext('({current,dirty,pendingImages,records,rendering})',c);let s=state();assert.equal(s.rendering,false);
 if(change==='title')assert.equal(s.current.title,'Newer unsaved owner edit');
 if(change==='destination')assert.equal(s.current.place,'Other');
 if(change==='new-empty')assert.equal(Object.keys(s.current).length,0);
 if(change==='start-edit')assert.equal(s.current.title,'Submitted original');
 if(change!=='none'&&outcome==='failure'){
  assert.equal(s.pendingImages.length,1);const buttons=get('#pending-image-items').children[0].children;
  buttons[2].onclick();assert.equal(exports[0].render_seed,'Exact submitted seed');assert.equal(exports[0].output_reference,'E:/QA/retained.png');
  if(s.dirty){buttons[1].onclick();assert.equal(state().pendingImages.length,1);assert.equal(confirmations,1);allow=true}
  buttons[1].onclick();s=state();assert.equal(s.pendingImages.length,0);assert.equal(s.current.render_host,'Mock host');assert.equal(s.current._id,undefined);assert.equal(s.dirty,true);
 }
 if(change==='none')assert.equal(s.current.render_state,'host-rendered');
 if(outcome==='success')assert.equal(s.records.length,1);
 assert.equal(calls,1);return {outcome,change,status:'PASS',provider_calls:0,mock_dispatches:calls};
}
(async()=>{const results=[];for(const outcome of ['success','failure'])for(const change of ['none','title','destination','start-edit','new-empty'])results.push(await run(outcome,change));console.log(JSON.stringify({status:'PASS',method:'Actual createImage/choose/mark/pendingImageList functions and pending open/export handlers; synthetic DOM/deferred API boundary, not native browser',results},null,2))})().catch(e=>{console.error(e);process.exitCode=1});
