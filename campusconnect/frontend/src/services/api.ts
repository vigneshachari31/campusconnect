const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

export async function api<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('campusconnect_token')
  const headers = new Headers(options.headers)
  if (!headers.has('Content-Type') && options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)
  const res = await fetch(`${API_URL}${path}`, { ...options, headers })
  let data: any = null
  try { data = await res.json() } catch {}
  if (!res.ok) throw new Error(data?.detail || data?.message || `Request failed (${res.status})`)
  return data as T
}

export const get = <T=any>(path:string) => api<T>(path)
export const post = <T=any>(path:string, body?:any) => api<T>(path, { method:'POST', body: body === undefined ? undefined : JSON.stringify(body) })
export const put = <T=any>(path:string, body?:any) => api<T>(path, { method:'PUT', body: body === undefined ? undefined : JSON.stringify(body) })
export const del = <T=any>(path:string) => api<T>(path, { method:'DELETE' })
