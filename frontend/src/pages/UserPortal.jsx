import React, { useState } from 'react';
import axios from 'axios';

const UserPortal = () => {
    const [formData, setFormData] = useState({
        mobile_no: '',
        account_no: '',
        email: '',
        bank_name: '',
        transaction_id: '',
        fraud_type: 'UPI',
        description: ''
    });
    const [status, setStatus] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus({ type: 'info', msg: 'Submitting...' });
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/portal/submit', formData);
            setStatus({ type: 'success', msg: `Complaint Registered! Ticket ID: #${res.data.ticket_id}` });
            setFormData({
                mobile_no: '',
                account_no: '',
                email: '',
                bank_name: '',
                transaction_id: '',
                fraud_type: 'UPI',
                description: ''
            });
        } catch (err) {
            console.error(err);
            setStatus({ type: 'error', msg: 'Submission Failed. Check format or connection.' });
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)', fontFamily: "'Inter', sans-serif" }}>
            <div style={{ width: '100%', maxWidth: '600px', padding: '40px', background: 'rgba(255, 255, 255, 0.03)', backdropFilter: 'blur(20px)', borderRadius: '24px', border: '1px solid rgba(255, 255, 255, 0.1)', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}>
                <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                    <div style={{ width: '60px', height: '60px', background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', borderRadius: '16px', margin: '0 auto 20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', boxShadow: '0 10px 25px -5px rgba(59, 130, 246, 0.5)' }}>🛡️</div>
                    <h1 style={{ color: 'white', fontSize: '1.8rem', fontWeight: '800', marginBottom: '10px' }}>Citizen Shield</h1>
                    <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>Secure Cybercrime Reporting Portal</p>
                </div>

                {status && (
                    <div style={{
                        padding: '16px', borderRadius: '12px', marginBottom: '24px', fontSize: '0.9rem', fontWeight: '500', textAlign: 'center',
                        background: status.type === 'success' ? 'rgba(34, 197, 94, 0.2)' : status.type === 'info' ? 'rgba(59, 130, 246, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        color: status.type === 'success' ? '#4ade80' : status.type === 'info' ? '#60a5fa' : '#f87171',
                        border: `1px solid ${status.type === 'success' ? '#22c55e' : status.type === 'info' ? '#3b82f6' : '#ef4444'}`
                    }}>
                        {status.msg}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                    <div style={{gridColumn: 'span 2'}}>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Mobile Number</label>
                        <input className="form-input" name="mobile_no" placeholder="9876543210" value={formData.mobile_no} onChange={handleChange} required style={inputStyle} />
                    </div>
                    
                    <div>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Account Number</label>
                        <input className="form-input" name="account_no" placeholder="XXXX-XXXX-XXXX" value={formData.account_no} onChange={handleChange} required style={inputStyle} />
                    </div>
                    <div>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Bank Name</label>
                        <input className="form-input" name="bank_name" placeholder="SBI / HDFC" value={formData.bank_name} onChange={handleChange} required style={inputStyle} />
                    </div>
                    
                    <div style={{gridColumn: 'span 2'}}>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Email Address</label>
                        <input className="form-input" name="email" type="email" placeholder="you@example.com" value={formData.email} onChange={handleChange} required style={inputStyle} />
                    </div>

                    <div>
                         <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Transaction ID</label>
                         <input className="form-input" name="transaction_id" placeholder="Optional" value={formData.transaction_id} onChange={handleChange} style={inputStyle} />
                    </div>

                    <div>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Fraud Type</label>
                        <select name="fraud_type" value={formData.fraud_type} onChange={handleChange} style={inputStyle}>
                            <option value="UPI">UPI Fraud</option>
                            <option value="CC">Credit/Debit Card</option>
                            <option value="PHISHING">Phishing Link</option>
                            <option value="KYC">Fake KYC</option>
                            <option value="OTHER">Other</option>
                        </select>
                    </div>

                    <div style={{gridColumn: 'span 2'}}>
                        <label className="form-label" style={{color: '#ccc', fontSize: '0.8rem', marginBottom: '5px', display: 'block'}}>Description of Incident</label>
                        <textarea name="description" rows="3" value={formData.description} onChange={handleChange} required style={inputStyle}></textarea>
                    </div>

                    <button type="submit" style={{
                        gridColumn: 'span 2', padding: '16px', borderRadius: '12px', border: 'none', fontSize: '1rem', fontWeight: '700', cursor: 'pointer', marginTop: '10px',
                        background: 'linear-gradient(135deg, #3b82f6, #2563eb)', color: 'white'
                    }}>
                        SUBMIT REPORT
                    </button>
                </form>
            </div>
        </div>
    );
};

const inputStyle = {
    width: '100%', padding: '12px', borderRadius: '8px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid #334155', color: 'white', outline: 'none', fontSize: '0.95rem'
};

export default UserPortal;
