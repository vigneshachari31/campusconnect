import { useState } from 'react'
import { Bell, Menu, Search, X, LogOut, LayoutDashboard, Shield, ChevronDown } from 'lucide-react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links=[['/events','Events'],['/clubs','Clubs'],['/opportunities','Opportunities'],['/resources','Resources'],['/support','Support']]
export default function Navbar(){
 const {user,logout}=useAuth(); const [open,setOpen]=useState(false); const [profile,setProfile]=useState(false); const navigate=useNavigate();
 const navClass=({isActive}:{isActive:boolean})=>`text-sm font-semibold ${isActive?'text-indigo-600':'text-slate-600 hover:text-slate-950'}`
 return <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/85 backdrop-blur-xl"><div className="mx-auto flex h-16 max-w-7xl items-center gap-6 px-4 sm:px-6 lg:px-8">
  <Link to="/" className="flex items-center gap-2 font-black tracking-tight"><span className="grid h-9 w-9 place-items-center rounded-xl bg-slate-950 text-white shadow-lg shadow-indigo-200">CC</span><span className="hidden sm:block">Campus<span className="text-indigo-600">Connect</span></span></Link>
  <nav className="hidden flex-1 items-center justify-center gap-6 lg:flex">{links.map(([to,label])=><NavLink key={to} to={to} className={navClass}>{label}</NavLink>)}<NavLink to="/search" className={navClass}><Search size={17}/></NavLink></nav>
  <div className="ml-auto flex items-center gap-2">
    {user?<>
      <Link to="/notifications" className="relative hidden rounded-xl p-2 text-slate-500 hover:bg-slate-100 sm:block"><Bell size={19}/><UnreadDot/></Link>
      <div className="relative"><button onClick={()=>setProfile(v=>!v)} className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-2 py-1.5 hover:bg-slate-50"><span className="grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-indigo-500 to-sky-500 text-xs font-black text-white">{user.full_name.split(' ').map(x=>x[0]).slice(0,2).join('')}</span><span className="hidden max-w-28 truncate text-sm font-semibold sm:block">{user.full_name.split(' ')[0]}</span><ChevronDown size={15} className="hidden text-slate-400 sm:block"/></button>{profile&&<div className="absolute right-0 mt-2 w-56 overflow-hidden rounded-2xl border border-slate-200 bg-white p-1 shadow-2xl"><Link onClick={()=>setProfile(false)} to="/dashboard" className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm hover:bg-slate-50"><LayoutDashboard size={16}/> Dashboard</Link>{user.role==='admin'&&<Link onClick={()=>setProfile(false)} to="/admin" className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm hover:bg-slate-50"><Shield size={16}/> Admin Console</Link>}<Link onClick={()=>setProfile(false)} to="/profile" className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm hover:bg-slate-50">Profile</Link><button onClick={()=>{logout();navigate('/')}} className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-rose-600 hover:bg-rose-50"><LogOut size={16}/> Logout</button></div>}</div>
    </>:<><Link to="/login" className="hidden rounded-xl px-3.5 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100 sm:block">Login</Link><Link to="/register" className="rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800">Create Account</Link></>}
    <button onClick={()=>setOpen(v=>!v)} className="rounded-xl p-2 text-slate-600 hover:bg-slate-100 lg:hidden">{open?<X size={20}/>:<Menu size={20}/>}</button>
  </div></div>
  {open&&<div className="border-t border-slate-200 bg-white px-4 py-4 lg:hidden"><nav className="grid gap-1">{links.map(([to,label])=><NavLink key={to} onClick={()=>setOpen(false)} to={to} className={({isActive})=>`rounded-xl px-3 py-2.5 text-sm font-semibold ${isActive?'bg-indigo-50 text-indigo-700':'text-slate-700 hover:bg-slate-50'}`}>{label}</NavLink>)}<NavLink onClick={()=>setOpen(false)} to="/search" className="rounded-xl px-3 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">Search</NavLink>{user&&<NavLink onClick={()=>setOpen(false)} to="/notifications" className="rounded-xl px-3 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">Notifications</NavLink>}</nav></div>}
 </header>
}
function UnreadDot(){return <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-indigo-600 ring-2 ring-white"/>}
