const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(path.resolve(__dirname,'../../plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace/app.js'),'utf8');
function between(a,b){const i=source.indexOf(a);assert.ok(i>=0);const j=source.indexOf(b,i);assert.ok(j>i);return source.slice(i,j)}
const body=between("$('#import').onchange=","document.querySelectorAll('[data-mode]')");
const helpers=between('function choose(','function orderedRecords(')+between('function mark(','function meaningful(')+between('function activeViewSnapshot(','function pendingImageList(');
async function run(kind){
 const elements=new Map(),get=s=>{if(!elements.has(s))elements.set(s,{textContent:'',value:'selected'});return elements.get(s)};
 let release,signal,calls=0,seen=[];const deferred=new Promise(resolve=>release=resolve),dispatched=new Promise(resolve=>signal=resolve);
 const c=vm.createContext({JSON,structuredClone,$:get,confirm:()=>kind!=='cancel',render(){},list(){},localStorage:{setItem(){}},status(text){get('#status').textContent=text},async api(route,body){calls++;seen.push(body);if(calls===1){signal();await deferred}else if(kind==='partial')throw new Error('Injected storage failure');return {...body.record,_id:'import-'+calls,_revision:1}}});
 vm.runInContext("let collectionGeneration=0,loadGeneration=0;let config={product:'qa'},current={title:'Original',place:'Original place',time:'1500'},dirty=false,records=[],group='';let start={place:'',time:'',title:''};function startRecord(){return structuredClone(start)};function canLeave(){return !dirty||confirm('Discard?')}",c);vm.runInContext(helpers+body,c);
 const incoming={records:[{_id:'old',title:'Imported',place:'Delta',time:'1600'}]};if(kind==='partial')incoming.records.push({title:'Second',place:'Bay',time:'1700'});
 if(kind==='welcome-edit')vm.runInContext("current={};dirty=false",c);
 const event={target:{value:'selected',files:[{size:100,text:async()=>JSON.stringify(incoming)}]}};
 const task=get('#import').onchange(event);
 if(kind!=='cancel'){await dispatched;if(kind==='welcome-edit')vm.runInContext("start.place='New welcome destination';start.time='1800'",c);if(kind==='edit')vm.runInContext("current.title='Newer edit';mark()",c);if(kind==='destination')vm.runInContext("current={title:'Other destination',place:'Other',time:'1800'};mark()",c);release()}
 await task;const s=vm.runInContext('({current,dirty,records})',c);assert.equal(event.target.value,'');
 if(kind==='welcome-edit'){assert.equal(Object.keys(s.current).length,0);assert.equal(vm.runInContext('start.place',c),'New welcome destination')}
 if(kind==='edit')assert.equal(s.current.title,'Newer edit');if(kind==='destination')assert.equal(s.current.title,'Other destination');
 if(kind==='untouched')assert.equal(s.current.title,'Imported');
 if(kind==='cancel'){assert.equal(calls,0);assert.equal(s.records.length,0);assert.equal(s.current.title,'Original')}
 else{assert.equal(s.records.length,1);assert.equal(s.records[0]._import_original,JSON.stringify(incoming.records[0]));assert.equal(seen[0].record._id,undefined)}
 if(kind==='partial'){assert.equal(calls,2);assert.match(get('#status').textContent,/1 moments were already imported; do not repeat/);assert.equal(s.current.title,'Original')}
 return {kind,status:'PASS',mock_record_calls:calls};
}
(async()=>{const results=[];for(const kind of ['untouched','edit','destination','cancel','partial','welcome-edit'])results.push(await run(kind));console.log(JSON.stringify({status:'PASS',method:'Actual wired Import JSON handler and choose/mark/shared snapshot; deferred mock record API and synthetic DOM; no browser/provider claim',results},null,2))})().catch(e=>{console.error(e);process.exitCode=1});
