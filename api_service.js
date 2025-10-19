// API Service for React Frontend to connect to Django Backend
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Authentication API
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  logout: () => api.post('/auth/logout/'),
  getUser: () => api.get('/auth/user/'),
  updateUser: (data) => api.put('/auth/user/', data),
};

// Applications API
export const applicationAPI = {
  getApplications: () => api.get('/applications/'),
  createApplication: (data) => api.post('/applications/', data),
  getApplication: (id) => api.get(`/applications/${id}/`),
  updateApplication: (id, data) => api.put(`/applications/${id}/`, data),
  deleteApplication: (id) => api.delete(`/applications/${id}/`),
  approveApplication: (id, notes) => api.post(`/applications/${id}/approve/`, {notes}),
  rejectApplication: (id, notes) => api.post(`/applications/${id}/reject/`, {notes}),
};

// Payments API
export const paymentsAPI = {
  getPayments: () => api.get('/payments/'),
  createPayment: (data) => api.post('/payments/', data),
  getPayment: (id) => api.get(`/payments/${id}/`),
  updatePayment: (id, data) => api.put(`/payments/${id}/`, data),
};

// Shares API
export const sharesAPI = {
  getShares: () => api.get('/shares/'),
  buyShares: (data) => api.post('/shares/', data),
  getShare: (id) => api.get(`/shares/${id}/`),
};

// Claims API
export const claimsAPI = {
  getClaims: () => api.get('/claims/'),
  createClaim: (data) => api.post('/claims/', data),
  getClaim: (id) => api.get(`/claims/${id}/`),
  updateClaim: (id, data) => api.put(`/claims/${id}/`, data),
  approveClaim: (id, notes) => api.post(`/claims/${id}/approve/`, {notes}),
  rejectClaim: (id, notes) => api.post(`/claims/${id}/reject/`, {notes}),
};

// Documents API
export const documentsAPI = {
  getDocuments: () => api.get('/documents/'),
  uploadDocument: (formData) => api.post('/documents/', formData, {
    headers: {'Content-Type': 'multipart/form-data'}
  }),
  getDocument: (id) => api.get(`/documents/${id}/`),
  deleteDocument: (id) => api.delete(`/documents/${id}/`),
  approveDocument: (id, notes) => api.post(`/documents/${id}/approve/`, {notes}),
  rejectDocument: (id, notes) => api.post(`/documents/${id}/reject/`, {notes}),
};

// Announcements API
export const announcementsAPI = {
  getAnnouncements: () => api.get('/announcements/'),
  createAnnouncement: (data) => api.post('/announcements/', data),
  getAnnouncement: (id) => api.get(`/announcements/${id}/`),
  updateAnnouncement: (id, data) => api.put(`/announcements/${id}/`, data),
  deleteAnnouncement: (id) => api.delete(`/announcements/${id}/`),
};

// Meetings API
export const meetingsAPI = {
  getMeetings: () => api.get('/meetings/'),
  createMeeting: (data) => api.post('/meetings/', data),
  getMeeting: (id) => api.get(`/meetings/${id}/`),
  updateMeeting: (id, data) => api.put(`/meetings/${id}/`, data),
  deleteMeeting: (id) => api.delete(`/meetings/${id}/`),
};

// Contact API
export const contactAPI = {
  getMessages: () => api.get('/contact/'),
  sendMessage: (data) => api.post('/contact/', data),
  getMessage: (id) => api.get(`/contact/${id}/`),
};

export default api;