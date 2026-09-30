import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { get, post, put } from '../services/api'

type User = { id:number; full_name:string; email:string; college:string; course:string; year:string; role:'student'|'admin'; avatar_url?:string|null }

type AuthContextType = {
  user: User | null; loading: boolean; login:(email:string,password:string)=>Promise<User>; register:(data:any)=>Promise<User>; logout:()=>void; refreshUser:()=>Promise<void>
}
const AuthContext=createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({children}:{children:React.ReactNode}){
  const [user,setUser]=useState<User|null>(null); const [loading,setLoading]=useState(true)
  useEffect(()=>{ (async()=>{ if(!localStorage.getItem('campusconnect_token')){setLoading(false);return} try{setUser(await get('/auth/me'))}catch{localStorage.removeItem('campusconnect_token');setUser(null)}finally{setLoading(false)} })() },[])
  const login=async(email:string,password:string)=>{ const res=await post<any>('/auth/login',{email,password}); localStorage.setItem('campusconnect_token',res.access_token); setUser(res.user); return res.user }
  const register=async(data:any)=>{ const res=await post<any>('/auth/register',data); localStorage.setItem('campusconnect_token',res.access_token); setUser(res.user); return res.user }
  const logout=()=>{localStorage.removeItem('campusconnect_token');setUser(null)}
  const refreshUser=async()=>{setUser(await get('/auth/me'))}
  const value=useMemo(()=>({user,loading,login,register,logout,refreshUser}),[user,loading])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
export const useAuth=()=>{const c=useContext(AuthContext);if(!c)throw new Error('useAuth must be used inside AuthProvider');return c}
