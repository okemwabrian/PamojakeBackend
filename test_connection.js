// Test Backend-Frontend Connection
// Copy this to your React project and run it to test the connection

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Test connection function
export const testConnection = async () => {
  try {
    console.log('Testing backend connection...');
    
    // Test health check endpoint
    const healthResponse = await axios.get(`${API_BASE_URL}/core/health/`);
    console.log('✅ Health Check:', healthResponse.data);
    
    // Test announcements endpoint (public)
    const announcementsResponse = await axios.get(`${API_BASE_URL}/announcements/`);
    console.log('✅ Announcements:', announcementsResponse.data);
    
    // Test login endpoint with dummy data (should fail but show endpoint works)
    try {
      await axios.post(`${API_BASE_URL}/auth/login/`, {
        username: 'test',
        password: 'test'
      });
    } catch (error) {
      if (error.response && error.response.status === 400) {
        console.log('✅ Login endpoint working (expected error for invalid credentials)');
      }
    }
    
    console.log('🎉 Backend connection successful!');
    return true;
    
  } catch (error) {
    console.error('❌ Backend connection failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    return false;
  }
};

// Usage in React component:
// import { testConnection } from './test_connection';
// 
// useEffect(() => {
//   testConnection();
// }, []);