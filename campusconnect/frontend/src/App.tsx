import { Navigate, Outlet, Route, Routes, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import About from './pages/About'
import Events from './pages/Events'
import EventDetail from './pages/EventDetail'
import Clubs from './pages/Clubs'
import ClubDetail from './pages/ClubDetail'
import Opportunities from './pages/Opportunities'
import Resources from './pages/Resources'
import Support from './pages/Support'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Notifications from './pages/Notifications'
import SearchPage from './pages/SearchPage'
import { OpportunityDetail, ResourceDetail } from './pages/Detail'
import Admin from './pages/Admin'
import { Login, Register } from './pages/Auth'
import { useAuth } from './context/AuthContext'

export default function App(){return <><Navbar/><Routes><Route path="/" element={<Home/>}/><Route path="/about" element={<About/>}/><Route path="/events" element={<Events/>}/><Route path="/events/:id" element={<EventDetail/>}/><Route path="/clubs" element={<Clubs/>}/><Route path="/clubs/:id" element={<ClubDetail/>}/><Route path="/opportunities" element={<Opportunities/>}/><Route path="/opportunities/:id" element={<OpportunityDetail/>}/><Route path="/resources" element={<Resources/>}/><Route path="/resources/:id" element={<ResourceDetail/>}/><Route path="/search" element={<SearchPage/>}/><Route path="/login" element={<Login/>}/><Route path="/register" element={<Register/>}/><Route element={<ProtectedRoute/>}><Route path="/dashboard" element={<Dashboard/>}/><Route path="/support" element={<Support/>}/><Route path="/notifications" element={<Notifications/>}/><Route path="/profile" element={<Profile/>}/></Route><Route element={<AdminRoute/>}><Route path="/admin" element={<Admin/>}/></Route><Route path="*" element={<NotFound/>}/></Routes></>}
function ProtectedRoute(){const {user,loading}=useAuth();const loc=useLocation();if(loading)return <div className="grid min-h-[calc(100vh-64px)] place-items-center"><div className="h-9 w-9 animate-spin rounded-full border-4 border-slate-200 border-t-indigo-600"/></div>;return user?<Outlet/>:<Navigate to="/login" replace state={{from:loc.pathname}}/>}
function AdminRoute(){const {user,loading}=useAuth();if(loading)return <div className="grid min-h-[calc(100vh-64px)] place-items-center"><div className="h-9 w-9 animate-spin rounded-full border-4 border-slate-200 border-t-indigo-600"/></div>;return user?.role==='admin'?<Outlet/>:<Navigate to={user?'/dashboard':'/login'} replace/>}
function NotFound(){return <main className="grid min-h-[calc(100vh-64px)] place-items-center px-4"><div className="text-center"><p className="text-sm font-black text-indigo-600">404</p><h1 className="mt-2 text-4xl font-black">Page not found</h1><p className="mt-3 text-slate-500">The page you are looking for does not exist.</p></div></main>}
