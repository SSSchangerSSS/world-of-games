const manifest = JSON.parse((await import('fs')).readFileSync('tests-manifest.json','utf8'));
function mulberry32(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
const T={ok(c,m){if(!c)throw new Error(m||'ok failed')},eq(a,b,m){const x=JSON.stringify(a),y=JSON.stringify(b);if(x!==y)throw new Error((m||'eq')+' '+x+' !== '+y)},approx(a,b,e,m){if(Math.abs(a-b)>(e||1e-9))throw new Error((m||'approx')+' '+a+' '+b)},throws(f,m){let t=0;try{f()}catch(e){t=1}if(!t)throw new Error(m||'expected throw')},near(a,b,d,m){if(Math.abs(a-b)>d)throw new Error((m||'near')+' '+a+' '+b)}};
let P=0,F=0;const fails=[];
for(const g of manifest){let L=null;try{L=new Function('store',g.logic+'\n;return typeof WOG_LOGIC==="undefined"?null:WOG_LOGIC;')({});if(!L)throw new Error('no WOG_LOGIC')}catch(e){F+=g.tests.length;fails.push(g.slug+' LOAD:: '+e.message);continue}
for(const t of g.tests){try{new Function('T','L','rng',t.js)(T,L,mulberry32(g.seed||12345));P++}catch(e){F++;fails.push(g.slug+' :: '+t.name+' :: '+e.message)}}}
console.log('LOGIC pass='+P+' fail='+F+(F?'\n'+fails.join('\n'):''));process.exit(F?1:0);
