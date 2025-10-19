// Frontend Form Handling Examples for Pamoja

// 1. Payment Form Submission
const handlePaymentSubmit = async (formData, fileInput) => {
    const api = new ApiService();
    
    const paymentData = {
        payment_type: formData.payment_type,
        amount: parseFloat(formData.amount),
        description: formData.description,
        payment_method: formData.payment_method,
        transaction_id: formData.transaction_id,
        payment_proof: fileInput.files[0] // Important: File object, not file path
    };

    try {
        const { response, data } = await api.createPayment(paymentData);
        if (response.ok) {
            alert('Payment submitted successfully!');
            // Refresh payments list
            loadPayments();
        } else {
            console.error('Payment error:', data);
            alert('Error submitting payment: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Network error. Please try again.');
    }
};

// 2. Claims Form Submission
const handleClaimSubmit = async (formData, fileInput) => {
    const api = new ApiService();
    
    // Validate required fields
    if (!formData.claim_type || !formData.member_name || !formData.amount_requested) {
        alert('Please fill in all required fields');
        return;
    }

    const claimData = {
        claim_type: formData.claim_type,
        member_name: formData.member_name,
        relationship: formData.relationship,
        amount_requested: parseFloat(formData.amount_requested),
        incident_date: formData.incident_date, // Format: YYYY-MM-DD
        description: formData.description,
        supporting_documents: fileInput.files[0] // Optional file
    };

    try {
        const { response, data } = await api.createClaim(claimData);
        if (response.ok) {
            alert('Claim submitted successfully!');
            // Reset form or redirect
            document.getElementById('claimForm').reset();
        } else {
            console.error('Claim error:', data);
            // Handle validation errors
            if (data.amount_requested) {
                alert('Amount error: ' + data.amount_requested[0]);
            } else if (data.incident_date) {
                alert('Date error: ' + data.incident_date[0]);
            } else {
                alert('Error submitting claim: ' + JSON.stringify(data));
            }
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Network error. Please try again.');
    }
};

// 3. Admin Payment Approval
const handlePaymentApproval = async (paymentId, action, notes = '') => {
    const api = new ApiService();
    
    try {
        let result;
        if (action === 'approve') {
            result = await api.approvePayment(paymentId, notes);
        } else if (action === 'reject') {
            result = await api.rejectPayment(paymentId, notes);
        }
        
        const { response, data } = result;
        if (response.ok) {
            alert(`Payment ${action}d successfully!`);
            // Refresh admin payments list
            loadAdminPayments();
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Network error. Please try again.');
    }
};

// 4. File Upload Validation
const validateFileUpload = (fileInput, maxSizeMB = 5) => {
    if (!fileInput.files || !fileInput.files[0]) {
        return { valid: false, message: 'Please select a file' };
    }
    
    const file = fileInput.files[0];
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    
    if (file.size > maxSizeBytes) {
        return { valid: false, message: `File size must be less than ${maxSizeMB}MB` };
    }
    
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, message: 'Only JPEG, PNG, and PDF files are allowed' };
    }
    
    return { valid: true, message: 'File is valid' };
};

// 5. React Component Example
const PaymentForm = () => {
    const [formData, setFormData] = useState({
        payment_type: 'activation_fee',
        amount: '',
        description: '',
        payment_method: '',
        transaction_id: ''
    });
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Validate file
        const fileValidation = validateFileUpload({ files: [file] });
        if (!fileValidation.valid) {
            alert(fileValidation.message);
            setLoading(false);
            return;
        }

        const api = new ApiService();
        const paymentData = {
            ...formData,
            amount: parseFloat(formData.amount),
            payment_proof: file
        };

        try {
            const { response, data } = await api.createPayment(paymentData);
            if (response.ok) {
                alert('Payment submitted successfully!');
                // Reset form
                setFormData({
                    payment_type: 'activation_fee',
                    amount: '',
                    description: '',
                    payment_method: '',
                    transaction_id: ''
                });
                setFile(null);
            } else {
                alert('Error: ' + (data.error || JSON.stringify(data)));
            }
        } catch (error) {
            alert('Network error. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <select 
                value={formData.payment_type}
                onChange={(e) => setFormData({...formData, payment_type: e.target.value})}
                required
            >
                <option value="activation_fee">Activation Fee</option>
                <option value="membership_single">Single Membership</option>
                <option value="membership_double">Double Membership</option>
                <option value="shares">Share Purchase</option>
            </select>
            
            <input
                type="number"
                placeholder="Amount"
                value={formData.amount}
                onChange={(e) => setFormData({...formData, amount: e.target.value})}
                required
                min="0"
                step="0.01"
            />
            
            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                accept=".jpg,.jpeg,.png,.pdf"
                required
            />
            
            <button type="submit" disabled={loading}>
                {loading ? 'Submitting...' : 'Submit Payment'}
            </button>
        </form>
    );
};

// 6. Error Handling Best Practices
const handleApiResponse = async (apiCall) => {
    try {
        const { response, data } = await apiCall();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            // Handle different error types
            if (response.status === 400) {
                // Validation errors
                const errorMessages = [];
                Object.keys(data).forEach(field => {
                    if (Array.isArray(data[field])) {
                        errorMessages.push(`${field}: ${data[field].join(', ')}`);
                    } else {
                        errorMessages.push(`${field}: ${data[field]}`);
                    }
                });
                return { success: false, error: errorMessages.join('\n') };
            } else if (response.status === 401) {
                return { success: false, error: 'Please log in again' };
            } else if (response.status === 403) {
                return { success: false, error: 'Permission denied' };
            } else if (response.status === 404) {
                return { success: false, error: 'Resource not found' };
            } else if (response.status === 415) {
                return { success: false, error: 'Invalid file format or missing Content-Type' };
            } else {
                return { success: false, error: 'Server error. Please try again.' };
            }
        }
    } catch (error) {
        return { success: false, error: 'Network error. Please check your connection.' };
    }
};

export {
    handlePaymentSubmit,
    handleClaimSubmit,
    handlePaymentApproval,
    validateFileUpload,
    PaymentForm,
    handleApiResponse
};