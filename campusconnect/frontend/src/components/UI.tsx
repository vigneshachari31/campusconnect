import { Loader2, Search, Sparkles, ArrowRight, CheckCircle2, AlertCircle, Inbox, X } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Button({children,variant='primary',className='',disabled=false,...props}:{children:React.ReactNode;variant?:'primary'|'secondary'|'ghost'|'danger';className?:string;disabled?:boolean;[key:string]:any}){
  const base='inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50'
  const variants={primary:'bg-slate-950 text-white hover:bg-slate-800 shadow-sm',secondary:'bg-white text-slate-800 border border-slate-200 hover:border-indigo-200 hover:bg-indigo-50/50',ghost:'text-slate-600 hover:bg-slate-100',danger:'bg-rose-600 text-white hover:bg-rose-700'}
  return <button disabled={disabled} className={`${base} ${variants[variant]} ${className}`} {...props}>{children}</button>
}

export function SectionTitle({eyebrow,title,description}:{eyebrow?:string;title:string;description?:string}){
 return <div className="max-w-3xl"><div className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[.18em] text-indigo-600"><Sparkles size={14}/>{eyebrow||'CampusConnect'}</div><h2 className="text-3xl font-black tracking-tight text-slate-950 sm:text-4xl">{title}</h2>{description&&<p className="mt-3 text-slate-600 leading-7">{description}</p>}</div>
}

export function Spinner(){return <Loader2 className="animate-spin" size={18}/>} 
export function EmptyState({title='Nothing here yet',description='There is no content to show right now.',action}:{title?:string;description?:string;action?:React.ReactNode}){return <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center"><Inbox className="mx-auto mb-3 text-slate-400" size={32}/><h3 className="font-bold text-slate-900">{title}</h3><p className="mt-1 text-sm text-slate-500">{description}</p>{action&&<div className="mt-5">{action}</div>}</div>}

export function Field({label,error,...props}:{label:string;error?:string;[key:string]:any}){return <label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span><input className={`w-full rounded-xl border ${error?'border-rose-300 ring-2 ring-rose-50':'border-slate-200'} bg-white px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-50`} {...props}/>{error&&<span className="mt-1 block text-xs text-rose-600">{error}</span>}</label>}

export function SelectField({label,options,...props}:{label:string;options:string[];[key:string]:any}){return <label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span><select className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-50" {...props}>{options.map(o=><option key={o}>{o}</option>)}</select></label>}

export function Toast({message,type,onClose}:{message:string;type:'success'|'error';onClose:()=>void}){return <div className="fixed bottom-5 right-5 z-[100] w-[min(92vw,380px)] rounded-2xl border border-slate-200 bg-white p-4 shadow-2xl"><div className="flex gap-3"><div className={`mt-0.5 rounded-full p-1.5 ${type==='success'?'bg-emerald-50 text-emerald-600':'bg-rose-50 text-rose-600'}`}>{type==='success'?<CheckCircle2 size={18}/>:<AlertCircle size={18}/>}</div><div className="flex-1"><p className="text-sm font-semibold text-slate-900">{message}</p></div><button onClick={onClose} className="text-slate-400 hover:text-slate-700"><X size={16}/></button></div></div>}

export function SearchBox({value,onChange,placeholder='Search...'}:{value:string;onChange:(v:string)=>void;placeholder?:string}){return <div className="relative"><Search size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"/><input value={value} onChange={e=>onChange(e.target.value)} placeholder={placeholder} className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-sm outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-50"/></div>}

export function LinkButton({to,children,variant='primary'}:{to:string;children:React.ReactNode;variant?:'primary'|'secondary'}){return <Link to={to} className={`inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold ${variant==='primary'?'bg-slate-950 text-white hover:bg-slate-800':'border border-slate-200 bg-white text-slate-800 hover:bg-slate-50'}`}>{children}<ArrowRight size={16}/></Link>}

export function Textarea({label,error,...props}:{label:string;error?:string;[key:string]:any}){return <label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span><textarea rows={5} className={`w-full resize-y rounded-xl border ${error?'border-rose-300':'border-slate-200'} bg-white px-4 py-3 text-sm outline-none focus:border-indigo-400 focus:ring-4 focus:ring-indigo-50`} {...props}/>{error&&<span className="mt-1 block text-xs text-rose-600">{error}</span>}</label>}
