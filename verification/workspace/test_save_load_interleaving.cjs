const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(path.resolve(__dirname,'../../plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace/app.js'),'utf8');
function between(a,b){const i=source.indexOf(a),j=source.indexOf(b,i);assert.ok(i>=0&&j>i);return source.slice(i,j)}
const actual=between('async function save()','function markdown()')+between('async function load()','function startRecord()');
const helpers=between('function choose(','function orderedRecords(')+between('function mark(','function meaningful(')+between('function activeViewSnapshot(','function pendingImageList(');
async function run(operation,change){
 const nodes=new Map(),get=s=>{if(!nodes.has(s))nodes.set(s,{textContent:'',inert:false,hidden:false,setAttribute(){},close(){this.closed=true}});return nodes.get(s)};let release,reject,calls=0;
 const pending=new Promise((resolve,fail)=>{release=resolve;reject=fail});
 const c=vm.createContext({JSON,structuredClone,Object,$:get,document:{querySelectorAll:()=>[]},localStorage:{setItem(){},getItem(){return null}},sessionStorage:{getItem(){return null}},cameraThemes:{chronoscope:[]},applySkin(){},render(){},list(){},openEditor(){},confirm(){throw new Error('Unexpected discard confirmation')},status(text){get('#status').textContent=text},api(){calls++;return pending}});
 vm.runInContext("let collectionGeneration=0,loadGeneration=0;let config={product:'qa',fields:[],version:'0.3.0'},records=[],current={_id:'old',_revision:1,title:'Original',place:'Delta',time:'1500'},dirty=false,group='',saving=false,locked=null,renderReady=false,renderModel='';let start={place:'',time:'',title:''};function startRecord(){return structuredClone(start)};function canLeave(){return !dirty||confirm('Discard?')}",c);vm.runInContext(helpers+actual,c);
 if(change==='welcome-edit')vm.runInContext("current={};dirty=false",c);
 const task=vm.runInContext(operation+'()',c);
 if(change==='welcome-edit')vm.runInContext("start.place='New welcome destination';start.time='1800'",c);
 if(change==='edit')vm.runInContext("current.title='Newer active work';mark()",c);
 if(change==='destination')vm.runInContext("current={title:'Other destination',place:'Bay',time:'1600'};mark()",c);
 const saved={_id:'old',_revision:2,title:'Original',place:'Delta',time:'1500'};
 if(change==='failure')reject(new Error('Injected save/state failure'));else release(operation==='save'?saved:{config:{product:'qa',fields:[],version:'0.3.0'},records:[saved],data_home:'E:/QA',render_ready:false});
 await task;const s=vm.runInContext('({current,dirty,saving,records})',c);assert.equal(calls,1);assert.equal(get('#workspace').inert,false);assert.equal(s.saving,false);
 if(change==='welcome-edit'){assert.equal(Object.keys(s.current).length,0);assert.equal(vm.runInContext('start.place',c),'New welcome destination')}
 if(change==='edit')assert.equal(s.current.title,'Newer active work');if(change==='destination')assert.equal(s.current.title,'Other destination');
 if(change==='untouched')assert.equal(s.current._revision,2);if(change==='failure'){assert.equal(s.current._revision,1);assert.match(get('#status').textContent,/Injected/)}
 if(operation==='save')assert.equal(get('#editor').inert,false);
 if(change==='edit'||change==='destination')assert.notEqual(get('#editor-dialog').closed,true);
 return {operation,change,status:'PASS',mock_requests:calls};
}
(async()=>{const results=[];for(const op of ['save','load'])for(const change of (op==='load'?['untouched','edit','destination','failure','welcome-edit']:['untouched','edit','destination','failure']))results.push(await run(op,change));console.log(JSON.stringify({status:'PASS',method:'Actual save/load/choose/mark/shared snapshot functions; synthetic DOM/deferred API, no visible-locking/browser/provider claim',results},null,2))})().catch(e=>{console.error(e);process.exitCode=1});
