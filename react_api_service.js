// Complete API Service for React Frontend
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
  approvePayment: (id, notes) => api.post(`/payments/${id}/approve/`, {notes}),
  rejectPayment: (id, notes) => api.post(`/payments/${id}/reject/`, {notes}),
  getFinancialReport: () => api.get('/payments/financial_report/'),
  getSharesReport: () => api.get('/payments/shares_report/'),
  submitActivationFee: (data) => api.post('/payments/activation_fee/', data),
};

// Shares API
export const sharesAPI = {
  getShares: () => api.get('/shares/'),
  createShare: (data) => api.post('/shares/', data),
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
  markRead: (id) => api.post(`/contact/${id}/mark_read/`),
  reply: (id, reply) => api.post(`/contact/${id}/reply/`, {reply}),
};

// Admin API
export const adminAPI = {
  // Users
  getUsers: () => api.get('/admin/users/'),
  getUserStats: () => api.get('/admin/users/stats/'),
  getRegisteredUsers: () => api.get('/admin/users/registered_users/'),
  toggleMembership: (id) => api.post(`/admin/users/${id}/toggle_membership/`),
  resetPassword: (id) => api.post(`/admin/users/${id}/reset_password/`),
  activateUser: (id) => api.post(`/admin/users/${id}/activate_user/`),
  deactivateUser: (id, reason) => api.post(`/admin/users/${id}/deactivate_user/`, {reason}),
  updateShares: (id, data) => api.post(`/admin/users/${id}/update_shares/`, data),
  deductSharesAll: (amount, reason) => api.post('/admin/users/deduct_shares_all/', {amount, reason}),
  
  // Applications
  getApplications: () => api.get('/admin/applications/'),
  approveApplication: (id) => api.post(`/admin/applications/${id}/approve/`),
  rejectApplication: (id) => api.post(`/admin/applications/${id}/reject/`),
  
  // Claims
  getClaims: () => api.get('/admin/claims/'),
  approveClaim: (id, amount) => api.post(`/admin/claims/${id}/approve/`, {amount_approved: amount}),
  rejectClaim: (id) => api.post(`/admin/claims/${id}/reject/`),
  
  // Payments
  getPayments: () => api.get('/admin/payments/'),
  approvePayment: (id, notes) => api.post(`/payments/${id}/approve/`, {notes}),
  rejectPayment: (id, notes) => api.post(`/payments/${id}/reject/`, {notes}),
  getFinancialReport: () => api.get('/payments/financial_report/'),
  getSharesReport: () => api.get('/payments/shares_report/'),
  
  // Contact Messages
  getContactMessages: () => api.get('/admin/contact/'),
  markMessageRead: (id) => api.post(`/admin/contact/${id}/mark_read/`),
  replyToMessage: (id, reply) => api.post(`/admin/contact/${id}/reply/`, {reply}),
};

export default api;