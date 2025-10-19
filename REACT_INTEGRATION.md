# React Frontend Integration Guide

## 1. Copy API Service to React Project

Copy the `react_api_service.js` file to your React project's `src/services/` directory:

```bash
cp react_api_service.js /path/to/your/react/project/src/services/api.js
```

## 2. Install Required Dependencies

In your React project, install axios:

```bash
npm install axios
```

## 3. Usage Examples

### Authentication

```javascript
import { authAPI } from './services/api';

// Login
const handleLogin = async (credentials) => {
  try {
    const response = await authAPI.login(credentials);
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    // Redirect to dashboard
  } catch (error) {
    console.error('Login failed:', error.response.data);
  }
};

// Register
const handleRegister = async (userData) => {
  try {
    const response = await authAPI.register(userData);
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    // Redirect to dashboard
  } catch (error) {
    console.error('Registration failed:', error.response.data);
  }
};

// Logout
const handleLogout = async () => {
  try {
    await authAPI.logout();
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Redirect to login
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
```

### Applications

```javascript
import { applicationAPI } from './services/api';

// Get user applications
const fetchApplications = async () => {
  try {
    const response = await applicationAPI.getApplications();
    setApplications(response.data.results || response.data);
  } catch (error) {
    console.error('Failed to fetch applications:', error);
  }
};

// Submit new application
const submitApplication = async (applicationData) => {
  try {
    const response = await applicationAPI.createApplication(applicationData);
    console.log('Application submitted:', response.data);
    // Refresh applications list
    fetchApplications();
  } catch (error) {
    console.error('Failed to submit application:', error.response.data);
  }
};
```

### Payments

```javascript
import { paymentsAPI } from './services/api';

// Get user payments
const fetchPayments = async () => {
  try {
    const response = await paymentsAPI.getPayments();
    setPayments(response.data.results || response.data);
  } catch (error) {
    console.error('Failed to fetch payments:', error);
  }
};

// Create payment
const createPayment = async (paymentData) => {
  try {
    const response = await paymentsAPI.createPayment(paymentData);
    console.log('Payment created:', response.data);
    fetchPayments();
  } catch (error) {
    console.error('Failed to create payment:', error.response.data);
  }
};
```

### Claims

```javascript
import { claimsAPI } from './services/api';

// Get user claims
const fetchClaims = async () => {
  try {
    const response = await claimsAPI.getClaims();
    setClaims(response.data.results || response.data);
  } catch (error) {
    console.error('Failed to fetch claims:', error);
  }
};

// Submit claim
const submitClaim = async (claimData) => {
  try {
    const response = await claimsAPI.createClaim(claimData);
    console.log('Claim submitted:', response.data);
    fetchClaims();
  } catch (error) {
    console.error('Failed to submit claim:', error.response.data);
  }
};
```

### Documents

```javascript
import { documentsAPI } from './services/api';

// Upload document
const uploadDocument = async (file, documentData) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', documentData.name);
  formData.append('document_type', documentData.document_type);
  formData.append('description', documentData.description);

  try {
    const response = await documentsAPI.uploadDocument(formData);
    console.log('Document uploaded:', response.data);
    fetchDocuments();
  } catch (error) {
    console.error('Failed to upload document:', error.response.data);
  }
};
```

### Announcements

```javascript
import { announcementsAPI } from './services/api';

// Get announcements
const fetchAnnouncements = async () => {
  try {
    const response = await announcementsAPI.getAnnouncements();
    setAnnouncements(response.data.results || response.data);
  } catch (error) {
    console.error('Failed to fetch announcements:', error);
  }
};
```

### Contact

```javascript
import { contactAPI } from './services/api';

// Send contact message
const sendMessage = async (messageData) => {
  try {
    const response = await contactAPI.sendMessage(messageData);
    console.log('Message sent:', response.data);
    // Show success message
  } catch (error) {
    console.error('Failed to send message:', error.response.data);
  }
};
```

## 4. Admin Panel Integration

For admin users, use the admin API endpoints:

```javascript
import { adminAPI } from './services/api';

// Get all users (admin only)
const fetchAllUsers = async () => {
  try {
    const response = await adminAPI.getUsers();
    setUsers(response.data);
  } catch (error) {
    console.error('Failed to fetch users:', error);
  }
};

// Get user statistics
const fetchUserStats = async () => {
  try {
    const response = await adminAPI.getUserStats();
    setStats(response.data);
  } catch (error) {
    console.error('Failed to fetch stats:', error);
  }
};

// Approve application
const approveApplication = async (applicationId) => {
  try {
    await adminAPI.approveApplication(applicationId);
    console.log('Application approved');
    fetchApplications();
  } catch (error) {
    console.error('Failed to approve application:', error);
  }
};
```

## 5. Error Handling

The API service includes automatic token handling. For better error handling, you can add interceptors:

```javascript
import api from './services/api';

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## 6. Environment Configuration

Create a `.env` file in your React project:

```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

Then update the API service:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
```

## 7. Authentication Context

Create an authentication context for managing user state:

```javascript
// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    const response = await authAPI.login(credentials);
    const { user, token } = response.data;
    
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    setUser(user);
    
    return response;
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
    }
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

## 8. Protected Routes

Create a component for protected routes:

```javascript
// components/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (adminOnly && !user.is_staff) {
    return <Navigate to="/dashboard" />;
  }

  return children;
};

export default ProtectedRoute;
```

This integration guide provides everything needed to connect your React frontend with the Django backend!