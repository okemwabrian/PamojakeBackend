// Frontend File Upload Example for Pamoja Backend
// This shows the correct way to handle file uploads with the Django backend

// 1. API Service Configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,  // Increased timeout for file uploads
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 2. Application Submission with File Upload
const submitApplication = async (applicationData, files) => {
  try {
    const formData = new FormData();
    
    // Add all form fields
    Object.keys(applicationData).forEach(key => {
      if (applicationData[key] !== null && applicationData[key] !== undefined) {
        formData.append(key, applicationData[key]);
      }
    });
    
    // Add files
    if (files.id_document) {
      formData.append('id_document', files.id_document);
    }
    if (files.spouse_id_document) {
      formData.append('spouse_id_document', files.spouse_id_document);
    }
    
    // IMPORTANT: Do NOT set Content-Type header
    // Axios will automatically set it with boundary for multipart/form-data
    const response = await api.post('/applications/', formData);
    return response.data;
  } catch (error) {
    console.error('Application submission error:', error.response?.data);
    throw error;
  }
};

// 3. Payment Submission with File Upload
const submitPayment = async (paymentData, paymentProofFile) => {
  try {
    const formData = new FormData();
    
    // Add payment fields
    formData.append('payment_type', paymentData.payment_type);
    formData.append('amount', paymentData.amount);
    formData.append('payment_method', paymentData.payment_method || 'bank');
    formData.append('description', paymentData.description || '');
    
    // Add payment proof file
    if (paymentProofFile) {
      formData.append('payment_proof', paymentProofFile);
    }
    
    const response = await api.post('/payments/', formData);
    return response.data;
  } catch (error) {
    console.error('Payment submission error:', error.response?.data);
    throw error;
  }
};

// 4. React Component Example
const ApplicationForm = () => {
  const [formData, setFormData] = useState({
    membership_type: 'single',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    // ... other fields
  });
  
  const [files, setFiles] = useState({
    id_document: null,
    spouse_id_document: null
  });
  
  const handleFileChange = (e) => {
    const { name, files: fileList } = e.target;
    setFiles(prev => ({
      ...prev,
      [name]: fileList[0]
    }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Validate required files
      if (!files.id_document) {
        alert('ID document is required');
        return;
      }
      
      if (formData.membership_type === 'double' && !files.spouse_id_document) {
        alert('Spouse ID document is required for double membership');
        return;
      }
      
      const result = await submitApplication(formData, files);
      console.log('Application submitted successfully:', result);
      // Handle success
    } catch (error) {
      console.error('Submission failed:', error);
      // Handle error
    }
  };
  
  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      {/* Form fields */}
      <input
        type="text"
        name="first_name"
        value={formData.first_name}
        onChange={(e) => setFormData({...formData, first_name: e.target.value})}
        required
      />
      
      {/* File inputs */}
      <input
        type="file"
        name="id_document"
        onChange={handleFileChange}
        accept=".pdf,.jpg,.jpeg,.png"
        required
      />
      
      {formData.membership_type === 'double' && (
        <input
          type="file"
          name="spouse_id_document"
          onChange={handleFileChange}
          accept=".pdf,.jpg,.jpeg,.png"
          required
        />
      )}
      
      <button type="submit">Submit Application</button>
    </form>
  );
};

// 5. Payment Form Example
const PaymentForm = () => {
  const [paymentData, setPaymentData] = useState({
    payment_type: 'share_purchase',
    amount: '',
    payment_method: 'bank',
    description: ''
  });
  
  const [paymentProof, setPaymentProof] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!paymentProof) {
      alert('Payment proof is required');
      return;
    }
    
    try {
      const result = await submitPayment(paymentData, paymentProof);
      console.log('Payment submitted successfully:', result);
    } catch (error) {
      console.error('Payment submission failed:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <select
        value={paymentData.payment_type}
        onChange={(e) => setPaymentData({...paymentData, payment_type: e.target.value})}
      >
        <option value="share_purchase">Share Purchase</option>
        <option value="membership_fee">Membership Fee</option>
        <option value="activation_fee">Activation Fee</option>
      </select>
      
      <input
        type="number"
        placeholder="Amount"
        value={paymentData.amount}
        onChange={(e) => setPaymentData({...paymentData, amount: e.target.value})}
        required
      />
      
      <input
        type="file"
        onChange={(e) => setPaymentProof(e.target.files[0])}
        accept=".pdf,.jpg,.jpeg,.png"
        required
      />
      
      <button type="submit">Submit Payment</button>
    </form>
  );
};

export { submitApplication, submitPayment, ApplicationForm, PaymentForm };