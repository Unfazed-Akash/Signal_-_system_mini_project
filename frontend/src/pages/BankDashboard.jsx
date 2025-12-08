import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:8000');

const BankDashboard = () => {
    const [stats, setStats] = useState({ total_saved_inr: 0, blocked_cards: 0, false_positive_rate: '0.4%' });
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const fetchStats = async () => {
            const res = await fetch('http://127.0.0.1:8000/api/bank/stats');
            const data = await res.json();
            setStats(data);
        };
        fetchStats();

        socket.on('new_alert', (alert) => {
            const txn = alert.transaction;
            setStats(prev => ({
                ...prev,
                total_saved_inr: prev.total_saved_inr + txn.amount,
                blocked_cards: prev.blocked_cards + 1
            }));

            setLogs(prev => [{
                time: new Date(txn.timestamp).toLocaleTimeString(),
                action: 'BLOCKED',
                desc: `Card ending ${txn.sender_id.slice(-4)} suspicious activity in ${txn.city}. Amount: ₹${txn.amount}`,
                id: txn.txn_id
            }, ...prev].slice(0, 10));
        });

        return () => socket.off('new_alert');
    }, []);

    return (
        <div style={{ minHeight: '100vh', background: '#f8fafc', color: '#0f172a', fontFamily: "'Inter', sans-serif" }}>
            {/* Top Bar */}
            <div style={{ background: 'white', borderBottom: '1px solid #e2e8f0', padding: '0 40px', height: '70px', display: 'flex', itemsAlign: 'center', justifyContent: 'space-between', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px', height: '100%' }}>
                    <h1 style={{ fontSize: '1.2rem', fontWeight: '800', color: '#2563eb' }}>KAVACH <span style={{ color: '#0f172a' }}>BANKING CORE</span></h1>
                    <span style={{ padding: '4px 10px', background: '#dbeafe', color: '#1e40af', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold' }}>LIVE SYNC ACTIVE</span>
                </div>
                <div style={{ fontSize: '0.9rem', color: '#64748b' }}>Administrator Mode</div>
            </div>

            <div style={{ padding: '40px', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '30px' }}>
                {/* Metric Cards */}
                <div style={{ background: 'white', padding: '30px', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', fontWeight: '600', marginBottom: '10px' }}>LIABILITY PREVENTED</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#16a34a' }}>₹{stats.total_saved_inr.toLocaleString()}</div>
                    <div style={{ color: '#16a34a', fontSize: '0.8rem', marginTop: '5px' }}>▲ +12% vs last hour</div>
                </div>

                <div style={{ background: 'white', padding: '30px', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', fontWeight: '600', marginBottom: '10px' }}>CARDS BLOCKED</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#ef4444' }}>{stats.blocked_cards}</div>
                    <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '5px' }}>Automated Actions</div>
                </div>

                <div style={{ background: 'white', padding: '30px', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', fontWeight: '600', marginBottom: '10px' }}>FALSE POSITIVE RATE</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: '#3b82f6' }}>{stats.false_positive_rate}</div>
                    <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '5px' }}>Optimal Range</div>
                </div>
            </div>

            {/* Logs Area */}
            <div style={{ padding: '0 40px 40px 40px' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '20px', color: '#334155' }}>Recent Automated Interventions</h3>
                <div style={{ background: 'white', borderRadius: '16px', overflow: 'hidden', border: '1px solid #e2e8f0' }}>
                    {logs.length === 0 ? (
                        <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>No recent interventions logged.</div>
                    ) : (
                        logs.map((log, i) => (
                            <div key={i} style={{ padding: '20px', borderBottom: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'space-between', transition: 'background 0.2s', cursor: 'pointer' }}
                                onMouseEnter={(e) => e.target.style.background = '#f8fafc'}
                                onMouseLeave={(e) => e.target.style.background = 'white'}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                                    <div style={{ padding: '8px 12px', background: '#fee2e2', color: '#991b1b', borderRadius: '8px', fontWeight: 'bold', fontSize: '0.8rem' }}>BLOCKED</div>
                                    <div>
                                        <div style={{ fontWeight: '600', color: '#0f172a' }}>{log.desc}</div>
                                        <div style={{ fontSize: '0.8rem', color: '#64748b' }}>Txn ID: {log.id}</div>
                                    </div>
                                </div>
                                <div style={{ fontFamily: 'monospace', color: '#94a3b8' }}>{log.time}</div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default BankDashboard;
