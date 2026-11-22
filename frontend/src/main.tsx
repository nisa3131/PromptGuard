import React,{useState} from 'react';
import {createRoot} from 'react-dom/client';
import {PieChart,Pie,Cell,Tooltip,ResponsiveContainer} from 'recharts';
import './styles.css';
const API='/api/v1';
function App(){
 const [key,setKey]=useState(sessionStorage.getItem('promptguard_key')||'');
 const [prompt,setPrompt]=useState('');const [result,setResult]=useState<any>(null);
 const [stats,setStats]=useState<any>(null);const [error,setError]=useState('');
 async function call(path:string,body?:object){setError('');try{
  const response=await fetch(API+path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json','X-API-Key':key},body:body?JSON.stringify(body):undefined});
  const data=await response.json();if(!response.ok)throw new Error(data.detail||'Request failed');return data;
 }catch(e){setError(String(e));return null}}
 async function analyze(){setResult(await call('/analyze',{prompt}))}
 async function analytics(){setStats(await call('/analytics'))}
 return <main><small>AI SECURITY OPERATIONS</small><h1>PromptGuard</h1><p>ML-assisted prompt injection detection and request monitoring.</p>
 <section><h2>API authentication</h2><input type="password" placeholder="API key" value={key} onChange={e=>{setKey(e.target.value);sessionStorage.setItem('promptguard_key',e.target.value)}}/><small>Configure the same key in the server environment.</small></section>
 <section><h2>Security playground</h2><textarea rows={5} placeholder="Enter a prompt to analyze..." value={prompt} onChange={e=>setPrompt(e.target.value)}/><button onClick={analyze} disabled={!prompt.trim()||!key}>Analyze prompt</button>{result&&<div className="metric"><strong>{result.status}</strong><p>Threat: {result.threat_type} · Confidence: {result.confidence_score??'Unavailable'} · Latency: {result.latency_ms} ms</p>{!result.model_available&&<small>ML model unavailable; heuristic-only fallback</small>}</div>}</section>
 <section><h2>Security analytics</h2><button onClick={analytics} disabled={!key}>Refresh dashboard</button>{stats&&<><div className="grid"><div className="metric"><small>Total requests</small><strong>{stats.total_requests}</strong></div><div className="metric"><small>Blocked</small><strong>{stats.blocked_percent}%</strong></div><div className="metric"><small>Average latency</small><strong>{stats.average_latency_ms} ms</strong></div></div><div style={{height:240}}><ResponsiveContainer><PieChart><Pie data={stats.threat_distribution} dataKey="value" nameKey="name" outerRadius={80}>{stats.threat_distribution.map((_:any,i:number)=><Cell key={i} fill={['#38bdf8','#fb7185','#a78bfa'][i%3]}/>)}</Pie><Tooltip/></PieChart></ResponsiveContainer></div><table><thead><tr><th>Time</th><th>Status</th><th>Threat</th><th>Latency</th></tr></thead><tbody>{stats.recent_logs.map((r:any)=><tr key={r.id}><td>{r.created_at}</td><td>{r.status}</td><td>{r.threat_type}</td><td>{r.latency_ms} ms</td></tr>)}</tbody></table></>}</section>{error&&<p role="alert">{error}</p>}
 </main>
}createRoot(document.getElementById('root')!).render(<App/>);
