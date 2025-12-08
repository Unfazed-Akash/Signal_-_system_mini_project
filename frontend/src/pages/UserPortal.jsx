import React, { useState } from 'react';
import axios from 'axios';

const UserPortal = () => {
    const [formData, setFormData] = useState({ name: '', category: 'UPI', desc: '' });
    const [status, setStatus] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://127.0.0.1:8000/api/portal/submit', formData);
            setStatus({ type: 'success', msg: `Complaint Registered! Ticket ID: #${res.data.ticket_id}` });
            setFormData({ name: '', category: 'UPI', desc: '' });
        } catch (err) {
            setStatus({ type: 'error', msg: 'Submission Failed. Server Offline.' });
        }
    };

    return (
        <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)', fontFamily: "'Inter', sans-serif" }}>
            <div style={{ width: '100%', maxWidth: '500px', padding: '40px', background: 'rgba(255, 255, 255, 0.03)', backdropFilter: 'blur(20px)', borderRadius: '24px', border: '1px solid rgba(255, 255, 255, 0.1)', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}>
                <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                    <div style={{ width: '60px', height: '60px', background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', borderRadius: '16px', margin: '0 auto 20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', boxShadow: '0 10px 25px -5px rgba(59, 130, 246, 0.5)' }}>🛡️</div>
                    <h1 style={{ color: 'white', fontSize: '1.8rem', fontWeight: '800', marginBottom: '10px' }}>Citizen Shield</h1>
                    <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>Secure Cybercrime Reporting Portal</p>
                </div>

                {status && (
                    <div style={{
                        padding: '16px', borderRadius: '12px', marginBottom: '24px', fontSize: '0.9rem', fontWeight: '500', textAlign: 'center',
                        background: status.type === 'success' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        color: status.type === 'success' ? '#4ade80' : '#f87171',
                        border: `1px solid ${status.type === 'success' ? '#22c55e' : '#ef4444'}`
                    }}>
                        {status.msg}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '20px' }}>
                    <div>
                        <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.85rem', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Full Name</label>
                        <input
                            type="text"
                            placeholder="e.g. Rahul Sharma"
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                            required
                            style={{ width: '100%', padding: '14px', borderRadius: '12px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid #334155', color: 'white', outline: 'none', transition: 'border-color 0.2s', fontSize: '1rem' }}
                            onFocus={e => e.target.style.borderColor = '#3b82f6'}
                            onBlur={e => e.target.style.borderColor = '#334155'}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.85rem', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Fraud Category</label>
                        <select
                            value={formData.category}
                            onChange={e => setFormData({ ...formData, category: e.target.value })}
                            style={{ width: '100%', padding: '14px', borderRadius: '12px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid #334155', color: 'white', outline: 'none', cursor: 'pointer', appearance: 'none', fontSize: '1rem' }}
                        >
                            <option value="UPI">UPI Fraud</option>
                            <option value="CC">Credit Card Theft</option>
                            <option value="PHISHING">Phishing / Scam</option>
                            <option value="OTHER">Other Cybercrime</option>
                        </select>
                    </div>

                    <div>
                        <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.85rem', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Incident Details</label>
                        <textarea
                            rows="4"
                            placeholder="Describe what happened..."
                            value={formData.desc}
                            onChange={e => setFormData({ ...formData, desc: e.target.value })}
                            required
                            style={{ width: '100%', padding: '14px', borderRadius: '12px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid #334155', color: 'white', outline: 'none', resize: 'vertical', minHeight: '100px', fontSize: '1rem' }}
                            onFocus={e => e.target.style.borderColor = '#3b82f6'}
                            onBlur={e => e.target.style.borderColor = '#334155'}
                        ></textarea>
                    </div>

                    <button
                        type="submit"
                        style={{
                            padding: '16px', borderRadius: '12px', border: 'none', fontSize: '1rem', fontWeight: '700', cursor: 'pointer', marginTop: '10px',
                            background: 'linear-gradient(135deg, #3b82f6, #2563eb)', color: 'white', letterSpacing: '0.5px',
                            boxShadow: '0 10px 15px -3px rgba(37, 99, 235, 0.4)', transition: 'transform 0.2s'
                        }}
                        onMouseDown={e => e.target.style.transform = 'scale(0.98)'}
                        onMouseUp={e => e.target.style.transform = 'scale(1)'}
                    >
                        SUBMIT REPORT
                    </button>
                </form>

                <div style={{ marginTop: '30px', textAlign: 'center', fontSize: '0.8rem', color: '#64748b' }}>
                    Your data is encrypted and sent directly to the Cyber Crime Coordination Centre.
                </div>
            </div>
        </div>
    );
};

export default UserPortal;
