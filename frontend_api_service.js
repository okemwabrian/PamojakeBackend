// Frontend API Service - Updated for Pamoja Backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('access_token');
    }

    // Helper method to get headers
    getHeaders(includeContentType = true) {
        const headers = {};
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        if (includeContentType) {
            headers['Content-Type'] = 'application/json';
        }
        return headers;
    }

    // Helper method for FormData requests
    getFormHeaders() {
        const headers = {};
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        // Don't set Content-Type for FormData - browser will set it with boundary
        return headers;
    }

    // Authentication
    async login(credentials) {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        });
        const data = await response.json();
        if (response.ok && data.access) {
            this.token = data.access;
            localStorage.setItem('access_token', data.access);
        }
        return { response, data };
    }

    // Payments
    async createPayment(paymentData) {
        const formData = new FormData();
        Object.keys(paymentData).forEach(key => {
            if (paymentData[key] !== null && paymentData[key] !== undefined) {
                formData.append(key, paymentData[key]);
            }
        });

        const response = await fetch(`${API_BASE_URL}/payments/`, {
            method: 'POST',
            headers: this.getFormHeaders(),
            body: formData
        });
        return { response, data: await response.json() };
    }

    async getPayments() {
        const response = await fetch(`${API_BASE_URL}/payments/`, {
            headers: this.getHeaders()
        });
        return { response, data: await response.json() };
    }

    // Claims
    async createClaim(claimData) {
        const formData = new FormData();
        Object.keys(claimData).forEach(key => {
            if (claimData[key] !== null && claimData[key] !== undefined) {
                formData.append(key, claimData[key]);
            }
        });

        const response = await fetch(`${API_BASE_URL}/claims/`, {
            method: 'POST',
            headers: this.getFormHeaders(),
            body: formData
        });
        return { response, data: await response.json() };
    }

    async getClaims() {
        const response = await fetch(`${API_BASE_URL}/claims/`, {
            headers: this.getHeaders()
        });
        return { response, data: await response.json() };
    }

    // Admin - Payments
    async approvePayment(paymentId, notes = '') {
        const response = await fetch(`${API_BASE_URL}/admin/payments/${paymentId}/approve_payment/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ notes })
        });
        return { response, data: await response.json() };
    }

    async rejectPayment(paymentId, notes = '') {
        const response = await fetch(`${API_BASE_URL}/admin/payments/${paymentId}/reject_payment/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ notes })
        });
        return { response, data: await response.json() };
    }

    // Admin - General
    async getAdminPayments() {
        const response = await fetch(`${API_BASE_URL}/admin/payments/`, {
            headers: this.getHeaders()
        });
        return { response, data: await response.json() };
    }

    async getAdminClaims() {
        const response = await fetch(`${API_BASE_URL}/admin/claims/`, {
            headers: this.getHeaders()
        });
        return { response, data: await response.json() };
    }

    async getAdminUsers() {
        const response = await fetch(`${API_BASE_URL}/admin/users/`, {
            headers: this.getHeaders()
        });
        return { response, data: await response.json() };
    }

    // Shares
    async createSharePurchase(shareData) {
        const formData = new FormData();
        Object.keys(shareData).forEach(key => {
            if (shareData[key] !== null && shareData[key] !== undefined) {
                formData.append(key, shareData[key]);
            }
        });

        const response = await fetch(`${API_BASE_URL}/shares/`, {
            method: 'POST',
            headers: this.getFormHeaders(),
            body: formData
        });
        return { response, data: await response.json() };
    }

    // Error handling helper
    handleApiError(response, data) {
        if (!response.ok) {
            console.error('API Error:', response.status, data);
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = '/login';
            }
        }
        return { response, data };
    }
}

// Usage examples:
/*
const api = new ApiService();

// Login
const { response, data } = await api.login({ username: 'user', password: 'pass' });

// Create payment with file
const paymentData = {
    payment_type: 'activation_fee',
    amount: 100,
    description: 'Activation fee payment',
    payment_proof: fileInput.files[0] // File object
};
await api.createPayment(paymentData);

// Create claim with file
const claimData = {
    claim_type: 'medical',
    member_name: 'John Doe',
    relationship: 'self',
    amount_requested: 500,
    incident_date: '2025-01-01',
    description: 'Medical emergency',
    supporting_documents: fileInput.files[0] // File object
};
await api.createClaim(claimData);

// Admin approve payment
await api.approvePayment(paymentId, 'Payment verified and approved');
*/

export default ApiService;