import React,{useState} from 'react';
import {createRoot} from 'react-dom/client';
import {PieChart,Pie,Cell,Tooltip,ResponsiveContainer} from 'recharts';
import './styles.css';
const API='/api/v1';
function App(){
 const [key,setKey]=useState(sessionStorage.getItem('promptguard_key')||'');
 const [prompt,setPrompt]=useState('');const [result,setResult]=useState<any>(null);
 const [stats,setStats]=useState<any>(null);const [error,setError]=useState('');
 const [busy,setBusy]=useState(false);const [keys,setKeys]=useState<any[]>([]);const [label,setLabel]=useState('');const [newKey,setNewKey]=useState('');
 async function call(path:string,body?:object,method?:string){setError('');try{
  const response=await fetch(API+path,{method:method||(body?'POST':'GET'),headers:{'Content-Type':'application/json','X-API-Key':key.trim()},body:body?JSON.stringify(body):undefined});
  const data=await response.json();if(!response.ok)throw new Error(response.status===401?'Invalid API key or administrator access required. Check your key.':String(data.detail||'Request failed'));return data;
 }catch(e){setError(String(e));return null}}
 async function analyze(){setBusy(true);setResult(null);try{setResult(await call('/analyze',{prompt}))}finally{setBusy(false)}}
 async function loadKeys(){const data=await call('/api-keys');if(data)setKeys(data)}
 async function createKey(){setNewKey('');const data=await call('/api-keys',{label:label.trim()});if(data){setNewKey(data.api_key);setLabel('');await loadKeys()}}
 async function revokeKey(id:number){if(!window.confirm('Revoke this API key?'))return;const data=await call('/api-keys/'+id,undefined,'DELETE');if(data)await loadKeys()}
 async function analytics(){setStats(await call('/analytics'))}
 return <main><small>AI SECURITY OPERATIONS</small><h1>PromptGuard</h1><p>ML-assisted prompt injection detection and request monitoring.</p>
 {error&&<p className="error" role="alert">{error}</p>}<section><h2>API authentication</h2><input type="password" placeholder="API key" value={key} onChange={e=>{setKey(e.target.value);sessionStorage.setItem('promptguard_key',e.target.value)}}/><small>Configure the same key in the server environment.</small></section>
 <section><h2>Security playground</h2><textarea rows={5} placeholder="Enter a prompt to analyze..." value={prompt} onChange={e=>setPrompt(e.target.value)}/><button onClick={analyze} disabled={busy||!prompt.trim()||!key.trim()}>{busy?'Analyzing…':'Analyze prompt'}</button>{result&&<div className="metric"><strong className={result.status==='SAFE'?'safe':'blocked'}>{result.status}</strong><p>Threat: {result.threat_type} · Confidence: {result.confidence_score??'Unavailable'} · Latency: {result.latency_ms} ms</p>{!result.model_available&&<small>ML model unavailable; requests are blocked by default</small>}</div>}</section>
 <section><h2>API key management</h2><p>Administrator key required. Created keys are displayed once and can only analyze prompts.</p><input aria-label="Key label" placeholder="Integration name" value={label} onChange={e=>setLabel(e.target.value)}/><button disabled={!key.trim()||!label.trim()} onClick={createKey}>Create API key</button><button disabled={!key.trim()} onClick={loadKeys}>List keys</button>{newKey&&<div className="metric"><small>Copy this key now; it will not be displayed again.</small><input readOnly aria-label="New API key" value={newKey}/><button onClick={()=>setNewKey('')}>Hide key</button></div>}{keys.map(k=><div className="keyrow" key={k.id}><span>{k.label} · {k.revoked?'Revoked':'Active'}</span><button disabled={k.revoked} onClick={()=>revokeKey(k.id)}>Revoke</button></div>)}</section>
 <section><h2>Security analytics</h2><button onClick={analytics} disabled={!key}>Refresh dashboard</button>{stats&&<><div className="grid"><div className="metric"><small>Total requests</small><strong>{stats.total_requests}</strong></div><div className="metric"><small>Blocked</small><strong>{stats.blocked_percent}%</strong></div><div className="metric"><small>Average latency</small><strong>{stats.average_latency_ms} ms</strong></div></div><div style={{height:240}}><ResponsiveContainer><PieChart><Pie data={stats.threat_distribution} dataKey="value" nameKey="name" outerRadius={80}>{stats.threat_distribution.map((_:any,i:number)=><Cell key={i} fill={['#38bdf8','#fb7185','#a78bfa'][i%3]}/>)}</Pie><Tooltip/></PieChart></ResponsiveContainer></div><table><thead><tr><th>Time</th><th>Status</th><th>Threat</th><th>Latency</th></tr></thead><tbody>{stats.recent_logs.map((r:any)=><tr key={r.id}><td>{r.created_at}</td><td>{r.status}</td><td>{r.threat_type}</td><td>{r.latency_ms} ms</td></tr>)}</tbody></table></>}</section>
 </main>
}createRoot(document.getElementById('root')!).render(<App/>);
