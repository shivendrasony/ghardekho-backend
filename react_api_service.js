/**
 * GharDekho — Axios API Service
 * Handles all communication with the Django backend.
 *
 * Place this file at: src/services/api.js
 * Then import in any page: import api from '../services/api'
 */

import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// ── Request Interceptor: attach JWT access token ────────────────────────────
api.interceptors.request.use(
  (config) => {
    const user = JSON.parse(localStorage.getItem('ghardekho_user') || '{}')
    if (user?.token) {
      config.headers.Authorization = `Bearer ${user.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ── Response Interceptor: auto-refresh on 401 ──────────────────────────────
let isRefreshing = false
let failedQueue  = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => error ? prom.reject(error) : prom.resolve(token))
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    // If 401 and not already retrying
    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        // Queue this request until token is refreshed
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        }).catch(err => Promise.reject(err))
      }

      original._retry   = true
      isRefreshing      = true

      try {
        const user = JSON.parse(localStorage.getItem('ghardekho_user') || '{}')
        const { data } = await axios.post(`${BASE_URL}/auth/token/refresh/`, {
          refresh: user?.refresh,
        })

        // Update stored token
        const updated = { ...user, token: data.access }
        localStorage.setItem('ghardekho_user', JSON.stringify(updated))
        api.defaults.headers.common.Authorization = `Bearer ${data.access}`

        processQueue(null, data.access)
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)

      } catch (refreshError) {
        processQueue(refreshError, null)
        // Refresh failed — log out
        localStorage.removeItem('ghardekho_user')
        window.location.href = '/login'
        return Promise.reject(refreshError)

      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api


// ── Auth Services ────────────────────────────────────────────────────────────
export const authService = {
  register: (data)     => api.post('/auth/register/', data),
  login:    (data)     => api.post('/auth/login/', data),
  logout:   (refresh)  => api.post('/auth/logout/', { refresh }),
  getMe:    ()         => api.get('/auth/me/'),
  updateMe: (data)     => api.patch('/auth/me/', data),
  changePassword: (data) => api.post('/auth/change-password/', data),
  getAgents: (params)  => api.get('/auth/agents/', { params }),
  getAgent:  (id)      => api.get(`/auth/agents/${id}/`),
}


// ── Property Services ────────────────────────────────────────────────────────
export const propertyService = {
  list:       (params) => api.get('/properties/', { params }),
  featured:   ()       => api.get('/properties/featured/'),
  detail:     (id)     => api.get(`/properties/${id}/`),
  create:     (data)   => api.post('/properties/create/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update:     (id, data) => api.patch(`/properties/${id}/`, data),
  delete:     (id)     => api.delete(`/properties/${id}/`),
  save:       (id)     => api.post(`/properties/${id}/save/`),
  saved:      ()       => api.get('/properties/saved/'),
  mine:       ()       => api.get('/properties/my/'),
  alerts:     ()       => api.get('/properties/alerts/'),
  createAlert:(data)   => api.post('/properties/alerts/', data),
  deleteAlert:(id)     => api.delete(`/properties/alerts/${id}/`),
}


// ── Lead Services ─────────────────────────────────────────────────────────────
export const leadService = {
  submit:      (data)    => api.post('/leads/', data),
  mine:        ()        => api.get('/leads/mine/'),
  agentLeads:  ()        => api.get('/leads/agent/'),
  updateStatus:(id, data)=> api.patch(`/leads/${id}/`, data),
  scheduleVisit:(data)   => api.post('/leads/visits/', data),
  myVisits:    ()        => api.get('/leads/visits/mine/'),
  agentVisits: ()        => api.get('/leads/visits/agent/'),
  updateVisit: (id, status) => api.patch(`/leads/visits/${id}/status/`, { status }),
}


// ── Blog Services ─────────────────────────────────────────────────────────────
export const blogService = {
  list:       (params) => api.get('/blog/', { params }),
  featured:   ()       => api.get('/blog/featured/'),
  categories: ()       => api.get('/blog/categories/'),
  detail:     (slug)   => api.get(`/blog/${slug}/`),
}


// ── Admin Services ────────────────────────────────────────────────────────────
export const adminService = {
  stats:          ()           => api.get('/stats/'),
  allProperties:  (params)     => api.get('/properties/admin/all/', { params }),
  verifyProperty: (id, action) => api.patch(`/properties/admin/${id}/verify/`, { action }),
  allUsers:       (params)     => api.get('/auth/users/', { params }),
}
